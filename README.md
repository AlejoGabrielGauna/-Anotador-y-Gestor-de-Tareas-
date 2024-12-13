# -Anotador-y-Gestor-de-Tareas-
Proyecto personal de creacion, manipulacion y gestion de tareas varias como un anotador personal, con una interfaz.

Gestor de tareas personal Descripción: 

Una aplicación para agregar, actualizar y eliminar tareas pendientes con fechas de vencimiento. Habilidades: Archivos (lectura/escritura), listas, diccionarios, funciones. Ampliación: Crear una versión con una interfaz gráfica usando tkinter o PyQt.

Conocimientos:
Python: manejo de listas, diccionarios, funciones y control de flujo.
Manejo básico de archivos para guardar y recuperar datos (lectura/escritura de archivos .txt o .json).

version 0.1:
Operaciones del Programa:
Agregar tarea: Incluir una nueva tarea con descripción y fecha de vencimiento.
Ver tareas: Mostrar todas las tareas pendientes.
Actualizar tarea: Modificar una tarea existente (por ejemplo, cambiar descripción o fecha).
Eliminar tarea: Eliminar una tarea de la lista.
Guardar y cargar tareas: Permitir guardar las tareas en un archivo para que persistan al cerrar el programa.


import json

# Archivo donde se guardarán las tareas
ARCHIVO_TAREAS = "tareas.json"

