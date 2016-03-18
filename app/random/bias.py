from .biased_pseudo_random import BiasedRandomDistribution
from app.models import RandomBias, Audience, db
from operator import attrgetter


class BiasedRandomValue(object):

    def __init__(self):
        self.list_of_vectors = []
        audiences = Audience().query.all()
        for audience in audiences:
            vector = []
            biases = sorted(RandomBias().query.filter_by(id_audience=audience.id).all(), key=attrgetter('vector_index'))
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

    def add_sample(self, audience_id, respondent_id):
        index = RandomBias().query.filter_by(id_audience=audience_id, id_respondent=respondent_id).first().vector_index
        self[audience_id].add_sample(index)
        biases = sorted(RandomBias().query.filter_by(id_audience=audience_id).all(), key=attrgetter('vector_index'))
        if len(biases) == 0:
            audience = Audience().query.filter_by(id=audience_id).first()
            index_counter = 0
            for respondent in sorted(audience.respondents, key=attrgetter('id')):
                random_bias = RandomBias(id_audience=audience_id,
                                         id_respondent=respondent.id,
                                         vector_index=index_counter,
                                         distribution_value=1)
                index_counter += 1
                db.session.add(random_bias)
        else:
            vector_index = 0
            for bias in biases:
                bias.distribution_value = self[audience_id][vector_index]
                vector_index += 1
        db.session.commit()
