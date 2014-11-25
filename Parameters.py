num_agents = 100 # updated for indexing new agents, records all agents ever
k_num_agents = 100 # kept constant
num_resources = 3
total_runs = 1

tau = 0.0

tau_freq = 1.0 # How often do we record data
tau_infreq = 5.0 # How often do we record less frequent data
tau_max = 500.0 # Max simulation time


attack = False
targeted_attack = False 
Attack_Time = [100.0, 150.0, 200.0, 250.0, 300.0, 350.0, 400.0, 450.0, tau_max+1.0]
specializedThreshold = 0.5
killPercentage = 0.5



noise = 0.9 # Shakey hands exchange noise
kp = 1.0 # Production Rate
ke = 0.5 # exchange rate 
sigma_e = 0.1
kh = 0.1 # History constant
specialization_rate = 0.7
death_rate = 10.0
birth_rate = 10.0

resource_flux = 1.0

sigma_m = 1.0
km = 0.5 # For mutation



############################################################################################
### Internally defined Parameters ##########################################################
############################################################################################

Agents= []


Dead_Agents = []
Ap_die = 0.0

Ap_donate = [0.0, 0.0, 0.0]
Ap_accept = [0.0, 0.0, 0.0]
Ap_Total_d = 0.0
Ap_Total_a = 0.0
Ap_total = 0.0