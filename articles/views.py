from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from .models import Article
import uuid
import random
from django.contrib.auth import get_user_model

# Create your views here.


# def article_list(request):

#     articles = Article.objects.all().order_by('date')


#     context = {
#         'articles':articles,
#         'title':'Articles'
#     }
#     return render(request,'articles/article_list.html',context)

def like_dislike(request):
    article = get_object_or_404(Article, id=request.POST.get('article_id'))
    if article.likes.filter(id=request.user.id):
        article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
    return HttpResponseRedirect(reverse('articles:detail', args=[article.slug]))

def get_top_users():
    u_model = get_user_model()
    users = u_model.objects.all()
    user_dict = {}
    for total_likes,user_name in [[sum([y.total_likes() for y in x.article_set.all()]),x] for x in users]:
        user_dict[user_name] = total_likes
    marklist = sorted(user_dict.items(), key=lambda x:-x[1])
    user_dict = dict(marklist)
    sorted_usernames = list(user_dict.keys())[:10]
    users = []
    [users.append(get_object_or_404(User, username=x)) for x in sorted_usernames]
    return users

class ArticleListView(ListView):
    model = Article
    template_name = "articles/article_list.html"
    context_object_name = "articles"
    ordering = ["-date"]
    paginate_by = 6

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        users = get_top_users()
        context['show_top_users'] = True
        context['top_users'] = users
        return context

class TrendingArticleListView(ArticleListView):
    ordering = ["-likes"]


class UserSpecificArticleListView(ArticleListView):
    template_name = 'articles/user_specific_articles.html'

    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Article.objects.filter(author=user).order_by('-date')


class ArticleDetailView(DetailView):
    model = Article
    is_random = False
    random_article = None
    def get_object(self, queryset=None):
        if self.is_random:
            self.random_article = random.choice(Article.objects.all())
            return self.random_article
        return Article.objects.get(slug=self.kwargs.get("slug"))

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        if self.is_random:
            article = self.random_article
        else:
            article = Article.objects.get(slug=self.kwargs.get("slug"))
        liked = False
        if article.likes.filter(id=self.request.user.id):
            liked = True
        context['liked'] = liked
        users = get_top_users()
        context['show_top_users'] = True
        context['top_users'] = users
        return context

class RandomArticleDetailView(ArticleDetailView):
    is_random = True


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ["title", "body",'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = str(uuid.uuid1().hex)
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ["title", "body","image"]
    template_name = "articles/article_update.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    success_url = reverse_lazy("articles:list")

    def get_object(self, queryset=None):
        return Article.objects.get(slug=self.kwargs.get("slug"))

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


