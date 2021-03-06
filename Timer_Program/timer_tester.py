# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 13:14:59 2021

@author: milth
"""

import numpy as np
import matplotlib.pyplot as plt
from numpy.random import randint, random
from time import monotonic, sleep
prog_start = monotonic()

def new_pop(ranges, num_app):
    population = randint(low=ranges[:, 0], high=ranges[:, 1], size=(num_app))
    return population

def cal_threshold(pop, thres, weight):
    for chrom in pop:
        for gen_idx in range(len(chrom)):
            if np.sum(weight*chrom) > thres:
                chrom[~gen_idx]=0
            else:
                break
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

def crossover(pop, offspring_size, Pcross):
    offspring = np.empty(offspring_size)
    # The point at which crossover takes place between two parents. Usually, it is at the center.
    # crossover_point = np.uint8(offspring_size[1]/2)
    crossover_point = np.uint8(randint(1,len(pop)))
                
    while random() > Pcross:     
        for k in range(offspring_size[0]):
            # Index of the first parent to mate.
            parent1_idx = k%parents.shape[0]
            # Index of the second parent to mate.
            parent2_idx = (k+1)%parents.shape[0]
            # The new offspring will have its first half of its genes taken from the first parent.
            offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
            # The new offspring will have its second half of its genes taken from the second parent.
            offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    return offspring

    # for i in range(len(pop)):
    #     if random()>Pcross:
    #         fp = randint(0,len(pop)-1)
    #         mp = randint(0,len(pop)-1)
    #         c_point = randint(1,len(pop)-1)
    
    #         if fp != mp:
    #             pop[fp][c_point:],pop[mp][c_point:] = pop[mp][c_point:],pop[fp][c_point:]
    # return pop

def mutation(P_mutate, offspring_crossover, num_mutations=12):
    # mutations_counter = np.uint8(offspring_crossover.shape[1] / num_mutations)
       
    # for idx in range(offspring_crossover.shape[0]):
    #     if random() > P_mutate:
    #         gene_idx = mutations_counter - 1
    #         for mutation_num in range(num_mutations):
    #             # The random value to be added to the gene.
    #             # random_value = randint(1, 25)
    #             random_value = randint(low=ranges[gene_idx, 0], high=ranges[gene_idx, 1])
    #             offspring_crossover[idx, gene_idx] = random_value
    #             gene_idx = gene_idx + mutations_counter
                
    for chrom in range(offspring_crossover.shape[0]):
        for gen_idx in range(offspring_crossover.shape[1]):
            if random() > P_mutate:
                # The random value to be added to the gene.
                # random_value = randint(1, 25)
                random_value = randint(low=ranges[gen_idx, 0], high=ranges[gen_idx, 1])
                offspring_crossover[chrom, gen_idx] = random_value
    
    return offspring_crossover

class Device():
    
    def __init__(self, name, clock):
        self.name = name
        # self.clock = clock*3600 #convert time in hours to seconds
        self.clock = clock
        self.state = 1
        
    def get_name(self):
        return self.name
    
    def get_time(self):
        return self.clock
    
    def get_state(self):
        return self.state
    
    def set_state(self, state):
        self.state = state

if __name__=='__main__' :

    # Parameter Inputs
    # num = 6
    ranges = np.array([[10,25], [8,23], [6,21], [4,19], [2,17], [1,15]])
    # ranges = np.array([[21,25], [17,21], [13,17], [9,13], [5,9], [1,5]])
    value = [600, 500, 400, 300, 200, 100]
    Power = [0.1, 0.007, 0.035, 0.3, 0.015, 0.015]
    num_parents_mating = int(len(Power)/2)
    Pc = 189
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
    num_generations = 50
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
        offspring_crossover = crossover(parents, offspring_size=(pop_size[0]-parents.shape[0], num_appliances), Pcross=0.4)
        offspring_crossover = cal_threshold(offspring_crossover, threshold, Power)
        print("Crossover")
        print(offspring_crossover)
        
        # Adding some variations to the offspring using mutation.
        offspring_mutation = mutation(0.3, offspring_crossover, num_appliances)
        offspring_mutation = cal_threshold(offspring_mutation, threshold, Power)
        print("Mutation")
        print(offspring_mutation)
        
        new_population[0:parents.shape[0], :] = parents
        new_population[parents.shape[0]:, :] = offspring_mutation
        print("New Population")
        print(new_population)
        print("--------------------------------------------------------------")
    # Getting the best solution after iterating finishing all generations.
    #At first, the fitness is calculated for each solution in the final generation.
    fitness = cal_pop_fitness(value, new_population)
    energy_con = np.sum(new_population*Power, axis=1)
    print("Fitness     : {}".format(fitness))
    print("Energy Consumption       : {}".format(energy_con))
    cal_threshold(new_population, threshold, Power)
    fitness = cal_pop_fitness(value, new_population)
    mean_fit = np.sum(fitness)/num_appliances
    
    best_outputs.append(np.max(fitness))
    mean_outputs.append(mean_fit)
    # Then return the index of that solution corresponding to the best fitness.
    best_match_idx = np.where(fitness == np.max(fitness))
    best_solution = new_population[best_match_idx, :]
    
    print("===============================================================================")
    print("Fitness     : {}".format(fitness))
    print("Best solution : ", best_solution)
    print("Best solution fitness : ", fitness[best_match_idx])
    print("Best solution energy usage: ",energy_con[best_match_idx])
    print("Threshold: {}".format(threshold))
    
    plt.plot(best_outputs, label='Max')
    plt.plot(mean_outputs, label='Mean')
    plt.xlabel("Iteration")
    plt.ylabel("Fitness")
    plt.legend()
    plt.show()
    
    schedule = list(best_solution[0,0])
    print(schedule)
    
    D_1 = Device('Device-1', schedule[0])
    D_2 = Device('Device-2', schedule[1])
    D_3 = Device('Device-3', schedule[2])
    D_4 = Device('Device-4', schedule[3])
    D_5 = Device('Device-5', schedule[4])
    D_6 = Device('Device-6', schedule[5])
    print("===============================================================================")
    print()
    # print(D_2.get_name(), end=' ')
    # print(D_2.get_time())
    # print(D_2.get_state())
    
    """ The Energy Management System Start From Here """
    startSys = monotonic()
    
    if D_1.get_time() !=0:
        D_1.set_state(0)
        
    elif D_2.get_time() !=0:
        D_2.set_state(0)
        
    elif D_3.get_time() !=0:
        D_3.set_state(0)
        
    elif D_4.get_time() !=0:
        D_4.set_state(0)
        
    elif D_5.get_time() !=0:    
        D_5.set_state((0))
        
    elif D_6.get_time() !=0:
        D_6.set_state(0)
    print()
    print()
    print("SYSTEM ARE ON")
    print("========================================================================")

    while True:
        endSys = monotonic()
        
        if round(endSys - startSys) == D_1.get_time()-3:
            print(D_1.get_name(), "has 3 hour left to operate")
        
        if round(endSys - startSys) == D_2.get_time()-2:
            print(D_2.get_name(), "has 2 hour left to operate")
            
        elif round(endSys - startSys) == D_3.get_time()-1:
            print(D_3.get_name(), "has 1 hour left to operate")
            
        elif round(endSys - startSys) == D_6.get_time():
            D_6.set_state(1)
            print(D_6.get_name(), "is OFF")
            
        elif round(endSys - startSys) == D_5.get_time():
            D_5.set_state(1)
            print(D_5.get_name(), "is OFF")
            
        elif round(endSys - startSys) == D_4.get_time():
            D_4.set_state(1)
            print(D_4.get_name(), "is OFF")
            
        elif round(endSys - startSys) == D_3.get_time()+2:
            D_3.set_state(1)
            print(D_3.get_name(), "is OFF")
            
        elif round(endSys - startSys) == D_2.get_time()+4:
            D_2.set_state(1)
            print(D_2.get_name(), "is OFF")
            
        elif round(endSys - startSys) == D_1.get_time()*2:
            D_1.set_state(1)
            print(D_1.get_name(), "is OFF")
            
        elif D_1.get_state() and D_2.get_state() and D_3.get_state() and D_4.get_state() and D_5.get_state() and D_6.get_state():
            break
        
        # print(round(endSys - startSys))
        sleep(1)
    
    print("========================================================================")
    print("ALl system has been shutdown")
    
    prog_end = monotonic()
    # print("The code has run for {} seconds".format(prog_end-prog_start))
       
