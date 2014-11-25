import numpy as np 
import math
import random
from time import clock
import os
import networkx as nx
import matplotlib.pyplot as plt

#####################################################################################################
def main():
	Runs = [[0.01, False, False, 0.0], [0.1, False, False, 0.0], [0.2, False, False, 0.0], [0.3, False, False, 0.0], [0.4, False, False, 0.0],
	[0.5, False, False, 0.0], [0.6, False, False, 0.0], [0.7, False, False, 0.0], [0.8, False, False, 0.0],  [0.9, False, False, 0.0], [0.99, False, False, 0.0],
	[0.0, True, False, 0.1], [0.0, True, False, 0.2], [0.0, True, False, 0.3], [0.0, True, False, 0.4], [0.0, True, False, 0.5], [0.0, True, False, 0.6], [0.0, True, False, 0.7],
	[0.0, True, True, 0.1], [0.0, True, True, 0.2], [0.0, True, True, 0.3], [0.0, True, True, 0.4], [0.0, True, True, 0.5], [0.0, True, True, 0.6], [0.0, True, True, 0.7]]     

	originalDirectory = os.getcwd()
	
	filename = 'NoiseVsHub.dat'
	file = open(filename, 'w')
	s = 'Noise level 	Most_connected node '
	file.write(s)
	file.write('\n')
	file.close()

	filename = 'TargetedAttackVsHub.dat'
	file = open(filename, 'w')
	s = 'Kill Percent 	Most_connected Node '
	file.write(s)
	file.write('\n')
	file.close()

	filename = 'RandomAttackVsHub.dat'
	file = open(filename, 'w')
	s = 'Kill Percent 	Most_connected Node  '
	file.write(s)
	file.write('\n')
	file.close()
	exp = 0
	for i in range(len(Runs)):
		sizes = []
		exp = 0
		print i, len(Runs)
		for exp in range(100):
			print exp
			os.chdir(originalDirectory)
			if Runs[i][1] == True:
			    if Runs[i][2] == True:
					dirname = ('/data/Targeted_N%.2f_K%.2f_exp%i' % (Runs[i][0], Runs[i][3], exp) )
					plotname = ('/data/Targeted_N%.2f_K%.2f_exp%i/Degree_distro.png' % (Runs[i][0], Runs[i][3], exp) )
					#print 'working'

			    else:
					dirname = ('/data/Random_N%.2f_K%.2f_exp%i' % (Runs[i][0], Runs[i][3], exp) ) 
					plotname = ('/data/Random_N%.2f_K%.2f_exp%i/Degree_distro.png' % (Runs[i][0], Runs[i][3], exp) )  


			else:
				dirname = ('/data/Normal_N%.2f_exp%i' % (Runs[i][0], exp))
				plotname = ('/data/Normal_N%.2f_exp%i/Degree_distro.png' % (Runs[i][0], exp))
				

			giant_size = generate_network(originalDirectory+ dirname+'/Exchanges.dat', originalDirectory+ plotname)
			print giant_size
			
			sizes.append(giant_size)


		if Runs[i][1] == True:
		    if Runs[i][2] == True:
		       	filename = 'TargetedAttackVsGiantComponent.dat'
		       	s = '%f' % Runs[i][3]
		    else:
		        filename = 'RandomAttackVsGiantComponent.dat'
		        s = '%f' % Runs[i][3]
		else:
		 	filename = 'NoiseVsHub.dat'
		   	s = '%f' % Runs[i][0]

		s += '		%f' % np.mean(sizes)
		file= open(filename, 'a')
		file.write(s)
		file.write('\n')
		file.close()

		print 'one run '

#########################################################################################								
def mean_self_relience():
	Runs = [[0.0, True, False, 0.1], [0.0, True, False, 0.2], [0.0, True, False, 0.3], [0.0, True, False, 0.4], [0.0, True, False, 0.5], [0.0, True, False, 0.6], [0.0, True, False, 0.7],
[0.0, True, True, 0.1], [0.0, True, True, 0.2], [0.0, True, True, 0.3], [0.0, True, True, 0.4], [0.0, True, True, 0.5], [0.0, True, True, 0.6], [0.0, True, True, 0.7]]     

	originalDirectory = os.getcwd()

	filename = 'TargetedAttackVsSelfRelience.dat'
	file = open(filename, 'w')
	s = 'Kill percent	Self Relience '
	file.write(s)
	file.write('\n')
	file.close()

	filename = 'RandomAttackVsSelfRelience.dat'
	file = open(filename, 'w')
	s = 'Kill percent	Self Relience '
	file.write(s)
	file.write('\n')
	file.close()
	
	exp = 0
	for i in range(len(Runs)):
		
		exp = 0
		reliences= []
		for exp in range(100):
			weighted_self_reliences =[]
			os.chdir(originalDirectory)
			if Runs[i][1] == True:
			    if Runs[i][2] == True:
					dirname = ('/data/Targeted_N%.2f_K%.2f_exp%i' % (Runs[i][0], Runs[i][3], exp) )
					plotname = ('/data/Targeted_N%.2f_K%.2f_exp%i/Degree_distro.png' % (Runs[i][0], Runs[i][3], exp) )
					#print 'working'

			    else:
					dirname = ('/data/Random_N%.2f_K%.2f_exp%i' % (Runs[i][0], Runs[i][3], exp) ) 
					plotname = ('/data/Random_N%.2f_K%.2f_exp%i/Degree_distro.png' % (Runs[i][0], Runs[i][3], exp) )  

			fitness, relience = np.loadtxt(originalDirectory+dirname+ '/Scatter.dat', unpack =True)
			total_fit = sum(fitness)
			for j in range(len(fitness)):
				weighted_self_reliences.append((fitness[j]*relience[j])/total_fit)
			reliences.append(sum(weighted_self_reliences))

		if Runs[i][1] == True:
		    if Runs[i][2] == True:
		       	filename = 'TargetedAttackVsSelfRelience.dat'
		       	s = '%f' % Runs[i][3]
		    else:
		        filename = 'RandomAttackVsSelfRelience.dat'
		        s = '%f' % Runs[i][3]

		s += '		%f' % (np.mean(reliences))
		file= open(filename, 'a')
		file.write(s)
		file.write('\n')
		file.close()

		print 'one run '

