from news import LoadSelenium
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
)
from typing import List
from utils.type_hint import ArticleTtype
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.constant import PAGE_LOAD_TIMEOUT
from settings.decorator import retry 


class DetikNews(LoadSelenium):
    def __init__(self, keyword: str | None) -> None:
        super().__init__()
        self.url: str = f"https://www.detik.com/search/searchall?query={keyword}"
        self.prev_url = self.url
        self.list_article_link: List[str] = []

    def do_search(self) -> None:
        self.driver.get(self.url)

    def do_apply_filter(self) -> None:
        # == Terbaru
        terbaru_el = self.driver.find_element(By.CSS_SELECTOR, "a[dtr-act='terbaru']")
        terbaru_el.click()

        # == Berita
        berita_el = self.driver.find_element(By.CSS_SELECTOR, "a[dtr-act='berita']")
        berita_el.click()

        # == Hari ini
        select_el = self.driver.find_element(By.ID, "timeselect")
        select_el.click()

        hari_ini = self.driver.find_element(
            By.CSS_SELECTOR, "select > option[value='1']"
        )
        hari_ini.click()

        self.prev_url = self.driver.current_url

    def do_get_pagination_links(self) -> List[str]:
        # Get maximum 2 pages, probably including "Prev" or "Next" btn
        pagination_container = self.driver.find_elements(
            By.CSS_SELECTOR, ".pagination > a[dtr-evt='search result']"
        )[:2]
        # Get all pagination links 
        pagination_link_list: List[str] = [
            href 
            for p in pagination_container
            if p.text.lower() not in ["prev", "next"] and (href := p.get_attribute("href"))
        ]
        return pagination_link_list

    @retry(exec_msg="Articles")
    def do_get_articles(self, pagination_list: List[str]) -> List[ArticleTtype]:
        article: List[ArticleTtype] = []

        for page_link in pagination_list:
            # Navigate to next pagination link
            self.list_article_link: List[str] = []
            self.driver.get(page_link)

            # Get list of news
            content_container = self.driver.find_element(
                By.CSS_SELECTOR, ".list-content"
            )
            list_content = content_container.find_elements(
                By.CSS_SELECTOR, ".list-content__item"
            )

            # Get all article link for each page
            for content in list_content:
                title = content.find_element(By.CSS_SELECTOR, ".media__title > a")
                title_link = title.get_attribute("href")

                if title_link is None or "video" in title.text.lower():
                    continue

                self.list_article_link.append(title_link)

            # Navigate to all articles link and scrap them
            for idx, title_link in enumerate(self.list_article_link):

                self.driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)

                try:
                    self.driver.get(title_link)
                except TimeoutException:
                    self.driver.execute_script("window.stop();")

                # Get the article title and body content
                try:
                    title = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".detail__title"))
                    )
                    body_container = self.driver.find_element(
                        By.CSS_SELECTOR, ".detail__body-text"
                    )
                except NoSuchElementException:
                    title = self.driver.find_element(By.TAG_NAME, "h1")
                    body_container = self.driver.find_element(
                        By.CSS_SELECTOR, ".detail__body"
                    )
                except TimeoutException:
                    continue

                all_p = body_container.find_elements(By.TAG_NAME, "p")
                all_p = [
                    p.text
                    for p in all_p
                    if "para_caption" not in str(p.get_attribute("class")).split()
                ]

                article.append(
                    {
                        "title": title.text,
                        "content": " ".join(all_p),
                        "link": self.driver.current_url,
                    }
                )

                print("-------------")
                print("Article info")
                print("-------------")
                print("Article Num  : ", idx + 1)
                print("title        : ", title.text)
                print("Link         : ", self.driver.current_url)

                self.driver.get(self.prev_url)

        self.driver.close()
        return article

    def get_article_links(self) -> List[str]:
        return self.list_article_link
