from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField()
    image = models.ImageField(default='None',upload_to='article_images')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,related_name='num_of_likes',)    


    def __str__(self):
        return self.title

    def snippet(self):
        return self.body[:50] + ("..." if len(self.body) > 50 else "")

    def get_absolute_url(self):
        return reverse('articles:detail', kwargs={'slug': self.slug})

    def total_likes(self):
        return self.likes.count()