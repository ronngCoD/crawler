import time
import random
from tqdm import tqdm
import json
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import lxml
import cchardet
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()


def crawl_company(sCompanyName, numPages=100):
    with open('data/' + sCompanyName + '.txt', 'w', encoding='utf-8') as f:
        sUrl = "https://www.teamblind.com/company/" +sCompanyName+ "/reviews?page=1"
        driver.get(sUrl)
        driver.find_element_by_css_selector('[class="btn_logIn"]').click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='text'")))
        email = driver.find_element_by_css_selector("input[type='text']")
        email.send_keys("ron.ng@chainofdemand.co")
        time.sleep(0.5)
        pas = driver.find_element_by_css_selector("input[type='password']")
        pas.send_keys("asdfghjkl;1")
        driver.find_element_by_css_selector("button[type='button'][class='submit']").click()

        for i in tqdm(range(2, numPages + 2)):
            time.sleep(random.randint(3, 15))
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, l"
                                     "ike Gecko) Chrome/91.0.4472.114 Safari/537.36"}
            requests_session = requests.Session()
            r = requests_session.get(sUrl, headers=headers)
            soup = BeautifulSoup(r.content, 'lxml', )
            reviews = soup.find_all('div', attrs={'class': "review_item"})
            for review in reviews:
                rating = -1
                ratingHTML = review.find('i', attrs={'class': "blind"}).next_sibling
                if ratingHTML is not None:
                    rating = ratingHTML.string
                desc = ''
                descHTML = review.find('h3', attrs={'class': "rvtit"})
                if descHTML is not None:
                    desc = descHTML.text
                pros = ''
                cons = ''
                proconsHTML = review.find_all('strong', attrs={'class': "abt"})
                if proconsHTML:
                    pros = proconsHTML[0].next_sibling.text
                    cons = proconsHTML[1].next_sibling.text
                authorInfo = ''
                authorInfoHTML = review.find('div', attrs={'class': 'auth'})
                if authorInfoHTML is not None:
                    authorInfo = authorInfoHTML.text
                reviewDict = {
                    'rating': rating,
                    'desc': desc,
                    'pros': pros,
                    'cons': cons,
                    'authorInfo': authorInfo
                }
                f.write(json.dumps(reviewDict) + '\n')
            sUrl = "https://www.teamblind.com/company/" +sCompanyName+ "/reviews?page=" + str(i)
            driver.get(sUrl)
            f.flush()


if __name__ == "__main__":
    crawl_company('Amazon', numPages=5)
