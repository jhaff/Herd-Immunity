import random, sys
random.seed(42)
from person import Person
from virus import Virus
from logger import Logger

class Simulation(object):


    def __init__(self, population_size, vacc_percentage, virus,
                 initial_infected=1):
        self.population_size = population_size
        self.population = []
        self.total_infected = 0
        self.current_infected = 0
        self.next_person_id = 0
        self.virus = virus
        self.vacc_percentage = vacc_percentage
        self._create_population(initial_infected);
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(virus_name, population_size, vacc_percentage, initial_infected)
        self.logger = Logger(self.file_name)

        # To track of all the people that catch the infection during a given time step.
        self.newly_infected = []


    def _create_population(self, initial_infected):
        # Returns an array filled with Person objects that matches the specifications of the
        # simulation (correct number of people in the population, correct percentage of
        # people vaccinated, correct number of initially infected people).
        print("creating population...")
        population = []
        infected_count = 0
        while len(self.population) != pop_size:
            print("creating person {}".format(len(self.population)))
            if infected_count !=  initial_infected:
                person = Person(self.next_person_id, False, self.virus)
                self.population.append(person)
                self.next_person_id += 1
                infected_count += 1
                print("  They're infected")
            else:
                vaxChance = random.uniform(0,1)
                #Person vaxxed or not based off random chance
                if vaxChance < self.vacc_percentage: #vaccinated person
                    person = Person(self.next_person_id, True, None)
                    self.population.append(person)
                    self.next_person_id += 1
                    print("  They're vaccinated")
                else: #unvaccinated person
                    person = Person(self.next_person_id, False, None)
                    self.population.append(person)
                    self.next_person_id += 1
                    print("  They're unvaccinated")
        self.current_infected += infected_count
        self.total_infected += infected_count
        print("population created.")
        return population

    def _simulation_should_continue(self):
        #checks whether sim should continue...
        #If everyone is dead or there are no infected people, it shouldn't.
        print("checking _simulation_should_continue")

        people_alive = False
        people_infected = False
        for person in self.population:
            if person.is_alive == True:
                people_alive = True
            # else:
            #     pass
            if person.infection != None:
                people_infected = True
            # else:
            #     pass
        if people_alive and people_infected:
            print("sim should continue")
            return True
        else:
            print("sim should NOT continue")
            return False

    def run(self):
        print("simulation running")

        time_step_counter = 0 # to track how many steps in we are

        should_continue = self._simulation_should_continue() #check if sim should continue
        print(should_continue)
        while should_continue:
            self.time_step()
            time_step_counter += 1
            print(time_step_counter)
            self.logger.log_time_step(time_step_counter)
            should_continue = self._simulation_should_continue() #check if sim should continue again

        print('The simulation has ended after {} turns.'.format(time_step_counter))
        self.logger.stats(self.population, self.total_infected)

    def time_step(self):

        number_of_interactions = 1

        for person in self.population:
            if person.infection and person.is_alive == True:
                print("running time step")
                while number_of_interactions <= 100: # Repeat for 100 total interactions:
                    stranger = random.choice(self.population) #grab a random person

                     # Prevent the person from acting on itself since we don't interact with the dead. Choose a new person.
                    while stranger._id == person._id or stranger.is_alive is False:
                         stranger = random.choice(self.population)

                    self.interaction(person, stranger) #conduct possible infection

                    number_of_interactions += 1

                number_of_interaction = 1 #reset number of interactions so the for loop can select another person and run again

            elif person.infection is not None and person.is_alive == True:
                self.logger.log_infection_survival(person, False)

        self._infect_newly_infected()


    def interaction(self, person, random_person):
        #only living people should be passed into this method.
        assert person.is_alive == True
        assert random_person.is_alive == True

        if random_person.is_vaccinated:
             self.logger.log_interaction(person, random_person, False, True, False)
        if random_person.infection is not None:
             self.logger.log_interaction(person, random_person, False, False, True)
        else:
             if random.random() < self.virus.repro_rate: #if luck is bad
                 self.newly_infected.append(random_person) #add 'em to the array
                 random_person.infection = self.virus
                 self.logger.log_interaction(person, random_person, True, False, False)
             else: #lucky intereaction with no infecting!
                 self.logger.log_interaction(person, random_person, False, False, False)

    def _infect_newly_infected(self): #Called at the end of every time step
        print("infecting newly_infected")

        for person in self.newly_infected: #Infect everyone in newly_infected[]
             person.infection = self.virus
             self.total_infected += 1 #increment counters
             self.current_infected += 1

        print(self.newly_infected)
        self.newly_infected = [] #since we are done infecting the newly infected, reset.

if __name__ == "__main__":
    params = sys.argv[1:]
    pop_size = int(params[0])
    vacc_percentage = float(params[1])
    virus_name = str(params[2])
    mortality_rate = float(params[3])
    repro_rate = float(params[4])
    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(virus_name, mortality_rate, repro_rate)
    simulation = Simulation(pop_size, vacc_percentage, virus, initial_infected)

    simulation.run()
