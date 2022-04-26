from django.contrib import admin

# Register your models here.
from .models import Movie, User, UserRate, UserTag, WouldLikeList, HaveWatchedList, MovieAttributes, UserAttributes

admin.site.site_header = '老王电影推荐'
admin.site.index_title = '欢迎使用老王电影推荐'


class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'country', 'score', 'rate_num', 'implicit_score']
    list_filter = ['score']
    search_fields = ['id', 'name']


admin.site.register(Movie, MovieAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'nick_name', 'phone', 'age', 'sex', 'profession']
    search_fields = ['id', 'account', 'nick_name']


admin.site.register(User, UserAdmin)


class UserTagAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'tag', 'tag_time', 'votes']
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


class MovieAttributesAdmin(admin.ModelAdmin):
    list_display = ['movie', 'plot', 'comedy', 'action', 'romance', 'animation', 'sci_fi', 'suspense',
             'thriller', 'fear', 'documentary', 'short', 'erotica', 'homosexual', 'music',
             'musical', 'family', 'children', 'biography', 'history', 'war', 'crime',
             'western', 'fantasy', 'adventure', 'disaster', 'martial', 'costume', 'sum_types']
    search_fields = ['movie__name']


admin.site.register(MovieAttributes, MovieAttributesAdmin)


class UserAttributesAdmin(admin.ModelAdmin):
    list_display = ['user', 'plot', 'comedy', 'action', 'romance', 'animation', 'sci_fi', 'suspense',
             'thriller', 'fear', 'documentary', 'short', 'erotica', 'homosexual', 'music',
             'musical', 'family', 'children', 'biography', 'history', 'war', 'crime',
             'western', 'fantasy', 'adventure', 'disaster', 'martial', 'costume']
    search_fields = ['user__nick_name']


admin.site.register(UserAttributes, UserAttributesAdmin)


