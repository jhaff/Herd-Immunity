from person import Person
from virus import Virus
import unittest


class PersonTest(unittest.TestCase):
    # Set up virus objects for following tests
    def setUp(self):
        self.easy_virus = Virus("Easy Virus", 0, 0)
        self.hard_virus = Virus("Hard Virus", 0.99, 0.99)


    # Checking the instantiation of person object with virus
    def test_person_instantiation(self):
        init_person = Person(1, False, self.easy_virus)
        assert init_person.infection is self.easy_virus
        assert init_person.is_alive is True
        assert init_person._id is 1
        assert init_person.is_vaccinated is False

    # Check two cases of person objects
    def test_did_survive_method(self):
        hard_infected_person = Person(1, False, self.hard_virus)
        easy_infected_person = Person(2, False, self.easy_virus)

        assert hard_infected_person.did_survive_infection() is False
        assert hard_infected_person.is_alive is False
        assert hard_infected_person.infection is not None

        assert easy_infected_person.did_survive_infection() is True
        assert easy_infected_person.is_alive is True
        assert easy_infected_person.infection is None
