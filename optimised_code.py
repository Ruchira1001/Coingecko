from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import os
from webdriver_manager.chrome import ChromeDriverManager


# Setup Selenium WebDriver
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")  
options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent bot detection

driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.coingecko.com/")
wait = WebDriverWait(driver, 15)
try:
    
    table_element = wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(@data-controller,'coin-row-ads')]/tbody")))

    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find("table", class_="tw-border-y")

    if table:
    
        headers = [th.text.strip() for th in table.find_all("th")]

 
        data = []
        for row in table.find_all("tr")[1:]:  # Skip header row
            cols = row.find_all("td")
            row_data = [col.text.strip().replace("\n", " ") for col in cols]
            if row_data:
                data.append(row_data)

        # Ensure DataFrame column alignment
        df = pd.DataFrame(data, columns=headers[:len(data[0])])

        # Clean "Buy" text from the table
        df.replace("Buy", "", regex=True, inplace=True)

        # Save DataFrame to Downloads folder
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        file_path = os.path.join(downloads_folder, "crypto1_data.xlsx")
        df.to_excel(file_path, index=False)

        # Display first 20 rows in the console
        print(df.head(20))
        print(f"File saved successfully at: {file_path}")

    else:
        print("No table found!")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    driver.quit()
