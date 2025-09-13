import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


# How many times to scroll the page and get a batch of articles
max_num_scrols = 300

def get_news_data(article: WebElement):
    try:
        news_type_element = article.find_element(By.CLASS_NAME, 'c-card--grid-card-trending__info-prefix')
        time_ago_element = article.find_element(By.CLASS_NAME, 'field--name-datetime')
        title_element = article.find_element(By.CLASS_NAME, 'c-card--grid-card-trending__headline')
        link = article.get_attribute('href')

        return {
            'type': news_type_element.get_attribute('innerHTML'),
            'time_ago': time_ago_element.get_attribute('innerHTML'),
            'title': title_element.get_attribute('innerHTML'),
            'link': link
        }
    except Exception as e:
        print("An error has occurred:")
        print(e)

        return {}


def export_data():
    filename = f"./article_links_{datetime.datetime.now().strftime('%d-%m-%y_%H-%M-%S')}"

    root = driver.find_element(By.TAG_NAME, 'html')

    with open(f"{filename}.html", "w", encoding="utf-8") as file:
        file.write(root.get_attribute('innerHTML'))

    print(f"Saved page contents to {filename}.html")

    news_articles = driver.find_elements(By.CLASS_NAME, "c-card--grid-card-trending")
    articles_data = [get_news_data(article) for article in news_articles]

    df = pd.DataFrame(data=articles_data)
    df["title"] = df["title"].str.strip()
    df.to_csv(f"{filename}.csv")

    print(f"Saved article links to {filename}.csv")


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get('https://www.ufc.com/trending/all')

    try:
        # Wait for the website to load
        time.sleep(2)

        # Reject cookies
        reject_cookies_button = driver.find_element(By.ID, 'onetrust-reject-all-handler')
        reject_cookies_button.click()

        for i in range(max_num_scrols):
            if i % 10 == 0:
                print("Batch", i)

            # Scroll down and load next batch
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                load_more_button = WebDriverWait(driver, timeout=10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[title="Load more items"]'))
                )
                load_more_button.click()

                loading_spinner = WebDriverWait(driver, timeout=10).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, 'ajax-progress'))
                )
            except KeyboardInterrupt:
                print("Keyboard interrupt, quitting...")
                break
            except Exception as e:
                print("An error has occurred:")
                print(e)
    except KeyboardInterrupt:
        print("Keyboard interrupt, quitting...")
    except Exception as e:
        print("An error has occurred")
        print(e)

    finally:
        export_data()
        driver.quit()