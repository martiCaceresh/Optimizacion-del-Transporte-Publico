import numpy as np
import copy
import sys
from numpy import loadtxt

#datos = loadtxt('matriz.txt')
#nodos=len(datos)

distancias=[[0,101,42,76,24,38,89,110],
		    [101,0,107,39,77,69,92,33],
			[42,107,0,72,52,38,97,116],
			[76,39,72,0,86,38,131,44],
			[24,77,52,86,0,48,65,86],
			[38,69,38,38,48,0,93,78],
			[89,92,97,131,65,93,0,125],
			[110,33,116,44,86,78,125,0]]

pasajeros=[[0,9,6,10,4,54,21,51],
           [28,0,16,44,4,41,4,24],
		   [26,51,0,50,14,56,16,1],
		   [39,14,12,0,25,40,52,8],
		   [19,55,60,42,0,37,32,37],
		   [6,10,59,36,60,0,18,10],
		   [35,37,25,5,32,9,0,3],
		   [43,4,27,17,6,42,9,0]]

n_nodos=len(distancias)
nodos=range(n_nodos)
max_rutas=n_nodos-1
min_rutas=2
nodos_minimo=3
n_individuos=10
f_ecologia=0.5
n_participantes=3
pm=0.3
pc=0.9
n_iteraciones=10

def crear_grafo(nodos):
        grafo = [[0 for columna in range(nodos)]
                      for fila in range(nodos)]
	return grafo

def imprimir(dist):
            print ([dist[nodo] for nodo in range(n_nodos)])

def distancia_min(dist, nv):

        min = sys.maxint

        for n in range(n_nodos):
            if dist[n] < min and nv[n] == False:
                min = dist[n]
                min_indice = n

        return min_indice

def dijkstra(inicio,grafo,matriz_dist):

        dist = [sys.maxint] * n_nodos
        dist[inicio] = 0
        nv = [False] * n_nodos

        for cout in range(n_nodos):

            u = distancia_min(dist, nv)

            nv[u] = True

            for v in range(n_nodos):
                if grafo[u][v] > 0 and nv[v] == False and dist[v] > dist[u] + grafo[u][v]:
                        dist[v] = dist[u] + grafo[u][v]

	matriz_dist.append(dist)
        #imprimir(dist)

def iniciar_dijkstra(grafo):
	matriz_dist=[]
	for i in range(n_nodos):
		dijkstra(i,grafo,matriz_dist)

	return matriz_dist


grafo=crear_grafo(n_nodos)
grafo = distancias
m_distancias=iniciar_dijkstra(grafo)


def buscar(nodo,nodos_totales):
	size=len(nodos_totales)
	i=0
	while i<size:
		if nodos_totales[i]==nodo:
			nodos_totales.remove(nodo)
			return nodos_totales
		i+=1

	return nodos_totales

def validar(linea,nodos_totales):
	for i in range(len(linea)):
		nodos_totales=buscar(linea[i],nodos_totales)

	return nodos_totales

def individuo_valido(individuo):
	nodos_totales=copy.copy(nodos)
	for i in range(len(individuo)):
		nodos_totales=validar(individuo[i],nodos_totales)

	return not len(nodos_totales)

def generar_ruta():
	ruta=[]
	size_ruta=np.random.randint(nodos_minimo,n_nodos)
	temp=copy.copy(nodos)
	for j in range(size_ruta):
		nodo=np.random.choice(temp)
		temp.remove(nodo)
		ruta.append(nodo)

	return ruta

def generar_lineas(n_lineas):
	lineas=[]
	for i in range(n_lineas):
		lineas.append(generar_ruta())

	return lineas, individuo_valido(lineas)

def generar_poblacion(size):
	poblacion=[]
	i=0
	while i<size:
		size_lineas=np.random.randint(min_rutas,max_rutas)
		lineas,valido=generar_lineas(size_lineas)
		while not valido:
			mutacion_individual(lineas)
			valido=individuo_valido(lineas)

		poblacion.append(lineas)
		i+=1

	return poblacion

def mutar():
	nueva_ruta=[]
	longitud_ruta=np.random.randint(nodos_minimo,n_nodos)
	lista_nodos=copy.copy(nodos)
	for i in range(longitud_ruta):
		nodo=np.random.choice(lista_nodos)
		lista_nodos.remove(nodo)
		nueva_ruta.append(nodo)

	return nueva_ruta

