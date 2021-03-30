from django.contrib import admin
# from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import MyUser

class MyAdmin(admin.ModelAdmin):
    list_display = ['email','nickname']


admin.site.register(MyUser,MyAdmin)
# admin.site.unregister(Group)
