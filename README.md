# Red de ciudades en Python - Unidad 3 (Grafos)

Asignatura: Algoritmos y Estructuras de Datos (Ciencia de Datos), UPS
Autor: Danny Pérez

Programa de consola que representa una red de ciudades del Ecuador unidas por carreteras. Con esa red se hacen recorridos y se calcula la ruta más corta usando grafos.

## Cómo ejecutarlo

1. Tener Python 3 instalado. No hace falta instalar nada más.
2. Descargar o clonar el repositorio y abrir la carpeta en la terminal.
3. Correr:

```
python main.py
```

En Windows también funciona `py main.py`. La red ya viene cargada, solo se elige una opción del menú.

## Archivos

- `main.py`: el menú y la red de ejemplo.
- `utilidades.py`: la clase `GrafoPonderado`, el BFS, el Dijkstra que dio el profe y las funciones para sacar las rutas.
- `README.md`: este archivo.

## La red de ejemplo (9 ciudades y 11 rutas)

| Ruta | Distancia (km) |
|---|---|
| Quito - Latacunga | 90 |
| Latacunga - Ambato | 45 |
| Quito - Ambato | 130 |
| Quito - Ibarra | 115 |
| Ambato - Riobamba | 55 |
| Riobamba - Cuenca | 230 |
| Riobamba - Macas | 190 |
| Quito - Guayaquil | 420 |
| Guayaquil - Cuenca | 200 |
| Cuenca - Macas | 215 |
| Cuenca - Loja | 205 |

## Qué hace cada requerimiento

**R1 (opción 1).** La red se guarda con lista de adyacencia: un diccionario donde cada ciudad tiene una lista de tuplas `(ciudad vecina, km)`. También muestra el grado de cada ciudad, que es con cuántas ciudades se conecta directo.

**R2 (opción 2).** Hace un BFS desde la ciudad que se elija y muestra a cuántas escalas está cada ciudad. Al final dice si la red está completamente conectada o si alguna ciudad quedó aislada. Con las opciones 5 y 6 se puede agregar una ciudad sin rutas para probar ese caso.

**R3 (opción 3).** Usa el Dijkstra que entregó el profe, sin cambiarlo. Muestra la distancia mínima en km hasta cada ciudad y dice cuál es la más cercana y cuál la más lejana.

**R4 (opción 4).** Compara la ruta con menos escalas (BFS) con la ruta de menos km (Dijkstra). Por ejemplo, de Quito a Cuenca:

- Menos escalas: Quito -> Guayaquil -> Cuenca (2 escalas, 620 km)
- Menos km: Quito -> Ambato -> Riobamba -> Cuenca (3 escalas, 415 km)

## Complejidades

| Operación | Complejidad |
|---|---|
| Grado de todas las ciudades (R1) | O(V) |
| BFS (R2) | O(V + E) |
| Dijkstra (R3) | O((V + E) log V) |
| Comparación (R4) | O((V + E) log V) |
