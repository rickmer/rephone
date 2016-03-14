class BiasedRandomDistribution(object):
    """
    A pseudo random number generator that can be biased to promote a pseudo random distribution
    of outbound calls, even if users have favors for choosing some particular dialog partners.
    """
    def __init__(self, cardinal):
        """
        :param cardinal: cardinality of the initial distribution vector as integer value with
                         evenly distributed chance of 1/cardinal.
                         or a list of integers representing the initial distribution vector.
                         Example: [1, 1, 1, 1] initialisation vector results in random numbers
                                  between 1 and 4 with initial chance of 1/4 each.
                                  [1, 1, 2, 1]initialisation vector results in random numbers
                                  between 1 and 4 where 1,2 and 4 have the initial chance of 1/5
                                  and 3 has the initial chance of 2/5.
        """
        from array import array
        if type(cardinal) == list:
            self.distribution_vector = array('I', cardinal)
            self.base = 0
            for value in cardinal:
                self.base += value
            self.cardinal = len(cardinal)
        elif type(cardinal) == int:
            self.distribution_vector = array('I')
            for item in range(0, cardinal):
                self.distribution_vector.append(1)
            self.base = cardinal
            self.cardinal = cardinal
        else:
            raise TypeError

    def __iter__(self):
        return iter(self.distribution_vector)

    def __getitem__(self, item):
        return self.distribution_vector[item]

    def __str__(self):
        return str(list(self.distribution_vector))

    def __len__(self):
        return len(self.distribution_vector)

    def _get_biased_random_number_(self):
        """
        :return: biased pseudo random integer between 1 and initial cardinality.
        """
        from random import randint
        basis = self._get_base_()
        random = randint(0, basis - 1)
        counter = 0
        temp_value = 0
        for number in self:
            counter += 1
            temp_value += number
            if temp_value >= random:
                return counter

    def _get_base_(self):
        """
        Recalculates the base of the current distribution vector.
        :return: int
        """
        self.base = 0
        for number in self:
            self.base += number
        return self.base

    def _mutate_(self, index):
        """
        Alters the distribution vector.
        :param index: integer value between 0 and cardinality - 1
        """
        if index > self.cardinal - 1 or index < 0:
            raise IndexError
        loop_index = 0
        for _ in self:
            if loop_index != index:
                self.distribution_vector[loop_index] += 1
            loop_index += 1
        self._get_base_()

    def add_sample(self, integer):
        """
        Alter the distribution vector
        :param integer: value between 1 and cardinality.
        """
        self._mutate_(integer - 1)

    def get_random_value(self):
        """
        :return: biased pseudo random integer
        """
        return self._get_biased_random_number_()
