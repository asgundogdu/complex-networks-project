# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 11:19:54 2017

@author: playe
"""

import csv
import numpy as np
import networkx as nx
from networkx import bipartite
import matplotlib as mpl
import scipy.optimize as sci_opt
import matplotlib.pyplot as plt

mpl.rc('xtick', labelsize=20, color="#222222") 
mpl.rc('ytick', labelsize=20, color="#222222") 
mpl.rc('font', **{'family':'sans-serif','sans-serif':['Arial']})
mpl.rc('font', size=20, weight='bold')
mpl.rc('xtick.major', size=6, width=1)
mpl.rc('xtick.minor', size=3, width=1)
mpl.rc('ytick.major', size=6, width=1)
mpl.rc('ytick.minor', size=3, width=1)
mpl.rc('axes', linewidth=1, edgecolor="#222222", labelcolor="#222222")
mpl.rc('text', usetex=False, color="#222222")

def log_degree_distribution(G,num_bins):
    k = list(dict(G.degree()).values())
    kmin = min(k)+1
    kmax = max(k)+1
    bin_edges = np.logspace(np.log10(kmin), np.log10(kmax), num=num_bins+1)
    
    k_hist = np.histogram(k,bins=bin_edges,range=(kmin,kmax),density=True)
    
    return (bin_edges[1:],k_hist[0])

def linear_degree_distribution(G,num_bins):
    k = list(dict(G.degree()).values())
    # Linearly bin the degrees between kmin and kmax
    kmin = min(k)
    kmax = max(k)+1
    bin_edges = np.linspace(kmin, kmax, num=num_bins+1)
    k_hist = np.histogram(k,bins=bin_edges,range=(kmin,kmax),density=True)

    # "x" should be midpoint of each bin
    x = (bin_edges[1:] + bin_edges[:-1])/2
    
    return (bin_edges[1:],k_hist[0])

def ffit(x,a,b):
    return a*x**(-b)

bipartite_edges = []
restaurant_nodes = []
edge_time = []
with open('C:/users/playe/documents/northeastern/fall 2017/complex networks/edgelist_16-17.csv',newline='') as csvfile:
   reader = csv.reader(csvfile,delimiter=',',quotechar='|')
   next(reader)
   for row in reader:
       bipartite_edges.append((row[0],row[1]))

with open('C:/users/playe/documents/northeastern/fall 2017/complex networks/nodedata_16-17.csv',newline='') as csvfile:
    reader = csv.reader(csvfile,delimiter=',',quotechar='|')
    for row in reader:
        restaurant_nodes.append(row[0])

user_nodes = [x[0] for x in bipartite_edges]
rest_nodes = [x[1] for x in bipartite_edges]
G = nx.Graph()
G.add_nodes_from(user_nodes,bipartite=0)
G.add_nodes_from(rest_nodes,bipartite=1)
G.add_edges_from(bipartite_edges)
B = nx.projected_graph(G,rest_nodes)
B_users = nx.projected_graph(G,user_nodes)


#M = nx.degree_mixing_matrix(B)
#plt.figure(figsize=(10,10))
#plt.matshow(M,fignum=1,cmap='jet')
#plt.show()

#(x,y) = linear_degree_distribution(B,10)
#(xu,yu) = linear_degree_distribution(B_users,10)
#fit = sci_opt.curve_fit(ffit,x,y)
#fitu = sci_opt.curve_fit(ffit,xu,yu)
#y_fit = [ffit(i,fit[0][0],fit[0][1]) for i in x]
#yu_fit = [ffit(i,fitu[0][0],fitu[0][1]) for i in xu]
#(x1,y1) = log_degree_distribution(B,10)
#(x1u,y1u) = log_degree_distribution(B_users,10)
#plt.figure(figsize=(15,10))
#plt.loglog(x1,y1,marker='o',markersize=12,linestyle='none')
#plt.loglog(x1u,y1u,marker='o',markersize=12,linestyle='none')
##plt.loglog(x,y_fit,linestyle='--',linewidth=3)
##plt.loglog(xu,yu_fit,linestyle='--',linewidth=3)
#print(fit[0][1])
#print(fitu[0][1])
#plt.title('Degree Distributions of Projected Networks',fontsize=26,fontweight='bold')
#plt.xlabel('k',fontsize=22,fontweight='bold')
#plt.ylabel('P(k)',fontsize=22,fontweight='bold')
#plt.legend(['Restaurant Projection', 'User Projection'])
#plt.show()
##
#
#
#A = list(nx.to_edgelist(B))
#
#edges1 = [x[0] for x in A]
#edges2 = [x[1] for x in A]
#with open('C:/users/playe/documents/northeastern/fall 2017/complex networks/toronto_rest_projected_16-17.csv','w',newline='') as csvfile:
#   fieldnames = ['Node1','Node2']
#   writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#   writer.writeheader()
#   for i in range(0,len(edges1)):
#       writer.writerow({'Node1':edges1[i],'Node2':edges2[i]})
    