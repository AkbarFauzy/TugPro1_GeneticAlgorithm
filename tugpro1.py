# -*- coding: utf-8 -*-
"""Tugpro1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LDpKLJkt3qJmYAGfNoeIZDVCSYLJNPxn
"""

import random
import math

"""

---
Variabel Global


---
"""

#batasan -1 ≤ x ≤2 dan -1 ≤ y ≤1
x = [-1, 2]
y = [-1, 1]

CONST_POPULATIONSIZE =50 #Banyaknya Individual di Populasi
CONST_CHROMOSOMESIZE = 10 #Banyaknya Genes di Chromosome
CONST_MUTATIONRATE = 0.05 #Propabilitas Mutasi
CONST_CROSSOVERRATE = 0.8 #Propabilitas Cross Over
CONST_GENERATIONLIMIT = 50 #Limit Generasi

"""

---
Pendefinisian Class


---


"""

# Kelas Individual
class Individual:
  def __init__(self, _chromosome):
    self.chromosome = _chromosome
    self.fitness = self.CalculateFitness(_chromosome.x1, _chromosome.x2)
   
    # Menghitung Fitness
  def CalculateFitness(self,x,y):
    return (x**2) * math.sin(y**2) + (x+y)

# Kelas Kromosom
class Chromosome:
  def __init__(self, _gen):
    self.gen = _gen
    self.x1 = self.decode(x[1],x[0], _gen[:len(_gen)//2]) 
    self.x2 = self.decode(y[1],y[0], _gen[len(_gen)//2:])
  
  # Fungsi Decode
  def decode(self, ra, rb, g):
    sum1 = 0
    sum2 = 0
    
    for i in range(len(g)):
      sum1 += 9*(1/pow(10,i+1))
    for i in range(len(g)):
      sum2 += g[i]*(1/pow(10,i+1))
    
    return rb+((ra-rb)/sum1)*sum2

"""

---
Generate Chromosome


---


"""

def GenerateChromosome():
  gen = []
  for i in range(CONST_CHROMOSOMESIZE):
    gen.append(random.randint(0,9))
  return Chromosome(gen)

"""

---
Generate Population


---


"""

def GeneratePopulation():
  population = []
  for i in range(CONST_POPULATIONSIZE):
    individual = Individual(GenerateChromosome())
    population.append(individual)
  
  return population

"""

---
Parent Selection (Roulette Wheel)


---

"""

def ParentSelection(population, weight,rate):
  parents = []
  for i in range(2):
    r = random.uniform(0,weight)
    for j in range(CONST_POPULATIONSIZE):
      if rate[j] > r:
        parents.append(population[j].chromosome.gen)
      if len(parents) == 2:
        return parents[i-1], parents[i]  
        
  print("returning null")
  return null

"""

---
Rekombinasi

---





"""

# 1-point Crossover
def Crossover(parent1, parent2):
  r = random.uniform(0,1)
  if r <= CONST_CROSSOVERRATE:
    r = random.randint(0,CONST_CHROMOSOMESIZE-1)
    child1 = parent1[:r] + parent2[r:]
    child2 = parent2[:r] + parent1[r:]
    return child1, child2
  return parent1, parent2

"""

---

Mutasi

---

"""

# Mutasi memilih nilai secara acak
def Mutation(gen):
  r = random.uniform(0,1)
  if r <= CONST_MUTATIONRATE:
    r = random.randint(0,CONST_CHROMOSOMESIZE-1)
    mutated_gen = random.randint(0,9)
    while mutated_gen == gen[r]:
      mutated_gen = random.randint(0,9)
    gen[r] = mutated_gen
  return gen

"""

---
Seleksi Survivor

---


"""

# Seleksi Survivor
def GetFitness(individual):
  return individual.fitness

def NextGen(population):
  #Memilih 2 fitness terbesar
  population.sort(key = GetFitness, reverse = True)
  newPopulation = population[0:2]

  #Membuat Roulette Wheel
  fitness_sum = 0
  partial_sum = []
  normalize_fitness = []
  # Total Fitness
  for i in range(CONST_POPULATIONSIZE):
    fitness_sum += population[i].fitness
  # Normalize Fitness
  for i in range(CONST_POPULATIONSIZE):
    normalize_fitness.append(population[i].fitness / fitness_sum)
  # Total Normalize Fitness
  fitness_sum = 0
  for i in range(CONST_POPULATIONSIZE):
    fitness_sum += normalize_fitness[i]
    partial_sum.append(fitness_sum)

  #Mating Pool
  for i in range((CONST_POPULATIONSIZE//2)-1):
    # Memilih Parent
    parent1, parent2 = ParentSelection(population,fitness_sum, partial_sum)
    # Crossover Parent
    offspring1, offspring2 = Crossover(parent1,parent2) # Returning Chromosome
    # New Individual based on Child
    newIndividual1 = Individual(Chromosome(Mutation(offspring1)))
    newIndividual2 = Individual(Chromosome(Mutation(offspring2)))
    
    newPopulation.append(newIndividual1)
    newPopulation.append(newIndividual2)
  return newPopulation

"""

---

Best Individual

---



"""

def GetBestIndividual(population):
  bestfitness = 0
  for i in range(CONST_POPULATIONSIZE):
    if bestfitness < population[i].fitness:
      bestfitness = population[i].fitness
      bestfitnessindex = i
  return population[bestfitnessindex]

"""

---
MAIN PROGRAM


---


"""

#print("Jumlah Populasi :" ,CONST_POPULATIONSIZE)
#print("Propabilitas CrossOver :" ,CONST_CROSSOVERRATE)
#print("Propabilitas Mutasi :" ,CONST_MUTATIONRATE)
population = GeneratePopulation()
best_individual_overall = population[0]
for generasi in range(CONST_GENERATIONLIMIT):
  print("=================================================================================================================================================================================")
  print("\t\t\t\t\t\t\t\t\t\tGenerasi = ", generasi)
  print("=================================================================================================================================================================================")
  # Output Individual
  for i in range(CONST_POPULATIONSIZE):
    print("Chromosome : ", population[i].chromosome.gen,"\t\t| X1 : ",population[i].chromosome.x1, " \t\t\t| X2 :", population[i].chromosome.x2, "\t\t | Fitness = ", population[i].fitness)
  print("=================================================================================================================================================================================")
  best_individual_in_generation = GetBestIndividual(population)
  print("Best Individual : ",best_individual_in_generation.chromosome.gen,"\t\tx: ", best_individual_in_generation.chromosome.x1,"\t\ty: ", best_individual_in_generation.chromosome.x2," \nFitness : ",best_individual_in_generation.fitness)
  print("=================================================================================================================================================================================")
  if best_individual_in_generation.fitness > best_individual_overall.fitness:
    best_individual_overall = best_individual_in_generation
  population = NextGen(population)
print("=================================================================================================================================================================================")
print("Chromosome terbaik : ",best_individual_overall.chromosome.gen,"\t\tx: ",best_individual_overall.chromosome.x1,"\t\ty: ",best_individual_overall.chromosome.x2,"\nFitness: ",best_individual_overall.fitness)
print("=================================================================================================================================================================================")