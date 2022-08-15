# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 14:27:33 2022

@author: milth
"""

import numpy as np
#import matplotlib.pyplot as plt
from numpy.random import randint, random
from math import floor
import sqlalchemy
import pandas as pd
from datetime import datetime
from DatabasePreprocessing import schedule_data_processing
    
def new_pop(ranges, num_app):
    population = randint(low=ranges[:, 0], high=ranges[:, 1], size=(num_app))
    return population

def cal_threshold(pop, thres, weight, ranges):
    for chrom in pop:
        while np.sum(weight*chrom) > thres:
            for gen_idx in reversed(range(0, len(chrom))):
                #persentase pengurangannya coba di random biar gk looping forever
                subs = chrom[gen_idx]*(0.09)
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

def mutation(P_mutate, offspring_crossover, num_mutations):
    for chrom in range(offspring_crossover.shape[0]):
        for gen_idx in range(offspring_crossover.shape[1]):
            if random() > P_mutate:
                ## The random value to be added to the gene.
                random_value = randint(low=ranges[gen_idx, 0], high=ranges[gen_idx, 1])
                offspring_crossover[chrom, gen_idx] = random_value
    
    return offspring_crossover

if __name__=='__main__' :
    
    ## Define Mysql Engine
    engine = sqlalchemy.create_engine('mysql+mysqlconnector://root:Ismilelabn209!!@172.23.142.168:3306/db_ismile', pool_pre_ping=True)
    
    # Retrieve data from database 
    billing_data = pd.read_sql_table("billinginput",engine)
    device_data = pd.read_sql_table("deviceinput", engine)
    indexes = list(device_data['user_id'].unique())
    indexes.sort(reverse=False)
    #indexes = [1]
    user_data = []
    for index in indexes:
        User = schedule_data_processing()
        User.get_data(billing_data=billing_data, device_data=device_data, index=index)
        User.preprocessing()
        user_data.append(User)
    
    for user in user_data:
        ##Parameter Inputs
        num_pop = 10
        Tarif = user.Tarif
        Tagihan = user.Tagihan
        Pc = Tagihan/Tarif #Power Cost
        days_left = 30
        
        ##Time Interval Possibilities for each appliance
        #-----------------------------------------------------------------------
        ranges = np.array(user.ranges)
        
        ## Another Initial Variable
        #-----------------------------------------------------------------------
        value = user.value
        Power = user.Power
        
        #calculate necesary input variables
        num_appliances = len(value)
        num_parents_mating = int(num_pop/2)
        pop_size = (num_pop,num_appliances)
        threshold = round(Pc/days_left, 2)
        
        # Intiate first population
        print("Inisialisasi Populasi")
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
        num_generations = 484
        
        for generation in range(num_generations):
            print("Generation         : ", generation)
            # Measuring the fitness of each chromosome in the population.
            fitness = cal_pop_fitness(value, new_population)
            mean_fit = np.sum(fitness)/num_appliances
            energy_con = np.sum(new_population*Power, axis=1) #energy consumption
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
            offspring_crossover = crossover(parents, offspring_size=(pop_size[0]-parents.shape[0], num_appliances), Pcross=0.9)
            offspring_crossover = cal_threshold(offspring_crossover, threshold, Power, ranges)
            print("Crossover")
            print(offspring_crossover)
            
            # Adding some variations to the offspring using mutation.
            offspring_mutation = mutation(0.7, offspring_crossover, num_appliances)
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
        
        # Insert Scheduling Result into Each Instance
        scheduled = best_solution[0,0]
        energy_usage = round(best_energy[~0], 2)
        now_datetime = datetime.now()
        date = now_datetime.strftime('%d-%m-%Y') 
        time = now_datetime.strftime('%H:%M:%S') 
        user.retrieve_data(scheduled=scheduled, energy_usage=energy_usage, energy_threshold=threshold, scheduled_date=date, scheduled_time=time)
        user.database_df()
    
    data_list = []
    for data in user_data:
        data_list.append(data.df)
    database_df = pd.concat(data_list)
    database_df.to_sql(
        name='hasil_penjadwalan', # database table name
        con=engine,
        if_exists='append',
        index=False
    )
    
#    for i in range(len(user_data)):
#        print("----------------------------")
#        user_data[i].Display()
#        print("----------------------------")
