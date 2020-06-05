import osmnx as ox
import os
import methods
import math
import networkx as nx

# matplotlib inline


def getGraph():
    G = ox.graph_from_place('Тюмень,Тюменская область,Ru', network_type='drive_service')
    ox.io.save_graphml(G,filepath='file\path')



if __name__=='__main__':
    #Проверка Дейкстры
    G=nx.MultiDiGraph()
    G.add_nodes_from([1,2,3,4])
    G.add_edges_from([(1,2,{"length":100}),(1,3,{"length":1}),(2,4,{"length":100}),(3,4,{"length":1})])
    path=methods.Dijkstra(G, 1, [4])
    print(path)
    #getGraph()   Запусти сначала эту функцию, она сохраняет граф, после этого можно функции ниже запускать
    #G=ox.io.load_graphml("C:\Python\ProjectG\data\g.graphml")  #Путь до файла
    #fig, ax = ox.plot_graph(ox.project_graph(G))





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