def mutacion(individuo,long_original):
	nueva_longitud=np.random.randint(min_rutas,max_rutas)
	if nueva_longitud<long_original:
		for i in range(nueva_longitud):
			aleatorio=np.random.uniform(0,1)
			if aleatorio<pm:
				individuo[i]=mutar()
		del individuo[nueva_longitud:]
	else:
		j=0
		for i in range(nueva_longitud):
			if j<long_original:
				aleatorio=np.random.uniform(0,1)
 				if aleatorio<pm:
 					individuo[i]=mutar()
				j+=1
			else:
				individuo.append(mutar())


def mutacion_individual(individuo):
	longitud=len(individuo)
	aleatorio=np.random.uniform(0,1)
	if aleatorio<pm:
		mutacion(individuo,longitud)

def mutacion_poblacion(poblacion):
	for i in range(n_individuos):
		mutacion_individual(poblacion[i])

def fitness(individuo,m_distancias):
	temp=copy.copy(m_distancias)
	for i in range(len(individuo)):
		for j in range(len(individuo[i])-1):
			temp[individuo[i][j]][individuo[i][j+1]]=temp[individuo[i][j]][individuo[i][j+1]]+5

	fit=0
	for i in range(n_nodos):
		for j in range(n_nodos):
			if i!=j:
				temp[i][j]=(1.0*(pasajeros[i][j]))/temp[i][j]
				fit=fit+temp[i][j]

	return fit


def calc_fitness(individuo,f_e):
	fit=fitness(individuo,m_distancias)
	es_valido=individuo_valido(individuo)
	penalizacion_inv=0
	if not es_valido:
		penalizacion_inv=10000
	penalizacion=fit*f_e
	optimizacion=fit-penalizacion-penalizacion_inv
	return optimizacion

def torneo(poblacion,participantes,f_e):
	indice_part=[]
	for i in range(participantes):
		indice_part.append(np.random.randint(n_individuos))

	minimo=-1000000000
	for i in indice_part:
		fit=calc_fitness(poblacion[i],f_e)
    	if fit>minimo:
			minimo=fit
			indice_win=i

	return indice_win

def repetidos(ruta,nodo):
	for i in range(len(ruta)):
		if nodo==ruta[i]:
			return True

	return False

def cruce(individuo1,individuo2):
	hijo=[]
	long1=np.random.randint(len(individuo1))
	long2=np.random.randint(len(individuo2))
	while long1+long2<3: #minimo de nodos en una ruta
		long1=np.random.randint(len(individuo1))
		long2=np.random.randint(len(individuo2))

	ind_elegido1=copy.copy(individuo1)
	ind_elegido2=copy.copy(individuo2)
	for i in range(long1):
		nodo=np.random.choice(ind_elegido1)
		ind_elegido1.remove(nodo)
		hijo.append(nodo)

	for i in range(long2):
		nodo=np.random.choice(ind_elegido2)
		ind_elegido2.remove(nodo)
		if not repetidos(hijo,nodo):
			hijo.append(nodo)

	return hijo

def cruzar(individuo1,individuo2):
	aleatorio=np.random.uniform(0,1)
	if aleatorio<pc:
		pos_cruce1=np.random.randint(len(individuo1))
		pos_cruce2=np.random.randint(len(individuo2))
		temp=cruce(individuo1[pos_cruce1],individuo2[pos_cruce2])
		individuo2[pos_cruce2]=cruce(individuo1[pos_cruce1],individuo2[pos_cruce2])
		individuo1[pos_cruce1]=temp

def cruzamiento(poblacion,participantes,f_e):
	for i in range(n_individuos/2):
		ip1=torneo(poblacion,participantes,f_e)
		ip2=torneo(poblacion,participantes,f_e)
		cruzar(poblacion[ip1],poblacion[ip2])

	return poblacion

def validar_poblacion(poblacion):
	for i in range(n_individuos):
		valido=individuo_valido(poblacion[i])
		while not valido:
			mutacion_individual(poblacion[i])
			valido=individuo_valido(poblacion[i])

def algorimo_genetico(n_individuos,f_ecologia,n_participantes,n_iteraciones):
	poblacion=generar_poblacion(n_individuos)
	for i in range(n_iteraciones):
		poblacion=cruzamiento(poblacion,n_participantes,f_ecologia)
		mutacion_poblacion(poblacion)
		validar_poblacion(poblacion)

	print
	for i in range(n_individuos):
		print poblacion[i]

algorimo_genetico(n_individuos,f_ecologia,n_participantes,n_iteraciones)
