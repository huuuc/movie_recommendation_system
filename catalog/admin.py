from django.contrib import admin

# Register your models here.
from .models import Movie, User, UserRate, UserTag, WouldLikeList, HaveWatchedList, Ban

admin.site.site_header = '老王电影推荐'
admin.site.index_title = '欢迎使用老王电影推荐'


class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'country', 'score', 'rate_num']
    list_filter = ['country']
    search_fields = ['id', 'name']


admin.site.register(Movie, MovieAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'nick_name', 'phone', 'age', 'sex', 'profession']
    list_filter = ['sex']
    search_fields = ['id', 'account', 'nick_name']


admin.site.register(User, UserAdmin)


class UserTagAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'tag', 'tag_time']
    search_fields = ['user__nick_name', 'movie__name']


admin.site.register(UserTag, UserTagAdmin)


class UserRateAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'rate', 'rate_time']
    search_fields = ['user__nick_name', 'movie__name']


admin.site.register(UserRate, UserRateAdmin)


class WouldLikeListAdmin(admin.ModelAdmin):
    list_display = ['user', 'want_watch_movie']
    search_fields = ['user__nick_name', 'want_watch_movie__name']


admin.site.register(WouldLikeList, WouldLikeListAdmin)


class HaveWatchedListAdmin(admin.ModelAdmin):
    list_display = ['user', 'have_watched_movie']
    search_fields = ['user__nick_name', 'have_watched_movie__name']


admin.site.register(HaveWatchedList, HaveWatchedListAdmin)


class BanAdmin(admin.ModelAdmin):
    list_display = ['user', 'reason', 'start_time', 'end_time']
    list_filter = ['start_time', 'end_time']
    search_fields = ['user__nick_name']


admin.site.register(Ban, BanAdmin)
