from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from article.forms import ArticlePostForm
from article.models import ArticlePost
import markdown


def article_list(request):

    art_list = ArticlePost.objects.all()
    for item in art_list:
        item.body = markdown.markdown(item.body, extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
    ])
    context = {'article_list': art_list}

    return render(request, 'article/article_list.html', context)


def article_detail(request, pid):

    article = ArticlePost.objects.get(id=pid)
    article.body = markdown.markdown(article.body, extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
    ])
    # 需要传递给模板的对象
    context = {'article': article}
    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)

def article_create(request):
    if request.method == 'POST':
        article_form = ArticlePostForm(data=request.POST)
        if article_form.is_valid():
            new_article_obj = article_form.save(commit=False)
            new_article_obj.author = User.objects.get(pk=1)  # 给博客安排一个作者
            new_article_obj.save()
            return redirect('article:list')
        else:
            return HttpResponse('提交错误')
    else:
        article_form = ArticlePostForm()
        context = {'article_form': article_form}
        return render(request, 'article/create.html', context)


def article_delete(request, pid):
    # 根据 id 获取需要删除的文章
    article = ArticlePost.objects.get(id=pid)
    # 调用.delete()方法删除文章
    print('准备执行')
    article.delete()
    print('执行了吗')
    # 完成删除后返回文章列表
    return redirect("article:list")