import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Initialize the Edge WebDriver and open the URL
driver = webdriver.Edge()
driver.get("http://127.0.0.1:5000/")
time.sleep(3)  # wait for the page to load

# Locate the text area element by its ID
search_box = driver.find_element(By.ID, "textArea")

# Bot's introduction message
bot_intro = "Hello! I am a Selenium bot created to automate web interactions."

# Simulate typing the introduction one character at a time

search_box.send_keys(bot_intro)
      # Simulate human-like typing speed

# Submit the message
search_box.send_keys(Keys.RETURN)
time.sleep(1000) 