#########################################################################################								
def mean_num_agents():
	Runs = [[0.01, False, False, 0.0], [0.1, False, False, 0.0], [0.2, False, False, 0.0], [0.3, False, False, 0.0], [0.4, False, False, 0.0],
[0.5, False, False, 0.0], [0.6, False, False, 0.0], [0.7, False, False, 0.0], [0.8, False, False, 0.0],  [0.9, False, False, 0.0], [0.99, False, False, 0.0]]

	originalDirectory = os.getcwd()

	filename = 'Mean_agents.dat'
	s = 'Noise 		Mean Agents'
	file= open(filename, 'w')
	file.write(s)
	file.write('\n')
	file.close()
	exp = 0
	for i in range(len(Runs)):
		
		exp = 0
		Mean_agents= []
		for exp in range(100):
			weighted_self_reliences =[]
			os.chdir(originalDirectory)
			
			dirname = ('/data/Normal_N%.2f_exp%i' % (Runs[i][0], exp) )
			plotname = ('/data/Normal_N%.2f_exp%i/Degree_distro.png' % (Runs[i][0], exp) )
			#print 'working'

			num_agents = 0.0    
			Agents_Lists, Lives = np.loadtxt(originalDirectory+dirname+ '/AgentProperties.dat', unpack =True, usecols= (0,2), skiprows = 1, dtype = str)
			for life in Lives:
				if life == "False":
					num_agents += 1
			Mean_agents.append(num_agents)

		        
		s = '%f		%f' % ( Runs[i][0], np.mean(Mean_agents))
		file= open(filename, 'a')
		file.write(s)
		file.write('\n')
		file.close()

		print 'one run '

								
								

