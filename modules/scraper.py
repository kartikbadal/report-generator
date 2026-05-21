import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

# Request headers to avoid being blocked by the websites

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def get_usd_to_inr() -> float:
    """
    Fetches USD to INR rate using a free public API.
    No API key required.
    """
    try:
        url = "https://api.frankfurter.app/latest?from=USD&to=INR"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        rate = data["rates"]["INR"]

        logger.info(f"USD to INR fetched: {rate}")
        return rate

    except Exception as e:
        logger.error(f"Failed to fetch exchange rate: {e}")
        raise

def get_page_text(url:str) -> str:
        """
        Fetches and returns all visible text from any webpage.
        General purpose scraper for any URL
        
        Args:
            url :Full URL of the webpage
        
        Returns:
            Cleaned text content of the page
        """
        try:
            response = requests.get(url, headers=HEADERS, timeout= 10)
            response.raise_for_status(10)

            soup = BeautifulSoup(response.text, "html.parser")

            # Remove script and style tags - not visible text
            for tag in soup(["script","style"]):
                tag.decompose()
            
            text = soup.get_text(separator = " ", strip = True)
            logger.info(f"Page text fetched from: {url}")
            return text
    
        except Exception as e:
            logger.error(f"Failed to fetch page: {e}")
            raise

