from django.urls import path, re_path

from article import views

app_name = 'article'

urlpatterns = [
    path('list/', views.article_list, name='list'),
    path('detail/<int:pid>/', views.article_detail, name='article_detail'),
    path('create/', views.article_create, name='article_create'),
    path('article-delete/<int:pid>/', views.article_delete, name='article_delete'),
    # path('article_edit/<int:pid>/', views.article_edit, name='article_edit')
    re_path(r'^article_edit/(?P<pid>\d+)/$', views.article_edit, name='article_edit')
]
