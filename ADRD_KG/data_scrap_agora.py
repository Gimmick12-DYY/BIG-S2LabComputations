from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time


driver = webdriver.Chrome()
driver.get("https://nda.nih.gov/general-query.html?q=query=collections%20~and~%20orderBy=id%20~and~%20orderDirection=Ascending")
time.sleep(60) # Wait for content to load, and give me time to change to the correct webpage as the script jumps to the wrong page for some reason

last_height = driver.execute_script("return document.body.scrollHeight")
print(f"Initial page height: {last_height}")

max_scroll_attempts = 10 # Prevent infinite loops, adjust as needed
scroll_count = 0



while True and scroll_count < max_scroll_attempts:
    scroll_count += 1
    print(f"Scrolling attempt {scroll_count}...")
    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for new content to load (adjust sleep time or use explicit waits for specific elements)
    time.sleep(3) # Give time for new content to render

    new_height = driver.execute_script("return document.body.scrollHeight")
    print(f"New page height: {new_height}")

    if new_height == last_height:
        # If the page height hasn't changed, we've likely reached the bottom
        print("Reached bottom of the page or no new content loaded.")
        break
    last_height = new_height

titles = driver.find_elements('xpath', "//div[contains(@class, 'col-md-8 filter-content')]")
graph = driver.find_elements('xpath', "//*[starts-with(@id, 'myChart')]")
sampleSizes = []
for sampleSize in graph:
	sampleSizes.append(sampleSize.get_attribute("data-total"))

count = 0

for label in titles:
	print(label.text)
	if(count <= len(sampleSizes)-1):
		print(sampleSizes[count])
	print("\n")
	count += 1

driver.quit()