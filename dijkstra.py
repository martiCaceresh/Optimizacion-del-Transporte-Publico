
import sys
from numpy import loadtxt

datos = loadtxt('matriz.txt')
  
nodos=len(datos)
def crear_grafo(nodos):
        grafo = [[0 for columna in range(nodos)] 
                      for fila in range(nodos)]
	return grafo

def imprimir(dist):
            print ([dist[nodo] for nodo in range(nodos)])
 
def distancia_min(dist, nv):
 
        min = sys.maxint
 
        for n in range(nodos):
            if dist[n] < min and nv[n] == False:
                min = dist[n]
                min_indice = n
 
        return min_indice
 
def dijkstra(inicio,grafo,matriz_dist):
        
        dist = [sys.maxint] * nodos
        dist[inicio] = 0
        nv = [False] * nodos
 
        for cout in range(nodos):
 
            u = distancia_min(dist, nv)

            nv[u] = True
 
            for v in range(nodos):
                if grafo[u][v] > 0 and nv[v] == False and dist[v] > dist[u] + grafo[u][v]:
                        dist[v] = dist[u] + grafo[u][v]
 
	matriz_dist.append(dist)
        imprimir(dist)

def iniciar(grafo):
	matriz_dist=[]
	for i in range(nodos):
		dijkstra(i,grafo,matriz_dist)

	return matriz_dist
 
grafo=crear_grafo(nodos)
grafo = datos;
m=iniciar(grafo);




