import osmnx as ox
import os
import math
import networkx as nx

import random
import time

import DB
import methods

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
            nodes = ox.distance.get_nearest_nodes(G, building[-1]["x"],building[-1]["y"])
            nodes= list(set(nodes))
            for node in nodes:
                nearest_nodes.update({node: building[0]})
    return nearest_nodes




def path_to_nearest(G,start_nodes_buildings,end_nodes_buildings,buildings,hospitals):
    path_to_nearest={}
    for node,building in start_nodes_buildings.items():
        is_Achivable=True
        Dijkstra_result = methods.Dijkstra_list_ends_nearest(G, node, list(end_nodes_buildings.keys()))
        if Dijkstra_result == False:
            is_Achivable = False
        if is_Achivable and (path_to_nearest.get(building)==None or path_to_nearest.get(building)[1]>Dijkstra_result[1]):
            path_to_nearest.update({building:Dijkstra_result})
    return path_to_nearest


def path_to_all(G,start_nodes_buildings,end_nodes_buildings,buildings,hospitals):
    path_to_all = {}
    for node_b, building in start_nodes_buildings.items():
        is_Achivable = True
        Dijkstra_result_dict = methods.Dijkstra_list_ends_short(G, node_b, list(end_nodes_buildings.keys()))
        for node_i, hospital in end_nodes_buildings.items():
            Dijkstra_result = Dijkstra_result_dict.get(node_i)
            # Dijkstra_result = methods.Dijkstra_one_end(G, node_b, node_h)
            # if Dijkstra_result==False:
            #     is_Achivable=False
            if path_to_all.get((building, hospital)) == None or path_to_all.get((building, hospital))[1] > \
                    Dijkstra_result[1]:
                path_to_all.update({(building, hospital): Dijkstra_result})
        print("done_to_all")
    return path_to_all


def path_to_all_maxlength(G, start_nodes_buildings, end_nodes_buildings, buildings, hospitals, maxlength):
    path_all=path_to_all(G, start_nodes_buildings, end_nodes_buildings, buildings, hospitals)
    path_filtered={}
    for key,path in path_all.items():
        if path[1]<maxlength:
            path_filtered.update({key:path})
    return path_filtered


def path_to_all_maxlength_from_path(path_all, buildings, hospitals,maxlength):
    path_filtered = {}
    for key, path in path_all.items():
        if path[1] < maxlength:
            path_filtered.update({key: path})
    return path_filtered



def path_back_and_foth(G,start_nodes_buildings,end_nodes_buildings,buildings,hospitals):
    # path={}
    # list_nodes_buildings=list(nodes_buildings.keys())
    # list_nodes_hospitals=list(nodes_hospitals.keys())
    # for node_b,building in nodes_buildings.item():
    #     for node_h,hospital in nodes_hospitalspitals.item():
    #         D=methods.Dijkstra_list_ends(G,node_b,list_nodes_hospitals)
    paths_BI=path_to_all(G,start_nodes_buildings,end_nodes_buildings,buildings,hospitals)

    paths_IB = path_to_all(G,end_nodes_buildings,start_nodes_buildings,buildings,hospitals)

    path_baf={}

    for building in buildings:
        for hospital in hospitals:
            path_BI=paths_BI.get((building[0],hospital[0]))
            path_IB=paths_IB.get((hospital[0], building[0]))
            if path_baf.get((building[0],hospital[0]))==None or path_baf.get((building[0],hospital[0]))>path_BI[1]+path_IB[1]:
                path_baf.update({(building[0],hospital[0]):[path_BI[0],path_IB[0],path_BI[1] + path_IB[1]]})

    for key,values in path_baf.items():
        print(key)
        print(values[0])
        print(values[1])
        print(values[2])
        print()
    return path_baf



def path_back_and_foth_maxlength(G,start_nodes_buildings,end_nodes_buildings,buildings,hospitals,maxlength):
    path_baf=path_back_and_foth(G,start_nodes_buildings,end_nodes_buildings,buildings,hospitals)

    path_filtered={}
    for key,path in path_baf.items():
        if path[2]<maxlength:
            path_filtered.update({key:path})
    return path_filtered


def path_back_and_foth_from_path(paths_BI,paths_IB, buildings,hospitals):
    path_baf = {}

    for building in buildings:
        for hospital in hospitals:
            path_BI = paths_BI.get((building[0], hospital[0]))
            path_IB = paths_IB.get((hospital[0], building[0]))
            if path_baf.get((building[0], hospital[0])) == None or path_baf.get((building[0], hospital[0])) > path_BI[
                1] + path_IB[1]:
                path_baf.update({(building[0], hospital[0]): [path_BI[0], path_IB[0], path_BI[1] + path_IB[1]]})
    return path_baf


def path_back_and_foth_from_path_maxlength(paths_BI,paths_IB, buildings,hospitals,maxlength):
    path_baf = {}

    for building in buildings:
        for hospital in hospitals:
            path_BI = paths_BI.get((building[0], hospital[0]))
            path_IB = paths_IB.get((hospital[0], building[0]))
            if path_baf.get((building[0], hospital[0])) == None or path_baf.get((building[0], hospital[0])) > path_BI[
                1] + path_IB[1]:
                path_baf.update({(building[0], hospital[0]): [path_BI[0], path_IB[0], path_BI[1] + path_IB[1]]})

    path_filtered = {}
    for key, path in path_baf.items():
        if path[2] < maxlength:
            path_filtered.update({key: path})

    return path_filtered


if __name__=='__main__':
    #Проверка Дейкстры
    Gtry=nx.MultiDiGraph()
    Gtry.add_nodes_from([1,2,3,4,5,6])
    Gtry.add_edges_from([(1,2,{"length":100}),(1,3,{"length":1}),(2,4,{"length":100}),(3,4,{"length":1}),(3,5,{"length":100}),(4,6,{"length":50})])
    path=methods.Dijkstra_list_ends(Gtry, 1, [5,6])
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


    path_from_B_to_H=path_to_all(G,nearest_nodes_buildings,nearest_nodes_hospitals,buildings,hospitals)
    path_from_H_to_B=path_to_all(G,nearest_nodes_hospitals,nearest_nodes_buildings,buildings,hospitals)

    p=path_back_and_foth_from_path(path_from_B_to_H,path_from_H_to_B,buildings,hospitals)
    print(p)

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
