# Función soporte regla

def ruleSupport(data, individual_values, lim_down, lim_up):
    support_ant = 0
    support_cons = 0
    support_rule = 0
    # Iterate over instances
    for i in data.index:
        verify = [] 
        # For each column of the antecedent of the rule, verify if the value of that instance is in the range given by the individual
        for c in range(len(data.columns)-1):
            if (data.iloc[i,c] >= individual_values[c*2]) & (data.iloc[i,c] <= individual_values[c*2+1]):
                verify.append(True)
            else:
                verify.append(False)
        # When verify == True for all the columns, the support of the antecedent of the rule increases by 1
        if all(verify): 
            support_ant += 1
            # If the consequent is in the range given to this function, the rule support increases by 1
            if (data.iloc[i,-1] < lim_up) & (data.iloc[i,-1] > lim_down):
                support_rule += 1
    return support_rule

