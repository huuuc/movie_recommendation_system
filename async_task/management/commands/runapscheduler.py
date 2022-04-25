import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
import os
import django
import pandas as pd
from surprise import Dataset, Reader
from surprise import KNNWithMeans
from collections import defaultdict
from django.core.cache import cache
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'localMovie.settings')
django.setup()
from catalog.models import UserRate, User, Movie

logger = logging.getLogger(__name__)


def get_top_n(algo, n=50):
    users = UserRate.objects.values_list('user', flat=True).distinct()
    movies = UserRate.objects.values_list('movie', flat=True).distinct()
    pub_movies = Movie.objects.all().order_by('-implicit_score')[:n]
    pub_list = []
    # 获取热门电影
    for movie in pub_movies:
        pub_list.append(str(movie.id))
    pub_moveis_str = " ".join(pub_list)

    for user in users:
        records = UserRate.objects.filter(user=user).values_list('movie_id', flat=True)
        record_num = len(records)
        if record_num == 0:
            user_key = str(user) + '_rec'
            cache.set(user_key, pub_moveis_str, timeout=None)
            continue
        tmp_res = []
        for movie in movies:
            if movie in records:
                continue
            pred, _ = algo.estimate(u=algo.trainset.to_inner_uid(user), i=algo.trainset.to_inner_iid(movie))
            tmp_res.append((str(movie), pred))
        tmp_res.sort(key=lambda x: x[1], reverse=True)
        mm_list = [movie_id for (movie_id, _) in tmp_res][:n]
        movies_str = " ".join(mm_list)
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

    # 训练
    trainset = data.build_full_trainset()
    algo = KNNWithMeans()
    algo.fit(trainset)

    # 预测并存入redis
    get_top_n(algo, 50)
    pass


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(
            get_recommend,
            trigger=CronTrigger(hour="20", minute="08"),
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

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

