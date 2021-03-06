# Generated by Django 4.0.3 on 2022-04-07 10:15

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('director', models.CharField(blank=True, max_length=30, null=True)),
                ('screen_writer', models.CharField(blank=True, max_length=30, null=True)),
                ('stars', models.CharField(blank=True, max_length=500, null=True)),
                ('type', models.CharField(blank=True, max_length=30, null=True)),
                ('country', models.CharField(blank=True, max_length=20, null=True)),
                ('language', models.CharField(blank=True, max_length=20, null=True)),
                ('release_time', models.DateTimeField(blank=True, null=True)),
                ('length', models.IntegerField(blank=True, null=True)),
                ('score', models.DecimalField(blank=True, decimal_places=3, max_digits=4, null=True)),
                ('implicit_score', models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=10, null=True)),
                ('rate_num', models.IntegerField(blank=True, null=True)),
                ('movie_url', models.CharField(blank=True, max_length=50, null=True)),
                ('insert_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nick_name', models.CharField(default='new_user', max_length=50)),
                ('account', models.CharField(blank=True, max_length=20, null=True)),
                ('password', models.CharField(blank=True, max_length=30, null=True)),
                ('phone', models.CharField(blank=True, max_length=11, null=True, validators=[django.core.validators.RegexValidator(code='no match', message='Length has to be 11', regex='^1\\d{10}$')])),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('age', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(120)])),
                ('sex', models.CharField(choices=[('male', '???'), ('female', '???')], default='male', max_length=6)),
                ('profession', models.CharField(blank=True, max_length=20, null=True)),
                ('user_md5', models.CharField(blank=True, max_length=32, null=True)),
                ('insert_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WouldLikeList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('insert_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.user')),
                ('want_watch_movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.movie')),
            ],
        ),
        migrations.CreateModel(
            name='UserTag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tag', models.CharField(max_length=500)),
                ('votes', models.IntegerField(blank=True, default=0, null=True)),
                ('tag_time', models.DateTimeField(auto_now_add=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.user')),
            ],
        ),
        migrations.CreateModel(
            name='UserRate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rate', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('rate_time', models.DateTimeField(auto_now_add=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.user')),
            ],
        ),
        migrations.CreateModel(
            name='SearchHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=30)),
                ('insert_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.user')),
            ],
        ),
        migrations.CreateModel(
            name='HaveWatchedList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('insert_time', models.DateTimeField(auto_now_add=True)),
                ('have_watched_movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.user')),
            ],
        ),
    ]
