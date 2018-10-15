import unittest
import random
from simulation import Simulation
from virus import Virus

class SimulationTest(unittest.TestCase):

    hiv = Virus("HIV", 0.5, 0.5)
    # bird_flu = Virus("Hard Virus", 0.99, 0.99)

    self.large_sim = Simulation(100, 0.5, hiv, 100)
    self.small_sim = Simulation(10, 0.25, hiv, 5)

    def test_create_population_method(self):
        infected_count = 0
        vaccinated = 0
        self.large_sim._create_population()
        assert len(self.large_sim.population) == 10000

        for person in self.large_sim.population:
            if person.infection is not None:
                infected_count += 1

        assert infected_count == 100

        for person in self.large_sim.population:
            if person.is_vaccinated and person.infection is None:
                vaccinated += 1

        assert vaccinated == 4950

    def test_should_continue_method(self):
        self.large_sim._create_population()
        assert self.large_sim._simulation_should_continue() is True

    def test_should_continue_method_cure_found_case(self):
        self.large_sim._create_population()

        for person in self.large_sim.population:
            person.is_alive = True
            person.infection = None
            person.is_vaccinated = True
        assert self.large_sim._simulation_should_continue() is False

    def test_should_continue_method_deaths_case(self):
        self.large_sim._create_population()

        for person in self.large_sim.population:
            person.is_alive = False
        assert self.large_sim._simulation_should_continue() is False

    def test_interaction(self):
        self.small_sim._create_population()
        number_of_interaction = 1
        for person in self.small_sim.population:
            while number_of_interaction <= 100:
                random_person = random.choice(self.small_sim.population)
                # Prevent interaction with dead people and with it self
                while random_person.is_alive is False or random_person._id == person._id:
                    rando = random.choice(self.small_sim.population)
                assert person._id is not random_person._id
                assert random_person.is_alive is True
                self.small_sim.interaction(person, rando)
                number_of_interaction += 1
            number_of_interaction = 1
