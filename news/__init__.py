from selenium import webdriver
from mixin.LoggerMixin import LoggerMixin
from settings.decorator import retry
from settings import LoadSettings
from typing import List
from utils.type_hint import EnvType


class LoadSelenium:
class LoadSelenium(LoggerMixin):
    def __init__(self) -> None:
        super().__init_logger__()

        # Load base config
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-css")
        # chrome_options.add_argument("--disable-javascript")
        self.driver = webdriver.Chrome(chrome_options)

    def do_search(self) -> None:
        """
        Search for content here
        """
        pass

    @retry(exec_msg="Filter")
    def do_apply_filter(self) -> None:
        """
        Apply filter here
        """
        pass

    @retry(exec_msg="Pagination")
    def do_get_pagination_links(self, *args, **kwargs) -> any:  # type: ignore
        """
        Get pagination nums
        Ex: 1, 2, 3, etc
        """
        pass

    @retry(exec_msg="Articles")
    def do_get_articles(self, *args, **kwargs) -> any:  # type: ignore
        """
        Get all artilces
        """
        pass
