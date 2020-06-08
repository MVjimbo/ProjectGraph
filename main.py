import osmnx as ox
import os
import math
import networkx as nx

import random
import time

import DB
import Dijkstra_methods
import Path_methods

# matplotlib inline

def getGraph():
    G = ox.graph_from_place('Тюмень,Тюменская область,Ru', network_type='drive_service')
    ox.io.save_graphml(G,filepath='file\path')

def get_nearest_nodes(G,buildings):
    nearest_nodes={}
    for building in buildings:
        if building[-1]["is_Pair"] == True:
            node=ox.distance.get_nearest_node(G,building[-1]["coordinates"])
            nearest_nodes.update({node:building[0]})
        else:
            X=0
            for i in building[-1].get('x'):
                X+=i
            X=X/len(building[-1].get('x'))
            Y=0
            for j in building[-1].get('y'):
                Y += j
            Y=Y/len(building[-1].get('y'))
            node = ox.distance.get_nearest_node(G,(Y,X))
            nearest_nodes.update({node: building[0]})

    return nearest_nodes





if __name__=='__main__':
    #Проверка Дейкстры
    Gtry=nx.MultiDiGraph()
    Gtry.add_nodes_from([1,2,3,4,5,6])
    Gtry.add_edges_from([(1,2,{"length":100}),(1,3,{"length":1}),(2,4,{"length":100}),(3,4,{"length":1}),(3,5,{"length":100}),(4,6,{"length":50})])
    path=Dijkstra_methods.Dijkstra_list_ends(Gtry, 1, [5,6])
    print(path)
    #getGraph()   Запусти сначала эту функцию, она сохраняет граф, после этого можно функции ниже запускать
    G=ox.io.load_graphml("C:\Python\ProjectG\data\g.graphml")  #Путь до файла
    #fig, ax = ox.plot_graph(ox.project_graph(G))
    buildings=random.sample(DB.getBuildings(),3)
    hospitals=random.sample(DB.getHospitals(),2)
    nearest_nodes_hospitals=get_nearest_nodes(G,hospitals)
    print(nearest_nodes_hospitals)
    nearest_nodes_buildings=get_nearest_nodes(G,buildings)
    print(nearest_nodes_buildings)

    sum_min_path(G,nearest_nodes_hospitals,nearest_nodes_buildings,buildings,hospitals)
    # path_from_B_to_H=path_to_all(G,nearest_nodes_buildings,nearest_nodes_hospitals,buildings,hospitals)
    # path_from_H_to_B=path_to_all(G,nearest_nodes_hospitals,nearest_nodes_buildings,buildings,hospitals)
    #
    # p=path_back_and_foth_from_path(path_from_B_to_H,path_from_H_to_B,buildings,hospitals)
    # print(p)

    # print(path_from_B_to_H)
    # print()
    # print(path_from_B_to_H_min)

    # for i,j in zip(path_new.items(),path_old.items()):
    #     if i[0]!=j[0] or i[1]!=j[1]:
    #         print("bruh")
    #         break





#G = ox.graph_from_place('Piedmont, California, USA', network_type='drive_service')
#ox.utils_graph.add_edge_lengths(G)
#for i in G.nodes(data=True):
#    for j in G.nodes(data=True):
#        if G.has_edge(i[0],j[0]):
#            G[i[0]][j[0]][0]["weight"]=math.sqrt(((i[1]['x']-j[1]['x'])*99257)**2+((i[1]['y']-j[1]['y'])*110806)**2)
#for i in G.nodes():
#    for j in G.nodes():
#        if G.has_edge(i,j):
           # print(G[i][j][0]['length'])
#a={}
#a.update({'a':'a'})
#print(a)
#ox.io.save_graphml(G)
# fig, ax = ox.plot_graph(ox.project_graph(G))
