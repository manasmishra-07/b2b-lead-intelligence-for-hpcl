"""
FastAPI main application
"""
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime, timedelta
from loguru import logger

from app.config.database import get_db, engine, Base
from app.config.settings import settings
from app.models.models import Company, Lead, Officer, Feedback, Source
from app.models.schemas import (
    CompanyCreate, CompanyResponse,
    LeadCreate, LeadResponse, LeadWithCompany, LeadDossier,
    OfficerCreate, OfficerResponse,
    FeedbackCreate, FeedbackResponse,
    SourceCreate, SourceResponse,
    AnalyticsResponse, LeadStats, ProductDistribution, TerritoryStats, WeeklyTrend
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="HPCL Lead Intelligence API",
    description="B2B Lead Intelligence System for HPCL Direct Sales",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== HEALTH CHECK ====================
@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "HPCL Lead Intelligence API",
        "version": "1.0.0"
    }


# ==================== COMPANY ENDPOINTS ====================
@app.post("/api/companies/", response_model=CompanyResponse)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    """Create a new company"""
    # Check if company already exists
    existing = db.query(Company).filter(Company.name == company.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Company already exists")
    
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


@app.get("/api/companies/", response_model=List[CompanyResponse])
def get_companies(
    skip: int = 0,
    limit: int = 100,
    state: Optional[str] = None,
    industry: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of companies with filters"""
    query = db.query(Company)
    
    if state:
        query = query.filter(Company.state == state)
    if industry:
        query = query.filter(Company.industry == industry)
    
    companies = query.offset(skip).limit(limit).all()
    return companies


@app.get("/api/companies/{company_id}", response_model=CompanyResponse)
def get_company(company_id: int, db: Session = Depends(get_db)):
    """Get company by ID"""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


# ==================== LEAD ENDPOINTS ====================
@app.post("/api/leads/", response_model=LeadResponse)
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    """Create a new lead"""
    db_lead = Lead(**lead.dict())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead


@app.get("/api/leads/", response_model=List[LeadWithCompany])
def get_leads(
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = None,
    intent_strength: Optional[str] = None,
    state: Optional[str] = None,
    officer_id: Optional[int] = None,
    min_score: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """
    Get leads with filters
    
    Filters:
    - status: new, contacted, qualified, converted, rejected, lost
    - intent_strength: high, medium, low
    - state: Territory state
    - officer_id: Assigned officer
    - min_score: Minimum lead score
    """
    # FIXED: Load company relationship
    query = db.query(Lead).options(joinedload(Lead.company))
    
    if status:
        query = query.filter(Lead.status == status)
    if intent_strength:
        query = query.filter(Lead.intent_strength == intent_strength)
    if state:
        query = query.filter(Lead.territory_state == state)
    if officer_id:
        query = query.filter(Lead.assigned_officer_id == officer_id)
    if min_score:
        query = query.filter(Lead.lead_score >= min_score)
    
    leads = query.order_by(Lead.created_at.desc()).offset(skip).limit(limit).all()
    return leads


@app.get("/api/leads/{lead_id}", response_model=LeadDossier)
def get_lead_dossier(lead_id: int, db: Session = Depends(get_db)):
    """Get complete lead dossier"""
    lead = db.query(Lead).options(joinedload(Lead.company)).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@app.put("/api/leads/{lead_id}/status")
def update_lead_status(
    lead_id: int,
    status: str,
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Update lead status"""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    lead.status = status
    if status == "contacted":
        lead.contacted_at = datetime.utcnow()
    
    db.commit()
    return {"message": "Lead status updated", "lead_id": lead_id, "status": status}


# ==================== OFFICER ENDPOINTS ====================
@app.post("/api/officers/", response_model=OfficerResponse)
def create_officer(officer: OfficerCreate, db: Session = Depends(get_db)):
    """Create a new sales officer"""
    # Check if email already exists
    existing = db.query(Officer).filter(Officer.email == officer.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Officer with this email already exists")
    
    db_officer = Officer(**officer.dict())
    db.add(db_officer)
    db.commit()
    db.refresh(db_officer)
    return db_officer


@app.get("/api/officers/", response_model=List[OfficerResponse])
def get_officers(
    skip: int = 0,
    limit: int = 100,
    state: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of officers"""
    query = db.query(Officer).filter(Officer.is_active == True)
    
    if state:
        query = query.filter(Officer.territory_state == state)
    
    officers = query.offset(skip).limit(limit).all()
    return officers


@app.get("/api/officers/{officer_id}", response_model=OfficerResponse)
def get_officer(officer_id: int, db: Session = Depends(get_db)):
    """Get officer by ID"""
    officer = db.query(Officer).filter(Officer.id == officer_id).first()
    if not officer:
        raise HTTPException(status_code=404, detail="Officer not found")
    return officer


@app.get("/api/officers/{officer_id}/leads", response_model=List[LeadWithCompany])
def get_officer_leads(
    officer_id: int,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all leads assigned to an officer"""
    query = db.query(Lead).options(joinedload(Lead.company)).filter(Lead.assigned_officer_id == officer_id)
    
    if status:
        query = query.filter(Lead.status == status)
    
    leads = query.order_by(Lead.created_at.desc()).all()
    return leads


# ==================== FEEDBACK ENDPOINTS ====================
@app.post("/api/feedback/", response_model=FeedbackResponse)
def create_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    """Submit feedback for a lead"""
    # Verify lead exists
    lead = db.query(Lead).filter(Lead.id == feedback.lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Get officer ID from lead
    officer_id = lead.assigned_officer_id
    if not officer_id:
        raise HTTPException(status_code=400, detail="Lead has no assigned officer")
    
    # Create feedback
    db_feedback = Feedback(
        officer_id=officer_id,
        **feedback.dict()
    )
    db.add(db_feedback)
    
    # Update lead status based on feedback
    if feedback.action == "converted":
        lead.status = "converted"
    elif feedback.action == "rejected":
        lead.status = "rejected"
    elif feedback.action == "accepted":
        lead.status = "contacted"
    
    db.commit()
    db.refresh(db_feedback)
    return db_feedback


@app.get("/api/feedback/lead/{lead_id}", response_model=List[FeedbackResponse])
def get_lead_feedback(lead_id: int, db: Session = Depends(get_db)):
    """Get all feedback for a lead"""
    feedback = db.query(Feedback).filter(Feedback.lead_id == lead_id).all()
    return feedback


# ==================== SOURCE ENDPOINTS ====================
@app.post("/api/sources/", response_model=SourceResponse)
def create_source(source: SourceCreate, db: Session = Depends(get_db)):
    """Add a new scraping source"""
    db_source = Source(**source.dict())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source


@app.get("/api/sources/", response_model=List[SourceResponse])
def get_sources(
    category: Optional[str] = None,
    is_active: bool = True,
    db: Session = Depends(get_db)
):
    """Get scraping sources"""
    query = db.query(Source).filter(Source.is_active == is_active)
    
    if category:
        query = query.filter(Source.category == category)
    
    sources = query.all()
    return sources


# ==================== ANALYTICS ENDPOINTS ====================
@app.get("/api/analytics/", response_model=AnalyticsResponse)
def get_analytics(
    days: int = 30,
    state: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get analytics dashboard data"""
    
    # Date range
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Base query
    query = db.query(Lead).filter(Lead.created_at >= start_date)
    if state:
        query = query.filter(Lead.territory_state == state)
    
    leads = query.all()
    
    # Calculate stats
    total_leads = len(leads)
    active_leads = len([l for l in leads if l.status in ["new", "contacted", "qualified"]])
    converted_leads = len([l for l in leads if l.status == "converted"])
    conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0
    avg_lead_score = sum([l.lead_score or 0 for l in leads]) / total_leads if total_leads > 0 else 0
    
    stats = LeadStats(
        total_leads=total_leads,
        active_leads=active_leads,
        converted_leads=converted_leads,
        conversion_rate=round(conversion_rate, 2),
        avg_lead_score=round(avg_lead_score, 2)
    )
    
    # Product distribution
    product_counts = {}
    for lead in leads:
        if lead.recommended_products:
            for prod in lead.recommended_products:
                product_name = prod.get('product', 'Unknown')
                product_counts[product_name] = product_counts.get(product_name, 0) + 1
    
    product_distribution = [
        ProductDistribution(
            product=product,
            count=count,
            percentage=round(count / total_leads * 100, 2) if total_leads > 0 else 0
        )
        for product, count in sorted(product_counts.items(), key=lambda x: x[1], reverse=True)
    ]
    
    # Territory stats
    territory_counts = {}
    territory_converted = {}
    for lead in leads:
        state = lead.territory_state or "Unknown"
        territory_counts[state] = territory_counts.get(state, 0) + 1
        if lead.status == "converted":
            territory_converted[state] = territory_converted.get(state, 0) + 1
    
    territory_stats = [
        TerritoryStats(
            state=state,
            lead_count=count,
            conversion_rate=round(territory_converted.get(state, 0) / count * 100, 2) if count > 0 else 0
        )
        for state, count in sorted(territory_counts.items(), key=lambda x: x[1], reverse=True)
    ]
    
    # Weekly trends (simple version)
    weekly_trends = [
        WeeklyTrend(week=f"Week {i+1}", lead_count=0)
        for i in range(4)
    ]
    
    return AnalyticsResponse(
        stats=stats,
        product_distribution=product_distribution,
        territory_stats=territory_stats,
        weekly_trends=weekly_trends
    )


# ==================== UTILITY ENDPOINTS ====================
@app.get("/api/stats/summary")
def get_summary_stats(db: Session = Depends(get_db)):
    """Get quick summary statistics"""
    total_companies = db.query(Company).count()
    total_leads = db.query(Lead).count()
    active_leads = db.query(Lead).filter(Lead.status.in_(["new", "contacted"])).count()
    total_officers = db.query(Officer).filter(Officer.is_active == True).count()
    
    return {
        "total_companies": total_companies,
        "total_leads": total_leads,
        "active_leads": active_leads,
        "total_officers": total_officers
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
# Add this import at the top

# Add these endpoints before the if __name__ == "__main__": line

@app.get("/api/sales-officers")
async def get_sales_officers(db: Session = Depends(get_db)):
    """Get all sales officers with their stats"""
    officers = db.query(SalesOfficer).all()
    
    result = []
    for officer in officers:
        # Count active leads for this officer
        active_leads = db.query(Lead).filter(
            Lead.sales_officer_id == officer.id,
            Lead.status.in_(["new", "contacted"])
        ).count()
        
        # Count total leads
        total_leads = db.query(Lead).filter(
            Lead.sales_officer_id == officer.id
        ).count()
        
        # Count conversions
        conversions = db.query(Lead).filter(
            Lead.sales_officer_id == officer.id,
            Lead.status == "converted"
        ).count()
        
        # Calculate conversion rate
        conversion_rate = round((conversions / total_leads * 100), 1) if total_leads > 0 else 0
        
        result.append({
            "id": officer.id,
            "name": officer.name,
            "email": officer.email,
            "phone": officer.phone,
            "territory": officer.territory,
            "active_leads": active_leads,
            "total_leads": total_leads,
            "conversions": conversions,
            "conversion_rate": conversion_rate,
            "created_at": officer.created_at
        })
    
    return result

@app.get("/api/sales-officers/{officer_id}")
async def get_sales_officer_details(officer_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific sales officer"""
    officer = db.query(SalesOfficer).filter(SalesOfficer.id == officer_id).first()
    
    if not officer:
        raise HTTPException(status_code=404, detail="Sales officer not found")
    
    # Get active leads
    active_leads = db.query(Lead).filter(
        Lead.sales_officer_id == officer.id,
        Lead.status.in_(["new", "contacted"])
    ).count()
    
    # Get total leads
    total_leads = db.query(Lead).filter(
        Lead.sales_officer_id == officer.id
    ).count()
    
    # Get conversions
    conversions = db.query(Lead).filter(
        Lead.sales_officer_id == officer.id,
        Lead.status == "converted"
    ).count()
    
    # Calculate conversion rate
    conversion_rate = round((conversions / total_leads * 100), 1) if total_leads > 0 else 0
    
    # Get recent leads (last 5)
    recent_leads = db.query(Lead).filter(
        Lead.sales_officer_id == officer.id
    ).order_by(Lead.detected_at.desc()).limit(5).all()
    
    recent_leads_data = [
        {
            "id": lead.id,
            "company": lead.company_name,
            "product": lead.recommended_product,
            "score": lead.lead_score,
            "status": lead.status,
            "detected_at": lead.detected_at
        }
        for lead in recent_leads
    ]
    
    return {
        "id": officer.id,
        "name": officer.name,
        "email": officer.email,
        "phone": officer.phone,
        "territory": officer.territory,
        "active_leads": active_leads,
        "total_leads": total_leads,
        "conversions": conversions,
        "conversion_rate": conversion_rate,
        "created_at": officer.created_at,
        "recent_leads": recent_leads_data
    }