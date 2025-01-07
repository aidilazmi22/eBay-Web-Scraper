import time
import pandas as pd
import re
import random
import sys
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

start_time = time.time()  # Start timer

# Setup Selenium WebDriver with headless mode
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode (no UI)
options.add_argument('--disable-gpu')  # Performance improvement
options.add_argument('--window-size=1920,1080')  # Ensure proper resolution in headless mode
options.add_argument('--disable-notifications')  # Disable notification request prompt
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=options)

print("--- eBay [Web Scraper] by aidilazmi22 ---\n")

# Request keyword input from user (e.g. 'toaster', 'air conditioner', 'smart tv', 'washing machine', etc.)
while True:
    search_input = re.sub(r"\s+", "+", input("Enter search keyword(s): ")).strip()  # Strip whitespace
    if not search_input:
        print("Input cannot be blank or just spaces. Please try again.\n")
    elif search_input:
        keyword = search_input
        break

# Ask user to select one of the refinement options
while True:
    text = """
Search refinement options:
1 = All
2 = Auction
3 = Buy It Now
"""
    print(text)

    refinements = {
        "1": "&LH_All=1",  # All selected
        "2": "&LH_Auction=1",  # Auction
        "3": "&LH_BIN=1"  # Buy It Now
    }

    option = input("Select an option (1, 2, or 3): ").strip().upper()  # Strip whitespace
    if not option:  # Check for blank input
        print("Input cannot be blank or just spaces. Please try again.\n")
    elif option in refinements:
        refinement = refinements[option]
        break
    else:
        print("Invalid input. Please enter only 1, 2, or 3.\n")

# Number of pages to scrape
while True:
    number = input("Enter the number of pages to scrape: ")
    if not number:  # Check for blank input
        print("Input cannot be blank or just spaces. Please try again.\n")
    elif number.isdigit():  # Accept only integer input
        total_pages = int(number)
        break
    else:
        print("Invalid input. Please enter only number(s) without decimal. (e.g. 1, 10, 50)")

# Open the eBay website
print("\nInitializing...")
url = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={keyword}&_sacat=0{refinement}&_pgn=1"
print("\n" + "Current URL: " + url)
driver.get(url)

# Wait for the table to load
try:
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.srp-results > li'))
    )
except:
    print("Error! No intended element(s) found on the page. Exiting...")
    sys.exit()  # Stop the program

# Function to extract data from the current page
def extract_data():
    rows = driver.find_elements(By.CSS_SELECTOR, 'ul.srp-results > li div.s-item__wrapper')

    data_rows = []  # Temporary storage for rows to sort later

    for row in rows:
        try:
            # Check if the row has seller info
            seller_info_element = row.find_element(By.CSS_SELECTOR, '.s-item__seller-info')
            seller_text = seller_info_element.text.strip()
            seller = seller_text.split(' ')[0]  # Extract the seller's name

            # Extract the product name
            item_name_element = row.find_element(By.CSS_SELECTOR, '.s-item__title')
            raw_product_name = item_name_element.text.strip()
            product_name = re.sub(r'^New Listing', '', raw_product_name, flags=re.IGNORECASE).strip()

            # Extract the price
            price_element = row.find_element(By.CSS_SELECTOR, '.s-item__price')
            price = price_element.text.strip()

            # Extract the product condition
            condition_element = row.find_element(By.CSS_SELECTOR, '.SECONDARY_INFO')
            condition = condition_element.text.strip()

            # Extract the location
            location_element = row.find_element(By.CSS_SELECTOR, '.s-item__location.s-item__itemLocation')
            location_text = location_element.text.strip()
            location = re.sub(r'^from\s+', '', location_text, flags=re.IGNORECASE).strip()

            customized_row_data = [
                product_name,  # Product Name
                price,  # Price
                condition,  # Condition
                location,  # Location
                seller,  # Seller
            ]
            data_rows.append(customized_row_data)
            print(customized_row_data)

        except Exception:
            # Skip rows that don't have seller info or other elements
            continue

    print()  # Blank row for neatness while program is running
    return data_rows

# Initialize an empty list to store all data
all_data = []

# Loop through pages numerically
for page in range(1, total_pages + 1):
    print(f"Scraping page {page} of {total_pages}...\n")

    # Extract data from the current page
    all_data.extend(extract_data())

    # If not on the last page, go to the next page
    if page < total_pages:
        try:
            # Random delay for rate limiting
            delay = random.uniform(5.0, 10.0)  # Random delay between 5 and 10 seconds
            print(f"Rate limiting: Waiting for {delay:.2f} seconds...\n")
            time.sleep(delay)

            # Construct the URL for the next page
            next_page_url = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={keyword}&_sacat=0{refinement}&_pgn={page + 1}"
            print("Current URL: " + next_page_url)
            driver.get(next_page_url)

            # Wait for the new page to load
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.srp-results > li'))
            )
        except Exception:
            print(f"Error navigating to page {page + 1}. Possible end of search result.\n")
            break

# Close the browser
driver.quit()

# Get the current date
current_date = date.today()
serial_number = random.randint(100000,999999)  # Add random number to file name
filename = f"ebay_{keyword}_{serial_number}_{current_date}"

# Save data to an Excel file using pandas
header = ['Product Name', 'Price', 'Condition', 'Location', 'Seller']  # Add headers
df = pd.DataFrame(all_data)
df.to_excel(f"{filename}.xlsx", index=False, header=header, engine='openpyxl')
# print(f"Data has been extracted, and saved to '{filename}.xlsx'\n")

end_time = time.time()  # End timer
elapsed_time = end_time - start_time
print(f"Time Elapsed: {elapsed_time:.2f} seconds")  # Print elapsed time

###########################################################################