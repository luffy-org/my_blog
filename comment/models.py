from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from article.models import ArticlePost

__all__ = ['Comment']

class Comment(models.Model):
    """
    评论表
    """
    article = models.ForeignKey(to=ArticlePost, blank=True, null=True, verbose_name='评论属于哪篇博客', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(to=User, blank=True, null=True, verbose_name='该评论是谁写的', on_delete=models.CASCADE)
    # body = models.TextField(verbose_name='评论内容')
    body = RichTextField(verbose_name='评论内容')  # 评论内容使用富文本插件的字段
    created = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')

    class Meta:
        ordering = ('created',)
        verbose_name = '03-评论表'
        verbose_name_plural = verbose_name
        db_table = verbose_name


    def __str__(self):
        return self.body[:10]