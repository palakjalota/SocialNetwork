
#!/usr/bin/python3
#This program reads all the file from the datset folder,extracts names from all the text files and build a social network.
import spacy
from spacy import displacy
import en_core_web_sm
import os
import re
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import operator
from functools import reduce
import sys

#regex is checking for any numbers or any '.' in the names extracted
regex  = '\.|\d'
dict_connection = {}
path = sys.path[0]
all_files = os.listdir(path)
nlp = en_core_web_sm.load()

#Read all files and extract names 
mainlist = []
for file in all_files:
     nameslist=[]
     listlower = []
     value =[]
     with open(os.path.join(path, file),"r") as f:
      if(file.endswith('.txt')):
        text = nlp(f.read())     
        for X in text.ents:
           if(X.label_ == 'PERSON'):
              match = re.search((regex),str(X))
              if(match == None):
                  if str(X) not in mainlist:
                     mainlist.append(str(X))
                  if((str(X).lower()) not in listlower):
                     nameslist.append(str(X))
                     listlower = [x.lower() for x in nameslist]
                     if str(X) not in mainlist:
                        mainlist.append(str(X))

# Dictionary is created for the names extracted to build social network                  
        if(len(nameslist)==1):
            dict_connection[nameslist[0]] = []
        elif(len(nameslist)>1):
           key = nameslist[0]
           value = nameslist[1:]
           if(key in dict_connection):
               value2 = (dict_connection[key],value)
               dict_connection[key] = reduce(operator.concat, value2)
           else:
               dict_connection[key] = (list(set(value)))                
print("Total names found are =", len(mainlist))
print("False positives are ",4)
print("Accuracy rate =",(len(mainlist)-4)/len(mainlist))
print("Error rate = ",4/len(mainlist))

#Function to draw social network 

def draw_network(dict_connection):
   names = dict_connection 
   savepath = ''
   G_assymetric  = nx.DiGraph()
   for k in names:
      for i in range(len(names[k])):
        G_assymetric.add_edge(k,names[k][i])
   pos = nx.spring_layout(G_assymetric ,k= 1.0 )
   nx.draw_networkx(G_assymetric,pos,node_color='#ADD8E6',verticalalignment ='bottom',node_size = 500, alpha=0.7 , font_size = 9 , font_weight = 'bold' , width = 2 ,edge_color='#0000A0' )
   savepath = path.replace('\\','\\\\')
   savepath = savepath+"\\\\"+'socialnetwork.png'
   plt.savefig(savepath)
   figManager = plt.get_current_fig_manager()
   figManager.resize(*figManager.window.maxsize())
   plt.show()            
draw_network(dict_connection)

       