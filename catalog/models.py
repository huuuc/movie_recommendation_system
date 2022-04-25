from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


# Create your models here.
class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    movie_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(blank=True, null=True, max_length=100)
    director = models.CharField(blank=True, null=True, max_length=300)
    stars = models.CharField(blank=True, null=True, max_length=500)
    type = models.CharField(blank=True, null=True, max_length=100)
    country = models.CharField(blank=True, null=True, max_length=100)
    language = models.CharField(blank=True, null=True, max_length=200)
    release_time = models.DateTimeField(blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)
    score = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=3, default=0)
    implicit_score = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=3, default=0)
    rate_num = models.IntegerField(blank=True, null=True)
    movie_url = models.CharField(blank=True, null=True, max_length=100)
    insert_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class User(models.Model):
    id = models.AutoField(primary_key=True)
    nick_name = models.CharField(null=False, max_length=30, default='new_user')
    account = models.CharField(null=False, max_length=32)
    password = models.CharField(null=False, max_length=32)
    phone = models.CharField(blank=True, null=True, validators=[RegexValidator(regex='^1\\d{10}$', message='Length has to be 11',
                                                                    code='no match')], max_length=11)
    email = models.EmailField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True, validators=[
        MinValueValidator(1),
        MaxValueValidator(120)
    ])
    sex = models.CharField(blank=True, null=True, max_length=6, choices=(('male', '男'), ('female', '女')), default='male')
    profession = models.CharField(blank=True, null=True, max_length=20)
    user_md5 = models.CharField(blank=True, null=True, max_length=32)
    insert_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nick_name


class UserTag(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    tag = models.CharField(null=False, max_length=500)
    votes = models.IntegerField(blank=True, null=True, default=0)
    tag_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + '_' + str(self.movie)


class UserRate(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    rate = models.IntegerField(null=False, validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ])
    rate_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + '_' + str(self.movie)


class WouldLikeList(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    want_watch_movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    insert_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + '_' + str(self.want_watch_movie)


class HaveWatchedList(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    have_watched_movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    insert_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + '_' + str(self.have_watched_movie)


class SearchHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.CharField(max_length=30)
    insert_time = models.DateTimeField(auto_now_add=True)
