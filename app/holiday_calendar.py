from collections import defaultdict
from typing import List, Dict
from datetime import datetime
from utils.type_hint import HolidayResponse
from utils.constant import LIST_OF_MONTHS
import requests
import calendar

class HolidayCalendarApp:
    def __init__(self, month: int) -> None:
        self.endpoint: str = "https://api-harilibur.vercel.app/api"
        self.month = month
        self.year = datetime.now().year

    def fetch_month_holiday(self) -> List[HolidayResponse]:
        endpoint: str = f"{self.endpoint}?month={self.month}"
        res: requests.Response = requests.get(endpoint)
        data = res.json()
        return data

    def get_month_holiday(self, list_of_calendar_data: List[HolidayResponse]) -> Dict[str, List[HolidayResponse]]:
        list_of_holidays: Dict[str, List[HolidayResponse]] = defaultdict(list)
        for holiday_response in list_of_calendar_data:
            if holiday_response['is_national_holiday']:
                list_of_holidays[holiday_response['holiday_date']].append(holiday_response)
        return list_of_holidays

    def construct_response(self, list_of_holidays: Dict[str, List[HolidayResponse]]) -> str:
        month_name_eng: str = calendar.month_name[self.month]
        month_name_id: str = LIST_OF_MONTHS.get(month_name_eng, month_name_eng)
        header: str = f"## Libur {month_name_id} {self.year}"
        body_template: str = ""

        has_national_holidays: bool = len(list_of_holidays) > 0
        if not has_national_holidays:
            body_template: str = "Tidak ada hari libur untuk bulan ini"

        else:
            for holiday_date, value in list_of_holidays.items():
                formatted_date: str = datetime.strptime(holiday_date, "%Y-%m-%d").strftime("%d %B %Y")

                day, month, year = formatted_date.split(" ")
                month_ind: str = LIST_OF_MONTHS.get(month, month)
                constructed_date: str = f"**{day} {month_ind} {year}**"

                body_template: str = f"{constructed_date}\n"
                for holiday in value:
                    body_template += f"- {holiday['holiday_name']}\n"
                body_template += "\n"

        body: str = body_template
        return f"{header}\n{body}"


