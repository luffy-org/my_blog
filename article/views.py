from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from article.forms import ArticlePostForm
from article.models import ArticlePost, ArticleColumn
import markdown

from comment.forms import CommentForm
from comment.models import Comment


def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    art_all = ArticlePost.objects.all()
    if search:
        art_all = art_all.filter(Q(title__contains=search) | Q(body__contains=search))
    else:
        search = ''
    if order == 'total_views':
        art_all = art_all.order_by('-total_views')
    if column is not None and column.isdigit():
        art_all = art_all.filter(column=column)

    paginator = Paginator(art_all, 3)

    # 拿到URL中的page参数
    page = request.GET.get('page')
    art_list = paginator.get_page(page)

    for item in art_all:
        item.body = markdown.markdown(item.body, extensions=[
            # 包含 缩写、表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',
        ])
    context = {'articles': art_list, 'order': order, 'search': search}

    return render(request, 'article/article_list.html', context)


def article_detail(request, pid):
    article = ArticlePost.objects.get(id=pid)
    md = markdown.Markdown(extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',

        # 目录的扩展
        'markdown.extensions.toc'
    ])
    article.body = md.convert(article.body)
    author = article.author
    comments = Comment.objects.filter(article_id=pid)
    comment_form = CommentForm()
    if request.user != author:
        article.total_views += 1
        article.save(update_fields=['total_views'])
    # 需要传递给模板的对象
    context = {'article': article, 'toc': md.toc, 'comments': comments, 'comment_form': comment_form}
    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)


def article_create(request):
    """
    创建博客
    :param request:
    :return:
    """
    if request.method == 'POST':
        article_form = ArticlePostForm(data=request.POST, files=request.FILES)
        if article_form.is_valid():
            new_article_obj = article_form.save(commit=False)
            new_article_obj.author = User.objects.get(pk=request.user.id)  # 给博客安排一个作者
            new_article_obj.save()
            article_form.save_m2m()
            return redirect('article:list')
        else:
            return HttpResponse('提交错误')
    else:
        column = ArticleColumn.objects.all()  # 获取栏目数据，用于前端页面展示
        article_form = ArticlePostForm()
        context = {'article_form': article_form, 'columns': column}
        return render(request, 'article/create.html', context)

@login_required(login_url='/article/list')
def article_edit(request, pid):
    article_obj = ArticlePost.objects.filter(id=pid).first()
    if request.method == 'GET':
        article_form = ArticlePostForm(instance=article_obj)
        context = {'article_form': article_form}
        return render(request, 'article/create.html', context)
    article_form = ArticlePostForm(data=request.POST, instance=article_obj, files=request.FILES)
    if article_form.is_valid():
        new_article_obj = article_form.save(commit=False)
        new_article_obj.author = User.objects.get(pk=request.user.id)
        new_article_obj.save()
        article_form.save_m2m()
        # return redirect(reverse('article:article_edit', kwargs={'pid': pid}))
        return redirect('article:article_detail', pid=pid)
    else:
        return HttpResponse('编辑错误')



def article_delete(request, pid):
    # 根据 id 获取需要删除的文章
    article = ArticlePost.objects.get(id=pid)
    # 调用.delete()方法删除文章
    print('准备执行')
    article.delete()
    print('执行了吗')
    # 完成删除后返回文章列表
    return redirect("article:list")

