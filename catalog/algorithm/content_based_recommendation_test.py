from surprise import AlgoBase
from surprise import PredictionImpossible
import numpy as np

from six import iteritems


class SymmetricAlgo(AlgoBase):
    """This is an abstract class aimed to ease the use of symmetric algorithms.

    A symmetric algorithm is an algorithm that can can be based on users or on
    items indifferently, e.g. all the algorithms in this module.

    When the algo is user-based x denotes a user and y an item. Else, it's
    reversed.
    """

    def __init__(self, sim_options={}, verbose=True, **kwargs):

        AlgoBase.__init__(self, sim_options=sim_options, **kwargs)
        self.verbose = verbose

    def fit(self, trainset):

        AlgoBase.fit(self, trainset)

        self.n_x = self.trainset.n_users
        self.n_y = self.trainset.n_items
        self.xr = self.trainset.ur
        self.yr = self.trainset.ir

        return self


class ContentBased(SymmetricAlgo):

    def __init__(self, sim_options={}, verbose=True, **kwargs):

        SymmetricAlgo.__init__(self, sim_options=sim_options,
                               verbose=verbose, **kwargs)

    def fit(self, trainset):
        print("start fit...")
        SymmetricAlgo.fit(self, trainset)
        self.attr_raw_matrix = np.loadtxt("attr_matrix.csv", delimiter=",")
        self.means = np.zeros(self.n_x)
        self.attr_matrix = np.zeros((self.n_x, 19))
        total_matrix = np.zeros((self.n_x, 19))
        for x, ratings in iteritems(self.xr):
            for (movie_id, r) in ratings:
                self.means[x] += r
                raw_movie_id = trainset.to_raw_iid(movie_id)
                movie_attr = self.attr_raw_matrix[int(raw_movie_id) - 1]
                self.attr_matrix[x] += r * movie_attr
                total_matrix[x] += movie_attr
            self.means[x] /= len(ratings)
        total_matrix = np.maximum(total_matrix, 1)
        self.attr_matrix /= total_matrix
        print("end fit...")
        return self

    def estimate(self, u, i):

        if not (self.trainset.knows_user(u) and self.trainset.knows_item(i)):
            raise PredictionImpossible('User and/or item is unknown.')

        sum_est = 0
        sum_res = 0

        raw_movie_id = self.trainset.to_raw_iid(i)
        movie_attr = self.attr_raw_matrix[int(raw_movie_id) - 1]

        for attr_index in range(len(movie_attr)):
            if movie_attr[attr_index] == 1:
                if self.attr_matrix[u][attr_index] == 0:
                    sum_est += self.means[u]
                else:
                    sum_est += self.attr_matrix[u][attr_index]
                sum_res += 1

        if sum_res == 0:
            return 0, {'actual_k': sum_res}

        est = sum_est / sum_res

        details = {'actual_k': sum_res}
        return est, details