import RPi.GPIO as GPIO
import time

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)

# Pines asignados (sin usar 2, 3, 4, 17, 22, 23, 24, 25)
TRIGGER = 5
ECHO = 6

GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Altura de la botella en centímetros
ALTURA_BOTELLA = 13.0  # cm

def medir():
    """Mide la distancia usando el sensor ultrasónico y calcula el nivel del agua."""
    GPIO.output(TRIGGER, True)
    time.sleep(0.00001)  # Pulso de 10 microsegundos
    GPIO.output(TRIGGER, False)

    # Esperar al inicio del pulso
    while GPIO.input(ECHO) == 0:
        inicio = time.time()

    # Esperar a que el pulso termine
    while GPIO.input(ECHO) == 1:
        fin = time.time()

    # Calcular la duración del pulso
    duracion = fin - inicio

    # Calcular la distancia (cm)
    distancia = (duracion * 34000) / 2

    # Calcular el nivel de agua
    if distancia > ALTURA_BOTELLA:
        nivel_agua = 0  # El agua está vacía o el sensor no mide correctamente
    else:
        nivel_agua = ALTURA_BOTELLA - distancia

    return nivel_agua, distancia

try:
    while True:
        nivel_agua, distancia = medir()
        print(f"Nivel de agua: {nivel_agua:.2f} cm")
        print(f"Distancia medida: {distancia:.2f} cm")
        time.sleep(1)
except KeyboardInterrupt:
    print("Programa finalizado")
finally:
    GPIO.cleanup()

