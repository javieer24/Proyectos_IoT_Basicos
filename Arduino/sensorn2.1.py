import RPi.GPIO as GPIO
import time
import threading
import adafruit_dht
import board
from RPLCD.i2c import CharLCD

# Configuración de GPIO
def configurar_gpio():
    GPIO.setmode(GPIO.BCM)

# Configuración inicial
IN1 = 24
EN = 25
SENSOR_PIN = 17
TRIGGER = 5
ECHO = 6
ALTURA_BOTELLA = 13.0  # Altura de la botella para el sensor ultrasónico

# Inicialización de sensores y LCD
SENSOR_INTERIOR = adafruit_dht.DHT11(board.D4)
SENSOR_EXTERIOR = adafruit_dht.DHT11(board.D22)
lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)

# Variables para almacenar datos
datos_temperatura_interior = []
datos_humedad_interior = []
datos_temperatura_exterior = []
datos_humedad_exterior = []
datos_humedad_suelo = []
datos_distancia = []

# Mostrar mensaje inicial en LCD y terminal
def iniciar_lcd():
    lcd.clear()
    lcd.write_string("Iniciando...")
    print("Iniciando...")
    time.sleep(2)
    lcd.clear()
    lcd.write_string("Bienvenido")
    print("Bienvenido")
    time.sleep(2)

# Control de la bomba según temperatura
def control_bomba(temperatura):
    if 21 <= temperatura <= 25:
        GPIO.output(IN1, GPIO.HIGH)
        lcd.clear()
        lcd.write_string("Bomba On")
        print("Bomba encendida")
    else:
        GPIO.output(IN1, GPIO.LOW)
        lcd.clear()
        lcd.write_string("Bomba Off")
        print("Bomba apagada")

# Leer datos del sensor DHT11 interior
def leer_sensor_interior():
    try:
        temperatura = SENSOR_INTERIOR.temperature
        humedad = SENSOR_INTERIOR.humidity
        return (temperatura, humedad)
    except RuntimeError:
        return None

# Mostrar datos del DHT11 interior
def dht11_interior():
    while True:
        lcd.clear()
        lcd.write_string("Datos interior")
        print("Mostrando datos del DHT11 interior...")
        time.sleep(3)
        lectura = leer_sensor_interior()
        if lectura:
            temperatura, humedad = lectura
            datos_temperatura_interior.append(temperatura)
            datos_humedad_interior.append(humedad)
            lcd.clear()
            lcd.write_string(f"Temp: {temperatura}C")
            lcd.crlf()
            lcd.write_string(f"Hum: {humedad}%")
            print(f"Temp: {temperatura}C, Hum: {humedad}%")
            control_bomba(temperatura)
        else:
            lcd.clear()
            lcd.write_string("Error DHT11")
        time.sleep(5)

# Leer datos del sensor DHT11 exterior
def leer_sensor_exterior():
    try:
        temperatura = SENSOR_EXTERIOR.temperature
        humedad = SENSOR_EXTERIOR.humidity
        return (temperatura, humedad)
    except RuntimeError:
        return None

# Mostrar datos del DHT11 exterior
def dht11_exterior():
    while True:
        lectura = leer_sensor_exterior()
        if lectura:
            temperatura, humedad = lectura
            datos_temperatura_exterior.append(temperatura)
            datos_humedad_exterior.append(humedad)
            print(f"Temp Ext: {temperatura}C, Hum Ext: {humedad}%")
        else:
            print("Error al leer DHT11 exterior")
        time.sleep(10)

# Sensor de humedad de suelo
def sensor_humedad():
    GPIO.setup(SENSOR_PIN, GPIO.IN)
    while True:
        estado = GPIO.input(SENSOR_PIN)
        if estado == GPIO.HIGH:
            datos_humedad_suelo.append("Seco")
            lcd.clear()
            lcd.write_string("Suelo seco")
            print("Tierra seca")
        else:
            datos_humedad_suelo.append("Húmedo")
            lcd.clear()
            lcd.write_string("Suelo húmedo")
            print("Tierra húmeda")
        time.sleep(5)

# Sensor ultrasónico
def medir_distancia():
    GPIO.setup(TRIGGER, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    while True:
        GPIO.output(TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(TRIGGER, False)

        while GPIO.input(ECHO) == 0:
            inicio = time.time()

        while GPIO.input(ECHO) == 1:
            fin = time.time()

        duracion = fin - inicio
        distancia = (duracion * 34000) / 2

        if distancia > ALTURA_BOTELLA:
            nivel_agua = 0
        else:
            nivel_agua = ALTURA_BOTELLA - distancia

        datos_distancia.append(nivel_agua)
        lcd.clear()
        lcd.write_string(f"Agua: {nivel_agua:.1f}cm")
        print(f"Nivel de agua: {nivel_agua:.1f} cm, Distancia: {distancia:.1f} cm")
        time.sleep(5)

# Programa principal
if __name__ == "__main__":
    configurar_gpio()
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(EN, GPIO.OUT)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(EN, GPIO.HIGH)

    iniciar_lcd()

    try:
        # Crear hilos para cada tarea
        dht11_interior_thread = threading.Thread(target=dht11_interior)
        dht11_exterior_thread = threading.Thread(target=dht11_exterior)
        humedad_thread = threading.Thread(target=sensor_humedad)
        distancia_thread = threading.Thread(target=medir_distancia)

        # Iniciar hilos
        dht11_interior_thread.start()
        dht11_exterior_thread.start()
        humedad_thread.start()
        distancia_thread.start()

        # Esperar a que terminen los hilos
        dht11_interior_thread.join()
        dht11_exterior_thread.join()
        humedad_thread.join()
        distancia_thread.join()

    except KeyboardInterrupt:
        print("\nPrograma finalizado por el usuario.")
    finally:
        GPIO.cleanup()
        SENSOR_INTERIOR.exit()
        SENSOR_EXTERIOR.exit()
        lcd.clear()
        print("Recursos liberados.")
