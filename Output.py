import numpy as np 
import random
import matplotlib as plt
import Parameters as Par
import os

##############################################################################################################
def record_Agents():
	'''Print the IDs, production and need lists of the Agents '''
	filename = '%s/AgentProperties.dat' % Par.dirname
	file = open(filename, 'w')
	s = 'ID 	fitness 	Dead 	Production1		Production2 	Production3 	Need1	Need2	Need3 \n'
	file.write(s)
	for Agent in Par.Agents:
		s = str(Agent.ID)+ '	'+ str(Agent.fitness)+ '	'+ str(Agent.dead)
		file.write(s)
		for i in range(Par.num_resources):
			s='		'+ str(Agent.production[i])
			file.write(s)
		for i in range(Par.num_resources):
			s='	'+ str(Agent.needs[i])
			file.write(s)
		file.write('\n')
	file.close()

##############################################################################################################
def record_exchange(Donating_ID, Accepting_ID, Donating_resource, donation):
	'''Record the Interactions between Agents '''
	filename = '%s/Exchanges.dat' % Par.dirname
	if Par.tau == 0.0:
		file= open(filename, 'w')
	else:
		file = open(filename, 'a')
	s = str(Donating_ID) + '	' + str(Accepting_ID) + '	' + str(Donating_resource) + '	'+ str(donation)
	file.write(s)
	file.write('\n')
	file.close()
##############################################################################################################
def print_agent_data():

	fitnesses = []
	time_since = []
	if not os.path.exists(Par.dirname+'/Populations'):
        	os.makedirs(Par.dirname+'/Populations')
	for Agent in Par.Agents:
		if Agent.dead != True:
		
			#Print Fitness
			# filename = Par.dirname + ('/Populations/%ifit.dat' %Agent.ID )
			# if Par.tau == 0:
			# 	file = open(filename, 'w')

			# else :
			# 	file = open(filename, 'a')
			# s = str(Par.tau) + '	' + str(Agent.fitness)
			# file.write(s)
			# file.write('\n')
			# file.close()
			fitnesses.append(Agent.fitness)
			time_since.append(Agent.time_since_needs_met)
			#Print Resources 
			# filename = Par.dirname+('/Populations/%iresources.dat' %Agent.ID )
			# if Par.tau == 0:
			# 	file = open(filename, 'w')
			# else :
			# 	file = open(filename, 'a')
			# s = str(Par.tau) + '	' + str(Agent.resources)
			# file.write(s)
			# file.write('\n')
			# file.close()

			#Print Needs 
			# filename = Par.dirname +('/Populations/%ineeds.dat' %Agent.ID )
			# if Par.tau == 0:
			# 	file = open(filename, 'w')
			# else :
			# 	file = open(filename, 'a')
			# s = str(Par.tau) + '	' + str(Agent.Ap_a)
			# file.write(s)
			# file.write('\n')
			# file.close()
	mean_time_since = np.mean(time_since)
	max_time_since = max(time_since)
	std_time_since = np.std(time_since)
	filename = Par.dirname + ('/suffering.dat')
	s = str(Par.tau) + '	' + str(mean_time_since)+ '	' + str(std_time_since)+ '		'+ str(max_time_since)
	if Par.tau == 0:
		file = open(filename, 'w')
	else :
		file = open(filename, 'a')
	file.write(s)
	file.write('\n')
	file.close()
	
	mean_fitness = np.mean(fitnesses)
	max_fitness = max(fitnesses)
	std_fitness = np.std(fitnesses)
	filename = Par.dirname + ('/fitness.dat')
	s = str(Par.tau) + '	' + str(mean_fitness)+ '	' + str(std_fitness)+ '		'+ str(max_fitness)
	if Par.tau == 0:
		file = open(filename, 'w')
	else :
		file = open(filename, 'a')
	file.write(s)
	file.write('\n')
	file.close()

	filename = Par.dirname + ('/Live_Agents.dat')
	s = str(Par.tau)
	for Agent in Par.Agents:
		if Agent.dead != True:
			s += '	'+str(Agent.ID)
	if Par.tau == 0:
		file = open(filename, 'w')
	else :
		file = open(filename, 'a')
	file.write(s)
	file.write('\n')
	file.close()
########################################################################################################
def print_histories():
	filename = Par.dirname + ('/Histories.dat')
	file =open(filename, 'w')
	for Agent in Par.Agents:
		s = str(Agent.ID) + str(Agent.history)
		file.write(s)
		file.write('\n')
	file.close()
########################################################################################################
def print_scatter_data():
	import matplotlib.pylab as plt
	filename = Par.dirname + ('/Scatter.dat')
	fitnesses = []
	self_reliences = []
	life_times = []
	self_reliences_dead = []

	for Agent in Par.Agents:
		if Agent.dead != True:
			fitnesses.append(Agent.fitness)
			Needs = Agent.needs
			Production = Agent.production
			selfReli = [0.0]*Par.num_resources
			for i in range(Par.num_resources):
				selfReli[i] = Production[i]*Needs[i]
			self_reliences.append(abs(sum(selfReli)))
		else:
			life_time = Agent.t_death - Agent.t_discovery 
			life_times.append(life_time)
			Needs = Agent.needs
			Production = Agent.production
			selfReli = [0.0]*Par.num_resources
			for i in range(Par.num_resources):
				selfReli[i] = Production[i]*Needs[i]
			self_reliences_dead.append(abs(sum(selfReli)))
			
	
	file =open(filename, 'w')

	for i in range(len(fitnesses)):
		s= str(fitnesses[i]) +'		'+ str(self_reliences[i])
		file.write(s)
		file.write('\n')
	file.close()	


	plt.scatter(self_reliences, fitnesses)
	plt.ylabel('Fitness')
	plt.xlabel('self_reliences')
	plt.savefig('FitnessVSR.png')
	plt.close()
	plt.scatter(self_reliences_dead, life_times)
	plt.ylabel('LifeTimes')
	plt.xlabel('self_reliences')
	plt.savefig('LifeTimeVSR.png')
	plt.close()
#############################################################################################################
def print_mean_specialization(Agents):
	specializations = []
	for Agent in Agents:
		if Agent.dead != True:
			
			Needs = Agent.needs
			Production = Agent.production
			selfReli = [0.0]*Par.num_resources
			for i in range(Par.num_resources):
				selfReli[i] = abs(Production[i]-Needs[i])
			specializations.append(sum(selfReli))
	print 'Mean Specialization: ', np.mean(specializations)
	print 'Std of specialization:', np.std(specializations)
	raw_input('Press Enter to Continue')
##############################################################################################################
def plot_data():
	import matplotlib.pylab as plt
	t, suffering = np.loadtxt('suffering.dat', unpack= True, usecols = (0,1))
	t, fitness = np.loadtxt('fitness.dat', unpack = True, usecols = (0,1))


	plt.plot(t, suffering)
	plt.xlabel('t')
	plt.ylabel('suffering')
	plt.savefig('suffering.png')
	plt.close()

	plt.plot(t, fitness)
	plt.xlabel('t')
	plt.ylabel('fitness')
	plt.savefig('fitness.png')
	plt.close()