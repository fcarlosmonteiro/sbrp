import pandas as pd

bd = pd.read_csv('base.csv')

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