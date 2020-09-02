import os
import sys
import random
import numpy as np
import networkx as nx
from dllist import Node, DoublyLinkedList

def update_last_occupied():
    global last_occupied
    while last_occupied >= 0:
        if bins[last_occupied].start_node != None:
            break
        last_occupied -= 1

def remove_from_graph(node):
    global last_occupied, to_go
    for x in g.predecessors(node.item):
        if dll_nodes[x] != None and in_degree[x] != 0:
            out_degree[x] -= 1
            v = abs(out_degree[x] + 1 - in_degree[x])
            bins[v].delete(dll_nodes[x])
            if out_degree[x] == 0:
                sinks.append(dll_nodes[x])
            else:
                v2 = abs(out_degree[x] - in_degree[x])
                bins[v2].insert(dll_nodes[x])
                if v2 > last_occupied:
                    last_occupied = v2
    for x in g.successors(node.item):
        if dll_nodes[x] != None and out_degree != 0:
            in_degree[x] -= 1
            v = abs(out_degree[x] - in_degree[x] - 1)
            bins[v].delete(dll_nodes[x])
            if in_degree[x] == 0:
                sources.append(dll_nodes[x])
            else:
                v2 = abs(out_degree[x] - in_degree[x])
                bins[v2].insert(dll_nodes[x])
                if v2 > last_occupied:
                    last_occupied = v2

    v = abs(out_degree[node.item] - in_degree[node.item])
    if in_degree[node.item] != 0 and out_degree[node.item] != 0:
        bins[v].delete(node)
    dll_nodes[node.item] = None
    update_last_occupied()

filepath = sys.argv[1]
filename = filepath.split('/')[-1]
resultpath = sys.argv[2]

#read graph from file and create lists and variables
g = nx.read_edgelist(filepath, create_using=nx.DiGraph(), nodetype=int)
nodes = list(g.nodes)
nodes.sort()
n = len(nodes)
left = []
s1 = []
s2 = []
in_degree = []
out_degree = []
sinks = []
sources = []
dll_nodes = []
bins = []
last_occupied = -1
to_go = n

#create bins
for i in range(n-1):
    bins.append(DoublyLinkedList())

#add each node to bin or source/sink list
for node in nodes:
    outd = len(list(g.successors(node)))
    ind = len(list(g.predecessors(node)))
    in_degree.append(ind)
    out_degree.append(outd)
    dll_node = Node(node)
    dll_nodes.append(dll_node)
    if outd == 0:
        sinks.append(dll_node)
    elif ind == 0:
        sources.append(dll_node)
    else:
        v = abs(outd - ind)
        if last_occupied < v:
            last_occupied = v
        bins[v].insert(dll_node)

#main loop of ELS-Abs algorithm
while to_go != 0:
    if len(sinks) != 0:
        chosen = sinks[-1]
        s2.append(chosen.item)
        sinks = sinks[:-1]
    elif len(sources) != 0:
        chosen = sources[-1]
        s1.append(chosen.item)
        sources = sources[:-1]
    else:
        chosen = bins[last_occupied].start_node
        if(out_degree[chosen.item] > in_degree[chosen.item]):
            s1.append(chosen.item)
        else:
            s2.append(chosen.item)
    remove_from_graph(chosen)
    to_go -= 1

#append s1 and s2
s2 = s2[::-1]
s = s1 + s2

dll_nodes = []
init_order = []
#create result double linked list
for node in nodes:
    dll_node = Node(node)
    dll_nodes.append(dll_node)
for node in s:
    init_order.append(dll_nodes[node])
result = DoublyLinkedList(init_order)

#main loop of sift sort algorithm
for node in s:
    result.delete(dll_nodes[node])
    best_result = 0
    prev = None
    node_list = result.to_list()
    for x in node_list:
        if node in g[x]:
            best_result += 1
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
sorted_nodes = result.to_list()
visited = np.zeros(len(nodes))
for node in sorted_nodes:
    visited[node] = True
    for neigh in g[node]:
        if visited[neigh]:
            left.append((node, neigh))

#save result to file
with open('{}/{}'.format(resultpath, filename), 'w') as f:
    f.write("{}\n".format(len(left)))
    f.write("\n".join("{} {}".format(arc[0],arc[1]) for arc in left))

