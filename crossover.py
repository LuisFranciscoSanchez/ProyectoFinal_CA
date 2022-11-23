import random

def crossover(parent0,parent1):
    if random.random() < 0.7:
        cut = random.randint(0,len(parent0)-1)
        #print ("cut: ", cut)
        offspring0 = []
        offspring1 = []
        for i in range(len(parent0)):
            if i <= cut:
                offspring0.append(parent0[i])
                offspring1.append(parent1[i])
            else:
                offspring0.append(parent1[i])
                offspring1.append(parent0[i])
    else:
        #print ("no crossover")
        offspring0 = parent0
        offspring1 = parent1
                
    
    return offspring0, offspring1