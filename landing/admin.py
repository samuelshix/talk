from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()

# Register your models here.

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Friend_request)
admin.site.register(Page)
admin.site.register(Product)
admin.site.register(Notifications)
# admin.site.register(Account)
# admin.site.register(User)