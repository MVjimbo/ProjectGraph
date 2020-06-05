def Dijkstra(G,start,end):
    len_shortest_way={node: 100000 for node in G.nodes()}
    len_shortest_way.update({start:0})

    previoust_node={}
    previoust_node.update({start:start})

    reading_node=start
    visited_nodes=[]
    nodes_to_visit=[start]

    while end.count(reading_node)==0 and len(nodes_to_visit)!=0:
        sort_len=[len_shortest_way[node] for node in nodes_to_visit]
        sort_len.sort()

        for node in nodes_to_visit:
            if len_shortest_way.get(node)==sort_len[0]:
                visited_nodes.append(reading_node)
                reading_node=node
                nodes_to_visit.remove(reading_node)
                break

        adjacent_nodes=[key for key in G[reading_node].keys()]

        adjacent_nodes=list(set(adjacent_nodes))

        for node in visited_nodes:
            if adjacent_nodes.count(node)>0:
                adjacent_nodes.remove(node)

        for node in adjacent_nodes:
            nodes_to_visit.append(node)

        nodes_to_visit=list(set(nodes_to_visit))

        for node in adjacent_nodes:
            if len_shortest_way.get(node)>len_shortest_way.get(reading_node)+G[reading_node][node][0]["length"]:
                length=len_shortest_way.get(reading_node) + G[reading_node][node][0]["length"]
                len_shortest_way.update({node:length})
                previoust_node.update({node:reading_node})

    shortest_way=[]
    shortest_way.append(reading_node)

    if (end.count(reading_node)==0):
        return False

    while (reading_node!=start):
        reading_node=previoust_node.get(reading_node)
        shortest_way.append(reading_node)
    shortest_way.reverse()
    return shortest_way