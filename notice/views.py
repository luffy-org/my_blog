from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import ListView

from article.models import ArticlePost


class CommentNoticeListView(LoginRequiredMixin, ListView):
    """
    消息通知视图类
    """
    context_object_name = 'notices'
    template_name = 'notice/list.html'
    login_url = '/userprofile/login/'

    def get_queryset(self):
        return self.request.user.notifications.unread()


class CommentNoticeUpdateView(View):
    """
    更行通知视图类
    """
    def get(self, request):
        notice_id = request.GET.get('notice_id')
        if notice_id:
            article = ArticlePost.objects.get(id=request.GET.get('article_id'))
            request.user.notifications.get(id=notice_id).mark_as_read()  # 找到具体的消息对象标记已读
            return redirect(article)
        else:  # 表示清楚所有消息
            request.user.notifications.mark_all_as_read()  # mark_all_as_read 所有消息已读
            return redirect('notice:list')