from django.urls import path
from . import views


urlpatterns = [
    path('', views.sign_in),
    path('sign_in', views.sign_in),  # 登录
    path('sign_up', views.sign_up),  # 注册
    path('get_type_list', views.get_type_list),  # 获取排行榜
    path('get_movie_detail', views.get_movie_detail),  # 获取电影详细数据
    path('get_user_detail', views.get_user_detail),  # 获取用户详情信息
    path('save_user_detail', views.save_user_detail),  # 保存用户详情数据
    path('rate_movie', views.rate_movie),  # 电影评分
    path('vote_tag', views.vote_tag),  # 点赞评论
    path('comment_movie', views.comment_movie),  # 评价电影
    path('add_would_like_movie', views.add_would_like_movie),  # 添加想看的电影
    path('add_have_watched_movie', views.add_have_watched_movie),  # 添加已经看过的电影
    path('get_movie_list', views.get_movie_list),  # 获取我想看的/我看过的电影列表
    path('get_rate_list', views.get_rate_list),  # 获取用户所有评分记录
    path('get_tag_list', views.get_tag_list),  # 获取电影所有评论记录
    path('get_recommend_list', views.get_recommend_list),  # 获取推荐列表

]
