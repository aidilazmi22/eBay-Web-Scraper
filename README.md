# eBay Web Scraper Documentation

## Project Overview
This Python project is a web scraper for extracting product data from eBay. It uses Selenium to automate browser interactions and Pandas to store the data in an Excel file. The scraper allows users to search for products based on keywords, refine the search by listing type (e.g., All, Auction, or Buy It Now), and scrape data across multiple pages.

### Features
- **Search Functionality**: Allows users to specify keywords to search for on eBay.
- **Refinement Options**: Supports filtering results by listing type (e.g., Auction, Buy It Now).
- **Pagination**: Scrapes multiple pages of search results.
- **Data Extraction**: Extracts product name, price, condition, location, and seller username.
- **Data Storage**: Saves the scraped data into an Excel file.

## Prerequisites
- Python 3.x
- Selenium
- Pandas
- ChromeDriver
- Web browser: Google Chrome

## Installation
1. Install Python packages:
    ```bash
    pip install selenium pandas openpyxl
    ```

2. Download ChromeDriver:
    - Ensure that ChromeDriver matches your Google Chrome version.
    - Add ChromeDriver to your system PATH or place it in the script's directory.

## How to Use
1. Run the script:
    ```bash
    python ebay2.py
    ```

2. Input the search keyword(s) when prompted.

3. Select a refinement option:
    - 1 for All
    - 2 for Auction
    - 3 for Buy It Now

4. Enter the number of pages to scrape.

5. The script will scrape the data and save it as an Excel file with a filename in the format:
    ```php
    ebay_<keyword>_<serial_number>_<current_date>.xlsx
    ```

## Output
The output Excel file contains the following columns:
- **Product Name**: The name of the product.
- **Price**: The price listed on eBay.
- **Condition**: The condition of the product (e.g., New, Used).
- **Location**: The location of the seller.
- **Seller**: The seller's username.

## Disclaimer
This project is intended for educational and personal use only. Please note the following:

- **Terms of Use**: Ensure compliance with eBay’s terms of service and scraping policies.
- **Rate Limits**: Avoid sending excessive requests that may overload eBay's servers.
- **Data Accuracy**: The extracted data may not always be accurate or up-to-date.
- **Legal Liability**: The author of this script assumes no liability for any misuse or damage resulting from its use.
- **Personal Responsibility**: It is your responsibility to use this tool ethically and lawfully.

## Limitations
- The script relies on eBay’s current page structure and may require updates if eBay changes its layout.
- Does not handle CAPTCHA or advanced bot detection mechanisms.
- May not work with all product categories or listings.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
