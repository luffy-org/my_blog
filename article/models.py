from django.contrib.auth.models import User
from django.db import models

from django.utils import timezone

__all__ = ['ArticlePost']

class ArticlePost(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='博客的作者')

    title = models.CharField(max_length=100, verbose_name='博客标题')

    body = models.TextField(verbose_name='博客正文')

    created = models.DateTimeField(default=timezone.now, verbose_name='博客创建时间')

    updated = models.DateTimeField(auto_now=True, verbose_name='博客更新时间')

    class Meta:
        ordering = ('-created',)
        verbose_name = '01-博客表'
        verbose_name_plural = verbose_name
        db_table = verbose_name

    def __str__(self):
        return self.title

