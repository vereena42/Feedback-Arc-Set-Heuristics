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
visited = np.zeros(len(g.nodes))
nodes = list(g.nodes)

#create random linear ordering of nodes
random.shuffle(nodes)

#create lists of leftward and rightward arcs
left = []
right = []
for node in nodes:
    visited[node] = True
    for neigh in g[node]:
        if visited[neigh]:
            left.append((node, neigh))
        else:
            right.append((node, neigh))

#save result to file
with open('{}/{}'.format(resultpath, filename), 'w') as f:
    if len(left) < len(right):
        f.write("{}\n".format(len(left)))
        f.write("\n".join("{} {}".format(arc[0],arc[1]) for arc in left))
    else:
        f.write("{}\n".format(len(right)))
        f.write("\n".join("{} {}".format(arc[0],arc[1]) for arc in right))

