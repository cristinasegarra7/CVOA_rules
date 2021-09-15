import pandas as pd
from cvoa2 import CVOA
import time as time
from rule_support_function import ruleSupport

data = pd.read_csv('earthquake_data.csv', sep = ';')

best_solutions=[]
best_values=[]
best_fitness=[]
rule_support=[]

cvoa = CVOA(max_time = 20, data = data, lim_down = 4.9, lim_up = 6.1 , n_solutions=10)

time1 = int(round(time.time() * 1000))
solutions = cvoa.run() 
time2 = int(round(time.time() * 1000)) - time1

for n in range(len(solutions)):
    best_solutions.append(solutions[n].kintegers)
    best_values.append(solutions[n].values)
    best_fitness.append(cvoa.fitness(solutions[n].values))
    rule_support.append(ruleSupport(data, solutions[n].values, 4.3, 6.3))

print("Execution time: " + str(time2 / 60000) + " mins")
print("Best solutions: " + str(best_solutions))
print("Intervals values: " + str(best_values))
print("Best fitness: " + str(best_fitness))
print("Rules support: " + str(rule_support))
