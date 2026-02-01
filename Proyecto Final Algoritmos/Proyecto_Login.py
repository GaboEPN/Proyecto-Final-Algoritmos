import os
import heapq

USUARIOS_FILE = "usuarios.txt"
CENTROS_FILE = "centros.txt"
RUTAS_FILE = "rutas.txt"

usuarios = []
centros = []
grafo = []

def inicializar_archivos():
    if not os.path.exists(USUARIOS_FILE):
        open(USUARIOS_FILE, "w").close()
    if not os.path.exists(CENTROS_FILE):
        open(CENTROS_FILE, "w").close()
    if not os.path.exists(RUTAS_FILE):
        open(RUTAS_FILE, "w").close()

def cargar_usuarios():
    usuarios.clear()
    with open(USUARIOS_FILE, "r") as f:
        for l in f:
            if l.strip():
                n, a, c, e, u, p, r = l.strip().split(",")
                usuarios.append({"user": u, "pass": p, "rol": r})

def password_segura(p):
    return any(c.isupper() for c in p) and any(c.islower() for c in p) and any(c.isdigit() for c in p)

def registrar_cliente():
    print("\n--- REGISTRO ---")
    nom = input("Nombres: ")
    ape = input("Apellidos: ")
    ced = input("Identificación: ")
    eda = input("Edad: ")
    usr = input("Usuario: ")
    pas = input("Contraseña: ")
    if not password_segura(pas):
        print("Error: Contraseña debe tener Mayúscula, Minúscula y Número.")
        return
    with open(USUARIOS_FILE, "a") as f:
        f.write(f"{nom},{ape},{ced},{eda},{usr},{pas},cliente\n")
    print("Usuario registrado.")

def login():
    cargar_usuarios()
    u = input("Usuario: ")
    p = input("Password: ")
    for us in usuarios:
        if us["user"] == u and us["pass"] == p:
            return us["rol"], u
    return None, None


def cargar_rutas_grafo():
    global grafo
    n = len(centros)
    grafo = [[0] * n for _ in range(n)]
    if os.path.exists(RUTAS_FILE):
        with open(RUTAS_FILE, "r") as f:
            for l in f:
                if l.strip():
                    a, b, c = map(int, l.strip().split(","))
                    if a < n and b < n:
                        grafo[a][b] = c
                        grafo[b][a] = c

def dijkstra(origen):
    n = len(grafo)
    dist = [float("inf")] * n
    dist[origen] = 0
    pq = [(0, origen)]
    while pq:
        costo, u = heapq.heappop(pq)
        if costo > dist[u]: continue
        for v in range(n):
            if grafo[u][v] > 0:
                nd = costo + grafo[u][v]
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
    return dist

def bfs_centros_cercanos(inicio_id):
    visitados = [False] * len(centros)
    cola = [inicio_id]
    visitados[inicio_id] = True
    resultado = []
    while cola:
        u = cola.pop(0)
        resultado.append(centros[u]["nombre"])
        for v in range(len(grafo)):
            if grafo[u][v] > 0 and not visitados[v]:
                visitados[v] = True
                cola.append(v)
    return resultado

def dfs_explorar_rutas(u, visitados):
    visitados[u] = True
    print(f"-> Explorando: {centros[u]['nombre']}")
    for v in range(len(grafo)):
        if grafo[u][v] > 0 and not visitados[v]:
            dfs_explorar_rutas(v, visitados)
            
class NodoArbol:
    def __init__(self, nombre):
        self.nombre = nombre
        self.hijos = []

def cargar_centros():
    centros.clear()
    if os.path.exists(CENTROS_FILE):
        with open(CENTROS_FILE, "r") as f:
            for l in f:
                if l.strip():
                    i, n, r = l.strip().split(",")
                    centros.append({"id": int(i), "nombre": n, "region": r})

def construir_arbol_regiones():
    raiz = NodoArbol("Ecuador")
    regiones = {}
    for c in centros:
        reg = c["region"]
        if reg not in regiones:
            nodo_reg = NodoArbol(reg)
            raiz.hijos.append(nodo_reg)
            regiones[reg] = nodo_reg
        regiones[reg].hijos.append(NodoArbol(c["nombre"]))
    return raiz

def mostrar_arbol(nodo, nivel=0):
    print("  " * nivel + "|--" + nodo.nombre)
    for hijo in nodo.hijos:
        mostrar_arbol(hijo, nivel + 1)

def quick_sort_centros(lista):
    if len(lista) <= 1:
        return lista
    pivote = lista[len(lista) // 2]["nombre"]
    izq = [x for x in lista if x["nombre"] < pivote]
    medio = [x for x in lista if x["nombre"] == pivote]
    der = [x for x in lista if x["nombre"] > pivote]
    return quick_sort_centros(izq) + medio + quick_sort_centros(der)            