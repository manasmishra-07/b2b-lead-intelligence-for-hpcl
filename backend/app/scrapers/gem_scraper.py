"""
Demo Scraper - Simulates realistic tender/news data
In production, this would connect to APIs or licensed data feeds
"""
from datetime import datetime, timedelta
from typing import List, Dict
import random
from loguru import logger


class GeMScraper:
    """Simulates GeM tender data (realistic mock)"""
    
    def scrape_tenders(self) -> List[Dict]:
        """Generate realistic tender data"""
        
        logger.info("📋 Generating realistic GeM tender data...")
        
        tenders = [
            {
                'company_name': 'National Thermal Power Corporation Ltd',
                'signal_text': 'NTPC Rihand invites tenders for supply of 5000 MT Furnace Oil for boiler operations. Requirement for power generation unit. Delivery required by March 2026.',
                'signal_url': 'https://gem.gov.in/tender/NTPC-2026-FO-001',
                'signal_type': 'tender',
                'source_domain': 'gem.gov.in',
                'detected_keywords': ['furnace oil', 'boiler', 'power generation'],
                'location': 'Sonebhadra, Uttar Pradesh',
                'scraped_at': datetime.utcnow().isoformat()
            },
            {
                'company_name': 'Indian Railways CORE',
                'signal_text': 'Indian Railways Central Organization for Railway Electrification requires 10000 liters HSD (High Speed Diesel) for DG sets and construction equipment at various project sites.',
                'signal_url': 'https://gem.gov.in/tender/CORE-2026-HSD-045',
                'signal_type': 'tender',
                'source_domain': 'gem.gov.in',
                'detected_keywords': ['HSD', 'diesel', 'DG sets'],
                'location': 'New Delhi',
                'scraped_at': datetime.utcnow().isoformat()
            },
            {
                'company_name': 'L&T Construction - Metro Rail Project',
                'signal_text': 'L&T Metro Rail Project Bangalore requires Bitumen VG-30 grade 500 MT for road construction and surface works. Part of Phase 3 metro expansion project.',
                'signal_url': 'https://gem.gov.in/tender/LT-BMRCL-2026-089',
                'signal_type': 'tender',
                'source_domain': 'gem.gov.in',
                'detected_keywords': ['bitumen', 'road construction', 'metro'],
                'location': 'Bangalore, Karnataka',
                'scraped_at': datetime.utcnow().isoformat()
            },
            {
                'company_name': 'Gujarat State Road Development Corporation',
                'signal_text': 'GSRDC invites bids for supply of Bitumen emulsion 2500 MT for state highway maintenance and new road projects under PMGSY scheme.',
                'signal_url': 'https://gem.gov.in/tender/GSRDC-2026-BE-234',
                'signal_type': 'tender',
                'source_domain': 'gem.gov.in',
                'detected_keywords': ['bitumen', 'highway', 'road'],
                'location': 'Gandhinagar, Gujarat',
                'scraped_at': datetime.utcnow().isoformat()
            },
            {
                'company_name': 'Marico Industries Ltd',
                'signal_text': 'Marico edible oil division requires Food Grade Hexane 50000 liters for solvent extraction plant. ISO certified supplier required for ongoing contract.',
                'signal_url': 'https://gem.gov.in/tender/MARICO-2026-HEX-012',
                'signal_type': 'tender',
                'source_domain': 'gem.gov.in',
                'detected_keywords': ['hexane', 'solvent extraction', 'edible oil'],
                'location': 'Mumbai, Maharashtra',
                'scraped_at': datetime.utcnow().isoformat()
            }
        ]
        
        logger.info(f"✅ Generated {len(tenders)} realistic GeM tenders")
        return tenders


class EconomicTimesScraper:
    """Simulates Economic Times news (realistic mock)"""
    
    def scrape_industry_news(self) -> List[Dict]:
        """Generate realistic industry news"""
        
        logger.info("📰 Generating realistic ET news data...")
        
        news = [
            {
                'company_name': 'Adani Power Ltd',
                'signal_text': 'Adani Power announces 1600 MW thermal power plant expansion in Chhattisgarh. Project requires continuous fuel oil supply for next 3 years. Construction to begin March 2026.',
                'signal_url': 'https://economictimes.indiatimes.com/industry/energy/adani-power-expansion',
                'signal_type': 'news',
                'source_domain': 'economictimes.indiatimes.com',
                'scraped_at': datetime.utcnow().isoformat()
            },
            {
                'company_name': 'JSW Steel Ltd',
                'signal_text': 'JSW Steel plans ₹5000 crore expansion of Vijayanagar plant. New blast furnaces to be commissioned requiring increased diesel and industrial fuel supplies.',
                'signal_url': 'https://economictimes.indiatimes.com/industry/metals/jsw-steel-expansion',
                'signal_type': 'news',
                'source_domain': 'economictimes.indiatimes.com',
                'scraped_at': datetime.utcnow().isoformat()
            },
            {
                'company_name': 'UltraTech Cement Ltd',
                'signal_text': 'UltraTech to set up 3 new grinding units across North India with combined capacity of 6 MTPA. Project involves significant diesel requirement for construction and operations.',
                'signal_url': 'https://economictimes.indiatimes.com/industry/cement/ultratech-expansion',
                'signal_type': 'news',
                'source_domain': 'economictimes.indiatimes.com',
                'scraped_at': datetime.utcnow().isoformat()
            },
            {
                'company_name': 'Asian Paints Ltd',
                'signal_text': 'Asian Paints announces new manufacturing facility in Gujarat. Plant to produce decorative coatings with capacity of 400 million liters. Requires solvents and petroleum derivatives.',
                'signal_url': 'https://economictimes.indiatimes.com/industry/paints/asian-paints-new-plant',
                'signal_type': 'news',
                'source_domain': 'economictimes.indiatimes.com',
                'scraped_at': datetime.utcnow().isoformat()
            }
        ]
        
        logger.info(f"✅ Generated {len(news)} realistic ET news articles")
        return news