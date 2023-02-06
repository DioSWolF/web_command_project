from django.urls import path
from news import views

app_name = "news"

urlpatterns = [
    path("today/", views.test, name="test"),
    path("articles_list/<str:news_type>", views.articles, name="aticle_list"),
    path("read_article/<int:artical_id>", views.read_article, name="read"),
]
