import time
import board
import busio
from adafruit_bmp280 import basic as adafruit_bmp280

# Crear la conexión I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Crear el objeto para manejar el sensor BMP280
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

# Establecer las opciones del sensor (puedes ajustarlas según lo que necesites)
bmp280.sea_level_pressure = 1013.25  # Presión al nivel del mar en hPa (puedes modificarlo si tienes información local)

def obtener_datos_bmp280():
    # Leer los valores del sensor
    temperatura = bmp280.temperature  # Temperatura en grados Celsius
    presion = bmp280.pressure         # Presión en hPa
    altitud = bmp280.altitude         # Altitud en metros

    # Imprimir los valores
    print(f"Temperatura: {temperatura:.2f} *C")
    print(f"Presión: {presion:.2f} hPa")
    print(f"Altitud: {altitud:.2f} m")
    print("----------------------------")

# Bucle principal
while True:
    obtener_datos_bmp280()
    time.sleep(1)  # Pausa de 1 segundo antes de la siguiente medición
