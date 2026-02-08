"""
Scheduled scraper - Now with REAL RSS data!
"""
from datetime import datetime
from loguru import logger
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.scrapers.gem_scraper import GeMScraper, EconomicTimesScraper
from app.scrapers.rss_scraper import RSSFeedScraper
from app.services.lead_processor import LeadProcessor


class ScraperScheduler:
    """Runs scrapers and processes results into leads"""
    
    def __init__(self):
        self.gem_scraper = GeMScraper()  # Mock data
        self.et_scraper = EconomicTimesScraper()  # Mock data
        self.rss_scraper = RSSFeedScraper()  # REAL DATA!
    
    def run_all_scrapers(self) -> dict:
        """Run all scrapers and process results"""
        
        logger.info("🚀 Starting scraper job...")
        start_time = datetime.utcnow()
        
        results = {
            'gem_tenders': 0,
            'et_news': 0,
            'rss_articles': 0,  # NEW!
            'leads_created': 0,
            'errors': []
        }
        
        db = SessionLocal()
        processor = LeadProcessor(db)
        
        try:
            # 1. Mock GeM tenders (for demo)
            logger.info("📋 Getting demo GeM tenders...")
            gem_tenders = self.gem_scraper.scrape_tenders()
            results['gem_tenders'] = len(gem_tenders)
            
            for tender in gem_tenders:
                try:
                    lead = processor.process_signal(tender)
                    if lead:
                        results['leads_created'] += 1
                        logger.success(f"✅ Created lead: {tender['company_name']}")
                except Exception as e:
                    results['errors'].append(str(e))
            
            # 2. Mock ET news (for demo)
            logger.info("📰 Getting demo ET news...")
            et_news = self.et_scraper.scrape_industry_news()
            results['et_news'] = len(et_news)
            
            for news in et_news:
                try:
                    lead = processor.process_signal(news)
                    if lead:
                        results['leads_created'] += 1
                        logger.success(f"✅ Created lead: {news['company_name']}")
                except Exception as e:
                    results['errors'].append(str(e))
            
            # 3. REAL RSS FEEDS! 🎉
            logger.info("📡 Scraping REAL RSS feeds...")
            rss_articles = self.rss_scraper.scrape_all_feeds()
            results['rss_articles'] = len(rss_articles)
            
            for article in rss_articles:
                try:
                    lead = processor.process_signal(article)
                    if lead:
                        results['leads_created'] += 1
                        logger.success(f"✅ Created REAL lead from RSS: {article['company_name']}")
                except Exception as e:
                    results['errors'].append(str(e))
            
        finally:
            db.close()
        
        elapsed = (datetime.utcnow() - start_time).total_seconds()
        logger.info(f"✅ Scraper job complete in {elapsed:.2f}s: {results}")
        
        return results


def run_scraper_job():
    """Entry point for running scraper job"""
    scheduler = ScraperScheduler()
    return scheduler.run_all_scrapers()


if __name__ == "__main__":
    run_scraper_job()