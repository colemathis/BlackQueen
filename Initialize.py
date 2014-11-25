import numpy as np 
import Parameters as Par 
import Interactions
import random
from Agents import Agent
############################################################################################
def Initialize_Agents():
	# Empty list of agents
	Par.Agents = []
	for ID in range(Par.num_agents):
		production = np.random.random(3)
		production /= production.sum()
		#print "Production:"
		#print production
		#print production.sum()

		need = np.random.random(3)
		need /= need.sum()
		#print "Need: "
		#print need
		#print need.sum()

		Par.Agents.append(Agent(ID, production, need))
		Par.Agents[ID].t_discovery = 0.0
	print len(Par.Agents)
	#print "Num  of Agents: " +str(len(Par.Agents))
###########################################################################################
def update_propensities(Agents, time_step):
	from operator import add, sub
	import Output

	# Zero totals out
	Ap_donate = [0.0, 0.0, 0.0]
	Ap_accept = [0.0, 0.0, 0.0]
	Ap_die = 0.0
	suffering_agents = 0
	Times_since_needs =0
	fitness = 0
	# There is a fixed amount of resouces flowing into the reactor and each organism gets an equal share
	resource_share = float(Par.k_num_agents)/float(Par.num_agents)

	for Agent in Agents:
		if Agent.dead != True:
			''' All the agents produce and some use resources to increase fitness '''
			new_resources = [time_step*Par.kp*resource_share*x for x in Agent.production]
			Agent.resources =np.add(new_resources, Agent.resources)

			if Agent.resources[0] >= Agent.consumption_rate*(Agent.needs[0]) and Agent.resources[1] >= Agent.consumption_rate*(Agent.needs[1]) and Agent.resources[2] >= Agent.consumption_rate*(Agent.needs[2]):
				Agent.time_since_needs_met = 0.0

				'''Consume to maintain '''
				Agent.resources =np.subtract(Agent.resources, Agent.consumption_rate*Agent.needs*time_step)

				'''Consume to increase fitness '''
				while Agent.resources[0] >= Agent.consumption_rate*(Agent.needs[0]) and Agent.resources[1] >= Agent.consumption_rate*(Agent.needs[1]) and Agent.resources[2] >= Agent.consumption_rate*(Agent.needs[2]):
					Agent.resources =np.subtract(Agent.resources, Agent.consumption_rate*Agent.needs)
					Agent.fitness +=1

			else:
				Agent.time_since_needs_met += time_step
				suffering_agents +=1


			''' Compute propensities to donate and accept '''
			for i in range(Par.num_resources):
				if Agent.resources[i] > Agent.needs[i]:
					Agent.Ap_d[i] = Par.ke*(Agent.resources[i] - Agent.needs[i])
					Agent.Ap_a[i] = 0.0
				elif Agent.resources[i] <= Agent.needs[i]:
				    Agent.Ap_d[i] = 0.0
				    Agent.Ap_a[i] = (Agent.needs[i] - Agent.resources[i])			
			Ap_donate = np.add(Ap_donate, Agent.Ap_d)
			Ap_accept = np.add(Ap_accept, Agent.Ap_a)
			Times_since_needs += Agent.time_since_needs_met
			fitness += Agent.fitness

	''' Calculate birth and death rates '''
	Par.Ap_death = Par.death_rate*float(suffering_agents/Par.num_agents)
	Par.Ap_birth = Par.birth_rate*fitness
	
	''' Update Propensities '''
	Par.Ap_donate = Ap_donate
	Par.Ap_Total_d = sum(Ap_donate)

	Par.Ap_accept = Ap_accept
	Par.Ap_Total_a = sum(Ap_accept)
	Par.Ap_Total = sum(Ap_donate)+ Par.death_rate + Par.birth_rate
	Par.Ap_die	= Ap_die
