# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 15:29:20 2017

@author: playe
"""

import csv
import numpy as np
import pandas as pd
import networkx as nx

#A = pd.read_csv('C:/users/playe/documents/northeastern/fall 2017/complex networks/toronto-2016-2017.csv')
#
#users = list(A['u_id'])
#latitude = list(A['b_latitude'])
#longtitude = list(A['b_longtitude'])
#business = list(A['b_name'])
#stars = list(A['b_stars'])
#categories = list(A['b_category'])
#time = list(A['t.date'])

users = []
latitude = []
longtitude = []
business = []
stars = []
categories = []
time = []

with open('C:/users/playe/documents/northeastern/fall 2017/complex networks/toronto_data.csv',newline='',encoding='utf8') as csvfile:
    reader = csv.reader(csvfile,delimiter=',',quotechar='|')
    next(reader) #skip header
    for row in reader:
        users.append(row[0])
        latitude.append(row[1])
        longtitude.append(row[2])
        business.append(row[3])
        stars.append(row[5])
        categories.append(row[6])
        time.append(row[7])

category_list = ['Restaurant','restaurant']

user_nodes = []
restaurant_nodes = []
restaurant_category = []
restaurant_location = []
bipart_edgelist = []
link_stars = []
link_time = []

genre_list = ['American','american','Barbecue','barbecue','Chinese','chinese','French',\
              'french','Hamburger','hamburger','Indian','indian','Italian','italian','Japanese',\
              'japanese','Mexican','mexican','Pizza','pizza','Seafood','seafood','Steak','steak',\
              'Sushi','sushi','Thai','thai']

#Create user/restaurant nodelists & node metadata
for i in range(0,len(users)-1):
    if any(x in categories[i] for x in category_list) and users[i] not in user_nodes:
        user_nodes.append(users[i])
    business_name = ''.join(q for q in business[i] if ord(q)<128)
    business_name.replace('"','')
    business_name.replace('&',' and ')
    if any(x in categories[i] for x in category_list) and business_name not in restaurant_nodes:
        restaurant_nodes.append(business_name)
        restaurant_location.append((latitude[i],longtitude[i]))
        test = False
        for j in range(0,int(len(genre_list)/2)):
            if genre_list[2*j] in categories[i] or genre_list[2*j+1] in categories[i]:
                genre = genre_list[2*j]
                test = True
        if not test:
            genre = 'Misc'
        restaurant_category.append(genre)

#Create bipartite edgelist & link data
for i in range(0,len(user_nodes)):
    idx_user = [j for j, x in enumerate(users) if x == user_nodes[i]]
    for k in range(0,len(idx_user)-1):
        business_name = ''.join(q for q in business[idx_user[k]] if ord(q)<128)
        business_name.replace('"','')
        business_name.replace('&',' and ')
        if business_name in restaurant_nodes:
            edge_tmp = (user_nodes[i],business_name)
            if type(edge_tmp) is tuple and len(edge_tmp) == 2:
                bipart_edgelist.append((user_nodes[i],business_name))
                link_stars.append(stars[idx_user[k]])
                link_time.append(time[idx_user[k]])
            
##writing to csv
#user_edges = [x[0] for x in bipart_edgelist]
#rest_edges = [x[1] for x in bipart_edgelist]
#with open('C:/users/playe/documents/northeastern/fall 2017/complex networks/edgelist_16-17.csv','w',newline='') as csvfile:
#   fieldnames = ['User', 'Restaurant','Stars','Date']
#   writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#   writer.writeheader()
#   for i in range(0,len(bipart_edgelist)):
#       writer.writerow({'User':user_edges[i],'Restaurant':rest_edges[i],'Stars':link_stars[i],'Date':link_time[i]})
#       
#with open('C:/users/playe/documents/northeastern/fall 2017/complex networks/nodedata_16-17.csv','w',newline='') as csvfile:
#    fieldnames = ['Restaurant','Category','Latitude','Longtitude']
#    writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
#    writer.writeheader()
#    for i in range(0,len(restaurant_nodes)):
#        writer.writerow({'Restaurant':restaurant_nodes[i],'Category':restaurant_category[i],'Latitude':restaurant_location[i][0],'Longtitude':restaurant_location[i][1]})