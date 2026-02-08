"""
Lead Processing Service - Orchestrates scraping, NLP, and lead creation
"""
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fuzzywuzzy import fuzz
from loguru import logger

from app.models.models import Company, Lead, Source, Officer
from app.ml.product_inference import ProductInferenceEngine
from app.services.email_service import EmailService


class LeadProcessor:
    """Process scraped data into actionable leads"""
    
    def __init__(self, db: Session):
        self.db = db
        self.inference_engine = ProductInferenceEngine()
        self.email_service = EmailService()
    
    def process_signal(self, signal_data: Dict) -> Optional[int]:
        """
        Process a signal from web scraping into a lead
        
        Args:
            signal_data: {
                'company_name': str,
                'signal_text': str,
                'signal_url': str,
                'signal_type': str (news/tender/expansion),
                'source_domain': str,
                'industry': str (optional),
                'location': str (optional),
                'state': str (optional)
            }
        
        Returns:
            lead_id if created, None otherwise
        """
        try:
            # Step 1: Find or create company
            company = self._find_or_create_company(signal_data)
            if not company:
                logger.warning(f"Could not create company for signal: {signal_data.get('company_name')}")
                return None
            
            # Step 2: Get or verify source
            source = self._get_or_create_source(signal_data['source_domain'])
            if not source:
                logger.warning(f"Could not find source: {signal_data['source_domain']}")
                return None
            
            # Step 3: Run NLP analysis
            analysis = self.inference_engine.analyze_text(signal_data['signal_text'])
            
            # Skip if no product recommendations
            if not analysis['recommended_products']:
                logger.info(f"No product recommendations for signal from {signal_data.get('company_name')}")
                return None
            
            # Step 4: Calculate lead score
            company_size = company.company_size or "medium"
            lead_score = self.inference_engine.calculate_lead_score(analysis, company_size)
            
            # Skip low-quality leads
            if lead_score < 30:
                logger.info(f"Lead score too low ({lead_score}) for {signal_data.get('company_name')}")
                return None
            
            # Step 5: Extract location
            locations = self.inference_engine.extract_location(signal_data['signal_text'])
            
            # Step 6: Determine territory and assign officer
            territory_state = signal_data.get('state') or company.state or (locations[0] if locations else None)
            assigned_officer = self._assign_officer(territory_state) if territory_state else None
            
            # Step 7: Create lead
            lead = Lead(
                company_id=company.id,
                source_id=source.id,
                signal_text=signal_data['signal_text'],
                signal_url=signal_data.get('signal_url'),
                signal_date=datetime.utcnow(),
                signal_type=signal_data.get('signal_type', 'unknown'),
                detected_keywords=analysis['detected_keywords'],
                detected_equipment=analysis['detected_equipment'],
                detected_locations=locations,
                recommended_products=analysis['recommended_products'],
                lead_score=lead_score,
                intent_strength=analysis['intent_strength'],
                urgency_days=self._calculate_urgency_days(analysis['urgency_score']),
                confidence=analysis['recommended_products'][0]['confidence'] if analysis['recommended_products'] else 0,
                assigned_officer_id=assigned_officer.id if assigned_officer else None,
                territory_state=territory_state,
                status="new",
                next_action=self._suggest_next_action(analysis)
            )
            
            self.db.add(lead)
            self.db.commit()
            self.db.refresh(lead)
            
            logger.info(f"✅ Created lead #{lead.id} for {company.name} with score {lead_score}")
            
            # Step 8: Send email notification
            if assigned_officer and assigned_officer.notification_enabled:
                self._send_lead_notification(lead, company, assigned_officer)
            
            return lead.id
        
        except Exception as e:
            logger.error(f"Error processing signal: {e}")
            self.db.rollback()
            return None
    
    def _find_or_create_company(self, signal_data: Dict) -> Optional[Company]:
        """Find existing company or create new one"""
        company_name = signal_data.get('company_name', '').strip()
        if not company_name:
            return None
        
        # Normalize name for matching
        normalized_name = company_name.lower().replace(' ', '')
        
        # Try exact match first
        company = self.db.query(Company).filter(Company.name == company_name).first()
        if company:
            return company
        
        # Try fuzzy matching on existing companies
        all_companies = self.db.query(Company).all()
        for existing in all_companies:
            similarity = fuzz.ratio(normalized_name, existing.normalized_name or '')
            if similarity > 85:  # 85% similarity threshold
                logger.info(f"Matched '{company_name}' to existing company '{existing.name}' ({similarity}% match)")
                return existing
        
        # Create new company
        company = Company(
            name=company_name,
            normalized_name=normalized_name,
            industry=signal_data.get('industry'),
            city=signal_data.get('location'),
            state=signal_data.get('state'),
            website=signal_data.get('website')
        )
        
        self.db.add(company)
        self.db.commit()
        self.db.refresh(company)
        
        logger.info(f"Created new company: {company_name}")
        return company
    
    def _get_or_create_source(self, domain: str) -> Optional[Source]:
        """Get or create scraping source"""
        source = self.db.query(Source).filter(Source.domain == domain).first()
        
        if not source:
            # Create new source
            source = Source(
                domain=domain,
                url=f"https://{domain}",
                category="unknown",
                trust_score=0.5,
                is_active=True
            )
            self.db.add(source)
            self.db.commit()
            self.db.refresh(source)
        
        # Update last crawled
        source.last_crawled = datetime.utcnow()
        self.db.commit()
        
        return source
    
    def _assign_officer(self, state: str) -> Optional[Officer]:
        """Assign lead to officer based on territory"""
        # Find officer responsible for this state
        officer = self.db.query(Officer).filter(
            Officer.territory_state == state,
            Officer.is_active == True
        ).first()
        
        if not officer:
            # Try to find any active officer (fallback)
            officer = self.db.query(Officer).filter(Officer.is_active == True).first()
        
        return officer
    
    def _calculate_urgency_days(self, urgency_score: float) -> int:
        """Convert urgency score to estimated days"""
        if urgency_score >= 0.8:
            return 7  # 1 week
        elif urgency_score >= 0.6:
            return 14  # 2 weeks
        elif urgency_score >= 0.4:
            return 30  # 1 month
        else:
            return 60  # 2 months
    
    def _suggest_next_action(self, analysis: Dict) -> str:
        """Suggest next action based on analysis"""
        intent = analysis['intent_strength']
        
        if intent == "high":
            return "Contact immediately - High intent signal detected (tender/procurement)"
        elif intent == "medium":
            return "Schedule call within 3 days - Expansion/new facility signal"
        else:
            return "Research company and prepare pitch - General signal"
    
    def _send_lead_notification(self, lead: Lead, company: Company, officer: Officer):
        """Send email notification to assigned officer"""
        try:
            lead_data = {
                'company_name': company.name,
                'industry': company.industry or 'N/A',
                'location': f"{company.city}, {company.state}" if company.city and company.state else company.state or 'N/A',
                'signal_type': lead.signal_type,
                'lead_score': lead.lead_score,
                'intent_strength': lead.intent_strength,
                'signal_text': lead.signal_text,
                'recommended_products': lead.recommended_products,
                'detected_keywords': lead.detected_keywords,
                'next_action': lead.next_action,
                'dossier_url': f"http://localhost:5173/leads/{lead.id}",  # Update with actual frontend URL
                'contact_phone': company.contact_phone or ''
            }
            
            self.email_service.send_lead_alert(
                officer_email=officer.email,
                officer_name=officer.name,
                lead_data=lead_data
            )
            
            logger.info(f"📧 Sent email notification to {officer.email}")
        
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")
    
    def batch_process_signals(self, signals: List[Dict]) -> Dict:
        """Process multiple signals in batch"""
        results = {
            'processed': 0,
            'created': 0,
            'skipped': 0,
            'errors': 0
        }
        
        for signal in signals:
            results['processed'] += 1
            lead_id = self.process_signal(signal)
            
            if lead_id:
                results['created'] += 1
            else:
                results['skipped'] += 1
        
        logger.info(f"Batch processing complete: {results}")
        return results