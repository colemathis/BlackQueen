import numpy as np 
import random
import Parameters as Par 
import Output
###########################################################################################################
def find_donor(): 
	'''Find an agent that is willing to donate a resource '''
	
	dice_roll = random.random()*Par.Ap_Total_d
	checkpoint = 0.0 
	''' Search All agents '''
	for Agent in Par.Agents:
		if Agent.dead != True:
			''' Search all resources '''
			for i in range(Par.num_resources):
				checkpoint += Agent.Ap_d[i]

				if checkpoint >= dice_roll:
					## Record who is donating and which resource they are donating ##
					Donating_resource = i 
					return (Agent.ID, Donating_resource)

	

##########################################################################################################
def find_acceptor(Donating_ID, resource):
	'''Find an agent that wants the resource being donated '''
	# dice_roll = random.random()*Par.Ap_accept[resource]

	'''Determine the total propensity to accept this resource based on histories and needs '''
	Ap_accept = 0.0
	for Agent in Par.Agents:
		if Agent.dead != True:
			Ap_accept += Agent.Ap_a[resource]*Agent.history[Donating_ID]
	if Ap_accept == 0.0:
		print "No exchange history bias"


	''' Use this propensity to find an aceepting agent '''
  	dice_roll = random.random()*Ap_accept 
	checkpoint = 0.0 
	
	for Agent in Par.Agents:
		if Agent.dead != True:
			checkpoint += Agent.Ap_a[resource] * Agent.history[Donating_ID]
			if checkpoint >= dice_roll:
				return Agent.ID
########################################################################################################
def Exchange_Resources(Donating_ID, Accepting_ID, Donating_resource):
	''' Exchange the resource in question (with nosie), and update the history of the agents'''
	
	'''Calculate the donation size '''
	donation = Par.ke*(Par.Agents[Donating_ID].resources[Donating_resource] - Par.Agents[Donating_ID].needs[Donating_resource])
	if donation < 0.0:
		print 'Exchange Broken'
		print 'donation: ', donation
		print 'Availible resources: ', Par.Agents[Donating_ID].resources[Donating_resource]
		print 'Resource Needs: ', Par.Agents[Donating_ID].needs[Donating_resource]
		Par.tau = Par.tau_max

	Par.Agents[Donating_ID].resources[Donating_resource] -= donation


	'''Determine if the donation was successful '''
	dice_roll = random.random() 
	if dice_roll > Par.noise:
		Par.Agents[Accepting_ID].resources[Donating_resource] += donation

		'''Update History'''
		Par.Agents[Accepting_ID].history[Donating_ID] += Par.kh
		for ID in range(len(Par.Agents)):
			if ID != Donating_ID and Par.Agents[Accepting_ID].history[ID] != 0.0:
				new_history = Par.Agents[Accepting_ID].history[Donating_ID] - float(Par.kh/Par.num_agents)
				if new_history < 0.0:
					new_history =0.0
				Par.Agents[Accepting_ID].history[Donating_ID] = new_history
		''' Record the exchange '''
		Output.record_exchange(Donating_ID, Accepting_ID, Donating_resource, donation)
		
########################################################################################################
def Death_Birth_Process():

    
    ''' Determine if death event happens '''
    dice_roll = random.random()

    if dice_roll <= Par.death_rate:
    	''' Kill an Agent '''
    	#print 'Ap_die:', Par.Ap_die
    	#print 'Killing Agent'
    	Dead_Agent = Find_Weak(Par.Agents)
    	#print'Killed ID:', Dead_Agent.ID
    	Par.Dead_Agents.append(Dead_Agent)
    	Dead_Agent.resources = [0.0, 0.0, 0.0]
    	Dead_Agent.Ap_a = [0.0, 0.0, 0.0]
    	Dead_Agent.Ap_d = [0.0, 0.0, 0.0]
    	# Dead_Agent.production =[0.0, 0.0, 0.0]
    	# Dead_Agent.needs = [0.0, 0.0, 0.0]
    	# Dead_Agent.fitness = 0.0
    	Dead_Agent.dead = True
    	#Par.num_agents -=1

    ''' Determine if an agent is born '''
    dice_roll = random.random()

    if dice_roll <= Par.birth_rate:
    	'''Add an Agent '''
    	## Create an Agent ##
    	Fit_Agent = Find_Fit(Par.Agents)
    	
    	copy_agent(Fit_Agent)
    	Par.num_agents +=1            
########################################################################################################
def Find_Fit(Agents):
    '''Find an agent giving higher probability to fitter agents '''
    total_fitness = 0.0
    for Agent in Agents:
        total_fitness += Agent.fitness

    checkpoint = 0.0
    dice_roll = random.random()*total_fitness
    for Agent in Par.Agents:
		checkpoint += Agent.fitness 
		if checkpoint >= dice_roll:
			return Agent
########################################################################################################
def Find_Weak(Agents):
	'''Find an agent giving higher probability to less fit agents'''  
	checkpoint = 0.0
	dice_roll = random.random()*Par.Ap_die
	#print 'dice_roll: ', dice_roll
	for Agent in Par.Agents:
		checkpoint += Agent.time_since_needs_met 
		if checkpoint >= dice_roll:
			return Agent
############################################################################################
def copy_agent(Fit_Agent):
	''' Make a mutated Copy of an agent '''
	from operator import add 
	from Agents import Agent
	
	ID = len(Par.Agents)
	production = Fit_Agent.production
	mutation = Par.km*np.absolute(np.random.normal(1.0, Par.sigma_m, 3))
	production = np.multiply(production, mutation) # Mutate
	production /= sum(production)
	#print "Production:"
	#print production
	#print production.sum()

	needs = Fit_Agent.needs
	mutation = Par.km*np.absolute(np.random.normal(1.0, Par.sigma_m, 3))
	needs = np.multiply(needs, mutation) # Mutate
	needs /= sum(needs)
	#print "Need: "
	#print need
	#print need.sum()

	Par.Agents.append(Agent(ID, production, needs))
	Par.Agents[ID].fitness = Fit_Agent.fitness
	Par.Agents[ID].t_discovery = Par.tau
	for i in range(len(Fit_Agent.history)):
		Par.Agents[ID].history[i]= Fit_Agent.history[i]
	
	for Agent in Par.Agents:
			Agent.history.append(1.0/(Par.k_num_agents))
	
############################################################################################
def targeted_attack(resource, threshold, probability):
	'''Targeted attack mechanism: 
		Required arguments- Resource: List index of the specific resource producers to target, 
							Threshold: float between (0,1], a measurement of how effective an agent must be to be Killed
							probability: float between (0,1], the chance that target meeting the resource/threshold requirements 
										will be killed in the attack '''
	for Agent in Par.Agents:
		if Agent.production[resource] > threshold:
			dice_roll = random.random()
			if dice_roll < probability:
				Agent.dead = True
				Agent.resources = [0.0, 0.0, 0.0]

############################################################################################
def random_attack(probability):
	'''Random Attack Mechanism:
		Required Arguments: probability, can be viewed as the fraction of agents killed in the attack'''
	for Agent in Par.Agents:
		dice_roll = random.random()
		if dice_roll < probability:
			Agent.dead = True
			Agent.resources = [0.0, 0.0, 0.0]
			Agent.needs = [0.0, 0.0, 0.0]
			Agent.productoin = [0.0, 0.0, 0.0]