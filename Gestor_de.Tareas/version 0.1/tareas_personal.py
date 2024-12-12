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
