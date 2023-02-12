import asyncio
from datetime import datetime
from random import randrange
import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

import news.parser.parse_dicts as pd
import news.parser.parse_cls as pcls
from news.models import News

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

class FindArticle:
    client_session = aiohttp.ClientSession
    bs4_model = BeautifulSoup
    fake_user_model = UserAgent
    linc_dict = pd.SITE_DICT
    parse_dict = pd.PARSE_DICT
    news_model = News
    artical_model = pcls.ParseArticle
    artc_text_model = pcls.ArticalTextContent

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
                    soup = self.bs4_model(await resp.text(), "lxml")

                    for artcl in soup.select(parse_cmd["select"]):
                        try:
                            parse_article = self.artical_model(artcl, arc_type)

                        except AttributeError:
                            continue
                        except IndexError:
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
                    soup = self.bs4_model(await resp.text(), "lxml")
                    content = self.artc_text_model(soup, article.news_type).value

                    self.text_content = {
                        "header": article.name,
                        "content": content,
                        "news_type": article.news_type,
                    }


class ArticalQuery:
    fast_news = pd.ARTICLE_DICT
    news_model = News

    async def get_fast_news(self) -> None:
        for artc_type in pd.SITE_DICT:
            news_list = self.news_model.objects.filter(news_type=artc_type).order_by("-push_time")[
                :5
            ]

            self.fast_news["articles"][artc_type] = news_list

    async def get_all_news(self, news_type: str) -> None:
        self.articles_list = self.news_model.objects.filter(news_type=news_type).order_by(
            "-push_time"
        )

    async def get_article(self, artical_id: int) -> None:
        self.article = self.news_model.objects.filter(id=artical_id).first()
    
    async def clean_list(self):
        date_now = datetime.now().date() 
        self.news_model.objects.exclude(created = date_now).delete()


async def find_article() -> None:

    async with aiohttp.ClientSession() as cl_session:
        article = FindArticle()
        await ArticalQuery().clean_list()
        await article.find_article(cl_session)

try:
    job_storage = DjangoJobStore()
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(job_storage, "default")
    job_storage.remove_all_jobs()

    @register_job(scheduler, "interval", seconds=60)
    def start_parse():
        asyncio.run(find_article())

    register_events(scheduler)

    scheduler.start()
except:
    pass