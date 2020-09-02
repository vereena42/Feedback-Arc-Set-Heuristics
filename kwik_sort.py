import os
import sys
import random
import numpy as np
import networkx as nx

def quicksort(lo, hi):
    global nodes
    if lo < hi:
        lt = lo
        gt = hi
        i = lo
        p = random.randint(lo, hi)
        swapped = False
        while i <= gt:
            if nodes[p] in g[nodes[i]]:
                swapped = True
                t = nodes[lt]
                nodes[lt] = nodes[i]
                nodes[i] = t
                lt += 1
                i += 1
            elif nodes[i] in g[nodes[p]]:
                swapped = True
                t = nodes[i]
                nodes[i] = nodes[gt]
                nodes[gt] = t
                gt -= 1
            else:
                i += 1

        quicksort(lo, lt - 1)
        if swapped:
            quicksort(lt, gt)
        quicksort(gt + 1, hi)

filepath = sys.argv[1]
filename = filepath.split('/')[-1]
resultpath = sys.argv[2]

#read graph from file
g = nx.read_edgelist(filepath, create_using=nx.DiGraph(), nodetype=int)
nodes = list(g.nodes)
random.shuffle(nodes)
visited = np.zeros(len(nodes))
left = []

#run algorithm on graph
quicksort(0, len(nodes) - 1)

#create leftward arcs list
for node in nodes:
    visited[node] = True
    for neigh in g[node]:
        if visited[neigh]:
            left.append((node, neigh))

#save result to file
with open('{}/{}'.format(resultpath, filename), 'w') as f:
    f.write("{}\n".format(len(left)))
    f.write("\n".join("{} {}".format(arc[0],arc[1]) for arc in left))
