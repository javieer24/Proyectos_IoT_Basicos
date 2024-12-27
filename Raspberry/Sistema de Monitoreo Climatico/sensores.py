import time
import board
import busio
import adafruit_dht
import adafruit_bmp280
import math
from datetime import datetime, timedelta
import db as _db
import random
import pytz

# Configuración del sensor DHT11 en el pin D4
SENSOR_DHT = adafruit_dht.DHT11(board.D4)

# Configuración del bus I²C
i2c = busio.I2C(board.SCL, board.SDA)

# Inicializa el BMP280 en la dirección 0x76
SENSOR_BMP = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)

# Configuración opcional para el BMP280
SENSOR_BMP.sea_level_pressure = 1013.25  # Presión a nivel del mar

# Función para calcular la presión de saturación del vapor de agua (Pvs) en hPa
def calcular_pvs(temperatura):
    return 6.112 * math.exp((17.67 * temperatura) / (temperatura + 243.5))

# Función para calcular la presión parcial del vapor de agua (Pv) en hPa
def calcular_pv(humedad, pvs):
    return (humedad / 100.0) * pvs

# Función para calcular la Humedad Absoluta (HA) en g/m³
def calcular_ha(pv, temperatura):
    return (pv * 100) / (461.5 * (temperatura + 273.15))

# Función para leer el sensor DHT11
def leer_sensor_dht():
    """Función para leer la temperatura y humedad relativa del sensor DHT11"""
    try:
        temperatura = SENSOR_DHT.temperature
        humedad_relativa = SENSOR_DHT.humidity
        if temperatura is not None and humedad_relativa is not None:
            # Calcular humedad absoluta
            pvs = calcular_pvs(temperatura)
            pv = calcular_pv(humedad_relativa, pvs)
            humedad_absoluta = calcular_ha(pv, temperatura)
            return (temperatura, humedad_relativa, humedad_absoluta)
        else:
            return None
    except RuntimeError as e:
        print(f"Error al leer el sensor DHT11: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado en el sensor DHT11: {e}")
        return None

# Función para leer el sensor BMP280
def leer_sensor_bmp():
    """Función para leer presión y altitud del sensor BMP280"""
    try:
        presion = SENSOR_BMP.pressure
        altitud = SENSOR_BMP.altitude
        return (presion, altitud)
    except Exception as e:
        print(f"Error inesperado en el sensor BMP280: {e}")
        return None

# Función principal para leer y mostrar los datos de ambos sensores
def main():
    """Bucle principal para leer ambos sensores"""
    intervalo_lectura = 2  # Tiempo entre lecturas en segundos
    temp_dht = None
    humedad_relativa = None
    humedad_absoluta = None
    presion = None

    try:
        while True:
            # Leer datos del sensor DHT11
            lectura_dht = leer_sensor_dht()
            if lectura_dht:
                temp_dht, humedad_relativa, humedad_absoluta = lectura_dht
                print(f"[DHT11] Temperatura: {temp_dht:.1f}°C, Humedad Relativa: {humedad_relativa:.1f}%, Humedad Absoluta: {humedad_absoluta:.2f} g/m³")
            else:
                print("[DHT11] No se pudieron obtener datos del sensor.")

            # Leer datos del sensor BMP280
            lectura_bmp = leer_sensor_bmp()
            if lectura_bmp:
                presion, altitud = lectura_bmp
                print(f"[BMP280] Presión: {presion:.2f} hPa, Altitud: {altitud:.2f} m")
            else:
                print("[BMP280] No se pudieron obtener datos del sensor.")

            print("-" * 40)
            time.sleep(intervalo_lectura)
            fecha_actual = datetime.now()
            diferencia_horaria = timedelta(hours=6)
            fecha_ajustada = fecha_actual + diferencia_horaria
            hora = fecha_ajustada.strftime('%Y-%m-%d %H:%M:%S')
            _db.insert(temp_dht,humedad_relativa,humedad_absoluta,round(random.uniform(0, 99), 2),presion, hora)


    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario.")

if __name__ == "__main__":
    main()
