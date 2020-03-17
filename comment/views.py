from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from notifications.signals import notify

from article.models import ArticlePost
from comment.forms import CommentForm
from comment.models import Comment


@login_required(login_url='/userprofile/login/')
def commit_comment(request, article_id, parent_comment_id=None):
    article_obj = get_object_or_404(ArticlePost, id=article_id)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_obj = comment_form.save(commit=False)
            comment_obj.article = article_obj
            comment_obj.user = request.user
            # comment_obj.save()

            if parent_comment_id:  # 如果有值，则是处理二级评论

                parent_comment = Comment.objects.get(id=parent_comment_id)  # 找到该评论的父级评论对象
                comment_obj.parent_id = parent_comment.get_root().pk  # 该评论的父级评论 = 父级评论对象的get_root方法
                comment_obj.reply_to = parent_comment.user  # 该评论的父级评论是哪个用户
                comment_obj.save()
                if not parent_comment.user.is_superuser:
                    notify.send(request.user, recipient=parent_comment.user, verb='回复了', target=article_obj,
                                action_object=comment_obj)
                return HttpResponse('200 OK')
            comment_obj.save()  # 如果是一级评论，进行保存
            # if not request.user.is_superuser:
            #     notify.send(
            #         request.user,
            #         recipient=User.objects.filter(is_superuser=1),
            #         verb='回复了你',
            #         target=article_obj,
            #         action_object=comment_obj,
            #     )

            return redirect('article:article_detail', pid=article_id)
        else:
            return HttpResponse('数据错误')

    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {'comment_form': comment_form, 'article_id': article_id, 'parent_comment_id': parent_comment_id}
        return render(request, 'comment/reply.html', context)
