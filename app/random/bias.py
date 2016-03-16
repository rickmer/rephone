from .biased_pseudo_random import BiasedRandomDistribution
from app.models import RandomBias, Audience, db


class BiasedRandomValue(object):

    def __init__(self):
        self.list_of_vectors = []
        audiences = Audience().query.all()
        for audience in audiences:
            vector = []
            biases = RandomBias().query.filter_by(id_audience=audience.id).all()
            if len(biases) == 0:
                for _ in audience.respondents:
                    vector.append(1)
            else:
                for bias in biases:
                    vector.append(bias.distribution_value)
            self.list_of_vectors.append(BiasedRandomDistribution(vector))

    def __iter__(self):
        return iter(self.list_of_vectors)

    def __getitem__(self, item):
        return self.list_of_vectors[item - 1]

    def get_random_value(self, audience_id):
        return self[audience_id].get_random_value()

    def add_sample(self, audience_id, value):
        self[audience_id].add_sample(value)
        biases = RandomBias().query.filter_by(id_audience=audience_id).all()
        if len(biases) == 0:
            for i in range(1, len(self[audience_id]) + 1):
                random_bias = RandomBias(id_audience=audience_id,
                                         id_respondent=i,
                                         distribution_value=1)
                db.session.add(random_bias)
        else:
            vector_index = 0
            for bias in biases:
                bias.distribution_value = self[audience_id][vector_index]
                vector_index += 1
        db.session.commit()
