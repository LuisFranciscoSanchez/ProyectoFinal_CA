import numpy as np
import matplotlib.pyplot as plt

from population import *
from gray2real import *
from fitness import *
from selection import *
from crossover import *
from mutation import *
from newindiv import *

def main():
    #create initial population
    n = 64    #num. of individuals
    c_len = 32 #length of chromosome
    g_len = 8  #length of genes
    pop = population(n,c_len)
    print("initial pop. ", pop)
    #######################################
    print("*** Genetic Algorithm ***")
    print("Population size:\t",n)
    print("Chromosome length:\t",c_len)
    
    bestfits_g = []
    tg = int(input("Cantidad de generaciones: "))
    for g in range(tg):
        #maxgen = int(input("Number of generations: \t"))
        fit = []
        for indiv in pop:
            fit.append(fitness(gray2real(indiv)))
        #print("pop.fitness: ", fit)
        #print("min.fitness: ", np.min(fit))
        #print("max.fitness: ", np.max(fit))
        #print("mean.fitness: ", np.mean(fit))
        #print("std_dev.fitness: ", np.std(fit))
        
        fit_index = selection(fit)
        parent0 = pop[fit_index]
        #print(fit_index)
        #print("parent0: ", parent0)
        
        fit_index = selection(fit)
        parent1 = pop[fit_index]
        
        while parent1 == parent0:
            fit_index = selection(fit)
            parent1 = pop[fit_index]
            
            
        #print(fit_index)
        #print("parent1: ", parent1)
        
        offspring0, offspring1 = crossover(parent0, parent1)
        
        offspring0 = mutation(offspring0)
        offspring1 = mutation(offspring1)
        
        #print ("offspring0: ", offspring0)
        #print ("offspring1: ", offspring1)

        fitp0 = fitness(gray2real(parent0))
        fitp1 = fitness(gray2real(parent1))
        fito0 = fitness(gray2real(offspring0))
        fito1 = fitness(gray2real(offspring1))
         
        #print("fit_par0: ",fitp0)
        #print("fit_par1: ",fitp1)
        #print("fit_off0: ",fito0)
        #print("fit_off1: ",fito1)
        
        newpop = []
        #selection of offseprings/parents
        if fito0 >= fitp0 or fito0 >= fitp1:
            newpop.append(offspring0)
        if fito1 >= fitp0 or fito1 >= fitp1:
            newpop.append(offspring1)
        if fitp0 >= fito0 and fitp0 >= fito1:
            newpop.append(parent0)
        if fitp1 >= fito0 and fitp1 >= fito1:
            newpop.append(parent1)
            
        # include best individual (elitism)
        bestfit = max(fit) # aptitud máxima
        bestfits_g.append(bestfit)
        #print(bestfit)
        bestindex = fit.index(bestfit) # el índice en la lista fit (posición) con la apt.max.
        newpop.append(pop[bestindex])
        #print(newpop)
        
        #extended elitism
        meanfit = np.mean(fit)
        stddevfit = np.std(fit)
        for i in range (len(fit)):
            if fit[i] > meanfit + stddevfit: # 
                newpop.append(pop[i])
        
        #fillers
        while (len(newpop) < n):
           newpop.append(newindiv(c_len))
            
        pop = newpop
    
    
    bestfit = max(fit) # aptitud máxima
    bestindex = fit.index(bestfit) # el índice en la lista fit (posición) con la apt.max.
    sol = gray2real(pop[bestindex])
    solfit = fitness(sol)
#     print(sol)
    
    s = 'W: '+str(abs(round(sol[0]*0.3,5)))+'\tL: '+str(abs(round(sol[1]*0.3,5)))+'\tm: '+str(abs(round(sol[2],5)))+'\tn: '+str(abs(round(sol[3],5)))
    print("Solution: ",s)
        
    plt.figure(1)
    plt.plot(bestfits_g)
    print("Aptitud: ",-solfit)
    print("W/L: ",round(sol[0]/sol[1],2))
#     plt.show()
    
        #Resistor voltage measured/simulated data
    VR_data = [1.00E-07, 2.50E-02, 1.00E-01, 2.25E-01, 4.00E-01, 6.25E-01, \
                9.00E-01, 1.23E+00, 1.57E+00, 1.84E+00, 2.07E+00]
    #gate-to-source voltage sweep  
    VGS = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

    #fixed parameters
    VDS = 5         #drain-to-source voltage  
    VT = 0.69       #treshold voltage (for silicon)
    beta = 4.5e-6   #transistor's beta 
    rsq = 25        #sheet resistance, ohms per square
    gamma = 0.01
    #transistor variables
    W = abs(0.3*sol[0]*1e-6)        #gate width
    L = abs(0.3*sol[1]*1e-6)        #gate length
    print('W: '+str(round(1e6*W,1))+'μm\t'+'L: '+str(round(1e6*L,1))+'μm')
    print("W/L",round(abs(W/L),2))

    #resistor
    m = abs(sol[2])          #resistor squares per line
    n = abs(sol[3])          #resistor lines
    R = (m+1)*n*rsq          # R(rsq, m, n)
    print("R:", R, 'Ω')

    #transistor's drain current I_D (for each V_GS value)
    #resistor voltage V_R = I_D * R
    VR = []
    for i in range(len(VGS)):
        if VGS[i] <= VT:
            ID = 0
        else:
            ID = ((beta/2)*(W/L)*(VGS[i]-VT)**2)*(1+gamma*VDS)
        VR.append(R*ID)

    # mean square error
    MSE = 0
    for i in range(len(VGS)):
        MSE += (VR[i]-VR_data[i])**2    
    MSE = (1/len(VGS))*MSE

    print("mean sq error: ", round(MSE, 7))

    plt.figure(2)
    plt.plot(VGS,VR_data)
    plt.plot(VGS,VR)
    plt.grid()
    plt.legend(['data','calculated'])
    plt.title('$V_R$ vs $V_{GS}$')
    plt.ylabel('resistor voltage (V)')
    plt.xlabel('gate-to-source voltage (V)')

    plt.show()

            
main()
