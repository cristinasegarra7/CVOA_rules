import pandas as pd
from cvoa2 import CVOA
from rule_support_function import ruleSupport
import multiprocessing as mp
import numpy as np
from copy import deepcopy
import sys as sys
import random as random
from individual import Individual

data = pd.read_csv('terremotos_data.csv', sep = ';')

class CVOA:
    MIN_SPREAD = 0
    MAX_SPREAD = 5
    MIN_SUPERSPREAD = 6
    MAX_SUPERSPREAD = 15
    SOCIAL_DISTANCING = 7
    P_ISOLATION = 0.7
    P_TRAVEL = 0.1
    P_REINFECTION = 0.001
    SUPERSPREADER_PERC = 0.1
    DEATH_PERC = 0.06 

    def __init__(self, max_time, data, lim_down, lim_up, n_solutions):
        self.infected = []
        self.recovered = []
        self.deaths = []
        self.max_time = max_time
        self.data = data
        self.size = (len(data.columns)-1)*2
        self.lim_down = lim_down 
        self.lim_up = lim_up
        self.n_solutions = n_solutions
        self.bestSolutions = []
        self.VACCINATION = 8

    def vaccinationRate(self, time):
        if time < 36:
            vaccination_rate = 5.11991750e-04*(time*7)+1.07728613e-06**(time*7)**2+1.71589004e-07*(time*7)**3-5.37069705e-10*(time*7)**4
        else:
            vaccination_rate = 0.8
        return vaccination_rate
    
    def propagateDisease(self, time):
        new_infected_list = []
        # Step 1. Assess fitness for each individual.
        for x in self.infected:
            x.fitness = self.fitness(x.values)
            # If x.fitness is NaN, move from infected list to deaths lists
            if np.isnan(x.fitness):
                self.deaths.append(x)
                self.infected.remove(x)
        
        # Step 2. Sort the infected list by fitness (descendent).
        self.infected = sorted(self.infected, key=lambda i: i.fitness, reverse=True)
        # Step 2.1 Add individuals to the bestSolutions until n_solutions is reached
        i=0
        while (len(self.bestSolutions)<self.n_solutions) and i<(len(self.infected)-1):
            if self.infected[i] not in self.bestSolutions:
                self.bestSolutions.append(deepcopy(self.infected[i]))
            i+=1
            
        self.bestSolutions = sorted(self.bestSolutions, key=lambda i: self.fitness(i.values), reverse=True)
        # Step 3. Update best global solutions, if proceed.
        if self.n_solutions > 1:
            i=0
            while i < (len(self.bestSolutions)-1) and i < (len(self.infected)-1):
                for j in range(i,len(self.bestSolutions)):
                    if ((self.fitness(self.bestSolutions[j].values)==None) or (self.fitness(self.infected[i].values) > self.fitness(self.bestSolutions[j].values))) and self.infected[i] not in self.bestSolutions:
                        self.bestSolutions[j] = deepcopy(self.infected[i])
                        break
                i=j
        else:
            if self.fitness(self.bestSolutions[0].values)==None or self.fitness(self.infected[0].values) > self.fitness(self.bestSolutions[0].values):
                self.bestSolutions[0] = deepcopy(self.infected[0])
        # Step 4. Assess indexes to point super-spreaders and deaths parts of the infected list.
        if len(self.infected)==1:
            idx_super_spreader=1
        else:
            idx_super_spreader = self.SUPERSPREADER_PERC * len(self.infected)
        if len(self.infected) == 1:
            idx_deaths = sys.maxsize
        else:
            idx_deaths = len(self.infected) - (self.DEATH_PERC * len(self.infected))
        
        # Step 5. Disease propagation.
        i = 0
        for x in self.infected:
            # Step 5.1 If the individual belongs to the death part, then die!
            if i >= idx_deaths:
                self.deaths.append(x)
            else:
                # Step 5.2 Determine the number of new infected individuals.
                if i < idx_super_spreader:  # This is the super-spreader!
                    ninfected = self.MIN_SUPERSPREAD + random.randint(0, self.MAX_SUPERSPREAD - self.MIN_SUPERSPREAD)
                else:
                    ninfected = random.randint(0, self.MAX_SPREAD)
                # Step 5.3 Determine whether the individual has traveled
                if random.random() < self.P_TRAVEL:
                    traveler = True
                else:
                    traveler = False
                # Step 5.4 Determine the travel distance, which indicates how many intervals of an individual will be infected.
                if traveler:
                    travel_distance = random.randint(1,self.size/2) 
                else:
                    travel_distance = 1 #The individual has not travel
                # Step 5.5 Infect!!
                for j in range(ninfected):
                    new_infected = x.infect(travel_distance=travel_distance)  # new_infected = infect(x, travel_distance)
                    # Propagate with no social distancing measures
                    if time < self.SOCIAL_DISTANCING:
                        if new_infected not in self.deaths and new_infected not in self.infected and new_infected not in new_infected_list and new_infected not in self.recovered:
                            new_infected_list.append(new_infected)
                        elif new_infected in self.recovered and new_infected not in new_infected_list:
                            if random.random() < self.P_REINFECTION:
                                new_infected_list.append(new_infected)
                                self.recovered.remove(new_infected)
                    elif time < self.VACCINATION: # After SOCIAL_DISTANCING iterations, there is a P_ISOLATION of not being
                        if random.random() > self.P_ISOLATION:
                            if new_infected not in self.deaths and new_infected not in self.infected and new_infected not in new_infected_list and new_infected not in self.recovered:
                                new_infected_list.append(new_infected)
                            elif new_infected in self.recovered and new_infected not in new_infected_list:
                                if random.random() < self.P_REINFECTION:
                                    new_infected_list.append(new_infected)
                                    self.recovered.remove(new_infected)
                        else: # Those saved by social distancing are sent to the recovered list
                            if new_infected not in self.deaths and new_infected not in self.infected and new_infected not in new_infected_list and new_infected not in self.recovered:
                                self.recovered.append(new_infected)
                    else: # After SOCIAL_DISTANCING iterations and VACCINATION iterations
                        if (random.random() > self.P_ISOLATION) and (random.random() > self.vaccinationRate(time)):
                            if new_infected not in self.deaths and new_infected not in self.infected and new_infected not in new_infected_list and new_infected not in self.recovered:
                                new_infected_list.append(new_infected)
                            elif new_infected in self.recovered and new_infected not in new_infected_list:
                                if random.random() < self.P_REINFECTION:
                                    new_infected_list.append(new_infected)
                                    self.recovered.remove(new_infected)
                        else: # Those saved by social distancing or vaccine are sent to the recovered list
                            if new_infected not in self.deaths and new_infected not in self.infected and new_infected not in new_infected_list and new_infected not in self.recovered:
                                self.recovered.append(new_infected)
            i+=1
        # Step 6. Add the current infected individuals to the recovered list.
        self.recovered.extend(self.infected)
        # Step 7. Update the infected list with the new infected individuals.
        self.infected = new_infected_list
    
    
    def run(self):
        epidemic = True
        time = 0
        # Step 1. Infect to Patient Zero
        pz = Individual.random(self.data, self.lim_down, self.lim_up)
        while self.fitness(pz.values) == 0:
            pz = Individual.random(self.data, self.lim_down, self.lim_up)
        self.infected.append(pz)
        print("Patient Zero: " + str(pz) + "\n")
        self.bestSolutions.append(deepcopy(pz))
        # Step 2. The main loop for the disease propagation
        while epidemic and time < self.max_time:
            self.propagateDisease(time)
            print("Iteration ", (time + 1))
            print("Best fitness so far: ",self.fitness(self.bestSolutions[0].values))
            print("Best individual: ", self.bestSolutions[0].kintegers)
            print("Infected: ", str(len(self.infected)), "; Recovered: ", str(len(self.recovered)), "; Deaths: ", str(len(self.deaths)))
            print("Recovered/Infected: " + str("{:.4f}".format(100 * ((len(self.recovered)) / (len(self.infected)+0.01))) + "%"))
            if not self.infected:
                epidemic = False
            time += 1
        return self.bestSolutions
    
    def fitness(self, individual_values):
        support_ant = 0
        support_cons = 0
        support_rule = 0
        # Iterate over instances
        for i in self.data.index:
            verify = [] 
            # For each column of the antecedent of the rule, verify if the value of that instance is in the range given by the individual
            for c in range(len(self.data.columns)-1):
                if (self.data.iloc[i,c] >= individual_values[c*2]) & (self.data.iloc[i,c] <= individual_values[c*2+1]):
                    verify.append(True)
                else:
                    verify.append(False)
            # When verify == True for all the columns, the support of the antecedent of the rule increases by 1
            if all(verify): 
                support_ant += 1
                # If the consequent is in the range given to this function, the rule support increases by 1
                if (self.data.iloc[i,-1] < self.lim_up) & (self.data.iloc[i,-1] > self.lim_down):
                    support_rule += 1
            # For each instance, if the consequent is in the range given to this function, the consequent support increases by 1
            if (self.data.iloc[i,-1] < self.lim_up) & (self.data.iloc[i,-1] > self.lim_down):
                support_cons += 1
        if support_ant !=0:
            conf = support_rule/support_ant # The confidence of the rule
        else:
            conf = 0
        lift = conf*len(self.data.index)/support_cons # The lift metric
        return lift
    
def job(instance):
    instance.run()
    return instance

if __name__ == "__main__":
    instances = [CVOA(max_time = 13, data = data, lim_down = 4.3, lim_up = 6.3, n_solutions=1) for strain in range(10)]
    with mp.Pool(processes=10) as p:
        instances = p.map(job, instances)

    for s, inst in enumerate(instances):
        best_solutions = [solution.kintegers for solution in inst.bestSolutions]
        best_values = [solution.values for solution in inst.bestSolutions]
        best_fitness = [inst.fitness(solution.values) for solution in inst.bestSolutions]
        rule_support = [ruleSupport(data, solution.values, 4.3, 6.3) for solution in inst.bestSolutions]
        print(s)
        print("Best solutions: " + str(best_solutions))
        print("Intervals values: " + str(best_values))
        print("Best fitness: " + str(best_fitness))
        print("Rules support: " + str(rule_support))


