import time

def mostrar_instrucciones():
    """Muestra las opciones iniciales."""
    print("\n=== Taxímetro digital ===")
    print("Comandos disponibles:")
    print("  iniciar   -> comenzar una carrera")
    print("  finalizar -> terminar una carrera activa")
    print("  salir     -> cerrar el programa")
    print()


def mostrar_instrucciones_carrera(tarifas):
    """Muestra el estado inicial, las tarifas y los comandos de la carrera."""
    print("\nCarrera iniciada en estado parado.")
    print(f"Tarifa actual: {tarifas['parado']:.2f} €/segundo.")

    print("Tarifas disponibles:")
    print(f"  Parado:     {tarifas['parado']:.2f} €/segundo.")
    print(f"  Movimiento: {tarifas['movimiento']:.2f} €/segundo.")

    print("Comandos durante la carrera:")
    print("  parado     -> cambiar a la tarifa de parado")
    print("  movimiento -> cambiar a la tarifa de movimiento")
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


def gestionar_carrera(tarifas):
    """Gestiona una carrera desde su inicio hasta su finalización."""
    inicio_carrera = iniciar_carrera() # Instante inicial de toda la carrera; permanece fijo.
    inicio_tramo = inicio_carrera # Inicio del tramo actual; se actualiza al cambiar de estado
    estado = "parado"
    importe_acumulado = 0.0

    mostrar_instrucciones_carrera(tarifas)

    while True:
        comando2 = input("carrera> ").strip().lower()

        if comando2 in ("parado", "movimiento"):
            if comando2 == estado:
                print(f"El taxi ya está en estado: {estado}.")
            else:
                instante_cambio = time.monotonic()
                duracion_tramo = instante_cambio - inicio_tramo

                # Cerramos el tramo anterior con su tarifa.
                importe_acumulado += calcular_importe(duracion_tramo, tarifas[estado]) # Nota: tarifas es un diccionario, por tanto accedemos a su valor

                # Empezamos el nuevo tramo. Actualizando nuestras variables
                inicio_tramo = instante_cambio
                estado = comando2

                print(f"Estado: {estado}. Tarifa: {tarifas[estado]:.2f} €/segundo.")

        elif comando2 == "finalizar":
            duracion, importe = finalizar_carrera(
                inicio_carrera,
                inicio_tramo,
                tarifas[estado],
                importe_acumulado,
            )

            print(f"Duración: {duracion:.2f} segundos.")
            print(f"Importe total: {importe:.2f} €.")
            break

        else:
            print("Comando no válido. Usa: parado, movimiento o finalizar.")


def main():
    tarifas = {"parado": 0.02, "movimiento": 0.05}
    mostrar_instrucciones()

    while True:
        comando = input("taximetro> ").strip().lower()

        if comando == "iniciar":
            gestionar_carrera(tarifas)
            mostrar_instrucciones()

        elif comando == "finalizar":
            print("No hay ninguna carrera activa.")

        elif comando == "salir":
            print("Programa cerrado.")
            break

        else:
            print("Comando no válido. Usa: iniciar, finalizar o salir.")

if __name__ == "__main__":
    main()