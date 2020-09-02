import os
import sys
import random
import numpy as np
import networkx as nx

filepath = sys.argv[1]
filename = filepath.split('/')[-1]
resultpath = sys.argv[2]

#read graph from file
g = nx.read_edgelist(filepath, create_using=nx.DiGraph(), nodetype=int)
nodes = list(g.nodes)
visited = np.zeros(len(nodes))
edge_list = []

#create random linear ordering on vertices
random.shuffle(nodes)

#main loop of Berger-Shor algorithm
for node in nodes:
    left = []
    right = []
    visited[node] = True
    for neigh in g.predecessors(node):
        if visited[neigh] == False:
            left.append((neigh, node))
    for neigh in g.successors(node):
        if visited[neigh] == False:
            right.append((node, neigh))
    if len(right) < len(left):
        edge_list.extend(right)
    else:
        edge_list.extend(left)

#save result to file
with open('{}/{}'.format(resultpath, filename), 'w') as f:
    f.write("{}\n".format(len(edge_list)))
    f.write("\n".join("{} {}".format(arc[0],arc[1]) for arc in edge_list))

