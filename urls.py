from fastapi import FastAPI
from typing import List, Tuple
from utils.type_hint import ArticleTtype
from fastapi.responses import JSONResponse
from utils.constant import No_NEWS_YET
import main as M

app: FastAPI = FastAPI()

@app.get("/get-today-news")
def index():
    gemini_api_key: str = M.get_gemini_api_key()

    # Do Scraping
    data: Tuple[List[ArticleTtype], List[str]] = M.do_scrap_news()
    articles: List[ArticleTtype] = data[0]
    article_links: List[str] = data[1]

    # Summarize
    response: str = (
        M.do_summarize(
            gemini_api_key=gemini_api_key,
            articles=articles,
            article_links=article_links,
        )
        if articles is not None and article_links is not None
        else No_NEWS_YET
    )

    return JSONResponse({
        'data': response
    })
