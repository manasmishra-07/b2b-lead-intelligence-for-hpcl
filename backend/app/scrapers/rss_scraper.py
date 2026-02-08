"""
RSS Feed Scraper - Pulls REAL data from public RSS feeds
100% Legal - No web scraping, just reading publicly available feeds
"""
import feedparser
from datetime import datetime
from typing import List, Dict
from loguru import logger
import re


class RSSFeedScraper:
    """Scraper for publicly available RSS feeds"""
    
    def __init__(self):
        # Public RSS feeds - 100% legal to read
        self.feeds = {
            'economic_times': 'https://economictimes.indiatimes.com/rssfeedstopstories.cms',
            'business_standard': 'https://www.business-standard.com/rss/home_page_top_stories.rss',
            'pib_business': 'https://pib.gov.in/rss/business.xml',
            'moneycontrol': 'https://www.moneycontrol.com/rss/businessnews.xml',
        }
        
        # Keywords to filter relevant news
        self.relevant_keywords = [
            'expansion', 'plant', 'project', 'investment', 'tender',
            'power', 'energy', 'fuel', 'diesel', 'petroleum', 'oil',
            'construction', 'infrastructure', 'manufacturing',
            'steel', 'cement', 'chemical', 'refinery', 'pipeline',
            'bitumen', 'road', 'highway', 'railway'
        ]
        
        # Known company names to extract
        self.companies = [
            'Reliance', 'Tata', 'Adani', 'JSW', 'Ultratech', 'L&T',
            'NTPC', 'ONGC', 'IOCL', 'BPCL', 'HPCL', 'Coal India',
            'Power Grid', 'SAIL', 'Hindalco', 'Vedanta', 'Grasim',
            'ACC', 'Ambuja', 'Shree Cement', 'Asian Paints', 'Marico',
            'Indian Oil', 'Bharat Petroleum', 'Hindustan Petroleum'
        ]
    
    def scrape_all_feeds(self) -> List[Dict]:
        """Scrape all RSS feeds and return relevant articles"""
        
        logger.info("📡 Scraping REAL RSS feeds...")
        all_articles = []
        
        for source_name, feed_url in self.feeds.items():
            try:
                logger.info(f"Reading {source_name}...")
                articles = self._scrape_feed(feed_url, source_name)
                all_articles.extend(articles)
                logger.info(f"✅ Found {len(articles)} relevant articles from {source_name}")
            except Exception as e:
                logger.error(f"❌ Error reading {source_name}: {e}")
        
        logger.info(f"📰 Total REAL articles scraped: {len(all_articles)}")
        return all_articles
    
    def _scrape_feed(self, feed_url: str, source_name: str) -> List[Dict]:
        """Scrape a single RSS feed"""
        
        articles = []
        
        try:
            # Parse RSS feed
            feed = feedparser.parse(feed_url)
            
            # Process each entry
            for entry in feed.entries[:20]:  # Top 20 articles
                
                # Extract data
                title = entry.get('title', '')
                summary = entry.get('summary', '') or entry.get('description', '')
                link = entry.get('link', '')
                published = entry.get('published', '')
                
                # Combine title and summary
                full_text = f"{title}. {summary}"
                
                # Check if relevant
                if not self._is_relevant(full_text):
                    continue
                
                # Extract company name
                company_name = self._extract_company(full_text)
                
                # Create article data
                article = {
                    'company_name': company_name,
                    'signal_text': full_text[:500],  # Limit length
                    'signal_url': link,
                    'signal_type': 'news',
                    'source_domain': source_name,
                    'detected_keywords': self._extract_keywords(full_text),
                    'scraped_at': datetime.utcnow().isoformat(),
                    'published_date': published
                }
                
                articles.append(article)
        
        except Exception as e:
            logger.error(f"Error parsing feed {feed_url}: {e}")
        
        return articles
    
    def _is_relevant(self, text: str) -> bool:
        """Check if article is relevant to our keywords"""
        text_lower = text.lower()
        
        # Check if any keyword is present
        for keyword in self.relevant_keywords:
            if keyword in text_lower:
                return True
        
        return False
    
    def _extract_company(self, text: str) -> str:
        """Extract company name from text"""
        
        # Check for known companies
        for company in self.companies:
            # Match company name (case insensitive)
            pattern = r'\b' + re.escape(company) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                # Return full company name
                return f"{company} Limited"
        
        # If no company found, try to extract from beginning
        # Often news articles start with company name
        words = text.split()
        if len(words) >= 2:
            # Check first 2-3 words
            potential_company = ' '.join(words[:2])
            if potential_company[0].isupper():
                return potential_company
        
        return "Industry News"
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from text"""
        text_lower = text.lower()
        found_keywords = []
        
        for keyword in self.relevant_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        return found_keywords[:5]  # Return top 5


def scrape_rss_feeds():
    """Entry point for RSS scraping"""
    scraper = RSSFeedScraper()
    return scraper.scrape_all_feeds()


if __name__ == "__main__":
    # Test the RSS scraper
    articles = scrape_rss_feeds()
    print(f"\n✅ Scraped {len(articles)} REAL articles from RSS feeds")
    
    # Show first article
    if articles:
        print("\nSample article:")
        print(f"Company: {articles[0]['company_name']}")
        print(f"Text: {articles[0]['signal_text'][:200]}...")
        print(f"URL: {articles[0]['signal_url']}")