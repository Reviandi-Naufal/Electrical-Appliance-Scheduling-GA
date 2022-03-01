# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 13:14:59 2021

@author: milth
"""

import numpy as np
from numpy.random import randint, random

def new_pop(ranges, num_app):
    population = randint(low=ranges[:, 0], high=ranges[:, 1], size=(num_app))
    return population

def cal_threshold(pop, thres, weight):
    for chrom in pop:
        for gen_idx in range(len(chrom)-1):
            if np.sum(weight*chrom) > thres:
                chrom[~gen_idx]=0
            else:
                pass
    return pop

def cal_pop_fitness(equation_inputs, pop):
    # Calculating the fitness value of each solution in the current population.
    # The fitness function calulates the sum of products between each input and its corresponding weight.
    fitness = np.sum(pop*equation_inputs, axis=1)
    return fitness
    

def select_mating_pool(pop, fitness, num_parents):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    parents = np.empty((num_parents, pop.shape[1]))
    for parent_num in range(num_parents):
        max_fitness_idx = np.where(fitness == np.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_num, :] = pop[max_fitness_idx, :]
        fitness[max_fitness_idx] = -9999
    return parents

def crossover(pop, Pcross):
    # The point at which crossover takes place between two parents picked at random
    for i in range(len(pop)):
        if random()>0.4:
            fp = randint(0,len(pop)-1)
            mp = randint(0,len(pop)-1)
            c_point = randint(1,len(pop)-1)
    
            if fp != mp:
                pop[fp][c_point:],pop[mp][c_point:] = pop[mp][c_point:],pop[fp][c_point:]
                
    return pop

def mutation(P_mutate, pop, ranges):
    # Mutation changes a number of genes pick in random. The changes are random too.
    for i in range(len(pop)):
        if random() > 0.4:
            x = randint(0,len(pop)-1)
            y = randint(0,len(pop)-1)
            #pick the gen x,y in pop to be mutate
            pop[x][y] = randint(low=ranges[y, 0], high=ranges[y, 1])
            # pop[x][y] = randint(low=1, high=25)
            
            
    return pop

if __name__=='__main__' :

    ## Parameter Inputs
    # num = 6
    ranges = np.array([[10,25], [8,23], [6,21], [4,19], [2,17], [1,15]]) 
    value = [600,500,400,300,200,100]
    Power = [0.1, 0.007, 0.035, 0.3, 0.015, 0.015]
    num_parents_mating = int(len(Power)/2)
    Pc = 185.12
    days_left = 30
    
    #calculate necesary input variables
    num_appliances = len(value)
    pop_size = (num_appliances,num_appliances)
    threshold = round(Pc/days_left, 2)
    # threshold = round(Pc/days_left)
    
    # Intial population
    new_population = new_pop(ranges, pop_size)
    # new_population = np.random.randint(low=1, high=25, size=(num, num_weights)
    print(new_population)
    
    best_outputs = []
    mean_outputs = []
    num_generations = 300
    for generation in range(num_generations):
        print("Generation         : ", generation)
        # Measuring the fitness of each chromosome in the population.
        fitness = cal_pop_fitness(value, new_population)
        mean_fit = np.sum(fitness)/num_appliances
        energy_con = np.sum(new_population*Power, axis=1)
        print("Fitness                  : {}".format(fitness))
        print("Mean Fitness             : {}".format(int(mean_fit)))
        print("Energy Consumption       : {}".format(energy_con))
        
        best_outputs.append(np.max(fitness))
        mean_outputs.append(mean_fit)
        best_idx = np.where(fitness == np.max(fitness))
        # The best result in the current iteration.
        print("Best Fitness             : ", best_outputs[~0])
        print("Best Fitness energy usage: ",energy_con[best_idx])
        
        # Selecting the best parents in the population for mating.
        parents = select_mating_pool(new_population, fitness, 
                                          num_parents_mating)
        print("Parents")
        print(parents)
        
           # Generating next generation using crossover.
        offspring_crossover = crossover(parents, Pcross=0.6)
        offspring_crossover = cal_threshold(offspring_crossover, threshold, Power)
        print("Crossover")
        print(offspring_crossover)
        
        # Adding some variations to the offspring using mutation.
        offspring_mutation = mutation(0.3, offspring_crossover, ranges)
        offspring_mutation = cal_threshold(offspring_mutation, threshold, Power)
        print("Mutation")
        print(offspring_mutation)
        
        new_population[0:parents.shape[0], :] = offspring_mutation
        new_population[parents.shape[0]:, :] = parents
        print("New Population")
        print(new_population)
        print("--------------------------------------------------------------")
        
        
    # Getting the best solution after iterating finishing all generations.
    #At first, the fitness is calculated for each solution in the final generation.
    fitness = cal_pop_fitness(value, new_population)
    mean_fit = np.sum(fitness)/num_appliances
    energy_con = np.sum(new_population*Power, axis=1)
    best_outputs.append(np.max(fitness))
    mean_outputs.append(mean_fit)
    # Then return the index of that solution corresponding to the best fitness.
    best_match_idx = np.where(fitness == np.max(fitness))
    
    print("===============================================================================")
    print("Best solution : ", new_population[best_match_idx, :])
    print("Best solution fitness : ", fitness[best_match_idx])
    print("Best solution energy usage: ",energy_con[best_match_idx])
    print("Threshold: {}".format(threshold))
    
    import matplotlib.pyplot
    matplotlib.pyplot.plot(best_outputs, label='Max')
    matplotlib.pyplot.plot(mean_outputs, label='Mean')
    matplotlib.pyplot.xlabel("Iteration")
    matplotlib.pyplot.ylabel("Fitness")
    matplotlib.pyplot.legend()
    matplotlib.pyplot.show()
