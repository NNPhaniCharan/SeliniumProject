import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

options = Options()
options.headless = True
# options.add_argument('window-size=1920x1080')

# website = 'https://www.audible.com/search'
website = 'https://www.audible.com/adblbestsellers?ref_pageloadid=not_applicable&ref=a_search_t1_navTop_pl0cg1c0r0&pf_rd_p=334a4a9c-12d2-4c3f-aee6-ae0cbc6a1eb0&pf_rd_r=T7P0QQWT7E201PBS9GF1&pageLoadId=wrq7QjXwQfmfPyI1&creativeId=7ba42fdf-1145-4990-b754-d2de428ba482'
driver = webdriver.Chrome(options=options)
driver.get(website)
driver.maximize_window()

pagination = driver.find_element(By.XPATH,'//ul[contains(@class,"pagingElements")]')
pages = pagination.find_elements(By.TAG_NAME,'li')
lastpage = int(pages[-2].text)

next_page = driver.find_element(By.XPATH,'//span[contains(@class,"nextButton")]')

current_page = 1

book_title = []
book_author = []
book_length = []

while current_page<=lastpage:
    # time.sleep(3)
    # container = driver.find_element(By.XPATH,'//div[@class="adbl-impression-container "]/div/span[2]/ul')
    container = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//div[@class="adbl-impression-container "]/div/span[2]/ul')))
    # products = container.find_elements(By.XPATH,'./li')
    products = WebDriverWait(container,5).until(EC.presence_of_all_elements_located((By.XPATH,'./li')))

    for product in products:
        book_title.append(product.find_element(By.XPATH,'.//h3[contains(@class,"bc-heading")]').text)
        book_author.append(product.find_element(By.XPATH,'.//li[contains(@class,"authorLabel")]').text)
        book_length.append(product.find_element(By.XPATH,'.//li[contains(@class,"runtimeLabel")]').text)
    current_page = current_page + 1
    try:
        next_page = driver.find_element(By.XPATH, '//span[contains(@class,"nextButton")]')
        next_page.click()
    except:
        pass


df = pd.DataFrame({'book_title' : book_title, 'book_author' : book_author, 'book_length' : book_length})
df.to_csv('Audible_BestSeller.txt',index=False)
