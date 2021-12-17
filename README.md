# CVOA_rules_vaccine
Optimization algorithm based on the coronavirus for numerical association rules mining

Here you have the implementation of CVOA for numerical association rules. You can run one or several strains. The lower and upper limits of the consequent of the rule are CVOA parameters that must be specified. As well as the number of solutions returned by the algorithm.

To run one strain of cvoa, open de fail "main_cvoa.py". Load the data. Now is being used earthquake data from Spain. Set the CVOA parameters as you like and run.

To run several strains use the file "cvoa_multiprocessing.py". Assign the number of strains you want to simulate to the length of the "strain" list and to the number of processes.
