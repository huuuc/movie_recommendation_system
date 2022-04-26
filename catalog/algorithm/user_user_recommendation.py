import os
import django
import numpy as np
import pandas as pd
from surprise import Dataset, Reader
from surprise import KNNWithMeans

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'localMovie.settings')
django.setup()
from catalog.models import UserRate, MovieAttributes


def get_top_n(algo, n=50):
    users = UserRate.objects.values_list('user', flat=True).distinct()
    movies = UserRate.objects.values_list('movie', flat=True).distinct()
    for user in users:
        records = UserRate.objects.filter(user=user).values_list('movie_id', flat=True)
        tmp_res = []
        for movie in movies:
            if movie in records:
                continue
            try:
                pred, _ = algo.estimate(u=algo.trainset.to_inner_uid(user), i=algo.trainset.to_inner_iid(movie))
            except:
                print(user, movie)
            tmp_res.append((movie, pred))
        tmp_res.sort(key=lambda x: x[1], reverse=True)
        print(tmp_res)


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


attrs = ['plot', 'comedy', 'action', 'romance', 'sci_fi', 'animation', 'suspense',
             'thriller', 'fear', 'documentary', 'short', 'erotica', 'homosexual', 'music',
             'musical', 'family', 'children', 'biography', 'history', 'war', 'crime',
             'western', 'fantasy', 'adventure', 'disaster', 'martial', 'costume']


def compute_movie_types():
    movies = MovieAttributes.objects.all()
    counts = np.zeros(len(movies))
    for attr in attrs:
        counts += movies.values_list(attr, flat=True)
    index = 0
    for movie in movies:
        movie.sum_types = counts[index]
        movie.save()
        index += 1


compute_movie_types()