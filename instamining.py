import csv
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class Instaminer:
    def __init__(self, initial_hashtag, max_hashtags):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.initial_hashtag = initial_hashtag
        self.max_hashtags = max_hashtags
        self.counted_hashtags = []
        self.used_hashtags = []

    def wait_for(self, locator):
        return WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(locator)
        )

    def clean_hashtag(self, hashtag):
        return hashtag[1:]

    def save_file(self):
        file = open(f"{self.initial_hashtag}-report.csv", "w")
        writer = csv.writer(file)
        writer.writerow(["Hashtag", "Post Count"])
        for hashtag in self.counted_hashtags:
            writer.writerow(hashtag)

    def start(self):
        self.get_related(
            f"https://www.instagram.com/explore/tags/{self.initial_hashtag}"
        )

    def get_related(self, target_url):
        self.browser.get(target_url)
        header = self.wait_for((By.TAG_NAME, "header"))
        hashtags = header.find_elements_by_class_name("AC7dP")
        for hashtag in hashtags:
            hashtag_name = self.clean_hashtag(hashtag.text)
            if hashtag_name not in self.used_hashtags:
                ActionChains(self.browser).key_down(Keys.COMMAND).click(
                    hashtag
                ).perform()

        for window in self.browser.window_handles:
            self.browser.switch_to.window(window)
            self.extract_data()
            time.sleep(1)

        if len(self.used_hashtags) < self.max_hashtags:
            for window in self.browser.window_handles[0:-1]:
                self.browser.switch_to.window(window)
                self.browser.close()
            self.browser.switch_to.window(self.browser.window_handles[0])
            self.get_related(self.browser.current_url)
        else:
            self.browser.quit()
            self.save_file()

    def extract_data(self):
        hashtag_name = self.wait_for((By.TAG_NAME, "h1"))
        post_count = self.wait_for((By.CLASS_NAME, "g47SY"))
        if post_count:
            post_count = int(post_count.text.replace(",", ""))
        if hashtag_name:
            hashtag_name = self.clean_hashtag(hashtag_name.text)
        if hashtag_name and post_count:
            if hashtag_name not in self.used_hashtags:
                self.counted_hashtags.append((hashtag_name, post_count))
                self.used_hashtags.append(hashtag_name)


Instaminer("dog", 20).start()
