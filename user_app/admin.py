from django.contrib import admin
from user_app.models import Account, Followers
# Register your models here.

admin.site.register(Account)
admin.site.register(Followers)