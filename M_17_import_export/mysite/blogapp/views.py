from django.shortcuts import render
from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from .models import Article

class ArticlesListView(ListView):
    queryset = (
        Article.objects
        .filter(published_at__isnull=False)
        .order_by("-published_at")

    )

class ArticelDetailView(DetailView):
    model = Article


class LatestArticlesFeed(Feed):
    title = "blog articles(latest)"
    discription = "Updates on changes and addition blog articles"
    link = reverse_lazy("blogapp:articles")

    def  items(self):
        return (
            Article.objects
            .filter(published_at__isnull=False)
            .order_by("-published_at")[:5]
        )

    def item_title(self, item: Article):
        return item.title

    def item_description(self, item:Article):
        return item.body[:200]

