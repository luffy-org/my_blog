from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save  # 引入内置信号
from django.dispatch import receiver   # 信号接收器的装饰器
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=64, blank=True, null=True, verbose_name='用户电话')
    avatar = models.ImageField(upload_to='avatar/%Y-%m-%d', blank=True, null=True, verbose_name='用户头像')
    bio = models.TextField(verbose_name='个人简介', blank=True, null=True)

    class Meta:
        verbose_name = '02-用户信息详细表'
        verbose_name_plural = verbose_name
        db_table = verbose_name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

