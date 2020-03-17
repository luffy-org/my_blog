import datetime
from time import sleep

from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.utils import timezone

from article.models import ArticlePost


# class AtriclePostModelTests(TestCase):
#     def test_was_created_recently_with_future_article(self):
#         """
#         测试文章创建时间
#         :return:
#         """
#         author = User(username='user1', password='123')
#         author.save()
#
#         future_article = ArticlePost(author=author, title='test', body='test....',
#                                      created=timezone.now() + datetime.timedelta(days=30)
#                                      )
#         self.assertIs(future_article.was_created_recently(), False)  # 检测函数结果是否 False相同


class ArticlePostViewTests(TestCase):
    def test_increase_view(self):
        author = User(username='user4', password='test_password')
        author.save()
        article = ArticlePost(
            author=author,
            title='test4',
            body='test4',
        )
        article.save()
        self.assertIs(article.total_views, 0)
        url = reverse('article:article_detail', kwargs={'pid': article.id})
        response = self.client.get(url)
        new_article = ArticlePost.objects.get(id=article.id)
        self.assertIs(new_article.total_views, 1)

    def test_increase_views_but_not_change_updated_field(self):
        # 请求详情视图时，不改变 updated 字段
        author = User(username='user5', password='test_password')
        author.save()
        article = ArticlePost(
            author=author,
            title='test5',
            body='test5',
        )
        article.save()
        sleep(0.5)
        url = reverse('article:article_detail', kwargs={'pid': article.id})
        self.client.get(url)
        new_article = ArticlePost.objects.get(id=article.id)
        self.assertIs(new_article.updated - new_article.created < timezone.timedelta(seconds=0.1), True)

