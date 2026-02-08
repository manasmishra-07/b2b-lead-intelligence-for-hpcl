"""
Demo Data Generator for testing the system
"""
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
from loguru import logger

from app.models.models import Company, Source, Lead, Officer
from app.ml.product_inference import ProductInferenceEngine


class DemoDataGenerator:
    """Generate realistic demo data for testing"""
    
    def __init__(self, db: Session):
        self.db = db
        self.inference_engine = ProductInferenceEngine()
    
    def generate_all(self):
        """Generate complete demo dataset"""
        logger.info("Starting demo data generation...")
        
        # 1. Create sources
        sources = self.create_sources()
        logger.info(f"✅ Created {len(sources)} sources")
        
        # 2. Create officers
        officers = self.create_officers()
        logger.info(f"✅ Created {len(officers)} officers")
        
        # 3. Create companies
        companies = self.create_companies()
        logger.info(f"✅ Created {len(companies)} companies")
        
        # 4. Create leads
        leads = self.create_leads(companies, sources, officers)
        logger.info(f"✅ Created {len(leads)} leads")
        
        logger.info("🎉 Demo data generation complete!")
        
        return {
            'sources': len(sources),
            'officers': len(officers),
            'companies': len(companies),
            'leads': len(leads)
        }
    
    def create_sources(self):
        """Create demo scraping sources"""
        sources_data = [
            {
                'domain': 'economictimes.indiatimes.com',
                'url': 'https://economictimes.indiatimes.com',
                'category': 'news',
                'trust_score': 0.9
            },
            {
                'domain': 'business-standard.com',
                'url': 'https://www.business-standard.com',
                'category': 'news',
                'trust_score': 0.85
            },
            {
                'domain': 'gem.gov.in',
                'url': 'https://gem.gov.in/tender',
                'category': 'tender',
                'trust_score': 1.0
            },
            {
                'domain': 'tenderwizard.com',
                'url': 'https://www.tenderwizard.com',
                'category': 'tender',
                'trust_score': 0.8
            },
            {
                'domain': 'indiamart.com',
                'url': 'https://www.indiamart.com',
                'category': 'directory',
                'trust_score': 0.7
            }
        ]
        
        sources = []
        for data in sources_data:
            source = Source(**data, is_active=True, requires_selenium=False)
            self.db.add(source)
            sources.append(source)
        
        self.db.commit()
        return sources
    
    def create_officers(self):
        """Create demo sales officers"""
        officers_data = [
            {
                'name': 'Rajesh Kumar',
                'email': 'rajesh.kumar@hpcl.co.in',
                'phone': '+91-9876543210',
                'territory_state': 'Maharashtra',
                'territory_cities': ['Mumbai', 'Pune', 'Nashik'],
                'dsro_office': 'Mumbai DSRO',
                'employee_id': 'HPCL001'
            },
            {
                'name': 'Priya Sharma',
                'email': 'priya.sharma@hpcl.co.in',
                'phone': '+91-9876543211',
                'territory_state': 'Gujarat',
                'territory_cities': ['Ahmedabad', 'Surat', 'Vadodara'],
                'dsro_office': 'Ahmedabad DSRO',
                'employee_id': 'HPCL002'
            },
            {
                'name': 'Amit Patel',
                'email': 'amit.patel@hpcl.co.in',
                'phone': '+91-9876543212',
                'territory_state': 'Tamil Nadu',
                'territory_cities': ['Chennai', 'Coimbatore', 'Madurai'],
                'dsro_office': 'Chennai DSRO',
                'employee_id': 'HPCL003'
            },
            {
                'name': 'Sneha Desai',
                'email': 'sneha.desai@hpcl.co.in',
                'phone': '+91-9876543213',
                'territory_state': 'Karnataka',
                'territory_cities': ['Bangalore', 'Mysore', 'Hubli'],
                'dsro_office': 'Bangalore DSRO',
                'employee_id': 'HPCL004'
            },
            {
                'name': 'Vikram Singh',
                'email': 'vikram.singh@hpcl.co.in',
                'phone': '+91-9876543214',
                'territory_state': 'Delhi',
                'territory_cities': ['New Delhi', 'Noida', 'Gurgaon'],
                'dsro_office': 'Delhi DSRO',
                'employee_id': 'HPCL005'
            }
        ]
        
        officers = []
        for data in officers_data:
            officer = Officer(**data, is_active=True, notification_enabled=True)
            self.db.add(officer)
            officers.append(officer)
        
        self.db.commit()
        return officers
    
    def create_companies(self):
        """Create demo companies"""
        companies_data = [
            {
                'name': 'Tata Steel Limited',
                'normalized_name': 'tatasteel',
                'website': 'https://www.tatasteel.com',
                'industry': 'Steel',
                'sector': 'Manufacturing',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'company_size': 'enterprise',
                'turnover_estimate': 200000
            },
            {
                'name': 'Reliance Industries Ltd',
                'normalized_name': 'reliance',
                'website': 'https://www.ril.com',
                'industry': 'Petrochemical',
                'sector': 'Chemicals',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'company_size': 'enterprise',
                'turnover_estimate': 800000
            },
            {
                'name': 'Ultratech Cement',
                'normalized_name': 'ultratech',
                'website': 'https://www.ultratechcement.com',
                'industry': 'Cement',
                'sector': 'Construction',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'company_size': 'large',
                'turnover_estimate': 50000
            },
            {
                'name': 'Adani Power Limited',
                'normalized_name': 'adanipower',
                'website': 'https://www.adanipower.com',
                'industry': 'Power Generation',
                'sector': 'Power',
                'city': 'Ahmedabad',
                'state': 'Gujarat',
                'company_size': 'enterprise',
                'turnover_estimate': 35000
            },
            {
                'name': 'Chennai Petroleum Corporation',
                'normalized_name': 'cpcl',
                'website': 'https://www.cpcl.co.in',
                'industry': 'Refinery',
                'sector': 'Petroleum',
                'city': 'Chennai',
                'state': 'Tamil Nadu',
                'company_size': 'large',
                'turnover_estimate': 60000
            },
            {
                'name': 'JSW Steel',
                'normalized_name': 'jswsteel',
                'website': 'https://www.jsw.in',
                'industry': 'Steel',
                'sector': 'Manufacturing',
                'city': 'Bangalore',
                'state': 'Karnataka',
                'company_size': 'enterprise',
                'turnover_estimate': 100000
            },
            {
                'name': 'Marico Industries',
                'normalized_name': 'marico',
                'website': 'https://www.marico.com',
                'industry': 'FMCG',
                'sector': 'Consumer Goods',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'company_size': 'large',
                'turnover_estimate': 9000
            },
            {
                'name': 'Asian Paints',
                'normalized_name': 'asianpaints',
                'website': 'https://www.asianpaints.com',
                'industry': 'Paints',
                'sector': 'Manufacturing',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'company_size': 'large',
                'turnover_estimate': 25000
            },
            {
                'name': 'L&T Construction',
                'normalized_name': 'lnt',
                'website': 'https://www.larsentoubro.com',
                'industry': 'Construction',
                'sector': 'Infrastructure',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'company_size': 'enterprise',
                'turnover_estimate': 150000
            },
            {
                'name': 'Indian Oil Corporation',
                'normalized_name': 'iocl',
                'website': 'https://www.iocl.com',
                'industry': 'Petroleum',
                'sector': 'Oil & Gas',
                'city': 'New Delhi',
                'state': 'Delhi',
                'company_size': 'enterprise',
                'turnover_estimate': 700000
            }
        ]
        
        companies = []
        for data in companies_data:
            company = Company(**data)
            self.db.add(company)
            companies.append(company)
        
        self.db.commit()
        return companies
    
    def create_leads(self, companies, sources, officers):
        """Create demo leads with realistic signals"""
        
        signal_templates = [
            {
                'text': '{company} has announced expansion of their thermal power plant in {city}. The new 500MW unit will require furnace oil and light diesel oil for auxiliary operations. Tender expected in Q2 2026.',
                'type': 'tender',
                'products': ['FO', 'LDO'],
                'intent': 'high'
            },
            {
                'text': '{company} is commissioning a new manufacturing facility in {city}. The plant will have captive power generation using diesel generators with an estimated requirement of 500 KL HSD monthly.',
                'type': 'expansion',
                'products': ['HSD'],
                'intent': 'medium'
            },
            {
                'text': 'News: {company} awards contract for new road construction project in {state}. Project requires bitumen supply for 50km highway construction starting March 2026.',
                'type': 'news',
                'products': ['Bitumen'],
                'intent': 'high'
            },
            {
                'text': '{company} seeking quotations for marine bunker fuel for their shipping fleet operating from {city} port. Annual requirement estimated at 10000 MT.',
                'type': 'tender',
                'products': ['Marine Bunker Fuel', 'LSHS'],
                'intent': 'high'
            },
            {
                'text': '{company} expanding edible oil extraction capacity in {city}. New solvent extraction unit will require hexane. Plant commissioning expected by June 2026.',
                'type': 'expansion',
                'products': ['Hexane'],
                'intent': 'medium'
            },
            {
                'text': '{company} paint manufacturing unit in {city} requires solvent 1425 and mineral turpentine oil for production. Monthly requirement: 100 KL.',
                'type': 'procurement',
                'products': ['Solvent 1425', 'Mineral Turpentine Oil'],
                'intent': 'medium'
            },
            {
                'text': 'Tender Notice: {company} invites bids for supply of furnace oil for their boiler operations at {city} facility. Quantity: 2000 KL per month.',
                'type': 'tender',
                'products': ['FO'],
                'intent': 'high'
            },
            {
                'text': '{company} setting up new jute processing mill in {state}. Will require jute batching oil for textile operations. Expected demand: 50 MT/month.',
                'type': 'news',
                'products': ['Jute Batch Oil'],
                'intent': 'low'
            }
        ]
        
        leads = []
        
        for i, company in enumerate(companies[:8]):  # Create leads for first 8 companies
            # Pick random template
            template = random.choice(signal_templates)
            
            # Fill in template
            signal_text = template['text'].format(
                company=company.name,
                city=company.city or 'their facility',
                state=company.state or 'the region'
            )
            
            # Analyze with ML
            analysis = self.inference_engine.analyze_text(signal_text)
            lead_score = self.inference_engine.calculate_lead_score(analysis, company.company_size)
            
            # Assign officer based on state
            officer = next((o for o in officers if o.territory_state == company.state), officers[0])
            
            # Create lead
            lead = Lead(
                company_id=company.id,
                source_id=random.choice(sources).id,
                signal_text=signal_text,
                signal_url=f"https://example.com/news/{i+1}",
                signal_date=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
                signal_type=template['type'],
                detected_keywords=analysis['detected_keywords'],
                detected_equipment=analysis['detected_equipment'],
                detected_locations=[company.state] if company.state else [],
                recommended_products=analysis['recommended_products'],
                lead_score=lead_score,
                intent_strength=template['intent'],
                urgency_days=random.randint(7, 60),
                confidence=analysis['recommended_products'][0]['confidence'] if analysis['recommended_products'] else 0.5,
                assigned_officer_id=officer.id,
                territory_state=company.state,
                status=random.choice(['new', 'new', 'new', 'contacted', 'qualified']),
                next_action=f"Contact {company.name} regarding {template['products'][0]} requirements"
            )
            
            self.db.add(lead)
            leads.append(lead)
        
        self.db.commit()
        return leads