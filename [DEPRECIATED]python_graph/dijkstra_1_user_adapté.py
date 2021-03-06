import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)



import numpy as np
from python_graph.class_vertice_graph import *
# Pour que ça fonctionne ne pas oublier de faire clic droit,
# "définir le répertoire courant en accord avec le fichier ouvert dans l'éditeur"
from queue import PriorityQueue as priorQ

def homemade_dijkstra(graph,start_index,type_cost=Edge.given_cost):

    for vertice in graph.list_of_vertices :
        vertice.visited = False
        vertice.priority = inf
        vertice.cost_dijkstra = inf
        vertice.antecedent = -inf

    PQ = priorQ() # initialisation file de priorité
    start_vertice = graph.list_of_vertices[start_index]
    start_vertice.priority = 0
    start_vertice.cost_dijkstra = 0
    start_vertice.visited = True
    PQ.put(start_vertice)
    # vertice de départ : priorité 0, coût 0 et déja visité
    n=0
    while PQ.empty() == False:
        n+=1
        if n%100000==0:
            print(n)
        top_vertice = PQ.get()
        # withdraws the upper element of the queue (lowest priority)
        for edge in top_vertice.edges_list :
            v=edge.linked[1]
            cost_between=type_cost(edge)
            if v.visited == False : #verifies if not visited yet

                new_cost = top_vertice.cost_dijkstra + cost_between
                # on calcule le coût du voyage pour aller vers v
                # en passant par top_vertice

                if new_cost < v.cost_dijkstra:
                # on la compare avec l'ancien coût
                    v.cost_dijkstra = new_cost
                    v.antecedent = top_vertice

                graph.list_of_vertices[top_vertice.index].visited = True
                # top vertice est maintenant visité
                v.priority = v.cost_dijkstra
                # on met v dans la file de priorite avec la priorite cost
                PQ.put(v)

def Homemade_path_finder(graph, start_index, end_index, type_cost=Edge.given_cost):
    """ Returns the list of vertices visited during the path from i to j. """

    homemade_dijkstra(graph, start_index, type_cost)
    path = [end_index]
    while path[-1] != start_index:
        path.append(graph.list_of_vertices[path[-1]].antecedent.index)
    path.reverse()
    return path

# Test"

# vertice0 = Vertice(0, (0,0))
# vertice1 = Vertice(1, (0,0))
# vertice2 = Vertice(2, (0,0))
# vertice3 = Vertice(3, (0,0))
# vertice4 = Vertice(4, (0,0))
# vertice5 = Vertice(5, (0,0))
# vertice0.neighbours_list([(vertice1,1), (vertice2,2)])
# vertice1.neighbours_list([(vertice3,1), (vertice0,1)])
# vertice2.neighbours_list([(vertice4,3), (vertice0,2)])
# vertice3.neighbours_list([(vertice5,4), (vertice4,1), (vertice1,1)])
# vertice4.neighbours_list([(vertice5,1), (vertice3,1), (vertice2,3)])
# vertice5.neighbours_list([(vertice3,4), (vertice4,1)])
#
# graph_test = Graph([vertice0,vertice1,vertice2,vertice3,vertice4,vertice5])
#
# print(Homemade_path_finder(graph_test,0,5))
#
# import cProfile
# import re
# cProfile.run('Homemade_path_finder(graph_test,0,5)')
