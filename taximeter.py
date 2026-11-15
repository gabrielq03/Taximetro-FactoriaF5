import time


def mostrar_instrucciones(tarifa_por_segundo):
    """Muestra cómo utilizar esta primera versión."""
    print("\n=== Taxímetro digital ===")
    print(f"Tarifa fija: {tarifa_por_segundo:.2f} €/segundo.")
    print("Comandos disponibles:")
    print("  iniciar   -> comenzar una carrera")
    print("  finalizar -> terminar la carrera y mostrar el importe")
    print("  salir     -> cerrar el programa")
    print()


def iniciar_carrera():
    """Devuelve el instante de inicio de una carrera."""
    return time.monotonic()


def calcular_importe(duracion_segundos, tarifa_por_segundo):
    """Calcula el coste sin redondear los resultados intermedios."""
    return duracion_segundos * tarifa_por_segundo


def finalizar_carrera(inicio_carrera, tarifa_por_segundo):
    """Calcula la duración y el importe de la carrera."""
    instante_final = time.monotonic() # monotonic actual
    duracion_segundos = instante_final - inicio_carrera # time.monotic da un valor al definirlo ; para contar el tiempo hay que restar dos monotonic defindios en diferentes instantes
    importe = calcular_importe(duracion_segundos, tarifa_por_segundo)
    return duracion_segundos, importe


def main():
    tarifa_por_segundo = 0.02
    inicio_carrera = None

    mostrar_instrucciones(tarifa_por_segundo)

    # Siempre sera verdadero hasta que el usuario decida salir del programa

    while True:
        comando = input("taximetro> ").strip().lower() # queremos que el usuario pueda escribir el comando en mayusculas o minusculas y que no importe si hay espacios al principio o al final

        if comando == "iniciar":
            if inicio_carrera is not None:
                print("Ya hay una carrera activa.")
            else:
                inicio_carrera = iniciar_carrera()
                print("Carrera iniciada.")

        elif comando == "finalizar":
            if inicio_carrera is None:
                print("No hay ninguna carrera activa.")
            else:
                duracion, importe = finalizar_carrera(
                    inicio_carrera, tarifa_por_segundo
                )
                inicio_carrera = None
                print(f"Duración: {duracion:.2f} segundos.")
                print(f"Importe total: {importe:.2f} €.")
                print("Puedes iniciar otra carrera o salir.")

        elif comando == "salir":
            if inicio_carrera is not None:
                print("Finaliza la carrera antes de salir.")
            else:
                print("Programa cerrado.")
                break # cierra programa

        else:
            print("Comando no válido. Usa: iniciar, finalizar o salir.")


if __name__ == "__main__":
    main()