#!/usr/bin/python

import os
import shutil
from subprocess import call

import multiprocessing
import time

# 0
Runs = [[0.01, False, False, 0.0], [0.1, False, False, 0.0], [0.2, False, False, 0.0], [0.3, False, False, 0.0], [0.4, False, False, 0.0],
[0.5, False, False, 0.0], [0.6, False, False, 0.0], [0.7, False, False, 0.0], [0.8, False, False, 0.0],  [0.9, False, False, 0.0], [0.99, False, False, 0.0],
[0.0, True, False, 0.1], [0.0, True, False, 0.2], [0.0, True, False, 0.3], [0.0, True, False, 0.4], [0.0, True, False, 0.5], [0.0, True, False, 0.6], [0.0, True, False, 0.7],
[0.0, True, True, 0.1], [0.0, True, True, 0.2], [0.0, True, True, 0.3], [0.0, True, True, 0.4], [0.0, True, True, 0.5], [0.0, True, True, 0.6], [0.0, True, True, 0.7]]     
jobs = []
job = 0
originalDirectory = os.getcwd()
pool = multiprocessing.Pool()


for i in range(len(Runs)):
    for exp in range(100):

        os.chdir(originalDirectory)
        if Runs[i][1] == True:
            if Runs[i][2] == True:
                dirname = ('/data/new_data/Targeted_N%.2f_K%.2f_exp%i' % (Runs[i][0], Runs[i][3], exp) )
                # if not os.path.exists(originalDirectory+ dirname):
                #     os.makedirs(originalDirectory+ dirname)
            else:
                dirname = ('/data/new_data/Random_N%.2f_K%.2f_exp%i' % (Runs[i][0], Runs[i][3], exp) )
                # if not os.path.exists(originalDirectory+ dirname):
                #     os.makedirs(originalDirectory+ dirname)

        else:
            dirname = ('/data/new_data/Normal_N%.2f_exp%i' % (Runs[i][0], exp))
            # if not os.path.exists(originalDirectory+ dirname):
            #     os.makedirs(originalDirectory+ dirname)

        newdir = originalDirectory +dirname
        # shutil.copy(originalDirectory+'/Main.py', newdir)
        # shutil.copy(originalDirectory+'/Interactions.py', newdir+'/Interactions.py')
        # shutil.copy(originalDirectory+'/Initialize.py', newdir+'/Initialize.py')
        # shutil.copy(originalDirectory+'/TemplateParameters.py', newdir+'/Parameters.py')
        # shutil.copy(originalDirectory+'/Output.py', newdir+'/Output.py')
        # shutil.copy(originalDirectory+'/Agents.py', newdir+'/Agents.py')
        # shutil.copy(originalDirectory+'/BlackQueen.pbs', newdir+'/BlackQueen.pbs')
        os.remove(newdir+'/Agents.py')
        os.remove(newdir+'/BlackQueen.pbs')
        os.remove(newdir+'/Main.py')
        os.remove(newdir+'/Output.py')
        os.remove(newdir+'/Parameters.py')
        os.remove(newdir+'/Initialize.py')
        os.remove(newdir+'/Interactions.py')

        # os.chdir(newdir)
        # file= open("Parameters.py", 'a')
        # s = '\n\nnoise = %f \nattack =  %s \ntargeted_attack = %s \nkillPercentage = %f' % (Runs[i][0], Runs[i][1], Runs[i][2], Runs[i][3])
        # file.write(s)
        # file.close()
        
        # job +=1
        # if job >= 301:
        #     time.sleep(300)
        #     print '\n \n \n \n \n'
        #     job = 0

         
        # call(['qsub', 'BlackQueen.pbs'])
        #call(['python', 'master.py'])
        call('pwd')
        #time.sleep(5)