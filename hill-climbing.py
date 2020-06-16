from random import random
from operator import itemgetter 
import pandas as pd

bd = pd.read_csv('base.csv')
capacity_sprints = 60 #in hours

global number_req
global iterations

number_req = 4

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

def objective_function(solution):
	data = []
	grau_depen = []
	for i in range(len(solution)):
		data.append(bd.iloc[solution[i],0:4])
		grau_depen.append(data[i].loc['Grau de dependencia'])

	gpd = 0
	for g in grau_depen:
		if pd.isnull(g):
			pass
		else:
			gpd += g
	gpd = (gpd/len(solution))

	fit_value, total = 0,0
	for i in range(len(solution)):
		fit_value += data[i].loc['Prioridade']
	
	#bonus and penality
	if sprints_capacity(solution) == capacity_sprints:
		total = (fit_value - gpd) + (0.1 * (fit_value - gpd))
	elif (0.6*capacity_sprints) >= sprints_capacity(solution) <= (0.9*capacity_sprints):
		total = 0.9 * (fit_value - gpd)
	elif sprints_capacity(solution) <= (0.59*capacity_sprints):
		total = 0.8 * (fit_value - gpd)
	else:
		total = fit_value - gpd

	return total

def sprints_capacity(solution):
	data = []
	data_estimate = []
	
	for i in range(len(solution)):
		
		data.append(bd.iloc[solution[i],0:5])
		data_estimate.append(data[i].loc['Estimativa'])

	estimate=0
	for e in data_estimate:
		if pd.isnull(e):
			pass
		else:
			estimate += e
	return estimate

def hc_process(iterations):
	c=0
	current=create_solution()
	while (c<iterations):
		neighborhood=extends_neighborhood(current)
		for sol in neighborhood[0:len(neighborhood)]:
			fit_current=objective_function(current)
			fit_neighbor=objective_function(sol)

			#print("current solution:", current, "| fit:",str(fit_current), "| estimate/h:", sprints_capacity(current))
			print("neighbor", sol,"| fit:",str(fit_neighbor),"| estimate/h:", sprints_capacity(current))
			print()
			current=sol.copy() if (fit_neighbor<=fit_current) else current	
		c=c+1
		print("New current:", current, "| fit:",str(fit_current), "| estimate/h:", sprints_capacity(current))
	
		
	return current

hc_process(100)
