from fastapi import FastAPI
from typing import List
from app.detik import DetikNews
from utils.type_hint import ArticleTtype
from fastapi.responses import JSONResponse
from utils.constant import No_NEWS_YET
import main as M

app: FastAPI = FastAPI()


@app.get("/get-today-news")
def index():
    # Load config
    gemini_api_key: str = M.get_gemini_api_key()

    # Do Scraping
    detik_news = DetikNews(keyword="prabowo")
    articles: List[ArticleTtype] = M.do_scrap_news(news_app=detik_news)
    article_links: List[str] = detik_news.get_article_links()

    if len(article_links) == 0 or len(articles) == 0:
        constructed_response: str = No_NEWS_YET

    else:
        # Summarize
        summarize_response: str = M.do_summarize(
            gemini_api_key=gemini_api_key, articles=articles
        )

        # Construct response
        constructed_response: str = M.construct_response(
            summarize_response=summarize_response,
            news_app=detik_news,
            article_links=article_links,
    )

    return JSONResponse({"data": constructed_response})


@app.get("/get-profile")
def profile():
    return JSONResponse({"data": M.get_profile()})

@app.get("/get-today-month-holiday")
def month_holiday():
    return JSONResponse({"data": M.get_today_month_holiday(month=8)})
