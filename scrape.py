from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import logging
import time
import streamlit as st

class WebScraper:
    def __init__(self):
        self.setup_logging()
        self.setup_driver()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
    def scrape_website(self, url: str, wait_time: int = 5) -> dict:
        try:
            self.logger.info(f"Scraping URL: {url}")
            self.driver.get(url)
            time.sleep(wait_time)  # Wait for dynamic content
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Extract specific elements
            data = {
                'title': soup.title.string if soup.title else '',
                'text_content': soup.get_text(separator=' ', strip=True),
                'links': [a.get('href') for a in soup.find_all('a', href=True)],
                'headers': [h.text for h in soup.find_all(['h1', 'h2', 'h3'])],
                'meta_description': soup.find('meta', {'name': 'description'}).get('content') if soup.find('meta', {'name': 'description'}) else ''
            }
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error scraping {url}: {str(e)}")
            return None
        
    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass
