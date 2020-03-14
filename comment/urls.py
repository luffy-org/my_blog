from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from comment import views

app_name = 'comment'

urlpatterns = [
    path('commit/<int:article_id>/', views.commit_comment, name='commit_comment')

]