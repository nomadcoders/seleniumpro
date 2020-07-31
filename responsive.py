import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

browser = webdriver.Chrome(ChromeDriverManager().install())

browser.get("https://nomadcoders.co")
browser.maximize_window()

sizes = [320, 480, 960, 1366, 1920]

for size in sizes:
    browser.set_window_size(size, 1027)
    time.sleep(5)
