from django.contrib import admin
from .models import Message, Report, Sharing


admin.site.register(Message)
admin.site.register(Report)
admin.site.register(Sharing)