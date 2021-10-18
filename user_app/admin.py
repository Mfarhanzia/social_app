from django.contrib import admin
from user_app.models import Account, Followers
# Register your models here.

admin.site.register(Account)

class FollowersAdmin(admin.ModelAdmin):
    list_display = ("follower", "followed",)
    list_filter = ("follower", "followed",)


admin.site.register(Followers, FollowersAdmin)