# Generated by Django 4.0.3 on 2022-04-23 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_remove_movie_screen_writer_alter_movie_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='score',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='account',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(blank=True, choices=[('male', '男'), ('female', '女')], default='male', max_length=6, null=True),
        ),
    ]
