from typing import TypedDict


class ArticleTtype(TypedDict):
    title: str
    content: str
    link: str


class EnvType(TypedDict):
    key: str
    value: str
    err_msg: str

class HolidayResponse(TypedDict):
    holiday_date: str
    holiday_name: str
    is_national_holiday: bool
