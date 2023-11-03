import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from data_collection import get_data_flags
from selenium.webdriver.chrome.options import Options
import itertools
import threading
import time
import sys
from datetime import datetime



chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless=new") # for Chrome >= 109
# chrome_options.add_argument("--headless")
# chrome_options.headless = True # also works

def scrape_and_save_data(data_flags):
    
    driver = webdriver.Chrome(options=chrome_options)

    final_data = []

    for data in data_flags:
        data_url = data.strip('[]')
        url = f"https://cims.cidb.gov.my/smis/regcontractor/reglocalsearch_view.vbhtml?search=P&comSSMNo={data_url}"
        driver.get(url)
        info_body = driver.find_elements(By.XPATH, "//tbody/tr")
        data_dict = {}

        for item in info_body:
            text = item.text

            if text.startswith("Name "):
                data_dict["Name"] = text.replace("Name ", "")
            elif text.startswith("Registered Address "):
                data_dict["Registered Address"] = text.replace("Registered Address ", "")
            elif text.startswith("Tel No "):
                data_dict["Tel No"] = text.replace("Tel No ", "")
            elif text.startswith("Fax No"):
                data_dict["Fax No"] = "Fax No"  # Since there is no associated value
            elif text.startswith("Correspondence Address "):
                data_dict["Correspondence Address"] = text.replace("Correspondence Address ", "")
            elif text.startswith("PPK Registration No "):
                data_dict["PPK Registration No"] = text.replace("PPK Registration No ", "")
            elif text.startswith("Member Since "):
                data_dict["Member Since"] = text.replace("Member Since ", "")
            elif text.startswith("Current Registration Expiry Date "):
                data_dict["Current Registration Expiry Date"] = text.replace("Current Registration Expiry Date ", "").strip()
                today = datetime.today().date()
                expiry_date = datetime.strptime(data_dict["Current Registration Expiry Date"], "%d/%m/%Y").date()
                if expiry_date < today:
                    data_dict["Status"] = "Expired"
                else:
                    data_dict["Status"] = "Active"
        
            elif not text.strip():  # Check for empty lines to indicate the end of one entry
                if data_dict:  # Add the entry if it's not an empty dictionary
                    final_data.append(data_dict)
                    data_dict = {}
        
    driver.quit()
    # Create a DataFrame to store the data
    df = pd.DataFrame(final_data)

    # Save the DataFrame to an Excel file
    output_file = 'updated_output_data.xlsx'
    folder_path = '/Users/yb/Documents/cibd/data/'
    file_path = folder_path + output_file
    df.to_excel(file_path, index=False)

    print(f"Data saved to {output_file}")

    
#here is the animation
done = False
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     ')

def main_process():
    data_flags = get_data_flags()
    scrape_and_save_data(data_flags)

t1 = threading.Thread(target=animate)
t2 = threading.Thread(target=main_process)

t1.start()
t2.start()

t2.join()  # wait for the main process to finish
done = True
t1.join()  # wait for the animation to stop


# Run the script
# $ python scraper.py
# Data saved to output.xlsx
# Check the output
# $ ls
# output.xlsx
# $ open output.xlsx
# The output should look like this:
# Image for post


