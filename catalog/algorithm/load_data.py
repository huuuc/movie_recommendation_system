# 使用MovieLens数据集，它是在实现和测试推荐引擎时所使用的最常见的数据集之一。它包含来自于943个用户
# 以及精选的1682部电影的100K个电影打分。
import pandas as pd
import numpy as np

# 获取用户信息:
u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
users = pd.read_csv('ml-100k/u.user', sep='|', names=u_cols, encoding='latin-1')

# 获取评分信息:
r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
ratings = pd.read_csv('ml-100k/u.data', sep='\t', names=r_cols, encoding='latin-1')

# 获取电影信息:
i_cols = ['movie id', 'movie title', 'release date', 'video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure',
          'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
          'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
items = pd.read_csv('ml-100k/u.item', sep='|', names=i_cols, encoding='latin-1')

n_users = ratings.user_id.unique().shape[0]
n_items = ratings.movie_id.unique().shape[0]
per_year_unix = 31536000
# csv文件读取评分矩阵
data_matrix = np.loadtxt("score_matrix.csv", delimiter=",")
# csv文件读取属性矩阵
attr_score_matrix = np.loadtxt("attribute_matrix.csv", delimiter=",")
# 存储原生电影属性
attr_matrix = np.loadtxt("attr_matrix.csv", delimiter=",")


# 获取评分矩阵
# for line in ratings.itertuples():
#     data_matrix[line[1] - 1, line[2] - 1] = line[3]
#     unix_matrix[line[1] - 1, line[2] - 1] = line[4] / per_year_unix
