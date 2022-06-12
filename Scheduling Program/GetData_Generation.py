# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 13:14:59 2021

@author: milth
"""
import numpy as np
#import matplotlib.pyplot as plt
from numpy.random import randint, random
import pandas as pd
from math import floor

num_test = 1000
columns_10 = ['Device_1', 'Device_2', 'Device_3', 'Device_4', 'Device_5', 'Device_6', 'Device_7',  
           'Device_8', 'Device_9', 'Device_10','Start_Max_Fit', 'End_Max_Fit', 'Diff_MaF', 
           'Start_Mean_Fit', 'End_Mean_Fit','Diff_MeF', 'E_Usage','Thres']

columns_20 = ['Device_1', 'Device_2', 'Device_3', 'Device_4', 'Device_5', 'Device_6', 'Device_7',  
           'Device_8', 'Device_9', 'Device_10','Device_11','Device_12', 'Device_13', 'Device_14', 
           'Device_15', 'Device_16', 'Device_17', 'Device_18', 'Device_19', 'Device_20','Start_Max_Fit', 'End_Max_Fit', 'Diff_MaF', 
           'Start_Mean_Fit', 'End_Mean_Fit','Diff_MeF', 'E_Usage','Thres']
#df = pd.DataFrame(columns=columns, index=range(num_test))

ranges_10 = np.array([[20,25], [20,25], [15,20], [15,20], [10,15], [10,15], [5,10], [5,10], [1,5], [1,5]])
value_10 = [500, 500, 400, 400, 300, 300, 200, 200, 100, 100]
Power_10 = [0.6, 0.3, 0.45, 0.011, 0.27, 0.35, 0.08, 0.35, 0.195, 0.04]

ranges_20 = np.array([[20,25], [20,25], [15,20], [15,20], [10,15], [10,15], [5,10], [5,10], [1,5], [1,5],[1,5], [1,5], [1,5], [1,5], [1,5], [1,5], [1,5], [1,5], [1,5], [1,5]])
value_20 = [500, 500, 400, 400, 300, 300, 200, 200, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
Power_20 = [0.6, 0.3, 0.45, 0.011, 0.27, 0.35, 0.08, 0.35, 0.195, 0.04, 0.4, 0.5, 0.32, 0.23, 0.32, 0.25, 0.37, 0.05, 0.15, 0.125]

devices = [10]
#gen_list_10 = [110, 123, 126, 130, 133, 155, 158, 195, 402, 419, 422, 433, 438, 444, 482, 488, 495]
#gen_list_20 = [223, 236, 247, 250, 254, 262, 265, 275, 280, 289, 295, 299, 417, 423, 433, 435, 444, 463, 484, 485]
gen_list_10 = [484]
gen_list_20 = [223, 236, 247, 250, 254, 262, 265, 275, 280, 289, 295, 299, 417, 423, 433, 435, 444, 463, 484, 485]

for device in devices:
    if device == 10 :
        ranges = ranges_10
        value = value_10
        Power = Power_10
        gen_list = gen_list_10
        df = pd.DataFrame(columns=columns_10, index=range(num_test))
    elif device == 20:
        ranges = ranges_20
        value = value_20
        Power = Power_20
        gen_list = gen_list_20
        df = pd.DataFrame(columns=columns_20, index=range(num_test))
    for gen in gen_list:
        for test in range(num_test):
            
            def new_pop(ranges, num_app):
                population = randint(low=ranges[:, 0], high=ranges[:, 1], size=(num_app))
                return population
    
            def cal_threshold(pop, thres, weight, ranges):
                for chrom in pop:
                    while np.sum(weight*chrom) > thres:
                        for gen_idx in reversed(range(0, len(chrom))):
                            #persentase pengurangannya coba di random biar gk looping forever
                            subs = chrom[gen_idx]*(0.2)
                            result = floor(chrom[gen_idx] - subs)
                            if result >= 0:
                                chrom[gen_idx] = result
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
                offspring = np.zeros(offspring_size)
                num = len(pop)-1
                crossover_point = np.uint8(randint(1,num))
                            
                while True:
                    for k in range(offspring_size[0]):
                        # Index of the first parent to mate.
                        parent1_idx = k%parents.shape[0]
                        # Index of the second parent to mate.
                        parent2_idx = (k+1)%parents.shape[0]
                        # The new offspring will have its first half of its genes taken from the first parent.
                        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
                        # The new offspring will have its second half of its genes taken from the second parent.
                        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
                    if random() < Pcross:
                        break
                return offspring
    
                # for i in range(len(pop)):
                #     if random()>Pcross:
                #         fp = randint(0,len(pop)-1)
                #         mp = randint(0,len(pop)-1)
                #         c_point = randint(1,len(pop)-1)
                
                #         if fp != mp:
                #             pop[fp][c_point:],pop[mp][c_point:] = pop[mp][c_point:],pop[fp][c_point:]
                # return pop
    
            def mutation(P_mutate, offspring_crossover, num_mutations):
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
                            ## The random value to be added to the gene.
                            random_value = randint(low=ranges[gen_idx, 0], high=ranges[gen_idx, 1])
                            offspring_crossover[chrom, gen_idx] = random_value
                
                return offspring_crossover
    
            if __name__=='__main__' :
    
                ##Parameter Inputs
                num_pop = 10
                ##Time Interval Possibilities for each appliance
                #-----------------------------------------------------------------------
                #ranges = np.array([[10,25], [8,23], [6,21], [4,19], [2,17], [1,15]])
                #ranges = np.array([[20,25], [16,21], [12,17], [8,13], [4,9], [1,5]])
                ##ranges = np.array([[20,25], [20,25], [15,20], [15,20], [10,15], [10,15], [5,10], [5,10], [1,5], [1,5]])
                #ranges = np.array([[16,25], [16,25], [16,25], [8,16], [8,16], [8,16], [1,8], [1,8], [1,8], [1,8]])
                ##ranges = np.array([[20,25], [20,25], [15,20], [15,20], [10,15], [10,15], [5,10], [5,10], [1,5], [1,5],[1,5], [1,5], [1,5], [1,5], [1,5], [1,5], [1,5], [1,5], [1,5], [1,5]])
                #-----------------------------------------------------------------------
                #value = [300, 300, 300, 200, 200, 200, 100, 100, 100, 100]
                ##value = [500, 400, 400, 300, 300, 300, 200, 200, 100, 100]
                ##Power = [0.6, 0.3, 0.45, 0.011, 0.27, 0.35, 0.08, 0.35, 0.195, 0.04]
                #value = [105, 100, 95, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10]
                ##value = [500, 400, 400, 300, 300, 300, 200, 200, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
                ##Power = [0.6, 0.3, 0.45, 0.011, 0.27, 0.35, 0.08, 0.35, 0.195, 0.04, 0.4, 0.5, 0.32, 0.23, 0.32, 0.25, 0.37, 0.05, 0.15, 0.125]
                Tarif = 1444.7
                Tagihan = 1800000
                Pc = Tagihan/Tarif
                days_left = 30
                
                #calculate necesary input variables
                num_appliances = len(value)
                #num_pop = len(value)
                num_parents_mating = int(num_pop/2)
                pop_size = (num_pop,num_appliances)
                threshold = round(Pc/days_left, 2)
                # threshold = round(Pc/days_left)
                
                # Intial population
                new_population = new_pop(ranges, pop_size)
                """for pop in new_population:
                    for i in range(len(pop)):
                        if Power[i] == 0:
                            pop[i] = 0
                """
                print(new_population)
                
                best_fitness = []
                mean_fitness = []
                best_energy = []
                num_generations = gen
                for generation in range(num_generations):
                    print("Generation         : ", generation)
                    # Measuring the fitness of each chromosome in the population.
                    fitness = cal_pop_fitness(value, new_population)
                    mean_fit = np.sum(fitness)/num_appliances
                    energy_con = np.sum(new_population*Power, axis=1)
                    print("Fitness                  : {}".format(fitness))
                    print("Mean Fitness             : {}".format(int(mean_fit)))
                    print("Energy Consumption       : {}".format(energy_con))
                    
                    best_fitness.append(np.max(fitness))
                    mean_fitness.append(mean_fit)
                    best_match_idx = np.where(fitness == np.max(fitness))
                    energy_list = energy_con[best_match_idx]
                    best_energy.append(np.max(energy_list))
                    # The best result in the current iteration.
                    print("Best Fitness             : ", best_fitness[~0])
                    print("Best Fitness energy usage: ", best_energy[~0])
                    
                    # Selecting the best parents in the population for mating.
                    parents = select_mating_pool(new_population, fitness, 
                                                      num_parents_mating)
                    print("Parents")
                    print(parents)
                    
                       # Generating next generation using crossover.
                    offspring_crossover = crossover(parents, offspring_size=([pop_size[0]-parents.shape[0], num_appliances]), Pcross=0.4)
                    offspring_crossover = cal_threshold(offspring_crossover, threshold, Power, ranges)
                    print("Crossover")
                    print(offspring_crossover)
                    
                    # Adding some variations to the offspring using mutation.
                    offspring_mutation = mutation(0.4, offspring_crossover, num_appliances)
                    offspring_mutation = cal_threshold(offspring_mutation, threshold, Power, ranges)
                    print("Mutation")
                    print(offspring_mutation)
                    
                    new_population[0:parents.shape[0], :] = parents
                    new_population[parents.shape[0]:, :] = offspring_mutation
                    """for pop in new_population:
                        for i in range(len(pop)):
                            if Power[i] == 0:
                                pop[i] = 0
                    """
                    new_population = cal_threshold(new_population, threshold, Power, ranges)
                    print("New Population")
                    print(new_population)
                    print("--------------------------------------------------------------")
                
                # Getting the best solution after iterating all generations.
                #At first, the fitness is calculated for each solution in the final generation.
                fitness = cal_pop_fitness(value, new_population)
                energy_con = np.sum(new_population*Power, axis=1)
                print("Fitness              : {}".format(fitness))
                print("Energy Consumption   : {}".format(energy_con))
                #-------------------------------------------------------------------------------------------
                fitness = cal_pop_fitness(value, new_population)
                mean_fit = np.sum(fitness)/num_appliances
                
                best_fitness.append(np.max(fitness))
                mean_fitness.append(mean_fit)
                best_match_idx = np.where(fitness == np.max(fitness))
                energy_list = energy_con[best_match_idx]
                best_energy.append(np.max(energy_list))
                best_solution = new_population[best_match_idx, :]
                
                print("===============================================================================")
                print("Fitness     : {}".format(fitness))
                print("Best solution : ", best_solution)
                print("Best solution fitness : ", best_fitness[~0])
                print("Best solution energy usage: ", round(best_energy[~0], 2))
                print("Threshold: {}".format(threshold))
                
                sol_data = list(best_solution[0,0])
                print(sol_data)
                
                if device == 10:
                    for datum in range(len(sol_data)):
                        df.iloc[test,datum] = sol_data[datum]
                    df.iloc[test, 10] = best_fitness[0]
                    df.iloc[test, 11] = best_fitness[~0]
                    df.iloc[test, 12] = best_fitness[~0]-best_fitness[0] 
                    df.iloc[test, 13] = mean_fitness[0]
                    df.iloc[test, 14] = mean_fitness[~0]
                    df.iloc[test, 15] = mean_fitness[~0]-mean_fitness[0]
                    df.iloc[test, 16] = round(best_energy[~0], 2)
                    df.iloc[test, 17] = threshold
                
                elif device == 20:
                    for datum in range(len(sol_data)):
                        df.iloc[test,datum] = sol_data[datum]
                    df.iloc[test, 20] = best_fitness[0]
                    df.iloc[test, 21] = best_fitness[~0]
                    df.iloc[test, 22] = best_fitness[~0]-best_fitness[0] 
                    df.iloc[test, 23] = mean_fitness[0]
                    df.iloc[test, 24] = mean_fitness[~0]
                    df.iloc[test, 25] = mean_fitness[~0]-mean_fitness[0]
                    df.iloc[test, 26] = round(best_energy[~0], 2)
                    df.iloc[test, 27] = threshold
                
                #plt.plot(best_fitness, label='Max')
                #plt.plot(mean_fitness, label='Mean')
                #plt.xlabel("Iteration")
                #plt.ylabel("Fitness")
                #plt.legend()
                #plt.show()
                
        #df.to_csv(f"Test Result/Epoch277_{device}Device_Pm_{p_mut}_WithCategory.csv")
        #df.to_excel(f"Test Result/Epoch277_{device}Device_Pm_{p_mut}_WithCategory.xlsx")
        
        df.to_csv(f"Test Result/Epoch{gen}_{device}Device_WithCategory.csv")
        df.to_excel(f"Test Result/Epoch{gen}_{device}Device_WithCategory.xlsx")