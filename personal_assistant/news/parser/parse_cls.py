from abc import ABC, abstractclassmethod
from datetime import datetime
import re
import news.parser.parse_dicts as pd


class Value(ABC):
    def __init__(self, value, type_news) -> None:
        self.type_news = type_news
        self.parse_cmd = pd.PARSE_DICT[type_news]

        self.__value: str = ""
        self.value: str = value

    @property
    @abstractclassmethod
    def value(self) -> str:
        pass

    @value.setter
    @abstractclassmethod
    def value(self, value) -> str:
        pass


class ArticleName(Value):
    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value) -> str:
        value = value.select_one(self.parse_cmd["name"]).text

        self.__value = value


class ArticleLink(Value):
    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value) -> str:
        value = value.select_one(self.parse_cmd["link"]).get("href")

        if self.parse_cmd["search_link"] not in value:
            value = self.parse_cmd["create_link"] + value

        self.__value = value


class ArticlePushTime(Value):
    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value) -> str:
        value = value.select_one(self.parse_cmd["push_time"]).text

        self.__value = value


class ArticleStop(Value):
    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value) -> str:
        date_now = datetime.now().date()

        stop_date = value.select_one(self.parse_cmd["stop_select"]).get("href")

        parse_date = re.findall(
            r"/+\d{4}/+\d{2}/+\d{2}|/+\d{4}/+\d{2}/+\d{1}", stop_date
        )[0]

        now_date = datetime.strftime(date_now, "/%Y/%m/" + str(date_now.day))

        if parse_date != now_date:
            self.__value = True
        else:
            self.__value = False


class ArticalTextContent(Value):
    def __init__(self, value, type_news) -> None:
        self.type_news = type_news
        self.parse_cmd = pd.PARSE_DICT

        self.__value: str = ""
        self.value: str = value

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value) -> str:
        for key in self.parse_cmd:
            parse_cmd = self.parse_cmd[key]

            cont = value.select(parse_cmd["text_content"])

            if cont != []:
                value = list([text.text for text in cont])
                break

        self.__value = value


class ParseArticle:
    parse_name = ArticleName
    parse_link = ArticleLink
    parse_stop = ArticleStop
    parse_push_time = ArticlePushTime

    def __init__(self, article, type_news: str) -> None:
        self.name: str = self.parse_name(article, type_news).value
        self.link: str = self.parse_link(article, type_news).value
        self.stop_iter: str = self.parse_stop(article, type_news).value
        self.push_time: str = self.parse_push_time(article, type_news).value
        self.type_news: str = type_news

