# main.py
# Red de ciudades del Ecuador - Unidad 3 (Grafos)
# Danny Perez - Algoritmos y Estructuras de Datos
# Para correrlo: python main.py   (en Windows: py main.py)
from utilidades import (
    GrafoPonderado, bfs, esta_conectada, camino_bfs,
    dijkstra, camino_minimo_km, buscar_ciudad,
)


def cargar_red():
    # red de ejemplo ya cargada: 9 ciudades y 11 rutas (km aproximados)
    g = GrafoPonderado()
    ciudades = ["Quito", "Latacunga", "Ambato", "Riobamba", "Cuenca",
                "Guayaquil", "Macas", "Loja", "Ibarra"]
    for c in ciudades:
        g.add_ciudad(c)

    g.add_ruta("Quito", "Latacunga", 90)
    g.add_ruta("Latacunga", "Ambato", 45)
    g.add_ruta("Quito", "Ambato", 130)
    g.add_ruta("Quito", "Ibarra", 115)
    g.add_ruta("Ambato", "Riobamba", 55)
    g.add_ruta("Riobamba", "Cuenca", 230)
    g.add_ruta("Riobamba", "Macas", 190)
    g.add_ruta("Quito", "Guayaquil", 420)  # directa pero larga
    g.add_ruta("Guayaquil", "Cuenca", 200)
    g.add_ruta("Cuenca", "Macas", 215)
    g.add_ruta("Cuenca", "Loja", 205)
    return g


def pedir_ciudad(g, mensaje):
    while True:
        texto = input(mensaje)
        ciudad = buscar_ciudad(g.grafo, texto)
        if ciudad:
            return ciudad
        print(f"No existe '{texto}'. Las ciudades son: {', '.join(g.grafo)}")


def sumar_km(g, ruta):
    # suma los km de una ruta ciudad por ciudad
    total = 0
    for i in range(len(ruta) - 1):
        for vecino, km in g.grafo[ruta[i]]:
            if vecino == ruta[i + 1]:
                total += km
    return total


def opcion_r1(g):
    print("\n--- R1: la red (lista de adyacencia) ---")
    for ciudad, vecinos in g.grafo.items():
        print(f"{ciudad}: {vecinos}")
    print()
    g.mostrar_grados()


def opcion_r2(g):
    print("\n--- R2: recorrido BFS ---")
    origen = pedir_ciudad(g, "Ciudad de origen: ")
    escalas, padre = bfs(g.grafo, origen)  # BFS: O(V + E)

    print(f"\nCiudades que se alcanzan desde {origen}:")
    for ciudad, n in sorted(escalas.items(), key=lambda par: par[1]):
        if ciudad != origen:
            print(f"  {ciudad}: {n} escala(s)")

    if esta_conectada(g.grafo, escalas):
        print("\nLa red esta completamente conectada.")
    else:
        aisladas = [c for c in g.grafo if c not in escalas]
        print(f"\nLa red NO esta conectada. Desde {origen} no se llega a: {aisladas}")


def opcion_r3(g):
    print("\n--- R3: distancias minimas con Dijkstra ---")
    origen = pedir_ciudad(g, "Ciudad de origen: ")
    dist = dijkstra(g.grafo, origen)  # Dijkstra: O((V + E) log V)

    print(f"\nDistancia minima desde {origen}:")
    for ciudad, km in dist.items():
        if ciudad != origen:
            if km == float('inf'):
                print(f"  {ciudad}: no se llega")
            else:
                print(f"  {ciudad}: {km} km")

    alcanzables = {}
    for ciudad, km in dist.items():
        if ciudad != origen and km != float('inf'):
            alcanzables[ciudad] = km

    if alcanzables:
        cercana = min(alcanzables, key=alcanzables.get)
        lejana = max(alcanzables, key=alcanzables.get)
        print(f"\nLa mas cercana es {cercana} ({alcanzables[cercana]} km)")
        print(f"La mas lejana es {lejana} ({alcanzables[lejana]} km)")
    else:
        print("\nDesde esa ciudad no se llega a ninguna otra.")


def opcion_r4(g):
    print("\n--- R4: menos escalas (BFS) contra menos km (Dijkstra) ---")
    origen = pedir_ciudad(g, "Ciudad de origen (ej. Quito): ")
    destino = pedir_ciudad(g, "Ciudad de destino (ej. Cuenca): ")

    escalas, padre = bfs(g.grafo, origen)  # BFS: O(V + E)
    dist = dijkstra(g.grafo, origen)       # Dijkstra: O((V + E) log V)
    ruta_bfs = camino_bfs(padre, destino)
    ruta_km = camino_minimo_km(g.grafo, dist, origen, destino)

    if ruta_bfs is None or ruta_km is None:
        print(f"No hay ruta entre {origen} y {destino}.")
        return

    print(f"\nMenos escalas (BFS): {' -> '.join(ruta_bfs)}")
    print(f"  {escalas[destino]} escalas, {sumar_km(g, ruta_bfs)} km en total")
    print(f"\nMenos km (Dijkstra): {' -> '.join(ruta_km)}")
    print(f"  {len(ruta_km) - 1} escalas, {dist[destino]} km en total")

    if ruta_bfs == ruta_km:
        print("\nLas dos rutas son la misma.")
    else:
        print("\nLas rutas NO son la misma: el BFS solo cuenta saltos (cada carretera")
        print("vale 1) y Dijkstra suma los km de cada carretera.")


def opcion_agregar_ciudad(g):
    nombre = input("Nombre de la ciudad nueva: ").strip()
    if nombre:
        g.add_ciudad(nombre)
        print("Queda sin rutas, sirve para probar una red desconectada en el R2")


def opcion_agregar_ruta(g):
    a = pedir_ciudad(g, "Ciudad 1: ")
    b = pedir_ciudad(g, "Ciudad 2: ")
    try:
        km = int(input("Distancia en km: "))
    except ValueError:
        print("Tiene que ser un numero entero")
        return
    if km <= 0:
        print("La distancia tiene que ser mayor a 0")
        return
    g.add_ruta(a, b, km)


def menu():
    g = cargar_red()
    while True:
        print("\n======= RED DE CIUDADES =======")
        print("1. R1 - Ver la red y el grado de cada ciudad")
        print("2. R2 - Recorrido BFS")
        print("3. R3 - Distancias minimas (Dijkstra)")
        print("4. R4 - Comparar menos escalas y menos km")
        print("5. Agregar ciudad (para probar)")
        print("6. Agregar ruta (para probar)")
        print("0. Salir")
        opcion = input("Opcion: ").strip()

        if opcion == "1":
            opcion_r1(g)
        elif opcion == "2":
            opcion_r2(g)
        elif opcion == "3":
            opcion_r3(g)
        elif opcion == "4":
            opcion_r4(g)
        elif opcion == "5":
            opcion_agregar_ciudad(g)
        elif opcion == "6":
            opcion_agregar_ruta(g)
        elif opcion == "0":
            print("Chao")
            break
        else:
            print("Esa opcion no existe")


if __name__ == "__main__":
    menu()
