from app.random.biased_pseudo_random import BiasedRandomDistribution


def test_biased_pseudo_random_distribution():
    """
    Tests if the the distribution_vector changed in an expectable degree
    over 1000 iterations with pseudo random samples.
    """
    biased_randomness = BiasedRandomDistribution(1000)
    for _ in range(1, 1000):
        random_number = biased_randomness.get_random_value()
        biased_randomness.add_sample(random_number)
    print(biased_randomness.distribution_vector)
    for integer in biased_randomness:
        assert integer / 100 >= 9.9
