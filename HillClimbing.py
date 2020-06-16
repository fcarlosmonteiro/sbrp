from random import random
from operator import itemgetter 
import pandas as pd
from ObjectiveFunction import objective_function
from SprintCapacity import sprints_capacity

bd = pd.read_csv('base.csv')

global iterations

capacity_sprints = 60 #in hours

def create_solution():
	current = []
	while sprints_capacity(current)<capacity_sprints:
		id=1+int(99*random())
		current.append(id)
		check_clone(current)
	print("current solution: ", current)
	return current

def extends_neighborhood(current):

	#neighbor1
	neighbor1 = current.copy()
	neighbor1[0] = neighbor1[0]+1
	check_clone(neighbor1)

	#neighbor2
	neighbor2=current.copy()
	neighbor2[1] = neighbor2[1]+1
	check_clone(neighbor2)
	
	#neighbor3
	neighbor3=current.copy()
	neighbor3[2] = neighbor3[2]+1
	check_clone(neighbor3)

	#neighbor4
	neighbor4=current.copy()
	neighbor4[3] = neighbor4[3]+1
	check_clone(neighbor4)
	
	neighborhood=[neighbor1,neighbor2,neighbor3,neighbor4]
	
	return neighborhood
		
def check_clone(solution):
	sol = []
	for id in solution:
		if id not in sol:
			sol.append(id)
		else:
			sol.append(1+int(99*random()))
	return sol

def hc_process(iterations):
	c=0
	current=create_solution()
	while (c<iterations):
		neighborhood=extends_neighborhood(current)
		for sol in neighborhood[0:len(neighborhood)]:
			fit_current=objective_function(current,capacity_sprints)
			fit_neighbor=objective_function(sol,capacity_sprints)

			#print("current solution:", current, "| fit:",str(fit_current), "| estimate/h:", sprints_capacity(current))
			print("neighbor", sol,"| fit:",str(fit_neighbor),"| estimate/h:", sprints_capacity(current))
			print()
			current=sol.copy() if (fit_neighbor<=fit_current) else current	
		c=c+1
		print("New current:", current, "| fit:",str(fit_current), "| estimate/h:", sprints_capacity(current))
	
		
	return current

hc_process(10)
