from django.http import HttpResponse
from django.shortcuts import render
import news.parser.parse_func as pars
from django.contrib.auth import decorators



async def test(request) -> HttpResponse:
    articles = pars.ArticalQuery()
    await articles.get_fast_news()
    return render(request, "news/today.html", context=articles.fast_news)


async def articles(request, news_type) -> HttpResponse:
    articles = pars.ArticalQuery()
    await articles.get_all_news(news_type)
    return render(
        request, "news/article_list.html", context={"artical": articles.articles_list}
    )


async def read_article(request, artical_id) -> HttpResponse:
    articles = pars.ArticalQuery()
    await articles.get_article(artical_id)
    content = pars.FindArticle()
    await content.parse_content(articles.article)
    return render(request, "news/read_article.html", context=content.text_content)
