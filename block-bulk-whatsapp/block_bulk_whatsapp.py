from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=./User_Data")  # Reuse login
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--remote-debugging-port=9222")
# options.add_argument("--headless")

driver = webdriver.Chrome(options=options)
driver.get("https://web.whatsapp.com")
time.sleep(2)  # wait for WhatsApp Web to fully load

def find_and_block_contacts(keyword):
    blocked = []
    
    # Locate and click the search input box
    search_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//div[@role="textbox" and @aria-label="Search input textbox"]'))
    )

    search_input.clear()
    search_input.send_keys(keyword)
    time.sleep(3)  # Wait for search results to populate

    # Get search result chats
    chats = driver.find_elements(By.XPATH, '//span[@dir="auto"]')
    
    for chat in chats:
        name = chat.text.strip().lower()

        if keyword.lower() in name and name not in blocked:
            try:
                print(f"Blocking: {name}")
                ActionChains(driver).move_to_element(chat).click().perform()
                time.sleep(1)

                # Open contact info
                driver.find_element(By.XPATH, '//header//div[@role="button"]').click()
                time.sleep(1)

                # Scroll down and click Block
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)

                block_buttons = driver.find_elements(By.XPATH, "//span[contains(text(), 'Block')]")
                if block_buttons:
                    block_buttons[-1].click()
                    time.sleep(1)
                    confirm_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[.//div[text()='Block']]"))
                    )
                    driver.execute_script("arguments[0].click();", confirm_btn)
                    print(f"{name} blocked.")
                    blocked.append(name)
                else:
                    print(f"No block button found for {name}.")
                time.sleep(1)

                # Clear search for next loop
                search_input = driver.find_element(By.XPATH, '//div[@role="textbox"][@title="Search input textbox"]')
                search_input.clear()
                time.sleep(2)

            except Exception as e:
                print(f"Error processing {name}: {e}")
                continue

find_and_block_contacts("mwada")
