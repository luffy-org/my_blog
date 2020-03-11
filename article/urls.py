from django.urls import path

from article import views

app_name = 'article'

urlpatterns = [
    path('list/', views.article_list, name='list'),
    path('detail/<int:pid>/', views.article_detail, name='article_detail'),
    path('create/', views.article_create, name='article_create'),
    path('article-delete/<int:pid>/', views.article_delete, name='article_delete'),
]
