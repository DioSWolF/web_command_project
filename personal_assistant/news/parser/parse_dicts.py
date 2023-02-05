import os

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


SITE_DICT = {
    "Politics": "https://www.pravda.com.ua/news/",
    "Europe": "https://www.eurointegration.com.ua/news/",
    "Economy": "https://www.epravda.com.ua/news/",
}


PARSE_DICT = {
    "Politics": {
        "select": ".article_news_list",
        "stop_select": ".article_header a",
        "name": ".article_header",
        "create_link": "https://www.pravda.com.ua",
        "search_link": "https://",
        "link": ".article_header a",
        "push_time": ".article_time",
        "text_content": ".post_text p",
    },
    "Europe": {
        "select": ".article_news",
        "stop_select": ".article__title a",
        "name": ".article__title",
        "create_link": "https://www.eurointegration.com.ua",
        "search_link": "https://",
        "link": ".article__title a",
        "push_time": ".article__time",
        "text_content": "post__text p",
    },
    "Economy": {
        "select": ".article_news",
        "stop_select": ".article__title a",
        "name": ".article__title",
        "create_link": "https://www.epravda.com.ua",
        "search_link": "https://",
        "link": ".article__title a",
        "push_time": ".article__time",
        "text_content": ".post__text p",
    },
}


ARTICLE_DICT = {"articles": {}}
