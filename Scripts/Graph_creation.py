
'''
It initializes empty lists and sets to store node features, node IDs, and edges.
For each root node (a node that tweeted a URL) in train_nodes:
a. If the root node has any neighbors, it adds the root node to the set of node IDs (Node_set).
b. It extracts the number of followers of the root node from a dictionary (Follower_cnt_dict_idx) and adds it to the node features along with a binary flag indicating whether the node tweeted a URL.
c. It iterates over the immediate neighbors of the root node (neighbours), adds them to the Node_set if they are not already in it, and adds the root node-neighbor edge to Level_1_Neighbours. It also extracts the number of followers of the neighbor node and adds it to the node features if it is not already in train_nodes.
d. It then iterates over the neighbors of the immediate neighbors (neighbour_l2) and adds them to Node_set if they are not already in it. It adds the neighbor-neighbor2 edge to Level_2_Neighbours and extracts the number of followers of the neighbor2 node and adds it to the node features if it is not already in train_nodes.
It deduplicates the edges in Level_1_Neighbours and Level_2_Neighbours and stores them in edge_list_dedup.
It creates a dictionary (node_index_idx) mapping each node ID to a unique index and stores the edges in edge_list_dedup as a list of tuples with the node indices instead of IDs (edge_list).
It creates the node features as a 2D tensor (features) with dimensions (num_nodes, num_node_features) and assigns the values from Node_Feature_list_sorted.
It creates a PyTorch Geometric Data object with the node features, edge indices, edge weights, and target label (y_val) and returns it.
'''


def Generate_Graph(train_nodes,y_val):
    """
    Generates a graph object for training a machine learning model based on the provided data.

    Args:
        train_nodes (list): A list of nodes that have tweeted a URL.
        y_val (int): The target variable value for the graph.

    Returns:
        graph_trn (torch_geometric.data.Data): A graph object containing node features and edge information for training a machine learning model.
    """

    Level_1_Neighbours = []

    Level_2_Neighbours = []

    Node_Feature_list = set()

    Node_set = set()


    for root_node in train_nodes:
        if root_node in similarity_dict_idx.keys():
            Node_set.add(root_node)

            follower_cnt = int(Follower_cnt_dict_idx.get(root_node,0))

            Node_Feature_list.add((root_node,follower_cnt,1))   ### add 2 features - 1 is follower cnt, 2 is binary flag that they tweeted url

            neighbours = similarity_dict_idx.get(root_node)
            for neighbour, weight in neighbours.items():
                if neighbour!=root_node:
                    Node_set.add(neighbour)
                    Level_1_Neighbours.append((root_node,neighbour,weight))
                    follower_cnt = int(Follower_cnt_dict_idx.get(neighbour,0))
                    if neighbour not in train_nodes:
                        Node_Feature_list.add((neighbour,follower_cnt,0))   ### add 2 features - 1 is follower cnt, 2 is binary flag that they tweeted url

                else:
                    continue
                if neighbour in  similarity_dict_idx.keys():
                    neighbour_l2 = similarity_dict_idx.get(neighbour)
                    for neighbour2, weight2 in neighbour_l2.items():
                        if neighbour!=neighbour2:
                            Node_set.add(neighbour2)
                            Level_2_Neighbours.append((neighbour,neighbour2,weight2))
                            follower_cnt = int(Follower_cnt_dict_idx.get(neighbour2,0))
                            if neighbour2 not in train_nodes:
                                Node_Feature_list.add((neighbour2,follower_cnt,0))   ### add 2 features - 1 is follower cnt, 2 is binary flag that they tweeted url

                        else:
                            continue
                
                
    #### IN aboe code we first identify immediate neighbours of nodes who tweeted a URL, Level_1_Neighbours
    #### then we first second level enighbours - Friend of Friend - stored in  Level_2_Neighbours          
    
    edge_list_1 = Level_1_Neighbours+Level_2_Neighbours  
    node_index_idx = {}

    for index,node in enumerate(Node_set):
    #     print(index,node)
        node_index_idx[node] = index

    edge_list_dedup_1 = list(set(edge_list_1))

    edge_list_dedup_2 = [(node_index_idx[w[0]],node_index_idx[w[1]],w[2]) for w in edge_list_dedup_1]
    edge_list_dedup = sorted(edge_list_dedup_2, key=lambda x: x[0])
    edge_weights = []
    for pairs in edge_list_dedup:
        edge_weights.append(pairs[2])
    edge_list = [w[:2] for w in edge_list_dedup]
    Node_Feature_list_tmp = []

    for node in Node_Feature_list:
        new_key = node_index_idx[node[0]]
        Node_Feature_list_tmp.append((new_key,node[1],node[2]))
    Node_Feature_list_sorted = sorted(Node_Feature_list_tmp, key=lambda x: x[0])
    features = torch.zeros((len(Node_Feature_list_sorted), 2))


    num_node_features = 2

    for node, feature_vector in enumerate(Node_Feature_list_sorted):
        try:
            features[node] = torch.tensor([int(feature_vector[1]),int(feature_vector[2])])
        except:
            print(node)
            break
    Num_nodes = len(features)
    graph_trn = Data(x=features, edge_index=torch.tensor(edge_list).T, edge_attr=torch.tensor(edge_weights), y = torch.tensor(y_val))
    return graph_trn
