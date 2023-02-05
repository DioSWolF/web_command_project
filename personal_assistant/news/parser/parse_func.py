import asyncio
from random import randrange
import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

import news.parser.parse_dicts as pd
import news.parser.parse_cls as pcls
from news.models import News


class FindArticle:
    client_session = aiohttp.ClientSession
    bs4_model = BeautifulSoup
    fake_user_model = UserAgent
    linc_dict = pd.SITE_DICT
    parse_dict = pd.PARSE_DICT
    # news_model = News

    async def create_headers(self) -> None:
        self.headers = {
            "User-Agent": self.fake_user_model().random,
            "Keep-Alive": str(randrange(60, 100)),
        }

    async def find_article(self, cl_session: aiohttp.ClientSession) -> None:
        self.cl_session = cl_session

        for arc_type, link in self.linc_dict.items():
            parse_cmd = self.parse_dict[arc_type]

            await self.create_headers()

            async with self.cl_session.get(link, headers=self.headers) as resp:
                if resp.status == 200:
                    soup = BeautifulSoup(await resp.text(), "lxml")

                    for artcl in soup.select(parse_cmd["select"]):
                        try:
                            parse_article = pcls.ParseArticle(artcl, arc_type)

                        except AttributeError:
                            continue

                        if parse_article.stop_iter:
                            continue

                        status = self.news_model.objects.filter(
                            link=parse_article.link, news_type=arc_type
                        ).first()

                        if status == None:
                            article = self.news_model(
                                name=parse_article.name,
                                link=parse_article.link,
                                push_time=parse_article.push_time,
                                news_type=arc_type,
                            )
                            article.save()

    async def parse_content(self, article: News) -> None:
        async with aiohttp.ClientSession() as cl_session:
            await self.create_headers()

            async with cl_session.get(article.link, headers=self.headers) as resp:
                if resp.status == 200:
                    soup = BeautifulSoup(await resp.text(), "lxml")
                    content = pcls.ArticalTextContent(soup, article.news_type).value

                    self.text_content = {
                        "header": article.name,
                        "content": content,
                        "news_type":  article.news_type,
                    }


class ArticalQuery:
    fast_news = pd.ARTICLE_DICT

    async def get_fast_news(self) -> None:
        for artc_type in pd.SITE_DICT:
            news_list = News.objects.filter(news_type=artc_type).order_by("-push_time")[
                :5
            ]

            self.fast_news["articles"][artc_type] = news_list

    async def get_all_news(self, news_type: str) -> None:
        self.articles_list = News.objects.filter(news_type=news_type).order_by(
            "-push_time"
        )

    async def get_article(self, artical_id: int) -> None:
        self.article = News.objects.filter(id=artical_id).first()


async def main() -> None:
    async with aiohttp.ClientSession() as cl_session:
        a = FindArticle()
        await a.find_article(cl_session)


# asyncio.run(main())
