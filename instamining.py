import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

browser = webdriver.Chrome(ChromeDriverManager().install())

main_hashtag = "dog"

browser.get(f"https://www.instagram.com/explore/tags/{main_hashtag}")

header = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "header"))
)
hashtags = header.find_elements_by_class_name("AC7dP")

for hashtag in hashtags:
    hashtag.click()


time.sleep(3)
browser.quit()
