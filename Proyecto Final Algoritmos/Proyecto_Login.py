import os
import heapq

USUARIOS_FILE = "usuarios.txt"
CENTROS_FILE = "centros.txt"
RUTAS_FILE = "rutas.txt"

usuarios=[]
centros=[]
grafo=[]

# ======================================================
# ARCHIVOS
# ======================================================
def inicializar_archivos():
    for f in [USUARIOS_FILE,CENTROS_FILE,RUTAS_FILE]:
        if not os.path.exists(f):
            open(f,"w").close()

# ======================================================
# USUARIOS
# ======================================================
def cargar_usuarios():
    usuarios.clear()
    with open(USUARIOS_FILE) as f:
        for l in f:
            if l.strip():
                n,a,c,e,u,p,r=l.strip().split(",")
                usuarios.append({"user":u,"pass":p,"rol":r})

def crear_admin_defecto():
    cargar_usuarios()
    for u in usuarios:
        if u["rol"]=="admin":
            return
    with open(USUARIOS_FILE,"a") as f:
        f.write("Admin,Principal,0000,30,admin,Admin123,admin\n")

def password_segura(p):
    return any(c.islower() for c in p) and any(c.isupper() for c in p) and any(c.isdigit() for c in p)

def registrar():
    print("\n--- REGISTRO ---")
    n=input("Nombres: "); a=input("Apellidos: ")
    c=input("ID: "); e=input("Edad: ")
    u=input("Usuario: "); p=input("Contraseña: ")
    if not password_segura(p):
        print("❌ Contraseña insegura"); return
    with open(USUARIOS_FILE,"a") as f:
        f.write(f"{n},{a},{c},{e},{u},{p},cliente\n")
    print("✅ Registrado correctamente")

def login():
    cargar_usuarios()
    u=input("Usuario: ")
    p=input("Pass: ")

    for us in usuarios:
        if us["user"] == u and us["pass"] == p:
            print("✅ Inicio de sesión exitoso\n")
            return us["rol"], u

    print("❌ Error en los datos ingresados\n")
    return None, None

# ======================================================
# CENTROS Y GRAFO
# ======================================================
def cargar_centros():
    centros.clear()
    with open(CENTROS_FILE) as f:
        for l in f:
            if l.strip():
                i,n,r=l.strip().split(",")
                centros.append({"id":int(i),"nombre":n,"region":r})

def guardar_centros():
    with open(CENTROS_FILE,"w") as f:
        for c in centros:
            f.write(f"{c['id']},{c['nombre']},{c['region']}\n")

def cargar_grafo():
    global grafo
    n=len(centros)
    grafo=[[0]*n for _ in range(n)]
    with open(RUTAS_FILE) as f:
        for l in f:
            if l.strip():
                a,b,c=map(int,l.strip().split(","))
                if a<n and b<n:
                    grafo[a][b]=c; grafo[b][a]=c

# ======================================================
# DIJKSTRA
# ======================================================
def dijkstra(origen):
    n=len(grafo)
    dist=[float("inf")]*n
    prev=[None]*n
    dist[origen]=0
    pq=[(0,origen)]
    while pq:
        costo,u=heapq.heappop(pq)
        for v in range(n):
            if grafo[u][v]>0:
                nd=costo+grafo[u][v]
                if nd<dist[v]:
                    dist[v]=nd; prev[v]=u
                    heapq.heappush(pq,(nd,v))
    return dist,prev

def reconstruir(prev,d):
    ruta=[]
    while d is not None:
        ruta.append(d); d=prev[d]
    return ruta[::-1]

# ======================================================
# BFS DFS
# ======================================================
def bfs(i):
    if i<0 or i>=len(centros):
        return ["ID inválido"]
    vis=[False]*len(centros)
    cola=[i]; vis[i]=True
    res=[]
    while cola:
        u=cola.pop(0)
        res.append(centros[u]["nombre"])
        for v in range(len(grafo)):
            if grafo[u][v]>0 and not vis[v]:
                vis[v]=True; cola.append(v)
    return res

def dfs(u,vis):
    vis[u]=True
    print(centros[u]["nombre"])
    for v in range(len(grafo)):
        if grafo[u][v]>0 and not vis[v]:
            dfs(v,vis)

# ======================================================
# ÁRBOL
# ======================================================
class NodoArbol:
    def __init__(self,n):
        self.nombre=n; self.hijos=[]

def construir_arbol():
    raiz=NodoArbol("Ecuador"); regs={}
    for c in centros:
        r=c["region"]
        if r not in regs:
            nodo=NodoArbol(r)
            raiz.hijos.append(nodo)
            regs[r]=nodo
        regs[r].hijos.append(NodoArbol(c["nombre"]))
    return raiz

def mostrar_arbol(n,l=0):
    print("  "*l+"|--"+n.nombre)
    for h in n.hijos:
        mostrar_arbol(h,l+1)

# ======================================================
# ADMIN
# ======================================================
def menu_admin():
    while True:
        print("\n--- ADMIN ---")
        print("1 Agregar Centro\n2 Agregar Ruta\n3 Listar Centros\n4 DFS\n0 Salir")
        op=input("Opción: ")

        if op=="1":
            n=input("Nombre: "); r=input("Región: ")
            centros.append({"id":len(centros),"nombre":n,"region":r})
            guardar_centros(); cargar_grafo()

        elif op=="2":
            for c in centros: print(c["id"],c["nombre"])
            try:
                a=int(input("Origen ID: "))
                b=int(input("Destino ID: "))
                c=int(input("Costo: "))
                with open(RUTAS_FILE,"a") as f:
                    f.write(f"{a},{b},{c}\n")
                cargar_grafo()
            except:
                print("❌ Error de entrada")

        elif op=="3":
            for c in centros:
                print(c["id"],c["nombre"],c["region"])

        elif op=="4":
            if centros:
                dfs(0,[False]*len(centros))

        elif op=="0": break

# ======================================================
# CLIENTE
# ======================================================
def menu_cliente(user):
    seleccion=[]
    while True:
        print("\n1 Árbol\n2 Ruta Óptima\n3 BFS\n4 Agregar Centro\n5 Ver Ruta\n0 Salir")
        op=input("Opción: ")

        if op=="1":
            mostrar_arbol(construir_arbol())

        elif op=="2":
            o=int(input("Origen ID: "))
            d=int(input("Destino ID: "))
            dist,prev=dijkstra(o)
            print("Ruta:",[centros[i]["nombre"] for i in reconstruir(prev,d)])
            print("Costo:",dist[d])

        elif op=="3":
            print(bfs(int(input("ID centro: "))))

        elif op=="4":
            seleccion.append(int(input("ID centro: ")))

        elif op=="5":
            total=0
            for i in range(len(seleccion)-1):
                dist,_=dijkstra(seleccion[i])
                total+=dist[seleccion[i+1]]
            print("Ruta:",[centros[i]["nombre"] for i in seleccion])
            print("Costo total:",total)

        elif op=="0": break

# ======================================================
# MAIN
# ======================================================
inicializar_archivos()
crear_admin_defecto()
cargar_centros()
cargar_grafo()

while True:
    print("\n=== POLIDELIVERY EPN ===")
    op=input("1 Registrar\n2 Login\n0 Salir\n")
    if op=="1": registrar()
    elif op=="2":
        rol,u=login()
        if rol=="admin": menu_admin()
        elif rol=="cliente": menu_cliente(u)
    elif op=="0": break
