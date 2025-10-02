from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import os

LIST_URL = "https://guide.michelin.com/kr/ko/selection/south-korea/restaurants"

def setup_driver():
    """Setup Chrome driver with options"""
    chrome_options = Options()
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def get_all_restaurant_urls(driver):
    """Get all restaurant URLs by going through all pages"""
    all_urls = set()
    
    print(f"Opening listing page: {LIST_URL}")
    driver.get(LIST_URL)
    
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a")))
    time.sleep(2)
    
    # Handle cookie consent popup
    print("Checking for cookie consent popup...")
    try:
        # Common cookie consent button selectors
        cookie_selectors = [
            "button#didomi-notice-agree-button",
            "button.didomi-button",
            "button[aria-label*='Accept']",
            "button[aria-label*='동의']",
            "button:contains('Accept')",
            "button:contains('동의')",
            ".didomi-notice-agree-button",
            "#onetrust-accept-btn-handler"
        ]
        
        cookie_dismissed = False
        for selector in cookie_selectors:
            try:
                cookie_button = driver.find_element(By.CSS_SELECTOR, selector)
                if cookie_button.is_displayed():
                    cookie_button.click()
                    print("  Clicked cookie consent button")
                    time.sleep(2)
                    cookie_dismissed = True
                    break
            except:
                continue
        
        if not cookie_dismissed:
            print("  No cookie popup found or already dismissed")
    except Exception as e:
        print(f"  Cookie handling error (continuing anyway): {e}")
    
    time.sleep(1)
    
    page_num = 1
    max_pages = 50
    
    while page_num <= max_pages:
        print(f"\n=== Processing page {page_num} ===")
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # Get ALL links on the page (not just class 'link')
        all_links = driver.find_elements(By.TAG_NAME, "a")
        print(f"  Total <a> tags on page: {len(all_links)}")
        
        page_count = 0
        for link in all_links:
            href = link.get_attribute("href")
            
            # Look for any link with /restaurant/ (singular) in the URL
            if href and "/restaurant/" in href:
                if href not in all_urls:
                    all_urls.add(href)
                    page_count += 1
        
        print(f"  Found {page_count} new restaurants on this page")
        print(f"  Total unique restaurants so far: {len(all_urls)}")
        
        # Try to find next page
        next_page_found = False
        
        try:
            # Look for page number buttons
            page_buttons = driver.find_elements(By.CSS_SELECTOR, "a, button")
            for button in page_buttons:
                button_text = button.text.strip()
                if button_text == str(page_num + 1):
                    try:
                        if button.is_displayed() and button.is_enabled():
                            driver.execute_script("arguments[0].scrollIntoView();", button)
                            time.sleep(1)
                            driver.execute_script("arguments[0].click();", button)
                            print(f"  Clicked page {page_num + 1} button")
                            time.sleep(4)
                            next_page_found = True
                            break
                    except:
                        pass
            
            # Try direct URL navigation
            if not next_page_found:
                next_url = f"{LIST_URL}?page={page_num + 1}"
                print(f"  Trying URL: {next_url}")
                current_count = len(all_urls)
                driver.get(next_url)
                time.sleep(3)
                
                # Check if we got new restaurants
                test_links = driver.find_elements(By.TAG_NAME, "a")
                test_count = 0
                for link in test_links:
                    href = link.get_attribute("href")
                    if href and "/restaurant/" in href and href not in all_urls:
                        test_count += 1
                
                if test_count > 0:
                    next_page_found = True
                    print(f"  Found {test_count} new restaurants via direct URL")
                else:
                    print(f"  No new restaurants found")
                    
        except Exception as e:
            print(f"  Error: {e}")
        
        if not next_page_found:
            print(f"\nNo more pages. Stopped at page {page_num}")
            break
        
        page_num += 1
    
    return list(all_urls)

def crawl_with_selenium():
    """Crawl Michelin Guide using Selenium"""
    
    driver = setup_driver()
    restaurants = []
    
    try:
        # Get all restaurant URLs
        restaurant_urls = get_all_restaurant_urls(driver)
        
        print(f"\n{'='*80}")
        print(f"Found {len(restaurant_urls)} total restaurants")
        print(f"{'='*80}\n")
        print("Starting to scrape details...\n")
        
        # Visit each restaurant
        for idx, url in enumerate(restaurant_urls, 1):
            print(f"[{idx}/{len(restaurant_urls)}] {url}")
            
            try:
                driver.get(url)
                time.sleep(5)
                
                # Wait for name to load
                try:
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "h1.data-sheet__title"))
                    )
                except:
                    print(f"  Timeout waiting for page")
                    continue
                
                # Extract name
                name = ""
                try:
                    name_elements = driver.find_elements(By.CSS_SELECTOR, "h1.data-sheet__title")
                    for elem in name_elements:
                        text = elem.text.strip()
                        if text:
                            name = text
                            break
                except Exception as e:
                    print(f"  Could not find name: {e}")
                
                # Skip address extraction - removed per user request
                address = ""
                
                # Extract coordinates
                latitude = None
                longitude = None
                try:
                    iframe = driver.find_element(By.CSS_SELECTOR, "iframe[src*='google.com/maps']")
                    iframe_src = iframe.get_attribute("src")
                    if "q=" in iframe_src:
                        coord_part = iframe_src.split("q=")[1].split("&")[0]
                        coords = coord_part.split(",")
                        if len(coords) == 2:
                            latitude = coords[0].strip()
                            longitude = coords[1].strip()
                except:
                    pass
                
                # Extract category (cuisine type only, without price symbols)
                category = ""
                try:
                    all_text_blocks = driver.find_elements(By.CSS_SELECTOR, "div.data-sheet__block--text")
                    for block in all_text_blocks:
                        text = block.text.strip()
                        if "₩" in text:
                            # Remove price symbols (₩₩₩, ₩₩, ₩) and the dot separator
                            category = text.replace("₩₩₩", "").replace("₩₩", "").replace("₩", "")
                            category = category.replace("·", "").strip()
                            category = " ".join(category.split())  # Clean up extra spaces
                            break
                except:
                    pass
                
                # Extract phone
                call_number = None
                try:
                    phone_link = driver.find_element(By.CSS_SELECTOR, "a[href^='tel:']")
                    call_number = phone_link.text.strip()
                except:
                    pass
                
                print(f"  {name}")
                if latitude and longitude:
                    print(f"    Coords: {latitude}, {longitude}")
                if category:
                    print(f"    Type: {category}")
                
                restaurants.append({
                    "name": name,
                    "url": url,
                    "latitude": latitude,
                    "longitude": longitude,
                    "category": category,
                    "call_number": call_number
                })
                
                time.sleep(1)
                
            except Exception as e:
                print(f"  Error: {e}")
                continue
        
    finally:
        driver.quit()
    
    # Save CSV
    project_path = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(project_path, "restaurants_all_pages.csv")
    
    with open(csv_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "url", "latitude", "longitude", "category", "call_number"])
        writer.writeheader()
        writer.writerows(restaurants)
    
    print(f"\nCrawling complete! Saved {len(restaurants)} restaurants to {csv_file}")

if __name__ == "__main__":
    print("="*80)
    print("MICHELIN GUIDE CRAWLER - ALL PAGES")
    print("="*80 + "\n")
    crawl_with_selenium()