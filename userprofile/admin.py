from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from userprofile.models import Profile

# 编写一个自己设置的admin
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = '02-用户详细信息表'

# 将自己定义的admin关联到User表中
class MyUserAdmin(UserAdmin):
    inlines = (ProfileInline,)


#重新注册User表
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)