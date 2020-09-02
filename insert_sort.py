import os
import sys
import random
import numpy as np
import networkx as nx
from dllist import Node, DoublyLinkedList

filepath = sys.argv[1]
filename = filepath.split('/')[-1]
resultpath = sys.argv[2]

#read graph from file and create lists and variables
g = nx.read_edgelist(filepath, create_using=nx.DiGraph(), nodetype=int)
nodes = list(g.nodes)
nodes.sort()
n = len(nodes)
left = []
dll_nodes = []
result = DoublyLinkedList()

#create DoubleLinkedList nodes for all vertices
for node in nodes:
    dll_node = Node(node)
    dll_nodes.append(dll_node)

#main loop of insert sort algorithm
for node in nodes:
    best_result = 0
    prev = None
    temp = result.start_node
    while temp is not None:
        if node in g[temp.item]:
            best_result += 1
        temp = temp.nref
    curr_result = best_result
    temp = result.start_node
    while temp is not None:
        if node in g[temp.item]:
            curr_result -= 1
        elif temp.item in g[node]:
            curr_result += 1
        if curr_result < best_result:
            best_result = curr_result
            prev = temp
        temp = temp.nref
    result.insert_after(dll_nodes[node], prev)

#create leftward arcs list
s = result.to_list()
visited = np.zeros(len(nodes))
for node in s:
    visited[node] = True
    for neigh in g[node]:
        if visited[neigh]:
            left.append((node, neigh))

#save result to file
with open('{}/{}'.format(resultpath, filename), 'w') as f:
    f.write("{}\n".format(len(left)))
    f.write("\n".join("{} {}".format(arc[0],arc[1]) for arc in left))
