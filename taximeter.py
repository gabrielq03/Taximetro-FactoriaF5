import time

import csv
import json

from datetime import date, datetime
from pathlib import Path

ARCHIVO_HISTORIAL = Path(__file__).resolve().with_name("historial.csv") # Ruta del csv (en la misma carpeta que el .py)
ARCHIVO_TARIFAS = Path(__file__).resolve().with_name("tarifas.json") # Ruta del .json (no lo crea el programa)

def mostrar_instrucciones():
    """Muestra las opciones del menú principal."""
    print("\n=== Taxímetro digital ===")
    print("Comandos disponibles:")
    print("  iniciar   -> comenzar una carrera")
    print("  finalizar -> terminar una carrera activa")
    print("  historial -> ver las carreras del día")
    print("  salir     -> cerrar el programa")
    print()

def mostrar_instrucciones_carrera(tarifas):
    """Muestra el estado inicial, las tarifas y los comandos de la carrera."""
    print("\nCarrera iniciada en estado parado.")
    print(f"Tarifa actual: {tarifas['parado']:.2f} €/segundo.") # parado es un estado que tiene que existir, siempre se empieza desde él

    print("Tarifas disponibles:")
    for estado, tarifa in tarifas.items():
        print(f"  {estado}: {tarifa:.2f} €/segundo.")

    print("Comandos durante la carrera:")
    for estado in tarifas:
        print(f"  {estado} -> cambiar a la tarifa de {estado}")

    print("  finalizar  -> terminar la carrera y mostrar el importe")
    print()

def iniciar_carrera():
    """Devuelve el instante de inicio de una carrera."""
    return time.monotonic()

def calcular_importe(duracion_segundos, tarifa_por_segundo):
    """Calcula el coste sin redondear los resultados intermedios."""
    return duracion_segundos * tarifa_por_segundo

def finalizar_carrera(inicio_carrera, inicio_tramo, tarifa_por_segundo, importe_acumulado):
    """Suma el último tramo y devuelve la duración y el importe totales."""
    instante_final = time.monotonic() # instante en el que se finalizo la carrera
    duracion_segundos = instante_final - inicio_carrera
    duracion_tramo = instante_final - inicio_tramo
    importe_tramo = calcular_importe(duracion_tramo, tarifa_por_segundo)

    return duracion_segundos, importe_acumulado + importe_tramo

def guardar_carrera(duracion_segundos, importe_euros):
    """Guarda la fecha y hora de cierre, la duración y el importe."""
    
    fecha_hora = datetime.now().isoformat(timespec="seconds") # fecha y hora actual. En formato "fecha" + "T" + "hora" ; 2026-11-18T21:35:42

    try:
        # Con "a" nos situamos al final del archivo. Si el CSV no existe, se crea.
        # newline="" permite que csv gestione los saltos de línea.
        with ARCHIVO_HISTORIAL.open("a", encoding="utf-8", newline="") as archivo:
            escritor = csv.writer(archivo) # para escribir en el archivo

            if archivo.tell() == 0:
                escritor.writerow(["fecha_hora", "duracion_segundos", "importe_euros"]) # en caso de que el csv este vacío, creamos la cabecera

            escritor.writerow([
                fecha_hora,
                f"{duracion_segundos:.2f}", # en la siguiente fila añadimos los datos de fecha_hora,duración e importe
                f"{importe_euros:.2f}",
            ])
    except OSError as error:
        print(f"No se pudo guardar la carrera en el historial ({error}).") # si hay errores

