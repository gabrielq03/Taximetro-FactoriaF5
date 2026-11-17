# Taxímetro digital — Factoría F5

Aplicación de terminal en Python que calcula el importe de una carrera según el tiempo transcurrido y el estado del taxi.

Proyecto desarrollado a partir del [enunciado de Factoría F5](https://github.com/Factoria-F5-madrid/project-py-taximetro).

## Estado del proyecto

**Fase 1 — MVP funcional: implementación completada y revisada.**

La aplicación permite:

- Iniciar una carrera.
- Cambiar entre parado y movimiento, aplicando la tarifa correspondiente.
- Finalizar la carrera y mostrar su importe en euros con dos decimales.
- Comenzar otra carrera sin cerrar el programa.

La [memoria de la fase 1](entregables/fase1/README.md) recoge el alcance, las decisiones técnicas, la validación y las evidencias de la entrega. La demostración en directo está pendiente de presentación.

## Requisitos y ejecución

- Python 3.10 o superior.
- Una terminal.
- Git, si se desea clonar el repositorio.

La aplicación principal utiliza únicamente `time`, de la biblioteca estándar de Python. No requiere instalar paquetes adicionales.

Para obtener el proyecto:

```bash
git clone https://github.com/gabrielq03/Taximetro-FactoriaF5.git
cd Taximetro-FactoriaF5
```

Desde la carpeta que contiene `taximeter.py`, ejecutar:

```bash
python taximeter.py
```

Si ya tienes el repositorio clonado, abre una terminal en su carpeta y ejecuta ese último comando.

## Uso del programa

### Menú principal

Al arrancar aparece el indicador `taximetro>`:

| Comando | Comportamiento |
| --- | --- |
| `iniciar` | Comienza una carrera. |
| `finalizar` | Avisa de que no hay una carrera activa. |
| `salir` | Cierra la aplicación. |

### Durante una carrera

Cada carrera comienza en estado **parado**. El indicador cambia a `carrera>`:

| Comando | Comportamiento |
| --- | --- |
| `parado` | Selecciona la tarifa de parado. |
| `movimiento` | Selecciona la tarifa de movimiento. |
| `finalizar` | Cierra la carrera, muestra su resultado y vuelve al menú principal. |

Los comandos admiten mayúsculas y espacios al principio o al final. Se confirman pulsando Enter.

Para cerrar la aplicación durante una carrera, primero introduce `finalizar` y después `salir` en el menú principal.

## Tarifas

| Estado | Tarifa |
| --- | --- |
| Parado | 0.02 €/segundo |
| Movimiento | 0.05 €/segundo |

El estado se selecciona mediante comandos. El programa calcula el coste de cada tramo y muestra el importe total al finalizar.

**El tiempo en parado también se factura.** Leer las instrucciones, escribir comandos o introducir una orden incorrecta no detiene el contador.

Por ejemplo, una carrera con 10 segundos parado, 20 segundos en movimiento y otros 5 segundos parado cuesta **1.30 €**. En el uso manual, el importe depende del tiempo real entre los comandos.

## Documentación y seguimiento

- [Memoria y evidencias de la fase 1](entregables/fase1/README.md).
- [Tablero de seguimiento](https://github.com/users/gabrielq03/projects/1).
- [Repositorio en GitHub](https://github.com/gabrielq03/Taximetro-FactoriaF5).

El tablero incluye una vista **Por fases** para organizar el trabajo. El campo **Status** registra el avance de cada tarea.