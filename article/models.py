from PIL import Image
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from django.utils import timezone
from taggit.managers import TaggableManager

__all__ = ['ArticlePost', 'ArticleColumn']


class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='博客的作者')

    title = models.CharField(max_length=100, verbose_name='博客标题')

    body = models.TextField(verbose_name='博客正文')

    created = models.DateTimeField(default=timezone.now, verbose_name='博客创建时间')

    updated = models.DateTimeField(auto_now=True, verbose_name='博客更新时间')

    total_views = models.PositiveIntegerField(default=0, verbose_name='博客阅读数量')

    column = models.ForeignKey(to='ArticleColumn', null=True, blank=True, on_delete=models.CASCADE,
                               related_name='article', verbose_name='博客归宿栏目')

    tag = TaggableManager(blank=True)

    avatar = models.ImageField(upload_to='article/%Y-%m-%d', blank=True, null=True, verbose_name='博客封面')

    def save(self, *args, **kwargs):
        """
        对用户上传的博客封面进行处理
        :param args:
        :param kwargs:
        :return:
        """

        article = super().save(*args, **kwargs)
        if self.avatar and not kwargs.get('update_fields'):  # update_fields 是在访问博客的时候对访客数量进行更行操作，排除这种操作
            print('get请求怎么会走save方法')
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            nex_y = int(new_x * (y/x))
            resized_image = image.resize((new_x, nex_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)
        return article




    class Meta:
        ordering = ('-created',)
        verbose_name = '01-博客表'
        verbose_name_plural = verbose_name
        db_table = verbose_name

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        redirct方法中传入模型会触发该模型的此方法
        :return:
        """
        return reverse('article:article_detail', args=[self.id])

    def was_created_recently(self):
        diff = timezone.now() - self.created
        if diff.days <= 0 and diff.seconds < 60:
            return True
        else:
            return False


class ArticleColumn(models.Model):
    """
    博客的栏目表
    一篇博客只有一个栏目，一个栏目可以对应多篇博客
    """
    title = models.CharField(verbose_name='栏目标题', blank=True, null=True, max_length=128)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = '04-博客栏目表'
        verbose_name_plural = verbose_name
        db_table = verbose_name

    def __str__(self):
        return self.title
