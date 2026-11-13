# utilidades.py
# Funciones de la Unidad 3 (Grafos) para la red de ciudades
# Danny Perez - Algoritmos y Estructuras de Datos
import heapq
from collections import deque


# R1: el grafo con lista de adyacencia
# cada ciudad guarda una lista de tuplas (ciudad vecina, km)
class GrafoPonderado:
    def __init__(self):
        self.grafo = {}

    def add_ciudad(self, ciudad):
        # O(1)
        if ciudad not in self.grafo:
            self.grafo[ciudad] = []
            return True
        print(f"La ciudad {ciudad} ya existe")
        return False

    def add_ruta(self, origen, destino, km):
        if origen not in self.grafo or destino not in self.grafo:
            print("Error: alguna de las ciudades no existe")
            return False
        if origen == destino:
            print("Error: no se puede unir una ciudad con ella misma")
            return False
        for vecino, _ in self.grafo[origen]:
            if vecino == destino:
                print(f"La ruta {origen} - {destino} ya existe")
                return False
        # las carreteras son de ida y vuelta, entonces se guarda en las dos
        self.grafo[origen].append((destino, km))
        self.grafo[destino].append((origen, km))
        return True

    def list_ciudad(self):
        print(list(self.grafo.keys()))

    def list_rutas_desde(self, ciudad):
        if ciudad not in self.grafo:
            print(f"La ciudad {ciudad} no existe")
            return False
        print(f"Rutas desde {ciudad}:")
        for vecino, km in self.grafo[ciudad]:
            print(f"{vecino} - {km} km")
        return True

    def grado(self, ciudad):
        # el grado es cuantos vecinos tiene la ciudad: O(1)
        return len(self.grafo[ciudad])

    def mostrar_grados(self):
        # recorre todas las ciudades: O(V)
        print("Grado de cada ciudad (con cuantas ciudades conecta directo):")
        suma = 0
        for ciudad in self.grafo:
            print(f"  {ciudad}: {self.grado(ciudad)}")
            suma += self.grado(ciudad)
        print(f"La suma de los grados es {suma}, que es el doble de {suma // 2} rutas")


# R2: BFS
def bfs(grafo, origen):
    # BFS: O(V + E)
    # escalas sirve tambien como visitados
    escalas = {origen: 0}
    padre = {origen: None}
    cola = deque([origen])
    while cola:
        v = cola.popleft()
        for vecino, km in grafo[v]:
            if vecino not in escalas:
                escalas[vecino] = escalas[v] + 1
                padre[vecino] = v
                cola.append(vecino)
    return escalas, padre


def esta_conectada(grafo, escalas):
    # si el BFS llego a todas las ciudades entonces la red esta conectada
    return len(escalas) == len(grafo)


def camino_bfs(padre, destino):
    # armo el camino con el diccionario de padres, de atras para adelante: O(V)
    if destino not in padre:
        return None
    camino = []
    v = destino
    while v is not None:
        camino.append(v)
        v = padre[v]
    return camino[::-1]


# R3: Dijkstra (el codigo que dio el profe, tal cual)
def dijkstra(grafo, origen):
    """Devuelve {ciudad: distancia_minima_desde_origen}."""
    # Dijkstra: O((V + E) log V)
    dist = {ciudad: float('inf') for ciudad in grafo}
    dist[origen] = 0
    heap = [(0, origen)]  # cola de prioridad
    while heap:
        d, u = heapq.heappop(heap)  # el mas cercano pendiente
        if d > dist[u]:
            continue  # ya teniamos una ruta mejor
        for vecino, peso in grafo[u]:
            if dist[u] + peso < dist[vecino]:  # relajacion
                dist[vecino] = dist[u] + peso
                heapq.heappush(heap, (dist[vecino], vecino))
    return dist


def camino_minimo_km(grafo, dist, origen, destino):
    # El Dijkstra del profe solo devuelve distancias y no la ruta.
    # Para no tocarlo, voy del destino hacia atras buscando el vecino
    # que cumpla dist[vecino] + peso == dist[actual]. O(V + E)
    if dist[destino] == float('inf'):
        return None
    camino = [destino]
    actual = destino
    while actual != origen:
        for vecino, peso in grafo[actual]:
            if dist[vecino] + peso == dist[actual]:
                camino.append(vecino)
                actual = vecino
                break
    return camino[::-1]


# para el menu: busca la ciudad sin importar mayusculas
def buscar_ciudad(grafo, texto):
    for ciudad in grafo:
        if ciudad.lower() == texto.strip().lower():
            return ciudad
    return None
