"""
SQLAlchemy database models
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base


class Company(Base):
    """Company/Customer entity"""
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    normalized_name = Column(String(255), index=True)
    website = Column(String(255))
    industry = Column(String(100), index=True)
    sector = Column(String(100))
    
    # Location
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100), index=True)
    pincode = Column(String(10))
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Identifiers
    cin = Column(String(50))
    gst = Column(String(50))
    
    # Contact
    contact_person = Column(String(255))
    contact_email = Column(String(255))
    contact_phone = Column(String(20))
    
    # Metadata
    company_size = Column(String(50))
    turnover_estimate = Column(Float)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    leads = relationship("Lead", back_populates="company")


class Source(Base):
    """Web source for scraping"""
    __tablename__ = "sources"
    
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(255), unique=True, nullable=False)
    url = Column(String(500))
    category = Column(String(50), index=True)
    
    # Scraping config
    trust_score = Column(Float, default=0.5)
    crawl_frequency_hours = Column(Integer, default=24)
    last_crawled = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    
    # Compliance
    robots_txt_allowed = Column(Boolean, default=True)
    requires_selenium = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    leads = relationship("Lead", back_populates="source")


class Lead(Base):
    """B2B Lead with product recommendations"""
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    
    # Signal information
    signal_text = Column(Text, nullable=False)
    signal_url = Column(String(500))
    signal_date = Column(DateTime(timezone=True), index=True)
    signal_type = Column(String(50))
    
    # Extracted entities
    detected_keywords = Column(JSON)
    detected_products = Column(JSON)
    detected_locations = Column(JSON)
    detected_equipment = Column(JSON)
    
    # Product recommendations
    recommended_products = Column(JSON)
    
    # Scoring
    lead_score = Column(Float, index=True)
    intent_strength = Column(String(20))
    urgency_days = Column(Integer)
    confidence = Column(Float)
    
    # Routing
    assigned_officer_id = Column(Integer, ForeignKey("officers.id"), index=True)
    territory_state = Column(String(100))
    
    # Status
    status = Column(String(20), default="new", index=True)
    
    # Follow-up
    contacted_at = Column(DateTime(timezone=True))
    next_action = Column(String(255))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    company = relationship("Company", back_populates="leads")
    source = relationship("Source", back_populates="leads")
    officer = relationship("Officer", back_populates="leads")
    feedback = relationship("Feedback", back_populates="lead")


class Officer(Base):
    """Sales Officer"""
    __tablename__ = "officers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20))
    
    # Territory
    territory_state = Column(String(100), index=True)
    territory_cities = Column(JSON)
    
    # Office
    dsro_office = Column(String(100))
    employee_id = Column(String(50), unique=True)
    
    # Settings
    notification_enabled = Column(Boolean, default=True)
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    leads = relationship("Lead", back_populates="officer")
    feedback = relationship("Feedback", back_populates="officer")


class Feedback(Base):
    """Lead feedback from sales officers"""
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False, index=True)
    officer_id = Column(Integer, ForeignKey("officers.id"), nullable=False)
    
    # Feedback
    action = Column(String(20), nullable=False)
    quality_rating = Column(Integer)
    notes = Column(Text)
    
    # Conversion details
    converted_product = Column(String(100))
    estimated_value = Column(Float)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    lead = relationship("Lead", back_populates="feedback")
    officer = relationship("Officer", back_populates="feedback")
