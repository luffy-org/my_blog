from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from article.models import ArticlePost
from comment.forms import CommentForm


def commit_comment(request, article_id):
    article_obj = get_object_or_404(ArticlePost, id=article_id)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_obj = comment_form.save(commit=False)
            comment_obj.article = article_obj
            comment_obj.user = request.user
            comment_obj.save()
            return redirect('article:article_detail', pid=article_id)
        else:
            return HttpResponse('数据错误')


