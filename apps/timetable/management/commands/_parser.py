from ... import constants as const
import requests


def load_main_db(domain: str) -> requests.Response:
    link = const.TIMETABLE_DATABASE_LINK.format(domain)
    return requests.post(url=link, json=const.TIMETABLE_DATABASE_DATA)
