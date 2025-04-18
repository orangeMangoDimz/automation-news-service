from typing import List
from news.detik import DetikNews
from utils import add_bottom_line, format_article
from utils.type_hint import ArticleTtype, EnvType
from service.gemini import GeminiService
from settings import LoadSettings


if __name__ == "__main__":
    # Load config
    list_env: List[EnvType] = LoadSettings.get_env()
    gemini_api_key: str = next(
        env.get("value") for env in list_env if env.get("key") == "GEMINI_API_KEY"
    )

    # Do Scraping
    detik_news = DetikNews(keyword="prabowo")
    detik_news.do_search()
    detik_news.do_apply_filter()
    pagination_number_list: List[str] = detik_news.do_get_pagination_nums()
    articles: List[ArticleTtype] = detik_news.do_get_articles(pagination_number_list)
    article_links: List[str] = detik_news.get_article_links()

    # Summarize
    gemini_service: GeminiService = GeminiService(api_key=gemini_api_key)
    instruction: str = format_article(articles)
    response: str = gemini_service.do_get_response(contents=instruction)
    response: str = add_bottom_line(response=response, article_link=article_links)
    print("response: ", response)
