import logging
from django.conf import settings
from django.utils import timezone
from django.forms.models import model_to_dict
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
import os
import numpy as np
import django
import pandas as pd
from surprise import Dataset, Reader
from surprise import KNNWithMeans
from django.core.cache import cache
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'localMovie.settings')
django.setup()
from catalog.models import UserRate, User, Movie, UserAttributes, MovieAttributes
from catalog.algorithm import content_based_recommendation

logger = logging.getLogger(__name__)


attrs = ['plot', 'comedy', 'action', 'romance', 'sci_fi', 'animation', 'suspense',
             'thriller', 'fear', 'documentary', 'short', 'erotica', 'homosexual', 'music',
             'musical', 'family', 'children', 'biography', 'history', 'war', 'crime',
             'western', 'fantasy', 'adventure', 'disaster', 'martial', 'costume']


def get_top_n(algo1, algo2, n=50):
    users = UserRate.objects.values_list('user', flat=True).distinct()
    rate_movies = UserRate.objects.values_list('movie', flat=True).distinct()
    movies_attrs = MovieAttributes.objects.all()
    pub_movies = Movie.objects.all().order_by('-implicit_score')[:n]
    pub_list = []
    # 获取热门电影
    for movie in pub_movies:
        pub_list.append(str(movie.id))
    pub_moveis_str = " ".join(pub_list)

    for user in users:
        rate_records = UserRate.objects.filter(user=user).values_list('movie_id', flat=True)
        rate_record_num = len(rate_records)
        user_attrs = model_to_dict(UserAttributes.objects.get(user=user))
        tmp_algo1_res = []

        # 没有评价记录，直接返回排行榜单
        if rate_record_num == 0:
            user_key = str(user) + '_rec'
            cache.set(user_key, pub_moveis_str, timeout=None)
            continue

        # 评价次数≤5，完全用基于内容的推荐算法
        if rate_record_num <= 5:
            pred = algo2.estimate(user, user_attrs, movies_attrs)
            pred.sort(key=lambda x: x[1], reverse=True)
            algo2_list = []
            count = 0
            for (movie_id, _) in pred:
                if movie_id in rate_records:
                    continue
                algo2_list.append(str(movie_id))
                count += 1
                if count == n:
                    break

            movies_str = " ".join(algo2_list)
            user_key = str(user) + '_rec'
            cache.set(user_key, movies_str, timeout=None)
            continue

        # 评价次数＞5且≤15，40部基于内容+10部协同过滤
        if 5 < rate_record_num <= 15:
            # 40部基于内容
            pred = algo2.estimate(user, user_attrs, movies_attrs)
            pred.sort(key=lambda x: x[1], reverse=True)
            algo2_list = []
            count = 0
            for (movie_id, _) in pred:
                if movie_id in rate_records:
                    continue
                algo2_list.append(str(movie_id))
                count += 1
                if count == n - 10:
                    break

            # 10部协同过滤
            for movie in rate_movies:
                if movie in rate_records:
                    continue
                if movie in algo2_list:
                    continue
                pred, _ = algo1.estimate(u=algo1.trainset.to_inner_uid(user), i=algo1.trainset.to_inner_iid(movie))
                tmp_algo1_res.append((str(movie), pred))
            tmp_algo1_res.sort(key=lambda x: x[1], reverse=True)
            algo1_list = [movie_id for (movie_id, _) in tmp_algo1_res][:10]

            # 存入redis
            movies_str = " ".join(algo2_list + algo1_list)
            user_key = str(user) + '_rec'
            cache.set(user_key, movies_str, timeout=None)
            continue

        # 评价次数>15,40部协同过滤+10部基于内容
        if rate_record_num > 15:
            # 40部协同过滤
            for movie in rate_movies:
                if movie in rate_records:
                    continue
                pred, _ = algo1.estimate(u=algo1.trainset.to_inner_uid(user), i=algo1.trainset.to_inner_iid(movie))
                tmp_algo1_res.append((str(movie), pred))
            tmp_algo1_res.sort(key=lambda x: x[1], reverse=True)
            algo1_list = [movie_id for (movie_id, _) in tmp_algo1_res][:n - 10]

            # 10部基于内容
            pred = algo2.estimate(user, user_attrs, movies_attrs)
            pred.sort(key=lambda x: x[1], reverse=True)
            algo2_list = []
            count = 0
            for (movie_id, _) in pred:
                if movie_id in rate_records:
                    continue
                if movie_id in algo1_list:
                    continue
                algo2_list.append(str(movie_id))
                count += 1
                if count == 10:
                    break
            # 存入redis
            movies_str = " ".join(algo1_list + algo2_list)
            user_key = str(user) + '_rec'
            cache.set(user_key, movies_str, timeout=None)


