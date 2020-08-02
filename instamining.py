import time
from selenium import webdriver
from selenium.webdriver import ActionChains
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
    ActionChains(browser).key_down(Keys.COMMAND).click(hashtag).perform()


for window in browser.window_handles:
    browser.switch_to.window(window)
    hashtag_name = browser.find_element_by_tag_name("h1")
    print(hashtag_name.text[1:])

time.sleep(3)
browser.quit()
