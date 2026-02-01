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