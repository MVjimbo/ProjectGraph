import osmnx as ox
import os
import math
import networkx as nx

import random

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


def path_from_B_to_H(G,start_nodes_buildings,end_nodes_hodpitals,buildings,hospitals):
    path_for_building={}
    for node,building in start_nodes_buildings.items():
        is_Achivable=True
        Dijkstra_result = methods.Dijkstra_list_ends_nearest(G, node, list(end_nodes_hodpitals.keys()))
        if Dijkstra_result == False:
            is_Achivable = False
        if is_Achivable and (path_for_building.get(building)==None or path_for_building.get(building)[1]>Dijkstra_result[1]):
            path_for_building.update({building:Dijkstra_result})
        # for node in value:
        #     Dijkstra_result=methods.Dijkstra(G,node,end_nodes_hodpitals.keys())
        #     if Dijkstra_result==False:
        #         is_Achivable=False
        #     if is_Achivable and Dijkstra_result[1]<min_len_way:
        #         min_way=Dijkstra_result[0]
        #         min_len_way=Dijkstra_result[1]
    for building,arr in path_for_building.items():
        print(building)
        print(arr[0])
        print(arr[1])
        print()


def path_from_H_to_B(G,start_nodes_hospitals,end_nodes_buildings,buildings,hospitals):
    path_for_hospitals={}
    for node,building in start_nodes_hospitals.items():
        is_Achivable=True
        Dijkstra_result = methods.Dijkstra_list_ends_nearest(G, node, list(end_nodes_buildings.keys()))
        if Dijkstra_result == False:
            is_Achivable = False
        if is_Achivable and (path_for_hospitals.get(building)==None or path_for_hospitals.get(building)[1]>Dijkstra_result[1]):
            path_for_hospitals.update({building:Dijkstra_result})
    for building, arr in path_for_hospitals.items():
        print(building)
        print(arr[0])
        print(arr[1])
        print()


def path_from_B_to_H_back(G,nodes_buildings,nodes_hodpitals,buildings,hospitals):
    path_from_B_to_H={}
    for node_b,building in nodes_buildings.items():
        is_Achivable=True
        Dijkstra_result_dict=methods.Dijkstra_list_ends(G,node_b,list(nodes_hodpitals.keys()))
        for node_h,hospital in nodes_hodpitals.items():
            Dijkstra_result=Dijkstra_result_dict.get(node_h)
            #Dijkstra_result = methods.Dijkstra_one_end(G, node_b, node_h)
            # if Dijkstra_result==False:
            #     is_Achivable=False
            if path_from_B_to_H.get((building,hospital))==None or path_from_B_to_H.get((building,hospital))[1]>Dijkstra_result[1]:
                path_from_B_to_H.update({(building,hospital): Dijkstra_result})
        print("Done hospitals")
    print("Done for buildings")

    path_from_H_to_B = {}
    for node_h, hospital in nodes_hodpitals.items():
        is_Achivable = True
        Dijkstra_result_dict = methods.Dijkstra_list_ends(G, node_h, list(nodes_buildings.keys()))
        for node_b, building in nodes_buildings.items():
            Dijkstra_result=Dijkstra_result_dict.get(node_b)
            # Dijkstra_result = methods.Dijkstra_one_end(G, node_h, node_b)
            # if Dijkstra_result == False:
            #     is_Achivable = False
            if path_from_H_to_B.get((hospital, building)) == None or path_from_H_to_B.get((hospital,building))[1]>Dijkstra_result[1]:
                path_from_H_to_B.update({(hospital,building): Dijkstra_result})
        print("Done buildings")
    print("Done for hospitals")
    print(len(path_from_B_to_H))
    print(len(path_from_H_to_B))

    path_back_and_foth={}

    for building in buildings:
        for hospital in hospitals:
            if path_back_and_foth.get((building[0],hospital[0]))==None or path_back_and_foth.get((building[0],hospital[0]))>path_from_B_to_H.get((building[0],hospital[0]))[1]+path_from_H_to_B.get((hospital[0],building[0]))[1]:
                path_back_and_foth.update({(building[0],hospital[0]):[path_from_B_to_H.get(
                    (building[0], hospital[0]))[0],path_from_H_to_B.get((hospital[0], building[0]))[0],path_from_B_to_H.get(
                    (building[0], hospital[0]))[1] + path_from_H_to_B.get((hospital[0], building[0]))[1]]})

    for key,values in path_back_and_foth.items():
        print(key)
        print(values[0])
        print(values[1])
        print(values[2])
        print()


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
    buildings=random.sample(DB.getBuildings(),5)
    hospitals=random.sample(DB.getHospitals(),3)
    nearest_nodes_hospitals=get_nearest_nodes(G,hospitals)
    print(nearest_nodes_hospitals)
    nearest_nodes_buildings=get_nearest_nodes(G,buildings)
    path_from_B_to_H_back(G,nearest_nodes_buildings,nearest_nodes_hospitals,buildings,hospitals)






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
