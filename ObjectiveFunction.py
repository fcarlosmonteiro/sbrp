import pandas as pd
from SprintCapacity import sprints_capacity

bd = pd.read_csv('base.csv')

def objective_function(solution,capacity_sprints):
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