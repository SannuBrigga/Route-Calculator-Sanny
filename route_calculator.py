import heapq
import random

# Inicializar la matriz 5x5
def inicializar_matriz():
    return [["🔳" for _ in range(5)] for _ in range(5)]

# Función para imprimir la matriz con guía visual
def imprimir_laberinto(lab):
    print("   0  1  2  3  4")  # Encabezado de las columnas
    for i in range(5):
        fila_str = str(i) + " "  # Encabezado de las filas
        fila_str += " ".join(lab[i])
        print(fila_str)

# Función para agregar entrada, salida y obstáculos
def agregar_entrada_salida_obstaculos(lab):
    entrada = input("Introduce la coordenada de entrada (x y): ")
    entrada_x, entrada_y = map(int, entrada.split())
    lab[entrada_x][entrada_y] = "🔽"
    
    salida = input("Introduce la coordenada de salida (x y): ")
    salida_x, salida_y = map(int, salida.split())
    lab[salida_x][salida_y] = '🏁'
    
    num_obstaculos = int(input("Introduce el número de obstáculos: "))
    for _ in range(num_obstaculos):
        while True:
            obstaculo = input("Introduce la coordenada del obstáculo (x y): ")
            obstaculo_x, obstaculo_y = map(int, obstaculo.split())
            if (0 <= obstaculo_x < 5) and (0 <= obstaculo_y < 5): # Verificar si está dentro de los límites
                if (obstaculo_x, obstaculo_y) != (entrada_x, entrada_y) and (obstaculo_x, obstaculo_y) != (salida_x, salida_y):
                    lab[obstaculo_x][obstaculo_y] = '🏢'
                    break
                else:
                    print("No se puede colocar un obstáculo en la coordenada de entrada o salida. Intenta de nuevo.")
            else:
                print("Coordenadas fuera de los límites de la matriz. Intenta de nuevo.")
    
    for _ in range(3):
        while True:
            bache_x = random.randint(0, 4)
            bache_y = random.randint(0, 4)
            if lab[bache_x][bache_y] == "🔳":
                lab[bache_x][bache_y] = '🗻'
                break

# Heurística Manhattan
def distancia_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Algoritmo A*
def a_estrella(lab, inicio, fin): #funcion A* que toma como parametro mi matriz, mi entrada y salida
    entrada_x, entrada_y = inicio # me guarda mi entrada en coordenadas x y
    salida_x, salida_y = fin #me guarda mi salida en coordenadas x y
    openset = [] # genera una variable con valor de una lista vacia
    heapq.heappush(openset, (0, entrada_x, entrada_y))#genera mi cola de prioridad, y emete dentro de mi lista vacia mi primer elementp de la cola de prioridad y entrada_x y entrada_y representa que estoy dentro de las oordenadas de mi inicio
    #(open_set,(f_score,(posicion x y)))
    viene_de = {}# se guarda en un diccionario las coordenadas que recorri
    g_score = { (i, j): float('inf') for i in range(5) for j in range(5) } #guarda todas mis filas y columnas con un valor inf.
    g_score[(entrada_x, entrada_y)] = 0 # le digo q vale 0, g score serria como mi costo, como ese paso o pasos a realizar ES G
    f_score = { (i, j): float('inf') for i in range(5) for j in range(5) } #guarda todas mis filas y columnas con un valor inf. ES F
    f_score[(entrada_x, entrada_y)] = distancia_manhattan(inicio, fin)

    while openset: # en el whilw se crea la variable esta, y sirve para crear una tipo lista para guardar valores//SE EJECUTA SIEMPRE MIENTRAS SEA TRUE, empiezo desde mi punto inicial
        _, x, y = heapq.heappop(openset)#toma la coordenada de menor valor de la cola openset // mientras mi conjunto abierto no este vacio

        if (x, y) == (salida_x, salida_y):# si x y que son mis valores recorridos son == al las coordenadas del final
            return reconstruir_camino(viene_de, (x, y))

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # son las direcciones en las cuales me puedo ir, van iterando
            nueva_x, nueva_y = x + dx, y + dy #nueva_x, nueva_y son las nuevas posiciones, que son la suma de la direccion y la coordenada actual, para ir moviendose
            #para verificar que se esta usando dentro de mi laberinto
            if 0 <= nueva_x < 5 and 0 <= nueva_y < 5: #evalua que el movimiento que hago esta dentro de las coordenadas de mi laberinto
                if lab[nueva_x][nueva_y] == '🏢': # si la nueva cordenada es igual a la posicion de un edificio que ignore ese y continue calculando los otros nodos
                    continue

                # Paso 1: Obtener el g_score del nodo actual
                g_score_actual = g_score[(x, y)]

                # Paso 2: Determinar el costo del movimiento al nodo vecino
                if lab[nueva_x][nueva_y] == '🗻':
                    costo_movimiento = 2
                else:
                    costo_movimiento = 1

                # Paso 3: Calcular el g_score tentativo para el nodo vecino
                tentative_g_score = g_score_actual + costo_movimiento 

                if tentative_g_score < g_score[(nueva_x, nueva_y)]:# esta condicion si se cumple porque el valor tentativo sempre es menor que el valor inf
                    viene_de[(nueva_x, nueva_y)] = (x, y)
                    g_score[(nueva_x, nueva_y)] = tentative_g_score
                    h_score=distancia_manhattan((nueva_x, nueva_y), fin)
                    f_score[(nueva_x, nueva_y)] = tentative_g_score + h_score
                    heapq.heappush(openset, (f_score[(nueva_x, nueva_y)], nueva_x, nueva_y))

    return None

# Reconstrucción del camino
def reconstruir_camino(viene_de, actual):
    camino = []
    while actual in viene_de:
        camino.append(actual)
        actual = viene_de[actual]
    camino.reverse()
    return camino

# Ejemplo de uso
laberinto = inicializar_matriz()

print("Matriz inicial:")
imprimir_laberinto(laberinto)

agregar_entrada_salida_obstaculos(laberinto)

print("\nMatriz final con entrada, salida, obstáculos y baches:")
imprimir_laberinto(laberinto)

# Determinar las coordenadas de inicio y fin
inicio = [(i, fila.index("🔽")) for i, fila in enumerate(laberinto) if "🔽" in fila][0]
fin = [(i, fila.index('🏁')) for i, fila in enumerate(laberinto) if '🏁' in fila][0]

# Encontrar el camino usando A*
camino = a_estrella(laberinto, inicio, fin)

# Marcar el camino en la matriz
if camino:
    for x, y in camino:
        if laberinto[x][y] == "🔳":
            laberinto[x][y] = '🔸'
else:
    print("No se encontró un camino.")

# Mostrar la matriz resultante
print("\nMatriz con el camino encontrado:")
imprimir_laberinto(laberinto)
