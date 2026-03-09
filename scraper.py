import requests
import urllib3
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrape_and_save_to_sheets(url, sheet_name="Scraper Results"):
    """
    Fetches product data and appends it to a Google Sheet using cloud secrets.
    """
    today_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    product_name = ""
    product_price = ""
    error_msg = ""
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US, en;q=0.5"
    }
    
    print(f"Fetching data from: {url}...")
    
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            name_element = soup.find("h1")
            product_name = name_element.get_text(strip=True) if name_element else ""
            if not name_element: error_msg += "Name not found. "
                
            price_element = soup.find("p", class_="price_color")
            product_price = price_element.get_text(strip=True) if price_element else ""
            if not price_element: error_msg += "Price not found. "
        else:
            error_msg = f"Failed to retrieve page. Status Code: {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        error_msg = f"Network error: {e}"
        
    row_data = [today_date, product_name, product_price, url, error_msg.strip()]
    
    try:
        print("Connecting to Google Sheets...")
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        # --- CHANGED FOR CLOUD DEPLOYMENT ---
        # We now load the JSON data directly from a secure environment variable
        google_creds_json = os.environ.get("GOOGLE_CREDENTIALS")
        if not google_creds_json:
            raise ValueError("GOOGLE_CREDENTIALS environment variable is missing!")
            
        creds_dict = json.loads(google_creds_json)
        credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        # ------------------------------------
        
        client = gspread.authorize(credentials)
        sheet = client.open(sheet_name).sheet1
        sheet.append_row(row_data)
        
        print(f"\n--- Success ---")
        print(f"Data securely pushed to Google Sheet: '{sheet_name}'")
        
    except Exception as e:
        print(f"\n--- Error ---")
        print(f"Failed to connect to Google Sheets: {e}")

if __name__ == "__main__":
    PRACTICE_URL = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html" 
    scrape_and_save_to_sheets(PRACTICE_URL)