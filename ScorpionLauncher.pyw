import minecraft_launcher_lib
import os
import subprocess
import tkinter as tk
import uuid
from tkinter import messagebox

# Configuraciones iniciales
titulo_launcher = "Minecraft Launcher - Scorpion"
minecraft_directory = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", ".minecraft")
usuarios_file = "usuarios.txt"
ram_asignada = "-Xmx4G"
versiones_validas = ["1.8.9", "1.12.2", "1.12", "Wurst MC 1.12", "1.16.5", "1.21", "1.20", "1.18", "1.17", "1.21.5", "1.21.4", "1.7", "1.8.9-OptiFine_HD_U_M5", "Wurst MC 1.12 OF"]

# Verifica la carpeta .minecraft
if not os.path.exists(minecraft_directory):
    os.makedirs(minecraft_directory)
    messagebox.showinfo("Configuración", "Se ha creado la carpeta .minecraft porque no existía.")

# Cargar y guardar usuarios
def cargar_usuarios():
    if not os.path.exists(usuarios_file):
        return []
    with open(usuarios_file, "r") as f:
        return [line.strip() for line in f if line.strip()]

def guardar_usuario(nombre):
    usuarios = cargar_usuarios()
    if nombre not in usuarios:
        with open(usuarios_file, "a") as f:
            f.write(nombre + "\n")

# Obtener versiones instaladas
def obtener_versiones_instaladas():
    installed_versions = minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory)
    return [version['id'] for version in installed_versions if version['id'] in versiones_validas]

# Ventana principal
ventana = tk.Tk()
ventana.geometry('500x550')
ventana.title(titulo_launcher)
ventana.resizable(False, False)

# Selector de versión
versiones_disponibles = obtener_versiones_instaladas()
if not versiones_disponibles:
    versiones_disponibles.append("No hay versiones detectadas")

version_seleccionada = tk.StringVar(ventana)
version_seleccionada.set(versiones_disponibles[0])
label_version = tk.Label(ventana, text="Selecciona la versión de Minecraft:")
label_version.pack()
menu_versiones = tk.OptionMenu(ventana, version_seleccionada, *versiones_disponibles)
menu_versiones.pack(pady=5)

# Entrada para instalar nueva versión
label_pregunta = tk.Label(ventana, text="¿Qué versión deseas instalar?")
label_pregunta.pack()
entrada_version = tk.Entry(ventana)
entrada_version.pack(pady=5)

# Selector de usuario
label_usuario = tk.Label(ventana, text="Selecciona o escribe tu usuario:")
label_usuario.pack()

usuarios = cargar_usuarios()
usuario_var = tk.StringVar(ventana)
usuario_var.set(usuarios[0] if usuarios else "")

entrada_usuario = tk.Entry(ventana, textvariable=usuario_var)
entrada_usuario.pack(pady=5)

# Solo se agrega el menú si hay usuarios
if usuarios:
    menu_usuarios = tk.OptionMenu(ventana, usuario_var, *usuarios)
    menu_usuarios.pack(pady=5)

# Descargar versión
def descargar_version():
    version = entrada_version.get().strip()
    versiones_actuales = obtener_versiones_instaladas()

    if version in versiones_actuales:
        messagebox.showinfo("Información", "Versión ya instalada.")
        return

    if version not in versiones_validas:
        messagebox.showerror("Error", "Esa versión no es válida.")
        return

    messagebox.showinfo("Descarga", f"Descargando Minecraft {version}...")
    minecraft_launcher_lib.install.install_minecraft_version(version, minecraft_directory)
    messagebox.showinfo("Descarga Completada", f"Minecraft {version} instalado exitosamente.")

    versiones_actualizadas = obtener_versiones_instaladas()
    version_seleccionada.set(versiones_actualizadas[0])
    menu_versiones['menu'].delete(0, 'end')
    for v in versiones_actualizadas:
        menu_versiones['menu'].add_command(label=v, command=tk._setit(version_seleccionada, v))

bt_descargar = tk.Button(ventana, text='Descargar Versión', command=descargar_version)
bt_descargar.pack(pady=10)

# Iniciar Minecraft
def ejecutar_minecraft():
    version = version_seleccionada.get()
    usuario = usuario_var.get().strip()

    if not usuario:
        messagebox.showerror("Error", "Debes escribir o seleccionar un usuario.")
        return

    if version == "No hay versiones detectadas":
        messagebox.showerror("Error", "No hay versiones instaladas para ejecutar.")
        return

    guardar_usuario(usuario)

    options = {
        'username': usuario,
        'uuid': str(uuid.uuid4()),
        'token': '',
        'jvmArguments': [ram_asignada],
        'launcherVersion': "1.0.0"
    }
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directory, options)
    ventana.destroy()
    subprocess.run(minecraft_command)

bt_ejecutar_minecraft = tk.Button(ventana, text='Iniciar Minecraft', command=ejecutar_minecraft)
bt_ejecutar_minecraft.pack(pady=10)

ventana.mainloop()
