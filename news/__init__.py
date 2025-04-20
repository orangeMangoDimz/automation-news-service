from selenium import webdriver
from mixin.LoggerMixin import LoggerMixin
from settings.decorator import retry
from settings import LoadSettings
from typing import List
from utils.type_hint import EnvType


class LoadSelenium(LoggerMixin):
    def __init__(self) -> None:
        super().__init_logger__()

        # Load base config
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)

        list_env: List[EnvType] = LoadSettings.get_env()
        debug_mode: str = next(
            env.get("value") for env in list_env if env.get("key") == "DEBUG_MODE"
        )

        required_args: List[str] = [
            "--blink-settings=imagesEnabled=false",
            "--disable-extensions",
            "--disable-popup-blocking",
            "--disable-notifications",
            "--disable-dev-shm-usage",
            "--no-sandbox",
            "--disable-css",
        ]

        # Load all selenium args
        for args in required_args:
            chrome_options.add_argument(args)

        # Ensure the DEBUG mode
        if debug_mode.lower() == "false":
            print("You are using headless mode")
            chrome_options.add_argument("--headless")

        self.is_debug_mode = debug_mode.lower() == "true"
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
