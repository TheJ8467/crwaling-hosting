import requests
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options

ANSAN_NEWS_URL="http://www.ansannews.co.kr/"

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

## Scrapping news
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get(ANSAN_NEWS_URL)


def fetch_articles():
    articles = []

    for i in range(1, 4):
        article_img = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div[2]/div/section/div[3]/div[2]/div/div[1]/div[1]/article/section/div/ul/li[{i}]/a/div[1]")
        article_img_src = f"http://www.ansannews.co.kr{article_img.get_attribute('style').split('(')[1].split(')')[0]}".replace('"', '')

        article_anchor_tag = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div[2]/div/section/div[3]/div[2]/div/div[1]/div[1]/article/section/div/ul/li[{i}]/a")
        article_href = article_anchor_tag.get_attribute('href')

        article_title = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div[2]/div/section/div[3]/div[2]/div/div[1]/div[1]/article/section/div/ul/li[{i}]/a/div[1]/span").text
        article_desc = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div[2]/div/section/div[3]/div[2]/div/div[1]/div[1]/article/section/div/ul/li[{i}]/a/div[2]/p").text

        articles.append({
            'img_src': article_img_src,
            'link': article_href,
            'title': article_title,
            'desc': article_desc
        })
    driver.close()
    return articles

def fetch_sub_articles():
    sub_articles = []
    for k in range(1,4):
        for j in range(1, 7):
            try:
                sub_article_title = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div[2]/div/section/div[3]/div[2]/div/div[1]/div[3]/article[{k}]/section/div/ul/li[{j}]/div[1]/a/strong").text
                sub_article_img_src = f"http://www.ansannews.co.kr{driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[2]/div/section/div[3]/div[2]/div/div[1]/div[3]/article[{k}]/section/div/ul/li[{j}]/a').get_attribute('style').split('(')[1].split(')')[0]}".replace('"', '')
                sub_article_desc = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div[2]/div/section/div[3]/div[2]/div/div[1]/div[3]/article[{k}]/section/div/ul/li[{j}]/p/a").text
                sub_article_href = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div[2]/div/section/div[3]/div[2]/div/div[1]/div[3]/article[{k}]/section/div/ul/li[{j}]/p/a").get_attribute('href')
                sub_articles.append({
                    'img_src': sub_article_img_src,
                    'title': sub_article_title,
                    'desc': sub_article_desc,
                    'link': sub_article_href,
                })
            except NoSuchElementException:
                try:
                    sub_article_title = driver.find_element(By.XPATH,
                                                            f"/html/body/div[1]/div/div[2]/div/section/div[3]/div[2]/div/div[1]/div[3]/article[{k}]/section/div/ul/li[{j}]/div[1]/a/strong").text
                    sub_article_desc = driver.find_element(By.XPATH,
                                                           f"/html/body/div[1]/div/div[2]/div/section/div[3]/div[2]/div/div[1]/div[3]/article[{k}]/section/div/ul/li[{j}]/p/a").text
                    sub_article_href = driver.find_element(By.XPATH,
                                                           f"/html/body/div[1]/div/div[2]/div/section/div[3]/div[2]/div/div[1]/div[3]/article[{k}]/section/div/ul/li[{j}]/p/a").get_attribute(
                        'href')

                    sub_articles.append({

                        'title': sub_article_title,
                        'desc': sub_article_desc,
                        'link': sub_article_href,
                    })
                except NoSuchElementException:
                    continue
    driver.close()
    return sub_articles

