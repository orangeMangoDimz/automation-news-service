from utils.type_hint import ArticleTtype
from typing import List


def format_article(article: List[ArticleTtype]):
    res: str = ""

    for idx, item in enumerate(article):
        res += f"Article #{idx + 1}\n\n"

        for key, value in item.items():
            res += f"{key}: {value}\n\n"

        res += "\n"

    return res.strip()


def add_bottom_line(response: str, article_link: List[str]) -> str:
    response += "\n\nReferensi:\n"

    for link in article_link:
        response += f"link: {link}\n"

    return response.strip()
