from random import random
from operator import itemgetter 
import pandas as pd

bd = pd.read_csv('base.csv')
capacity_sprints = 15

global number_req
global iterations

number_req = 4

def create_solution(number_req):
	current = []
	for i in range(number_req):
		id=1+int(99*random())
		current.append(id)
	check_clone(current)
	#print("current solution: ", current)
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

def fitness_function(solution):
	dados = []
	grau_depen = []
	for i in range(number_req):
		dados.append(bd.iloc[solution[i],0:4])
		grau_depen.append(dados[i].loc['Grau de dependencia'])

	gpd = 0
	for g in grau_depen:
		if pd.isnull(g):
			pass
		else:
			gpd += g
	gpd = (gpd/number_req)

	fit_value = 0
	for i in range(number_req):
		fit_value += dados[i].loc['Prioridade']
	fit_value -= gpd

	return fit_value

def sprints_capacity(solution):

	return True

def hc_process(iterations):
	c=0
	current=create_solution(number_req)
	while (c<iterations):
		neighborhood=extends_neighborhood(current)
		for sol in neighborhood[0:len(neighborhood)]:
			fit_current=fitness_function(current)
			fit_neighbor=fitness_function(sol)

			print("current solution:", current, " fit:",str(fit_current))
			print("neighbor", sol," fit:",str(fit_neighbor))
			
			current=sol.copy() if (fit_neighbor<=fit_current) else current	
		c=c+1
	print('new current:',current)
		
	return current

hc_process(1)
