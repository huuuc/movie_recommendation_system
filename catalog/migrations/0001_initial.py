# Generated by Django 4.0.3 on 2022-03-16 15:30

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
                ('nick_name', models.CharField(max_length=30)),
                ('account', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(code='no match', message='Length has to be 11', regex='^1\\d{10}$')])),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('age', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(120)])),
                ('sex', models.CharField(choices=[('male', '男'), ('female', '女')], default='male', max_length=6)),
                ('profession', models.CharField(blank=True, max_length=20, null=True)),
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
                ('tag', models.CharField(max_length=100)),
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
            name='HaveWatchedList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('insert_time', models.DateTimeField(auto_now_add=True)),
                ('have_watched_movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.user')),
            ],
        ),
        migrations.CreateModel(
            name='Ban',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('reason', models.CharField(blank=True, max_length=50, null=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.user', unique=True)),
            ],
        ),
    ]