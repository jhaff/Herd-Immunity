class Logger(object):
    '''
    Utility class responsible for logging all interactions of note during the
    simulation.
    _____Attributes______
    file_name: the name of the file that the logger will be writing to.
    _____Methods_____
    __init__(self, file_name):
    write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
        basic_repro_num):
        - Writes the first line of a logfile, which will contain metadata on the
            parameters for the simulation.
    log_interaction(self, person1, person2, did_infect=None, person2_vacc=None, person2_sick=None):
        - Expects person1 and person2 as person objects.
        - Expects did_infect, person2_vacc, and person2_sick as Booleans, if passed.
        - Between the values passed with did_infect, person2_vacc, and person2_sick, this method
            should be able to determine exactly what happened in the interaction and create a String
            saying so.
        - The format of the log should be "{person1.ID} infects {person2.ID}", or, for other edge
            cases, "{person1.ID} didn't infect {person2.ID} because {'vaccinated' or 'already sick'}"
        - Appends the interaction to logfile.
    log_infection_survival(self, person, did_die_from_infection):
        - Expects person as Person object.
        - Expects bool for did_die_from_infection, with True denoting they died from
            their infection and False denoting they survived and became immune.
        - The format of the log should be "{person.ID} died from infection" or
            "{person.ID} survived infection."
        - Appends the results of the infection to the logfile.
    log_time_step(self, time_step_number):
        - Expects time_step_number as an Int.
        - This method should write a log telling us when one time step ends, and
            the next time step begins.  The format of this log should be:
                "Time step {time_step_number} ended, beginning {time_step_number + 1}..."
        - STRETCH CHALLENGE DETAILS:
            - If you choose to extend this method, the format of the summary statistics logged
                are up to you.  At minimum, it should contain:
                    - The number of people that were infected during this specific time step.
                    - The number of people that died on this specific time step.
                    - The total number of people infected in the population, including the newly
                        infected
                    - The total number of dead, including those that died during this time step.
    '''

    def __init__(self, file_name):
        # TODO:  Finish this initialization method.  The file_name passed should be the
        # full file name of the file that the logs will be written to.

        self.file_name = file_name
        self.file = open(self.file_name, "w")
        self.add_to_file = open(self.file_name, "a")

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                       basic_repro_num):
        # The simulation class should use this method
        # immediately upon creation, to log the specific parameters of the simulation
        # as the first line of the file.  This line of metadata should be tab-delimited
        # (each item separated by a '\t' character).

        # Since this is the first method called, it will create the text file
        # that we will store all logs in.  Be sure to use 'w' mode when you open the file.
        # For all other methods use the 'a' mode to append our new log to the end,
        # since 'w' overwrites the file.


        first_line = (str(pop_size + vacc_percentage + virus_name + mortality_rate + basic_repro_num).split("\t"))

        self.file.write(first_line)

        pass

    def log_interaction(self, person1, person2, did_infect=None,
                        person2_vacc=None, person2_sick=None):
        # The Simulation object should use this method to
        # log every interaction a sick individual has during each time step.  This method
        # should accomplish this by using the information from person1 (the infected person),
        # person2 (the person randomly chosen for the interaction), and the optional
        # keyword arguments passed into the method.  See documentation for more info
        # on the format of the logs that this method should write.

        if person2_vacc:
            log = "{} didn't infect {} because {} was vaccinated\n".format(person1._id, person2._id, person2._id)
        elif person2_sick:
            log = "{} didn't infect {} because {} was already sick\n".format(person1._id, person2._id, person2._id)
        else:
            log = "{} infected {}\n".format(person1._id, person2._id)

        self.add_to_file.write(log)


    def log_general(self, quote):

        self.add_to_file.write(quote)

    def log_infection_survival(self, person, did_die_from_infection):

        if did_die_from_infection:
            log = "{} died from infection\n".format(person._id)

        else:
            log = "{} survived from infection\n".format(person._id)


        self.add_to_file.write(log)

        # The Simulation object should use this method to log
        # the results of every call of a Person object's .resolve_infection() method.
        # If the person survives, did_die_from_infection should be False.  Otherwise,
        # did_die_from_infection should be True.  See the documentation for more details
        # on the format of the log.

    def log_time_step(self, time_step_number):
        #log when a time step ends, and a new one begins.

        self.add_to_file.write("Time step {} ended, beginning {} ...\n".format(time_step_number, time_step_number + 1))

        pass

    def stats(self, population, total_infected):
        total_dead = 0
        for person in population:
            if person.is_alive == False:
                total_dead += 1
            else:
                pass
        print("Total number infected: {}".format(total_infected))
        print("Total number dead: {}.".format(total_dead))
        # print("The total size of the population is {}".format(len(population)))

        final_stats = open("final_stats.txt", "a")
        final_stats.write("\nThe percentage of infected for this simulation was {}% \nThe percentage of dead for this simulation was {}% \nThe number of times someone was saved because they were vaccinated is {}".format(total_infected/len(population) * 100, total_dead/len(population) * 100, self.saved_by_vaccine))
