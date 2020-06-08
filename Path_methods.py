import Dijkstra_methods

def path_to_nearest(G,start_nodes_buildings,end_nodes_buildings,buildings,hospitals):
    path_to_nearest={}
    for node,building in start_nodes_buildings.items():
        is_Achivable=True
        Dijkstra_result = Dijkstra_methods.Dijkstra_list_ends_nearest(G, node, list(end_nodes_buildings.keys()))
        if Dijkstra_result == False:
            is_Achivable = False
        if is_Achivable and (path_to_nearest.get(building)==None or path_to_nearest.get(building)[1]>Dijkstra_result[1]):
            path_to_nearest.update({building:Dijkstra_result})
    return path_to_nearest


def path_to_all(G,start_nodes_buildings,end_nodes_buildings,buildings,hospitals):
    path_to_all = {}
    for node_b, building in start_nodes_buildings.items():
        is_Achivable = True
        Dijkstra_result_dict = Dijkstra_methods.Dijkstra_list_ends_short(G, node_b, list(end_nodes_buildings.keys()))
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



def path_back_and_forth(G,start_nodes_buildings,end_nodes_buildings,buildings,hospitals):
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

    return path_baf



def path_back_and_forth_maxlength(G,start_nodes_buildings,end_nodes_buildings,buildings,hospitals,maxlength):
    path_baf=path_back_and_foth(G,start_nodes_buildings,end_nodes_buildings,buildings,hospitals)

    path_filtered={}
    for key,path in path_baf.items():
        if path[2]<maxlength:
            path_filtered.update({key:path})
    return path_filtered


def path_back_and_forth_from_path(paths_BI,paths_IB, buildings,hospitals):
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