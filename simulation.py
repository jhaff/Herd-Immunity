import random, sys
random.seed(42)
from person import Person
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

        # TODO: Create a Logger object and bind it to self.logger.  You should use this
        # logger object to log all events of any importance during the simulation.  Don't forget
        # to call these logger methods in the corresponding parts of the simulation!
        self.logger = None

        # track of all the people that catch the infection during a given time step.
        self.newly_infected = []

        self.population = self._create_population(initial_infected);

        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(virus_name, population_size, vacc_percentage, initial_infected)


    def _create_population(self, initial_infected):
        # Returns an array filled with Person objects that matches the specifications of the
        # simulation (correct number of people in the population, correct percentage of
        # people vaccinated, correct number of initially infected people).
        population = []
        infected_count = 0
        while len(population) != pop_size:
            if infected_count !=  initial_infected:
                person = Person(self.next_person_id, False, self.virus)
                self.population.append(person)
                self.next_person_id += 1
                infected_count += 1
                pass
            else:
                vaxChance = random.uniform(0,1)
                #Person vaxxed or not based off random chance
                if vaxChance < self.vacc_percentage: #vaccinated person
                    person = Person(self.next_person_id, True, None)
                    self.population.append(person)
                    self.next_person_id += 1
                else: #unvaccinated person
                    person = Person(self.next_person_id, False, None)
                    self.population.append(person)
                    self.next_person_id += 1
        self.current_infected += infected_count
        self.total_infected += infected_count
        return population

    def _simulation_should_continue(self):
        #checks whether sim should continue...
        #If everyone is dead or there are no infected people, it shouldn't.
        if self.population_size == 0 or self.current_infected == 0:
            return False
        else:
            return True

    def run(self):

        time_step_counter = 0 # to track how many steps in we are

        should_continue = self._simulation_should_continue() #check if sim should continue
        while should_continue:
            self.time_step()
            time_step_counter += 1
            should_continue = self.should_continue() #check if sim should continue again
        print('The simulation has ended after {time_step_counter} turns.'.format(time_step_counter))

    def time_step(self):

        number_of_interactions = 1

        for person in self.population:
            if person.infection:
                 while number_of_interactions <= 100: # Repeat for 100 total interactions:
                     stranger = random.choice(self.population) #grab a random person

                     # Prevent the person from acting on itself since we don't interact with the dead. Choose a new person.
                     while stranger._id == person._id or stranger.is_alive is False:
                         stranger = random.choice(self.population)

                     self.interaction(person, stranger) #conduct possible infection

                     number_of_interactions += 1

                number_of_interaction = 1 #reset number of interactions so the for loop can select another person and run again

            else:
                pass

            self._infect_newly_infected()

    def interaction(self, person, random_person):
        #only living people should be passed into this method.
        assert person1.is_alive == True
        assert random_person.is_alive == True

        if random_person.is_vaccinated:
             self.logger.log_interaction(person, random_person, False, True, False)
        if random_person.infection is not None:
             self.logger.log_interaction(person, random_person, False, False, True)
        else:
             if random.random() < self.basic_repro_num: #if luck is bad
                 self.newly_infected.append(random_person._id) #add 'em to the array
                 random_person.infection = self.virus
                 self.logger.log_interaction(person, random_person, True, False, False)
             else: #lucky intereaction with no infecting!
                 self.logger.log_interaction(person, random_person, False, False, False)

    def _infect_newly_infected(self): #Called at the end of every time step

        for person in self.newly_infected: #Infect everyone in newly_infected[]
             person.infection = self.virus
             self.total_infected += 1 #increment counters
             self.current_infected += 1

         self.newly_infected = [] #since we are done infecting the newly infected, reset.

if __name__ == "__main__":
    params = sys.argv[1:]
    pop_size = int(params[0])
    vacc_percentage = float(params[1])
    virus_name = str(params[2])
    mortality_rate = float(params[3])
    basic_repro_num = float(params[4])
    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1
    simulation = Simulation(pop_size, vacc_percentage, virus_name, mortality_rate,
                            basic_repro_num, initial_infected)
    simulation.run()
