import RPi.GPIO as GPIO
import time

# Configuración del pin GPIO del sensor
SENSOR_PIN = 17

# Configuración de la biblioteca GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

def leer_sensor():
    """
    Lee el estado del sensor YL-69.
    Devuelve:
        - "Húmeda" si el sensor detecta tierra húmeda.
        - "Seca" si el sensor detecta tierra seca.
        - "Sensor no conectado" si no hay señal.
    """
    try:
        estado = GPIO.input(SENSOR_PIN)
        if estado == GPIO.HIGH:
            return "Seca"
        elif estado == GPIO.LOW:
            return "Húmeda"
        else:
            return "Sensor no conectado"
    except Exception as e:
        return f"Error al leer el sensor: {e}"

try:
    print("Leyendo estado del sensor...")
    while True:
        estado_tierra = leer_sensor()
        print(f"Estado de la tierra: {estado_tierra}")
        time.sleep(1)  # Lee el sensor cada segundo
except KeyboardInterrupt:
    print("\nSaliendo...")
finally:
    GPIO.cleanup()