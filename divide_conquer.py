import os
import sys
import random
import numpy as np
import networkx as nx

def gain(i, V1, V2, G):
    if i in V1:
        n = 0
        o = 0
        for node in G[i]:
            if node in V1:
                n = n + 1
        for node in G.predecessors(i):
            if node in V2:
                o = o + 1
        return o - n
    n = 0
    o = 0
    for node in G[i]:
        if node in V1:
            o = o + 1
    for node in G.predecessors(i):
        if node in V2:
            n = n + 1
    return o - n
        

def perturb(V1, V2, G, p):
    S1 = []
    S2 = []
    nodes = list(G.nodes)
    random.shuffle(nodes)
    for i in nodes:
        if gain(i, V1, V2, G) > random.randint(p, 0):
            if i in V1 and len(V1) > 1:
                V1.remove(i)
                V2.add(i)
                S2.append(i)
            elif i in V2 and len(V2) > 1:
                V2.remove(i)
                V1.add(i)
                S1.append(i)
    while len(V1) > 0.6 * len(nodes) and len(V1) - len(V2) > 1:
        j = S1.pop()
        V1.remove(j)
        V2.add(j)
    while len(V2) > 0.6 * len(nodes) and len(V2) - len(V1) > 1:
        j = S2.pop()
        V2.remove(j)
        V1.add(j)
    return (V1, V2)

def cost(H, J, G):
    c = 0
    for j in J:
        for h in G[j]:
            if h in H:
                c = c + 1
    return c

def bisect(G):
    nodes = list(G.nodes)
    random.shuffle(nodes)
    middle_index = len(nodes)//2
    V1 = set(nodes[:middle_index])
    V2 = set(nodes[middle_index:])
    B1 = V1.copy()
    B2 = V2.copy()
    p = -1
    R = 10
    counter = 0
    while counter <= R and counter > - 100000:
        c_pre = cost(V1, V2, G)
        V1, V2 = perturb(V1, V2, G, p)
        c_post = cost(V1, V2, G)
        if c_post < c_pre:
            B1 = V1.copy()
            B2 = V2.copy()
            counter = counter - R
        else:
            if c_post > c_pre:
                V1 = B1.copy()
                V2 = B2.copy()
            counter = counter + 1
        if c_post == c_pre:
            p = p - 2
        else:
            p = -1
    return (B1, B2)
    

def back_edges(H, J, G):
    res = []
    for j in J:
        for h in G[j]:
            if h in H:
                res.append((j, h))
    return res

def fas(G):
    P = nx.strongly_connected_components(G)
    P2 = list(P)
    if len(P2) == 1:
        H, J = bisect(G)
        res = back_edges(H, J, G)
        if(len(H) > 1):
            res.extend(fas(nx.subgraph(G,H)))
        if len(J) > 1:
            res.extend(fas(nx.subgraph(G,J)))
    else:
        res = []
        for H in P2:
            if len(H) > 1:
                res.extend(fas(nx.subgraph(G,H)))
    return res

filepath = sys.argv[1]
filename = filepath.split('/')[-1]
resultpath = sys.argv[2]

#read graph from file and run divide-sonquer algorithm
g = nx.read_edgelist(filepath, create_using=nx.DiGraph(), nodetype=int)
left = fas(g)

#save result to file
with open('{}/{}'.format(resultpath, filename), 'w') as f:
    f.write("{}\n".format(len(left)))
    f.write("\n".join("{} {}".format(arc[0],arc[1]) for arc in left))