def mostrar_historial():
    """Muestra las carreras del día y suma los importes registrados."""
    hoy = date.today().isoformat() # fecha de hoy

    try:
        with ARCHIVO_HISTORIAL.open("r", encoding="utf-8", newline="") as archivo:
            
            lector = csv.DictReader(archivo) # DictReader devuelve cada fila como un diccionario

            carreras_hoy = [ # lista de diccionarios
                carrera for carrera in lector # carrera es un diccionario
                if carrera["fecha_hora"].startswith(f"{hoy}T") # si la fecha del registro coincide con la fecha de hoy agrega el registro a "carreras_hoy"
            ]
    except FileNotFoundError:
        # Si todavía no se ha guardado ninguna carrera, el CSV puede no existir.
        carreras_hoy = []
    except OSError as error:
        print(f"No se pudo leer el historial ({error}).")
        return

    print(f"\n=== Historial del día ({hoy}) ===")

    if not carreras_hoy:
        print("No hay carreras registradas hoy.")
        return

    for carrera in carreras_hoy:
        
        hora = carrera["fecha_hora"].split("T", 1)[1] # nos quedamos con la parte que va después de la T, que es la hora
        print(
            f"{hora} | {carrera['duracion_segundos']} s "
            f"| {carrera['importe_euros']} €"
        )

    # El CSV devuelve los importes como texto. Los pasamos a float para sumarlos.
    total = sum(float(carrera["importe_euros"]) for carrera in carreras_hoy) # suma de un generador

    print(f"Carreras finalizadas: {len(carreras_hoy)}")
    print(f"Total de caja: {total:.2f} €.")

def gestionar_carrera(tarifas):
    """Gestiona una carrera desde su inicio hasta su finalización."""
    # El inicio de la carrera queda fijo. El del tramo cambia con el estado.
    inicio_carrera = iniciar_carrera()
    inicio_tramo = inicio_carrera
    estado = "parado"
    importe_acumulado = 0.0

    mostrar_instrucciones_carrera(tarifas)

    while True:
        comando_carrera = input("carrera> ").strip().lower()

        if comando_carrera in tarifas:
            if comando_carrera == estado:
                print(f"El taxi ya está en estado: {estado}.")
            else:
                instante_cambio = time.monotonic()
                duracion_tramo = instante_cambio - inicio_tramo

                # Cerramos el tramo anterior con la tarifa que tenía hasta ahora.
                importe_acumulado += calcular_importe(duracion_tramo, tarifas[estado])

                # El final del tramo anterior es el inicio del nuevo tramo.
                inicio_tramo = instante_cambio
                estado = comando_carrera

                print(f"Estado: {estado}. Tarifa: {tarifas[estado]:.2f} €/segundo.")

        elif comando_carrera == "finalizar":
            duracion, importe = finalizar_carrera(
                inicio_carrera,
                inicio_tramo,
                tarifas[estado],
                importe_acumulado,
            )

            print(f"Duración: {duracion:.2f} segundos.")
            print(f"Importe total: {importe:.2f} €.")

            guardar_carrera(duracion, importe) # guardar registros tras finalizar carrera
            break

        else:
            estados_disponibles = ", ".join(tarifas) # unir claves de tarifas en un solo texto
            print(f"Comando no válido. Usa: {estados_disponibles} o finalizar.")


def main():
    mostrar_instrucciones()

    while True:
        comando = input("taximetro> ").strip().lower()

        if comando == "iniciar":

            try:
                with ARCHIVO_TARIFAS.open("r", encoding="utf-8") as archivo: # abrir archivo en formato lectura
                    tarifas = json.load(archivo)

            except FileNotFoundError:
                print("Tarifas no especificadas. Falta el fichero tarifas.json")
                break # si no hay tarifas salir del programa

            except ValueError:
                print("Formato no adecuado. Ejemplo de tarifas.json:")
                print('{\n  "parado": 0.02,\n  "movimiento": 0.05\n}')
                continue # opción de volver a taximetro> y cambiar el json

            gestionar_carrera(tarifas)
            mostrar_instrucciones()

        elif comando == "finalizar":
            print("No hay ninguna carrera activa.")

        elif comando == "historial":
            mostrar_historial()

        elif comando == "salir":
            print("Programa cerrado.")
            break

        else:
            print("Comando no válido. Usa: iniciar, finalizar, historial o salir.")

if __name__ == "__main__":
    main()