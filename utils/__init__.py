from datetime import datetime
from utils.type_hint import ArticleTtype
from utils.constant import LIST_OF_DAYS, LIST_OF_MONTHS
from typing import List
from datetime import datetime


def format_article(article: List[ArticleTtype]):
    res: str = ""

    for idx, item in enumerate(article):
        res += f"Article #{idx + 1}\n\n"

        for key, value in item.items():
            res += f"{key}: {value}\n\n"

        res += "\n"

    return res.strip()

def add_top_line(response: str, news_base_url: str, news_title: str) -> str:
    # Get the date
    current_date: datetime = datetime.now()
    formatted_date = current_date.strftime("%A, %d %B %Y")

    day_name_eng, rest = formatted_date.split(", ")
    day, month_name_eng, year = rest.split(" ")

    day_name_id = LIST_OF_DAYS.get(day_name_eng, day_name_eng)
    month_name_id = LIST_OF_MONTHS.get(month_name_eng, month_name_eng)

    final_date = f"{day_name_id}, {day} {month_name_id} {year}"

    # Get source
    source: str = f"Source [{news_title}]({news_base_url})"

    # Constructed response
    formatted_response: str = f"""
    {final_date}\n
    {source}\n\n

    ### Berita penting hari ini\b
    {response}
    """
    return formatted_response


def add_bottom_line(response: str, article_link: List[str]) -> str:
    response += "\n\nReferensi:\n"

    for link in article_link:
        response += f"link: {link}\n"

    return response.strip()
