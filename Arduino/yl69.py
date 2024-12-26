import RPi.GPIO as GPIO
import time

# Configuración del pin GPIO
SOIL_SENSOR_PIN = 7  # Número del pin GPIO de la Raspberry Pi

# Configuración de la biblioteca GPIO
GPIO.setmode(GPIO.BOARD)  # Usa la numeración física de los pines
GPIO.setup(SOIL_SENSOR_PIN, GPIO.IN)  # Configura el pin como entrada

print("Iniciando medición de humedad del suelo...")

try:
    while True:
        # Leer el estado del sensor
        soil_state = GPIO.input(SOIL_SENSOR_PIN)

        # Interpretar la lectura
        if soil_state == GPIO.HIGH:
            print("El suelo está seco.")
        else:
            print("El suelo está húmedo.")

        time.sleep(2)  # Pausa entre lecturas
except KeyboardInterrupt:
    print("\nPrograma interrumpido. Limpiando configuración GPIO...")
    GPIO.cleanup()  # Restablece los pines GPIO
