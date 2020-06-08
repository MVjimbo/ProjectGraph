import Path_methods

def min_max_BI(G,start_nodes_buildings,end_nodes_buildings,buildings,infrastructure):
    path_to_all=Path_methods.path_to_all(G,start_nodes_buildings,end_nodes_buildings,buildings,infrastructure)

    max_path={}
    for inf_building in infrastructure:
        for building in buildings:
            if max_path.get(inf_building[0])==None or max_path.get(inf_building[0])[1]<path_to_all.get((building[0],inf_building[0]))[1]:
                max_path.update({inf_building[0]:path_to_all.get((building[0],inf_building[0]))})

    min_max_path=[0,0]
    for inf_building in max_path.keys():
        if min_max_path[0]==0 or min_max_path[1][1]>max_path.get(inf_building)[1]:
            min_max_path[0]=inf_building
            min_max_path[1] = max_path.get(inf_building)
    print(min_max_path)

def min_max_from_path_BI(path_to_all,buildings,infrastructure):
    max_path={}
    for inf_building in infrastructure:
        for building in buildings:
            if max_path.get(inf_building[0])==None or max_path.get(inf_building[0])[1]<path_to_all.get((building[0],inf_building[0]))[1]:
                max_path.update({inf_building[0]:path_to_all.get((building[0],inf_building[0]))})

    min_max_path=[0,0]
    for inf_building in max_path.keys():
        if min_max_path[0]==0 or min_max_path[1][1]>max_path.get(inf_building)[1]:
            min_max_path[0]=inf_building
            min_max_path[1] = max_path.get(inf_building)
    print(min_max_path)



def min_max_IB(G,start_nodes_buildings,end_nodes_buildings,buildings,infrastructure):
    path_to_all=Path_methods.path_to_all(G,start_nodes_buildings,end_nodes_buildings,buildings,infrastructure)

    max_path={}
    for inf_building in infrastructure:
        for building in buildings:
            if max_path.get(inf_building[0])==None or max_path.get(inf_building[0])[1]<path_to_all.get((inf_building[0],building[0]))[1]:
                max_path.update({inf_building[0]:path_to_all.get((inf_building[0],building[0]))})

    min_max_path=[0,0]
    for inf_building in max_path.keys():
        if min_max_path[0]==0 or min_max_path[1][1]>max_path.get(inf_building)[1]:
            min_max_path[0]=inf_building
            min_max_path[1] = max_path.get(inf_building)
    print(min_max_path)

def min_max_from_path_IB(path_to_all,buildings,infrastructure):
    max_path={}
    for inf_building in infrastructure:
        for building in buildings:
            if max_path.get(inf_building[0])==None or max_path.get(inf_building[0])[1]<path_to_all.get((inf_building[0],building[0]))[1]:
                max_path.update({inf_building[0]:path_to_all.get((inf_building[0],building[0]))})

    min_max_path=[0,0]
    for inf_building in max_path.keys():
        if min_max_path[0]==0 or min_max_path[1][1]>max_path.get(inf_building)[1]:
            min_max_path[0]=inf_building
            min_max_path[1] = max_path.get(inf_building)
    print(min_max_path)



def min_max_back_and_forth(G,start_nodes_buildings,end_nodes_buildings,buildings,infrastructure):
    path_to_all=Path_methods.path_back_and_forth(G,start_nodes_buildings,end_nodes_buildings,buildings,infrastructure)

    max_path={}
    for inf_building in infrastructure:
        for building in buildings:
            if max_path.get(inf_building[0])==None or max_path.get(inf_building[0])[1]<path_to_all.get((building[0],inf_building[0]))[1]:
                max_path.update({inf_building[0]:path_to_all.get((building[0],inf_building[0]))})

    min_max_path=[0,0]

    for inf_building in max_path.keys():
        print(max_path.get(inf_building)[2])
        if min_max_path[0]==0 or min_max_path[1][2]>max_path.get(inf_building)[2]:
            min_max_path[0]=inf_building
            min_max_path[1] = max_path.get(inf_building)
    print(min_max_path)


def min_max_from_path_back_and_forth(path_to_all,buildings,infrastructure):
    max_path={}
    for inf_building in infrastructure:
        for building in buildings:
            if max_path.get(inf_building[0])==None or max_path.get(inf_building[0])[1]<path_to_all.get((building[0],inf_building[0]))[1]:
                max_path.update({inf_building[0]:path_to_all.get((building[0],inf_building[0]))})

    min_max_path=[0,0]
    for inf_building in max_path.keys():
        print(max_path.get(inf_building)[2])
        if min_max_path[0]==0 or min_max_path[1][2]>max_path.get(inf_building)[2]:
            min_max_path[0]=inf_building
            min_max_path[1] = max_path.get(inf_building)
    print(min_max_path)