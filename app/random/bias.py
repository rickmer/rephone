from .biased_pseudo_random import BiasedRandomDistribution
from app.models import RandomBias, Audience, db


class Bias(object):

    bias_vectors = {}

    def __init__(self):
        audiences = Audience.query.all()
        for audience in audiences:
            vector_values = RandomBias().query.filter_by(id_audience=audience.id).all()
            if not vector_values:
                self.bias_vectors[audience.id] = BiasedRandomDistribution(cardinal=len(audience.respondents))
            else:
                vector = []
                for value in vector_values:
                    vector.append(value.distribution_value)
                self.bias_vectors[audience.id] = BiasedRandomDistribution(vector)

    def store_value(self, audience_id, respondent_id):
        self.bias_vectors[audience_id].add_sample(respondent_id)
        self._persist_to_db_(audience_id)

    def _persist_to_db_(self, audience_id):
        records = RandomBias().query.filter_by(id_audience=audience_id).all()
        if not records:
            for dimension in self.bias_vectors[audience_id].distribution_vector:
                db.session.add(RandomBias(id_audience=audience_id,
                                          id_respondent=dimension))
            db.session.commit()
        else:
            for record in records:
                record.distribution_value = self.bias_vectors[record.id_respondent]
            db.session.commit()


