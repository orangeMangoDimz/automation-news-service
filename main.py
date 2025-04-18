from typing import List, Tuple
from news.detik import DetikNews
from utils import add_bottom_line, format_article
from utils.type_hint import ArticleTtype, EnvType
from service.gemini import GeminiService
from settings import LoadSettings


def get_gemini_api_key() -> str:
    list_env: List[EnvType] = LoadSettings.get_env()
    gemini_api_key: str = next(
        env.get("value") for env in list_env if env.get("key") == "GEMINI_API_KEY"
    )

    return gemini_api_key


def do_scrap_news() -> Tuple[List[ArticleTtype], List[str]]:
    detik_news = DetikNews(keyword="prabowo")
    detik_news.do_search()
    detik_news.do_apply_filter()
    pagination_links_list: List[str] = detik_news.do_get_pagination_links()
    articles: List[ArticleTtype] = detik_news.do_get_articles(pagination_links_list)
    article_links: List[str] = detik_news.get_article_links()
    return articles, article_links


def do_summarize(
    gemini_api_key: str, articles: List[ArticleTtype], article_links: List[str]
) -> str:
    gemini_service: GeminiService = GeminiService(api_key=gemini_api_key)
    instruction: str = format_article(articles)
    response: str = gemini_service.do_get_response(contents=instruction)
    response: str = add_bottom_line(response=response, article_link=article_links)
    return response

if __name__ == "__main__":
    # Load config
    gemini_api_key: str = get_gemini_api_key()

    # Do Scraping
    data: Tuple[List[ArticleTtype], List[str]] = do_scrap_news()
    articles: List[ArticleTtype] = data[0]
    article_links: List[str] = data[1]

    # Summarize
    response: str = do_summarize(
        gemini_api_key=gemini_api_key,
        articles=articles,
        article_links=article_links,
    )
    print("response: ", response)
