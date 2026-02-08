"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# Enums
class IntentStrength(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class LeadStatus(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    CONVERTED = "converted"
    REJECTED = "rejected"
    LOST = "lost"


class FeedbackAction(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CONVERTED = "converted"
    LOST = "lost"


# Company Schemas
class CompanyBase(BaseModel):
    name: str
    website: Optional[str] = None
    industry: Optional[str] = None
    sector: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None


class CompanyCreate(CompanyBase):
    normalized_name: Optional[str] = None
    address: Optional[str] = None
    pincode: Optional[str] = None
    cin: Optional[str] = None
    gst: Optional[str] = None


class CompanyResponse(CompanyBase):
    id: int
    normalized_name: Optional[str] = None
    address: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Product Recommendation Schema
class ProductRecommendation(BaseModel):
    product: str
    confidence: float = Field(..., ge=0, le=1)
    reason: str


# Lead Schemas
class LeadBase(BaseModel):
    signal_text: str
    signal_type: Optional[str] = None


class LeadCreate(LeadBase):
    company_id: int
    source_id: int
    signal_url: Optional[str] = None
    detected_keywords: Optional[List[str]] = None
    recommended_products: Optional[List[Dict[str, Any]]] = None
    lead_score: Optional[float] = None
    intent_strength: Optional[IntentStrength] = None


class LeadResponse(BaseModel):
    id: int
    company_id: int
    lead_score: float
    intent_strength: str
    status: str
    recommended_products: List[Dict[str, Any]]
    detected_keywords: Optional[List[str]] = []
    created_at: datetime
    assigned_officer_id: Optional[int] = None
    signal_text: str
    
    class Config:
        from_attributes = True


class LeadWithCompany(LeadResponse):
    """Lead with company details"""
    company: Optional[CompanyResponse] = None


class LeadDossier(LeadWithCompany):
    """Complete lead dossier with all details"""
    signal_url: Optional[str] = None
    signal_date: Optional[datetime] = None
    detected_equipment: Optional[List[str]] = []
    detected_locations: Optional[List[str]] = []
    urgency_days: Optional[int] = None
    confidence: Optional[float] = None
    next_action: Optional[str] = None


# Officer Schemas
class OfficerBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None


class OfficerCreate(OfficerBase):
    territory_state: str
    territory_cities: Optional[List[str]] = None
    employee_id: str
    dsro_office: Optional[str] = None


class OfficerResponse(OfficerBase):
    id: int
    territory_state: str
    dsro_office: Optional[str] = None
    is_active: bool
    
    class Config:
        from_attributes = True


# Feedback Schemas
class FeedbackCreate(BaseModel):
    lead_id: int
    action: FeedbackAction
    quality_rating: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = None
    converted_product: Optional[str] = None
    estimated_value: Optional[float] = None


class FeedbackResponse(BaseModel):
    id: int
    lead_id: int
    officer_id: int
    action: str
    quality_rating: Optional[int] = None
    notes: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Source Schemas
class SourceCreate(BaseModel):
    domain: str
    url: str
    category: str
    trust_score: float = 0.5
    requires_selenium: bool = False


class SourceResponse(BaseModel):
    id: int
    domain: str
    category: str
    trust_score: float
    is_active: bool
    last_crawled: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Analytics Schemas
class LeadStats(BaseModel):
    total_leads: int
    active_leads: int
    converted_leads: int
    conversion_rate: float
    avg_lead_score: float


class ProductDistribution(BaseModel):
    product: str
    count: int
    percentage: float


class TerritoryStats(BaseModel):
    state: str
    lead_count: int
    conversion_rate: float


class WeeklyTrend(BaseModel):
    week: str
    lead_count: int


class AnalyticsResponse(BaseModel):
    stats: LeadStats
    product_distribution: List[ProductDistribution]
    territory_stats: List[TerritoryStats]
    weekly_trends: List[WeeklyTrend]