# Función para cargar tareas desde el archivo
def cargar_tareas():
    try:
        with open(ARCHIVO_TAREAS, "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []  # Si el archivo no existe, devolver lista vacía

# Función para guardar tareas en el archivo
def guardar_tareas(tareas):
    with open(ARCHIVO_TAREAS, "w") as archivo:
        json.dump(tareas, archivo, indent=4)

# Función para mostrar tareas
def mostrar_tareas(tareas):
    if not tareas:
        print("No hay tareas pendientes.")
    else:
        print("Tareas que se deben cumplir:")
        for i, tarea in enumerate(tareas, start=1):
            print(f"{i}. {tarea['descripcion']} - Vence el {tarea['fecha']}")

# Función para agregar una tarea
def agregar_tarea(tareas):
    descripcion = input("Describe la tarea: ")
    fecha = input("Fecha de vencimiento (YYYY-MM-DD): ")
    tareas.append({"descripcion": descripcion, "fecha": fecha})
    print("Tarea agregada con éxito.")

# Función para eliminar una tarea
def eliminar_tarea(tareas):
    mostrar_tareas(tareas)
    try:
        indice = int(input("Elige el número de la tarea a eliminar: ")) - 1
        if 0 <= indice < len(tareas):
            tarea_eliminada = tareas.pop(indice)
            print(f"Tarea '{tarea_eliminada['descripcion']}' eliminada.")
        else:
            print("Número de tarea inválido.")
    except ValueError:
        print("Entrada no válida.")

# Menú principal
def menu():
    tareas = cargar_tareas()
    while True:
        print("\nGestor de Tareas")
        print("1. Ver tareas")
        print("2. Agregar tarea")
        print("3. Eliminar tarea")
        print("4. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            mostrar_tareas(tareas)
        elif opcion == "2":
            agregar_tarea(tareas)
            guardar_tareas(tareas)
        elif opcion == "3":
            eliminar_tarea(tareas)
            guardar_tareas(tareas)
        elif opcion == "4":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()




---------------------------------------------------------------------------------------------------------------------------------------------------

version 0.2:
Cambios en el código:
Actualizar estructura de datos: Añadir un atributo de prioridad a cada tarea.
Permitir al usuario establecer la prioridad al agregar o modificar tareas.

Notificaciones para tareas:
Calcular la diferencia entre la fecha actual y la fecha de vencimiento.
Mostrar una advertencia si una tarea está próxima a vencer.

Interfaz:
Uso de la libreria: tkinter.



import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# Funciones de backend
def cargar_tareas():
    try:
        with open("tareas.json", "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []

def guardar_tareas(tareas):
    with open("tareas.json", "w") as archivo:
        json.dump(tareas, archivo, indent=4)

def notificar_tareas_proximas(tareas):
    hoy = datetime.today().date()
    proximas = []
    for tarea in tareas:
        fecha_vencimiento = datetime.strptime(tarea['fecha'], "%Y-%m-%d").date()
        dias_restantes = (fecha_vencimiento - hoy).days

        if dias_restantes <= 3:
            proximas.append(f"\u2022 {tarea['descripcion']} vence en {dias_restantes} d\u00edas")
    return proximas

# Funciones para la interfaz gráfica
def agregar_tarea_gui():
    descripcion = descripcion_entry.get()
    fecha = fecha_entry.get()
    prioridad = prioridad_combo.get()

    if not descripcion or not fecha or not prioridad:
        messagebox.showwarning("Campos incompletos", "Por favor, completa todos los campos.")
        return

    try:
        datetime.strptime(fecha, "%Y-%m-%d")  # Validar formato de fecha
    except ValueError:
        messagebox.showerror("Fecha no válida", "Por favor, ingresa una fecha válida (YYYY-MM-DD).")
        return

    nueva_tarea = {"descripcion": descripcion, "fecha": fecha, "prioridad": prioridad}
    tareas.append(nueva_tarea)
    guardar_tareas(tareas)
    actualizar_lista()

    descripcion_entry.delete(0, tk.END)
    fecha_entry.delete(0, tk.END)
    prioridad_combo.set("")
    messagebox.showinfo("Tarea agregada", "La tarea se ha agregado correctamente.")

def actualizar_lista():
    lista_tareas.delete(*lista_tareas.get_children())
    for i, tarea in enumerate(tareas, start=1):
        lista_tareas.insert("", "end", values=(i, tarea['descripcion'], tarea['fecha'], tarea['prioridad']))

    # Notificar tareas próximas a vencer
    proximas = notificar_tareas_proximas(tareas)
    if proximas:
        messagebox.showwarning("Tareas próximas a vencer", "\n".join(proximas))

def eliminar_tarea():
    try:
        seleccion = lista_tareas.selection()[0]
        indice = int(lista_tareas.item(seleccion)['values'][0]) - 1
        del tareas[indice]
        guardar_tareas(tareas)
        actualizar_lista()
        messagebox.showinfo("Tarea eliminada", "La tarea se ha eliminado correctamente.")
    except IndexError:
        messagebox.showerror("Error", "Por favor, selecciona una tarea para eliminar.")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Gestor de Tareas")
ventana.geometry("600x400")

# Entradas para agregar tareas
tk.Label(ventana, text="Descripción:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
descripcion_entry = tk.Entry(ventana, width=30)
descripcion_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(ventana, text="Fecha de vencimiento (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
fecha_entry = tk.Entry(ventana, width=30)
fecha_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(ventana, text="Prioridad:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
prioridad_combo = ttk.Combobox(ventana, values=["baja", "media", "alta"], state="readonly", width=27)
prioridad_combo.grid(row=2, column=1, padx=10, pady=5)

# Botones
tk.Button(ventana, text="Agregar Tarea", command=agregar_tarea_gui).grid(row=3, column=0, columnspan=2, pady=10)

# Lista de tareas
columnas = ("#", "Descripción", "Fecha de Vencimiento", "Prioridad")
lista_tareas = ttk.Treeview(ventana, columns=columnas, show="headings", height=10)
for col in columnas:
    lista_tareas.heading(col, text=col)
    lista_tareas.column(col, width=150 if col == "Descripción" else 100, anchor="center")

lista_tareas.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Botón para eliminar tareas
tk.Button(ventana, text="Eliminar Tarea", command=eliminar_tarea).grid(row=5, column=0, columnspan=2, pady=10)

# Cargar tareas iniciales
tareas = cargar_tareas()
actualizar_lista()

ventana.mainloop()