# End Function Main ############################################################
#########################################################################################
def generate_network(filename, savename):
	
	donors, acceptors, resources, amounts = np.loadtxt(filename, unpack = True)
	exchange_senarios = zip(donors, acceptors, resources)
	reduced_exchange_senarios = list(set(exchange_senarios))
	reduced_amounts = []

	for senario in reduced_exchange_senarios:
		sum_exchanged = 0.0
		for single_senario in exchange_senarios:
			if single_senario == senario:
				index = exchange_senarios.index(single_senario)
				sum_exchanged += amounts[index]
		reduced_amounts.append(sum_exchanged)

	#print len(reduced_exchange_senarios)
	#print len(reduced_amounts)
	donors, acceptors, resources = zip(*reduced_exchange_senarios)
	graphdata = zip(donors, acceptors, resources, reduced_amounts)


	#sizes = data.shape # used in for loops
	graph = nx.MultiDiGraph()
	# listofdonors = [] # used to avoid redundancy in collecting data
	# listofagents = [] # used to avoid redundancy in collecting data
	# graphdata = [] # data used for making the graph.  Each row is an interaction.  The columns are: donor, acceptor, resource, number of instances of interaction
	# currList = [] # placeholder used to populate graphdata
	# # we loop over every row in the data obtained from the exchanges file
	# for i in range(0, sizes[0]):
	#     listofacceptors = [] # used later, just need to clear here
	#     # if we haven't come across the donating agent yet, we add it to the list of agents
	#     if not(data[i, 0] in listofagents):
	#         listofagents.append(data[i, 0])
	#     # if we haven't come across the accepting agent yet, we add it to the list of agents
	#     if not(data[i, 1] in listofagents):
	#         listofagents.append(data[i, 1])
	#     # if we haven't come across the donating agent yet as a donor, we add it to the list of donors
	#     # since the donating agent has not donated yet, we know we need to make a new row corresponding to this 
	#     # particular interaction in graphdata
	#     if not(data[i, 0] in listofdonors):
	#         listofdonors.append(data[i, 0])
	#         currList.append(data[i, 0]) # donor
	#         currList.append(data[i, 1]) # recipient
	#         currList.append(data[i, 2]) # resource
	#         currList.append(1) # initial number of instances, since this interaction has not happened before
	#         graphdata.append(currList)
	#         currList = []
	#     else:
	#     # in this case, we have come across the donating agent as a donor
	#     # we have to check see if it has donated to the acceptor yet
	#     # for that, we need a list of agents the donor has donated to so far
	#         for j in range(0, len(graphdata)):
	#             if graphdata[j][0] == data[i, 0]:
	#                 listofacceptors.append(data[i, 1]) # this is that list
	#         # if the donor has NOT donated to this particular acceptor yet, 
	#         # we create a new row corresponding to this particular interaction in graphdata
	#         if not(data[i, 1] in listofacceptors):
	#             currList.append(data[i, 0]) # donor
	#             currList.append(data[i, 1]) # recipient
	#             currList.append(data[i, 2]) # resource
	#             currList.append(1) # initial weight
	#             graphdata.append(currList)
	#             currList= []
	#         # if the donor HAS donated to this particular acceptor before, 
	#         # this interaction has already happened before (up to resource), and so there is already a 
	#         # corresponding row in graphdata.  So all we have to do here is 
	#         # add 1 to the number of instances of this interaction
	#         # If the resource is not the same as it was before, then we add a new row again.
	#         else:
	#             counter = 0
	#             resources = set([])
	#             while counter < len(graphdata):
	#                 # if we find the donor-acceptor pair (guaranteed) we chekc to see which resource was traded.  We add the traded resource to the
	#                 # set of resources for keeping track
	#                 if (graphdata[counter][0] == data[i, 0] and graphdata[counter][1] == data[i, 1]):
	#                     resources.add(data[i, 2])
	#                 # if we find that the exact interaction has occurred before, we simply update the number of instances of the interaction by adding 1 and then stop
	#                 if (graphdata[counter][0] == data[i, 0] and graphdata[counter][1] == data[i, 1] and graphdata[counter][2] == data[i, 2]):
	#                     graphdata[counter][3] = graphdata[counter][3] + 1
	#                     #print "repeat interaction"
	#                     break
	#                 counter = counter + 1
	#             #if, after searching through all appropriate interactions, we find that the 
	#             # particular resource has not been involved, we add a new row to graphdata
	#             if not(data[i, 2] in resources): 
	#                 currList.append(data[i, 0]) # donor
	#                 currList.append(data[i, 1]) # recipient
	#                 currList.append(data[i, 2]) # resource
	#                 currList.append(1) # initial weight
	#                 graphdata.append(currList)
	#                 currList= []
	colorvec = ["red", "blue", "yellow"]
	#print(len(graphdata))
	#print(graphdata[:][3])
	#print(graphdata[24])
	#print(graphdata[25])
	#print " Finished data collection, making graph"
	colors = []
	weights = []
	for k in range(0, len(graphdata)):
	    #print k
	    if graphdata[k][3] > 1:
	        colors.append(colorvec[int(graphdata[k][2])])
	        weights.append(graphdata[k][3])
	        graph.add_edge(graphdata[k][0], graphdata[k][1], weight = graphdata[k][3], resource = graphdata[k][2])     
	print "made graph"
        
        #nx.draw(graph, edge_color = colors, edge_labels = weights, with_labels=False, node_size=30)
        

	
	#plot the degree distribution
	# degree_sequence=sorted(nx.degree(graph).values(),reverse=True) # degree sequence
	# plt.hist(degree_sequence,12,normed = True)
	# #plt.ylim(0,0.5)
	# plt.xlim(0,40)
	# plt.title("Degree Distribution")
	# plt.ylabel("density")
	# plt.xlabel("degree")
	# plt.savefig(savename)
	# plt.close()
	sorts_degree = sorted(graph.degree().values())
	index = len(sorts_degree) - 1
	print index
	if index < 0:
		print sorts_degree
		return 0.0
	else: 
		Most_connected = sorts_degree[len(sorts_degree)-1]
		print Most_connected
	
	#giant component
	# ungraph = graph.to_undirected()
	# pos=nx.spring_layout(ungraph)
	# #nx.draw(ungraph,pos,with_labels=False,node_size=30)
	# Gcc=sorted(nx.connected_component_subgraphs(ungraph), key = len, reverse=True)
	# G0=Gcc[0]
	#print len(Gcc)

	#nx.draw_networkx_edges(G0,pos,with_labels=False,edge_color='r',width=4.0)
	# show other connected components
	# for Gi in Gcc[1:]:
	# 	if len(Gi)>1:
	# 		nx.draw_networkx_edges(Gi,pos,with_labels=False,edge_color='r',alpha=0.3,width=3.0)

	return Most_connected
##########################################################################################
def plot_noiseVSgc():
	noise, gc = np.loadtxt('NoiseVsHub.dat', unpack =True, skiprows= 1)

	plt.scatter(noise, gc)
	plt.show()
##########################################################################################
if __name__=="__main__":
	main()
	plot_noiseVSgc()