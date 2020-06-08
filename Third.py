import Path_methods

def sum_min_path(G,start_nodes_buildings,end_nodes_buildings,buildings,infrastructure):
    path_to_all=Path_methods.path_to_all(G,start_nodes_buildings,end_nodes_buildings,buildings,infrastructure)

    sum_min={inf_building[0]:0 for inf_building in infrastructure}
    for inf_building in infrastructure:
        for building in buildings:
            sum_min.update({inf_building[0]:sum_min.get(inf_building[0])+path_to_all.get((inf_building[0],building[0]))[1]})

    min_id=0
    min_value=1000000000
    for key,value in sum_min.items():
        if value<min_value:
            min_id=key
            min_value=value


    paths={}
    for building in buildings:
        paths.update({(min_id,building[0]):path_to_all.get((min_id,building[0]))})