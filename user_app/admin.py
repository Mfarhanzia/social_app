from django.contrib import admin
from user_app.models import Account, Followers
# Register your models here.


class FollowersAdmin(admin.ModelAdmin):
    list_display = ("follower", "followed",)
    list_filter = ("follower", "followed",)


admin.site.register(Followers, FollowersAdmin)


class AccountAdmin(admin.ModelAdmin):
    readonly_fields = ("password", "date_joined", "last_login",)


admin.site.register(Account, AccountAdmin)