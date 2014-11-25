#Cole Mathis 2014
# CSSS14 Cooperation Trade off
import numpy as np
import Parameters as Par
###################################################################################################
class Agent(object):
    """An genetic population"""
    
    def __init__(self, ID, production, needs):
        #print("A new population has been born!")
        self.ID = ID # Unique populaton identifier
       	self.fitness = 0.0 # Population fitness
        self.production = production # Resource Production 3-vector
        self.needs = needs # Resource Needs 3-vector
        self.resources = [0.0, 0.0, 0.0] #Current resource supply
        self.consumption_rate = 1.0 - Par.specialization_rate*max(production) # Rate of resource consumption
        
        self.Ap_d = [0.0, 0.0, 0.0] # Propensity to donate resources
        self.Ap_a = [0.0, 0.0, 0.0] # Propensity to accept resources

        self.history = [(1.0/Par.k_num_agents)]*(Par.num_agents) # History vector, mostly inherieted from parents
        self.dead = False
        
        self.t_discovery = 0.0
        self.t_death = 0.0
        self.time_since_needs_met = 0
        
