#  Automated E-Commerce Price Scraper

##  Project Overview
This project is an automated data pipeline designed to monitor competitor pricing on e-commerce websites. It extracts product data (name, price, and URL) daily and securely logs the historical data into a cloud-based Google Sheet for analysis. 

I built this project to demonstrate practical skills in web scraping, cloud API integration, secure credential management, and CI/CD automation.

##  Tech Stack
* **Language:** Python 3
* **Web Scraping:** `requests`, `BeautifulSoup4` (bs4)
* **Cloud Database:** Google Sheets API, Google Drive API
* **Authentication:** `google-auth` (Service Accounts)
* **Automation & CI/CD:** GitHub Actions

##  Key Features
* **Automated Extraction:** Uses BeautifulSoup to parse HTML and extract specific DOM elements.
* **Graceful Error Handling:** If a product price is removed or out of stock, the script catches the error, logs the missing data gracefully, and prevents the pipeline from crashing.
* **Cloud Integration:** Authenticates with Google Cloud via a secure Service Account to push data directly to a live spreadsheet using `gspread`.
* **Serverless Automation:** Scheduled to run autonomously every day at midnight (UTC) using a GitHub Actions `cron` job.
* **Secure Secrets Management:** API keys and JSON credentials are encrypted and stored in GitHub Secrets, ensuring no sensitive data is exposed in the codebase.

##  Architecture & Workflow
1. **Trigger:** GitHub Actions spins up an Ubuntu environment daily.
2. **Setup:** The workflow installs Python dependencies from `requirements.txt`.
3. **Execution:** `scraper.py` fetches the target URL and parses the HTML.
4. **Authentication:** The script pulls the `GOOGLE_CREDENTIALS` environment variable to securely log into Google Cloud.
5. **Storage:** The extracted data is appended as a new row in a connected Google Sheet, timestamped for historical tracking.

##  Future Improvements
* Integrate proxy rotation to bypass strict anti-bot protections on larger e-commerce sites.
* Add email notifications (via SMTP) if a target product's price drops below a certain threshold.
