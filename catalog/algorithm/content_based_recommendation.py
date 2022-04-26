from surprise import AlgoBase
from surprise import PredictionImpossible
import numpy as np
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'localMovie.settings')
django.setup()
from catalog.models import UserAttributes, MovieAttributes
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
        self.attrs = sim_options['attrs']

    def fit(self, trainset):
        print("start fit...")
        SymmetricAlgo.fit(self, trainset)
        self.means = np.zeros(self.n_x)
        for x, ratings in iteritems(self.xr):
            for (movie_id, r) in ratings:
                self.means[x] += r
            self.means[x] /= len(ratings)

        print("end fit...")
        return self

    def get_means(self, u):
        return self.means[self.trainset.to_inner_uid(u)]

    def estimate(self, u, user_attrs, movies_attrs):
        mean = self.get_means(u)

        sum_res = np.zeros(len(movies_attrs))
        movies_id = np.array(movies_attrs.values_list('movie', flat=True))
        for attr in self.attrs:
            user_attr = float(user_attrs[attr])
            if user_attr == 0:
                user_attr = mean
            attr_list = np.array(movies_attrs.values_list(attr, flat=True))
            sum_res = sum_res + attr_list * user_attr

        sum_types = np.array(movies_attrs.values_list('sum_types', flat=True))
        score = sum_res / sum_types

        est = list(zip(movies_id, score))

        return est
