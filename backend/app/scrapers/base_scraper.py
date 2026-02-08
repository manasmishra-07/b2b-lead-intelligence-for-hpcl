"""
Base web scraper with robots.txt compliance and rate limiting
"""
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from urllib.robotparser import RobotFileParser
from typing import Dict, List, Optional
from loguru import logger
from app.config.settings import settings


class BaseScraper:
    """Base scraper with ethical scraping practices"""
    
    def __init__(self, user_agent: str = None):
        self.user_agent = user_agent or settings.USER_AGENT
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        self.robots_cache = {}
        self.last_request_time = {}
    
    def check_robots_txt(self, url: str) -> bool:
        """Check if URL is allowed by robots.txt"""
        if not settings.RESPECT_ROBOTS_TXT:
            return True
        
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        
        # Check cache
        if base_url in self.robots_cache:
            rp = self.robots_cache[base_url]
        else:
            # Fetch and parse robots.txt
            rp = RobotFileParser()
            robots_url = urljoin(base_url, '/robots.txt')
            try:
                rp.set_url(robots_url)
                rp.read()
                self.robots_cache[base_url] = rp
            except Exception as e:
                logger.warning(f"Could not fetch robots.txt for {base_url}: {e}")
                # If robots.txt unavailable, assume allowed
                return True
        
        return rp.can_fetch(self.user_agent, url)
    
    def rate_limit(self, domain: str):
        """Implement rate limiting per domain"""
        if domain in self.last_request_time:
            elapsed = time.time() - self.last_request_time[domain]
            if elapsed < settings.SCRAPE_DELAY_SECONDS:
                time.sleep(settings.SCRAPE_DELAY_SECONDS - elapsed)
        
        self.last_request_time[domain] = time.time()
    
    def fetch_page(self, url: str, timeout: int = 10) -> Optional[str]:
        """Fetch page content with error handling"""
        # Check robots.txt
        if not self.check_robots_txt(url):
            logger.warning(f"URL blocked by robots.txt: {url}")
            return None
        
        # Rate limiting
        domain = urlparse(url).netloc
        self.rate_limit(domain)
        
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML content"""
        return BeautifulSoup(html, 'lxml')
    
    def extract_text(self, soup: BeautifulSoup, selector: str) -> List[str]:
        """Extract text from elements matching CSS selector"""
        elements = soup.select(selector)
        return [elem.get_text(strip=True) for elem in elements]
    
    def extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract all links from page"""
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(base_url, href)
            links.append(absolute_url)
        return links
    
    def clean_text(self, text: str) -> str:
        """Clean extracted text"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text.strip()


class NewsScaper(BaseScraper):
    """Scraper for news websites"""
    
    def scrape_article(self, url: str) -> Optional[Dict]:
        """Scrape news article"""
        html = self.fetch_page(url)
        if not html:
            return None
        
        soup = self.parse_html(html)
        
        try:
            # Extract title
            title = soup.find('h1')
            title_text = title.get_text(strip=True) if title else ""
            
            # Extract date (common patterns)
            date_elem = soup.find('time') or soup.find(class_=['date', 'published', 'post-date'])
            date = date_elem.get('datetime', '') if date_elem else ""
            
            # Extract content (common patterns)
            content_div = soup.find('article') or soup.find(class_=['content', 'article-content', 'post-content'])
            content = content_div.get_text(strip=True) if content_div else ""
            
            return {
                'url': url,
                'title': self.clean_text(title_text),
                'date': date,
                'content': self.clean_text(content),
                'type': 'news'
            }
        except Exception as e:
            logger.error(f"Error parsing article {url}: {e}")
            return None


class TenderScraper(BaseScraper):
    """Scraper for tender portals"""
    
    def scrape_tender_list(self, url: str) -> List[Dict]:
        """Scrape tender listing page"""
        html = self.fetch_page(url)
        if not html:
            return []
        
        soup = self.parse_html(html)
        tenders = []
        
        try:
            # This is a generic pattern - need to customize per portal
            tender_rows = soup.find_all('tr', class_=['tender', 'tender-row'])
            
            for row in tender_rows:
                title_elem = row.find('a')
                title = title_elem.get_text(strip=True) if title_elem else ""
                tender_url = title_elem.get('href', '') if title_elem else ""
                
                # Extract other fields
                cells = row.find_all('td')
                
                tender_data = {
                    'title': self.clean_text(title),
                    'url': urljoin(url, tender_url),
                    'type': 'tender'
                }
                
                tenders.append(tender_data)
        
        except Exception as e:
            logger.error(f"Error parsing tenders from {url}: {e}")
        
        return tenders


class CompanyScraper(BaseScraper):
    """Scraper for company websites"""
    
    def scrape_company_info(self, url: str) -> Optional[Dict]:
        """Scrape company information from website"""
        html = self.fetch_page(url)
        if not html:
            return None
        
        soup = self.parse_html(html)
        
        try:
            # Extract company name
            name = soup.find('h1') or soup.find(class_=['company-name', 'brand'])
            company_name = name.get_text(strip=True) if name else ""
            
            # Extract about/description
            about = soup.find(class_=['about', 'description', 'company-info'])
            description = about.get_text(strip=True) if about else ""
            
            # Extract contact info
            contact = soup.find(class_=['contact', 'contact-info'])
            contact_text = contact.get_text(strip=True) if contact else ""
            
            return {
                'url': url,
                'name': self.clean_text(company_name),
                'description': self.clean_text(description),
                'contact': self.clean_text(contact_text),
                'type': 'company_site'
            }
        except Exception as e:
            logger.error(f"Error parsing company site {url}: {e}")
            return None