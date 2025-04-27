from typing import List
from app import LoadSelenium
from app.detik import DetikNews
from app.profile import ProfileApp
from utils import add_top_line, add_bottom_line, format_article
from utils.type_hint import ArticleTtype, EnvType
from service.gemini import GeminiService
from settings import LoadSettings


def get_gemini_api_key() -> str:
    list_env: List[EnvType] = LoadSettings.get_env()
    gemini_api_key: str = next(
        env.get("value") for env in list_env if env.get("key") == "GEMINI_API_KEY"
    )

    return gemini_api_key


def do_scrap_news(news_app: LoadSelenium) -> List[ArticleTtype]:
    news_app.do_search()
    news_app.do_apply_filter()
    pagination_links_list: List[str] = news_app.do_get_pagination_links()
    articles: List[ArticleTtype] = news_app.do_get_articles(pagination_links_list)
    return articles


def do_summarize(gemini_api_key: str, articles: List[ArticleTtype]) -> str:
    gemini_service: GeminiService = GeminiService(api_key=gemini_api_key)
    instruction: str = format_article(articles)
    response: str = gemini_service.do_get_response(contents=instruction)
    return response


def construct_response(
    summarize_response: str, news_app: LoadSelenium, article_links: List[str]
) -> str:
    response: str = add_top_line(
        response=summarize_response,
        news_base_url=news_app.get_base_title,
        news_title=news_app.get_base_title,
    )
    constructed_response: str = add_bottom_line(
        response=response, article_link=article_links
    )
    return constructed_response


def get_profile() -> str:
    return ProfileApp.get_profile()


if __name__ == "__main__":
    # Load config
    gemini_api_key: str = get_gemini_api_key()

    # Do Scraping
    detik_news = DetikNews(keyword="prabowo")
    articles: List[ArticleTtype] = do_scrap_news(news_app=detik_news)
    article_links: List[str] = detik_news.get_article_links()

    # Summarize
    summarize_response: str = do_summarize(
        gemini_api_key=gemini_api_key, articles=articles
    )

    # Construct response
    constructed_response: str = construct_response(
        summarize_response=summarize_response,
        news_app=detik_news,
        article_links=article_links,
    )

    print("response: ", constructed_response)
