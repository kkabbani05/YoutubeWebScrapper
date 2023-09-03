#imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException

#initialize a web driver instance to control a chrom window in headless mode
options = Options()

#headless mode set on to allow instaces to be launched behind the seen with no UI
options.add_argument('--headless=new')

driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()), options=options)

#scraping logic... 

#Target youtube video url and visting the page on controlled browser
url = 'https://www.youtube.com/watch?v=kuDuJWvho7Q'
driver.get(url)

#Accepting Youtube cookies
try:
    #wait up to 15 seconds for the consent dialog to show up 
    consent_overlay = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, 'dialog'))
    )
    #select the consent option button
    consent_buttons = consent_overlay.find_elements(By.CSS_SELECTOR, '.eom-buttons button.yt-spec-button-shape-next')
    if len(consent_buttons)>1:
        # retrieve and click the Accept All
        accept_all_button = consent_buttons[1]
        accept_all_button.click()
except TimeoutException:
    print('Cookie modal missing')

#wait for Youtube to load the page data
WebDriverWait(driver, 15).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1.ytd-watch-metadata'))
)

#data structure to store scraped info
video = {}

#Extract video title
title = driver \
    .find_element(By.CSS_SELECTOR, 'h1.ytd-watch-metadata') \
    .text

#Dictionary that stores channel info
channel = {}

#scrape the channel info attributes
channel_element = driver \
    .find_element(By.ID, 'owner')
    
channel_url = channel_element \
    .find_element(By.CSS_SELECTOR, 'a.yt-simple-endpoint') \
        .get_attribute('href')
channel_name = channel_element \
    .find_element(By.ID, 'channel-name') \
        .text
        
channel_image = channel_element \
    .find_element(By.ID, 'img') \
        .get_attribute('src')

channel_subs = channel_element \
    .find_element(By.ID, 'owner-sub-count') \
        .text \
            .replace(' subscribers', '')

channel['url'] = channel_url
channel['name'] = channel_name
channel['image'] = channel_image
channel['subs'] = channel_subs

infoContainerElements = driver \
    .find_element(By.CSS_SELECTOR, '#info-container span') 
views = infoContainerElements[0] \
    .text \
        .replace(' views', '')
likes = driver \
    .find_element(By.ID, 'segmented-like-button') \
        .text
video['url'] = url
video['title'] = title
video['channel'] = channel
video['views'] = views
video['likes'] = likes

#close the browser and free up the resources
driver.quit()