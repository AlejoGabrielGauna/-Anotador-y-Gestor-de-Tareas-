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
