#Preliminary model for the Cooperation experiments
import numpy as np 
import math
import random
from time import clock
import os
import Parameters as Par 
from Interactions import *
from Output import *
from Agents import *
from Initialize import *

#####################################################################################################
def main():
	for exp in range(Par.total_runs):
		'''Initialize and make data directory '''
		start_time = clock()
		Par.tau = 0.0
		tau_max = Par.tau_max
		freq_counter = 0.0
		attack_count = 0 
		
        Par.dirname =os.getcwd()
        Initialize_Agents()
        update_propensities(Par.Agents, 1.0)
    
        tau_step = 1.0
        #print Par.tau

        ''' Main Stochastic Evolution Loop (SSA - Simplified Stochastic Algorithm ) '''
        while Par.tau < tau_max:

			'''Determine Event '''
			dice_roll = Par.Ap_Total*random.random()
			''' Resource Exchange '''
			if dice_roll < Par.Ap_Total_d:
				(Donating_ID, Donating_resource) = find_donor()

				''' Find an Agent wanting that resource '''
				if Par.Ap_accept[Donating_resource] > 0.0:
					Accepting_ID = find_acceptor(Donating_ID, Donating_resource)
					if type(Accepting_ID) != int :
						print Par.Ap_Total_a
						print len(Par.Ap_accept)
						print "Accepting ID is not being found"
						break
					if Accepting_ID == Donating_ID:
						print "Self Interaction... Wtf!?"
						break

					''' Exchange the resource with shakey hands '''
					Exchange_Resources(Donating_ID, Accepting_ID, Donating_resource)

			elif dice_roll < Par.Ap_Total_d +Par.Ap_death:
				Dead_Agent = Find_Weak(Par.Agents)
				
				Par.Dead_Agents.append(Dead_Agent)
				Dead_Agent.resources = [0.0, 0.0, 0.0]
				Dead_Agent.Ap_a = [0.0, 0.0, 0.0]
				Dead_Agent.Ap_d = [0.0, 0.0, 0.0]
				
				Dead_Agent.dead = True
				Dead_Agent.t_death = Par.tau

			else:
				Fit_Agent = Find_Fit(Par.Agents)

				copy_agent(Fit_Agent)
				Par.num_agents +=1       

			''' Random roll through time '''
			dice_roll = random.random()
			tau_step = -math.log(dice_roll)/ Par.Ap_Total


			if freq_counter <= Par.tau:

				freq_counter += Par.tau_freq
				''' Record Data'''
				print_agent_data()

			'''Attack Mechanicisms '''
			if Par.attack == True:
				if Par.Attack_Time[attack_count] < Par.tau:
					if Par.targeted_attack == True:
						targeted_attack(random.randint(0,2), Par.specializedThreshold, Par.killPercentage)
						attack_count +=1
					else:	
						random_attack(Par.killPercentage)
						attack_count +=1
					
				
			''' Update the agents fitness, chance of donation, chance of acceptance  '''
			update_propensities(Par.Agents, tau_step)


			''' update time '''
			Par.tau+= tau_step	
		
        record_Agents()
        print_histories()
        print_scatter_data()
        plot_data()
        run_time = clock()- start_time
        #print run_time
        #print "Run Time: ",  run_time
# End Function Main ############################################################



if __name__=="__main__":
    main()