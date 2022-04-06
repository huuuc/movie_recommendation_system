import os
import io
from surprise import SVD, KNNBaseline, KNNBasic, KNNWithMeans
from surprise import Dataset
from catalog.algorithm import knn_based_recommendation, content_based_recommendation
from surprise.model_selection import cross_validate

# Load the movielens-100k dataset (download it if needed).
data = Dataset.load_builtin('ml-100k')


# 得到id-name以及name-id映射
def read_item_names():
    file_name = (os.path.expanduser('~') +
                 '/.surprise_data/ml-100k/ml-100k/u.item')
    rid_to_name = {}
    name_to_rid = {}
    with io.open(file_name, 'r', encoding='ISO-8859-1') as f:
        for line in f:
            line = line.split('|')
            rid_to_name[line[0]] = line[1]
            name_to_rid[line[1]] = line[0]

    return rid_to_name, name_to_rid


# # 使用KNNBasic算法
# trainset = data.build_full_trainset()
# sim_options = {'name': 'pearson_baseline', 'user_based': False}
# algo = KNNBaseline(sim_options=sim_options)
# algo.fit(trainset)
sim_options = {'name': 'pearson', 'user_based': False}
# algo = customize_recommendation.KNNWithTime()
algo = content_based_recommendation.ContentBased()
# 5折交叉验证计算并打印结果.
cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

# # 获取电影名到电影id和电影id到电影名的映射
# id_to_name, name_to_id = read_item_names()
#
# # 获取电影的inner_id
# movie_id = name_to_id['Toy Story (1995)']
# movie_inner_id = algo.trainset.to_inner_iid(movie_id)
#
# # 获取最近邻
# movie_neighbors = algo.get_neighbors(movie_inner_id, k=10)
#
# # 获取最近邻电影名
# movie_neighbors = (algo.trainset.to_raw_iid(inner_id) for inner_id in movie_neighbors)
# movie_neighbors = (id_to_name[rid] for rid in movie_neighbors)
#
# print()
# print('The 10 nearest neighbors of Toy Story are:')
# for movie in movie_neighbors:
#     print(movie)
