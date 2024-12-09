import tkinter as tk
from tkinter import messagebox
import sqlite3

# Configuración de la base de datos
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Crear tabla de usuarios si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    contraseña TEXT NOT NULL
)''')

# Crear tabla de clientes si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL,
    telefono TEXT NOT NULL
)''')

# Variable global para almacenar el último email ingresado
ultimo_email = ""

# Función para mostrar la lista de clientes
def mostrar_lista_clientes():
    # Limpiar la ventana actual y mostrar la lista de clientes
    for widget in ventana_inicio.winfo_children():
        widget.destroy()

    tk.Label(ventana_inicio, text="Clientes Registrados", font=("Arial", 14)).pack(pady=10)
    
    # Crear un frame para la lista
    frame_lista = tk.Frame(ventana_inicio)
    frame_lista.pack(fill=tk.BOTH, expand=True)
    
    # Crear un scrollbar
    scrollbar = tk.Scrollbar(frame_lista)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Crear una lista
    lista_clientes = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set, font=("Arial", 12))
    lista_clientes.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=lista_clientes.yview)
    
    # Consultar clientes de la base de datos
    cursor.execute("SELECT nombre, email, telefono FROM clientes")
    for cliente in cursor.fetchall():
        lista_clientes.insert(tk.END, f"Nombre: {cliente[0]} | Email: {cliente[1]} | Teléfono: {cliente[2]}")

# Función para iniciar sesión
def iniciar_sesion(event=None):  # Event es para manejar el "Enter"
    global ultimo_email
    email = entry_email.get()
    contraseña = entry_contraseña.get()
    
    # Verificar credenciales
    cursor.execute("SELECT * FROM usuarios WHERE email = ? AND contraseña = ?", (email, contraseña))
    usuario = cursor.fetchone()
    
    if usuario:
        ultimo_email = email  # Guardar el último email ingresado
        mostrar_lista_clientes()  # Mostrar la lista de clientes
    else:
        lbl_mensaje.config(text="Credenciales incorrectas", fg="red")

# Función para cambiar a la ventana de registro
def ir_a_registro():
    ventana_inicio.withdraw()  # Ocultar la ventana actual
    ventana_registro.deiconify()  # Mostrar la ventana de registro

# Función para registrar usuario
def registrar_usuario():
    email = entry_reg_email.get()
    contraseña = entry_reg_contraseña.get()
    confirmacion = entry_reg_confirmacion.get()
    
    if contraseña != confirmacion:
        lbl_reg_mensaje.config(text="Las contraseñas no coinciden", fg="red")
        return
    
    # Insertar nuevo usuario en la base de datos
    try:
        cursor.execute("INSERT INTO usuarios (email, contraseña) VALUES (?, ?)", (email, contraseña))
        conn.commit()
        lbl_reg_mensaje.config(text="Usuario registrado correctamente", fg="green")
    except sqlite3.IntegrityError:
        lbl_reg_mensaje.config(text="El email ya está registrado", fg="red")

# Función para regresar al inicio de sesión desde el registro
def regresar_a_inicio():
    ventana_registro.withdraw()  # Ocultar ventana de registro
    ventana_inicio.deiconify()  # Mostrar ventana de inicio de sesión

# Funciones para manejar el placeholder
def agregar_placeholder(entry, placeholder, es_contraseña=False):
    if entry.get() == "":
        entry.insert(0, placeholder)
        entry.config(fg="gray", show="" if not es_contraseña else "")

def remover_placeholder(entry, placeholder, es_contraseña=False):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)
        entry.config(fg="black", show="*" if es_contraseña else "")

# Ventana de inicio de sesión
ventana_inicio = tk.Tk()
ventana_inicio.title("Inicio de Sesión")
ventana_inicio.geometry("300x250")

# Campo de email
entry_email = tk.Entry(ventana_inicio, fg="black")
entry_email.pack(pady=5)
if ultimo_email:
    entry_email.insert(0, ultimo_email)
else:
    entry_email.insert(0, "Email")
    entry_email.config(fg="gray")
entry_email.bind("<FocusIn>", lambda e: remover_placeholder(entry_email, "Email"))
entry_email.bind("<FocusOut>", lambda e: agregar_placeholder(entry_email, "Email"))

# Campo de contraseña
entry_contraseña = tk.Entry(ventana_inicio, fg="gray")
entry_contraseña.insert(0, "Contraseña")
entry_contraseña.pack(pady=5)
entry_contraseña.bind("<FocusIn>", lambda e: remover_placeholder(entry_contraseña, "Contraseña", True))
entry_contraseña.bind("<FocusOut>", lambda e: agregar_placeholder(entry_contraseña, "Contraseña", True))
entry_contraseña.bind("<Return>", iniciar_sesion)  # Detectar "Enter" para iniciar sesión

# Botón para iniciar sesión
btn_iniciar = tk.Button(ventana_inicio, text="Iniciar Sesión", command=iniciar_sesion)
btn_iniciar.pack(pady=10)

# Mensaje de error/success
lbl_mensaje = tk.Label(ventana_inicio, text="", fg="red", font=("Arial", 10))
lbl_mensaje.pack()

# Botón para registrar
btn_registrar = tk.Button(ventana_inicio, text="Registrar nueva cuenta", command=ir_a_registro)
btn_registrar.pack(pady=5)

# Ventana de registro
ventana_registro = tk.Toplevel()
ventana_registro.title("Registro de Usuario")
ventana_registro.geometry("300x300")
ventana_registro.withdraw()  # Ocultar ventana de registro inicialmente

entry_reg_email = tk.Entry(ventana_registro, fg="gray")
entry_reg_email.insert(0, "Email")
entry_reg_email.pack(pady=5)
entry_reg_email.bind("<FocusIn>", lambda e: remover_placeholder(entry_reg_email, "Email"))
entry_reg_email.bind("<FocusOut>", lambda e: agregar_placeholder(entry_reg_email, "Email"))

entry_reg_contraseña = tk.Entry(ventana_registro, fg="gray")
entry_reg_contraseña.insert(0, "Contraseña")
entry_reg_contraseña.pack(pady=5)
entry_reg_contraseña.bind("<FocusIn>", lambda e: remover_placeholder(entry_reg_contraseña, "Contraseña", True))
entry_reg_contraseña.bind("<FocusOut>", lambda e: agregar_placeholder(entry_reg_contraseña, "Contraseña", True))

entry_reg_confirmacion = tk.Entry(ventana_registro, fg="gray")
entry_reg_confirmacion.insert(0, "Confirmar Contraseña")
entry_reg_confirmacion.pack(pady=5)
entry_reg_confirmacion.bind("<FocusIn>", lambda e: remover_placeholder(entry_reg_confirmacion, "Confirmar Contraseña", True))
entry_reg_confirmacion.bind("<FocusOut>", lambda e: agregar_placeholder(entry_reg_confirmacion, "Confirmar Contraseña", True))

btn_guardar = tk.Button(ventana_registro, text="Registrar", command=registrar_usuario)
btn_guardar.pack(pady=10)

lbl_reg_mensaje = tk.Label(ventana_registro, text="", fg="red", font=("Arial", 10))
lbl_reg_mensaje.pack()

btn_cancelar = tk.Button(ventana_registro, text="Cancelar", command=regresar_a_inicio)
btn_cancelar.pack(pady=5)

# Ejecutar aplicación
ventana_inicio.mainloop()
