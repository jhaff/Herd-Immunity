class Virus(object):

    def __init__(self, name, mortality_rate, repro_rate):
        self.name = name
        self.mortality_rate = mortality_rate
        self.repro_rate = repro_rate


def test_virus_instantiation(): #pytest to ensure init is working
    virus = Virus("AIDS", 0.8, 0.2)
    assert virus.name == "AIDS"
    assert virus.mortality_rate == 0.8
    assert virus.repro_rate == 0.3
