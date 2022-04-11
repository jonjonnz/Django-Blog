"""bloggyhell URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from . import views
from .views import ArticleListView,ArticleDetailView,ArticleCreateView,ArticleUpdateView,ArticleDeleteView,UserSpecificArticleListView,TrendingArticleListView,RandomArticleDetailView


app_name = 'articles'

urlpatterns = [
    re_path('^$', ArticleListView.as_view(),name='list'),
    re_path('^trending$', TrendingArticleListView.as_view(),name='trending'),
    re_path('^random$', RandomArticleDetailView.as_view(),name='random'),
    re_path('^user/(?P<username>[\w]+)$', UserSpecificArticleListView.as_view(), name='user-article-list'),
    re_path('^create/$', ArticleCreateView.as_view(), name='create'),
    re_path('^(?P<slug>[\w-]+)$', ArticleDetailView.as_view(), name='detail'),
    re_path('^(?P<slug>[\w-]+)/update/$', ArticleUpdateView.as_view(), name='update'),
    re_path('^(?P<slug>[\w-]+)/delete/$', ArticleDeleteView.as_view(), name='delete'),
    re_path('^likedislike/$', views.like_dislike, name='like-dislike'),
]
