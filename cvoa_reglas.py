import pandas as pd
from cvoa2 import CVOA
import time as time
from rule_support_function import ruleSupport

data = pd.read_csv('terremotos_data.csv', sep = ';')
"""
best_solutions=[]
best_values=[]
best_fitness=[]
rule_support=[]

for i in range(10):
    # lim_down y lim_up son los límetes del intervalo del consecunte (no inclusive)
    cvoa = CVOA(max_time = 20, data = data, lim_down = 4.9, lim_up = 6.1, n_solutions=1)
    #time1 = int(round(time.time() * 1000))
    print("Bucle" + str(i))
    solution = cvoa.run()
    #time2 = int(round(time.time() * 1000)) - time1
    best_solutions.append(solution[0].kintegers)
    best_values.append(solution[0].values)
    best_fitness.append(cvoa.fitness(solution[0].values))
    rule_support.append(ruleSupport(data, solution[0].values, 4.9, 6.1))
    
print(best_solutions)
print(best_values)
print(best_fitness)
print(rule_support)
"""
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
print("Best solution values: " + str(best_values))
print("Best fitness: " + str(best_fitness))
print(rule_support)
print(len(best_values ))


"""
print("Best solution: " + str(solution))
print("Best solution values: " + str(solution.values))
print("Best fitness: " + str(cvoa.fitness(solution.values)))
print("Execution time: " + str(time2 / 60000) + " mins")
"""
