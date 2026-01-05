import httpx
from bs4 import BeautifulSoup
import json
import re
import asyncio

async def scrape_event_price(url: str, source: str = "ticketmaster"):
    """
    Attempts to scrape the price from a given event URL.
    Returns (price_low, price_high) or (None, None) if failed.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }
    
    async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
        try:
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Scraper: Failed to fetch {url} - Status {response.status_code}")
                return None, None
                
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            
            # Strategy 1: Look for JSON-LD (Schema.org)
            # This is the most reliable way as it's structured data
            scripts = soup.find_all('script', type='application/ld+json')
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    # Handle both single object and list of objects
                    if isinstance(data, list):
                        items = data
                    else:
                        items = [data]
                        
                    for item in items:
                        if item.get('@type') == 'Event':
                            offers = item.get('offers')
                            if offers:
                                return extract_price_from_offers(offers)
                except:
                    continue
                    
            # Strategy 2: Look for common meta tags (OpenGraph, Twitter)
            # Sometimes price is in description
            og_desc = soup.find("meta", property="og:description")
            if og_desc:
                content = og_desc.get("content", "")
                prices = extract_prices_from_text(content)
                if prices:
                    return prices
                    
            # Strategy 3: Regex on visible text (Fallback/Risky)
            # Look for "$XX.XX" patterns
            text = soup.get_text()
            # Simple heuristic: find "Price" or "Tickets" context
            # This is very prone to errors, so maybe skip for now to be safe
            
            return None, None
            
        except Exception as e:
            print(f"Scraper: Error scraping {url}: {e}")
            return None, None

def extract_price_from_offers(offers):
    if isinstance(offers, dict):
        # Single offer
        low = offers.get('lowPrice') or offers.get('price')
        high = offers.get('highPrice') or offers.get('price')
        currency = offers.get('priceCurrency', 'USD')
        
        if low:
            return float(low), float(high) if high else float(low)
            
    elif isinstance(offers, list):
        # Aggregate offer list
        prices = []
        for offer in offers:
            p = offer.get('price')
            if p:
                prices.append(float(p))
            elif offer.get('lowPrice'):
                prices.append(float(offer['lowPrice']))
                
        if prices:
            return min(prices), max(prices)
            
    return None, None

def extract_prices_from_text(text):
    # Matches $10, $10.50, etc.
    matches = re.findall(r'\$(\d+(?:\.\d{2})?)', text)
    if matches:
        prices = sorted([float(p) for p in matches])
        if len(prices) >= 1:
            return prices[0], prices[-1]
    return None