def get_recommend():
    """
    获取用户电影推荐信息，存入redis中
    """
    # 导入数据
    reader = Reader(rating_scale=(1, 5))
    user_rate = pd.DataFrame(UserRate.objects.values())
    data = Dataset.load_from_df(df=user_rate[['user_id', 'movie_id', 'rate']], reader=reader)

    trainset = data.build_full_trainset()
    # 协同过滤训练
    algo1 = KNNWithMeans()
    algo1.fit(trainset)

    # 基于内容训练
    algo2 = content_based_recommendation.ContentBased(sim_options={'attrs': attrs})
    algo2.fit(trainset)

    # 预测并存入redis
    get_top_n(algo1, algo2, 50)
    pass


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


# 更新用户兴趣属性表
def update_user_attr():
    today = timezone.now()
    yesterday = today - timezone.timedelta(days=1)
    users = UserRate.objects.filter(rate_time__gte=yesterday).values_list('user', flat=True).distinct()
    for user in users:
        movies = UserRate.objects.filter(user=user).order_by('movie').values_list('movie', flat=True)
        rate = UserRate.objects.filter(user=user).order_by('movie').values_list('rate', flat=True)
        movies_attr = MovieAttributes.objects.filter(movie__in=movies)
        user_attrs = UserAttributes.objects.filter(user=user)

        for index, attr in enumerate(attrs):
            attr_list = movies_attr.values_list(attr, flat=True)
            div = list(attr_list).count(1)
            if div == 0:
                continue
            user_attrs.update(**{attr: sum([x * y for x, y in zip(attr_list, rate)]) / list(attr_list).count(1)})


def update_movie_attr():
    attrs_cn = ['剧情', '喜剧', '动作', '爱情', '科幻', '动画', '悬疑', '惊悚', '恐怖', '纪录片',
                '短片', '情色', '同性', '音乐', '歌舞', '家庭', '儿童', '传记', '历史', '战争',
                '犯罪', '西部', '奇幻', '冒险', '灾难', '武侠', '古装']

    today = timezone.now()
    yesterday = today - timezone.timedelta(days=1)
    for index, attr_cn in enumerate(attrs_cn):
        movies_id = Movie.objects.filter(update_time__gte=yesterday, type__contains=attr_cn)
        MovieAttributes.objects.filter(movie__in=movies_id).update(**{attrs[index]: 1})

    movies = MovieAttributes.objects.filter(update_time__gte=yesterday)
    counts = np.zeros(len(movies))
    for attr in attrs:
        counts += movies.values_list(attr, flat=True)
    index = 0
    for movie in movies:
        movie.sum_types = counts[index]
        movie.save()
        index += 1


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(
            get_recommend,
            trigger=CronTrigger(hour="21", minute="23"),
            id="get_recommend",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'get_recommend'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="23", minute="50"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        scheduler.add_job(
            update_user_attr,
            trigger=CronTrigger(hour="21", minute="19"),
            id="update_user_attr",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added daily job: 'update_user_attr_executions'."
        )

        scheduler.add_job(
            update_movie_attr,
            trigger=CronTrigger(hour="21", minute="19"),
            id="update_movie_attr",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added daily job: 'update_user_attr_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

