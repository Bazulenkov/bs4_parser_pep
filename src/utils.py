# utils.py
import logging

from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import ParserFindTagException


# Перехват ошибки RequestException.
def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = "utf-8"
        return response
    except RequestException:
        logging.exception(
            f"Возникла ошибка при загрузке страницы {url}", stack_info=True
        )


def get_soup(session, url):
    response = get_response(session, url)
    if response is None:
        return
    return BeautifulSoup(response.text, features="lxml")


# Перехват ошибки поиска тегов.
def find_tag(soup, *args, **kwargs):
    searched_tag = soup.find(*args, **kwargs)
    if searched_tag is None:
        error_msg = f"Не найден тег {args[0]} {kwargs or None}"
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag
