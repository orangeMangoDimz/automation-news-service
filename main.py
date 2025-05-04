from datetime import datetime
from typing import List, Dict
from app import LoadSelenium
from app.detik import DetikNews
from app.profile import ProfileApp
from app.holiday_calendar import HolidayCalendarApp
from utils import add_top_line, add_bottom_line, format_article
from utils.constant import LIST_OF_DAYS, LIST_OF_MONTHS, SUMMARIZE_INSTRUCTION, TODAY_WORD_CONTENT, TODAY_WORD_INSTRUCTION
from utils.type_hint import ArticleTtype, EnvType, HolidayResponse
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
    response: str = gemini_service.do_get_response(contents=instruction, instruction=SUMMARIZE_INSTRUCTION)
    return response


def construct_response(
    summarize_response: str, news_app: LoadSelenium, article_links: List[str]
) -> str:
    response: str = add_top_line(
        response=summarize_response,
        news_base_url=news_app.get_domain_url,
        news_title=news_app.get_base_title,
    )
    constructed_response: str = add_bottom_line(
        response=response, article_link=article_links
    )
    return constructed_response

def get_today_month_holiday(month: int) -> str:
    holiday_calendar: HolidayCalendarApp = HolidayCalendarApp(month=month)
    calendar_data: List[HolidayResponse] = holiday_calendar.fetch_month_holiday()
    filtered_calendar_data: Dict[str, List[HolidayResponse]] = (
        holiday_calendar.get_month_holiday(list_of_calendar_data=calendar_data)
    )
    return holiday_calendar.construct_response(list_of_holidays=filtered_calendar_data)


def get_profile() -> str:
    return ProfileApp.get_profile()

def get_todays_word(gemini_api_key: str):
    gemini_service: GeminiService = GeminiService(api_key=gemini_api_key)
    response: str = gemini_service.do_get_response(contents=TODAY_WORD_CONTENT, instruction=TODAY_WORD_INSTRUCTION)
    return response

def construct_todays_word_response(response: str) -> str:
    formatted_date = datetime.now().strftime('%d %B %Y')
    today_day_name = datetime.now().strftime('%A')
    day_indo: str = LIST_OF_DAYS.get(today_day_name, today_day_name)
    constructed_response: str = f"**{day_indo}, {formatted_date}**\nKata-kata hari ini:\n{response}"
    return constructed_response


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
