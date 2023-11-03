from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def get_data_flags():
    # Start a Chrome WebDriver
    driver = webdriver.Chrome()
    
    # Navigate to the web page
    url = "https://cims.cidb.gov.my/smis/regcontractor/reglocalsearchcontractor.vbhtml"
    driver.get(url)
    
    # Locate the dropdown menu and select the "1000" option
    select_1000 = Select(driver.find_element(By.ID, 'selpagesize'))
    select_1000.select_by_value('1000')
    
    # Locate dropdown menu and select expired
    select_expired = Select(driver.find_element(By.ID, 'selvalidity'))
    select_expired.select_by_visible_text('Expired')
    
    # Scroll down (you can adjust the scroll amount as needed)
    
    paparan_links = driver.find_elements(By.CLASS_NAME, 'open-AddBookDialog1')
    
    data_flags = []
    
    for element in paparan_links:
        data_flag = element.get_attribute('data-flag')
        data_flags.append(data_flag)
    
    driver.quit()
    
    return data_flags

if __name__ == "__main__":
    data_flags = get_data_flags()
    print("Data Flags:", data_flags)