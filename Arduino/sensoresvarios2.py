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

# Inicialización de sensores y LCD
SENSOR = adafruit_dht.DHT11(board.D4)
lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)

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

# Control del motor
def motor_control():
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(EN, GPIO.OUT)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(EN, GPIO.LOW)

    while True:
        x = input("Opciones: r-run s-stop e-exit: ")
        if x == 'r':
            GPIO.output(IN1, GPIO.HIGH)
            GPIO.output(EN, GPIO.HIGH)
            lcd.clear()
            lcd.write_string("Bomba On")
            print("Bomba encendida")
        elif x == 's':
            GPIO.output(IN1, GPIO.LOW)
            lcd.clear()
            lcd.write_string("Bomba Off")
            print("Bomba apagada")
        elif x == 'e':
            GPIO.cleanup()
            break
        else:
            print("Dato incorrecto. Usa 'r', 's' o 'e'.")

# Leer datos del sensor DHT11
def leer_sensor_dht():
    try:
        temperatura = SENSOR.temperature
        humedad = SENSOR.humidity
        return (temperatura, humedad)
    except RuntimeError:
        return None

# Mostrar datos del DHT11
def dht11_lcd():
    while True:
        lcd.clear()
        lcd.write_string("Datos interior")
        print("Mostrando datos del DHT11...")
        time.sleep(3)
        lectura = leer_sensor_dht()
        if lectura:
            temperatura, humedad = lectura
            lcd.clear()
            lcd.write_string(f"Temp: {temperatura}C")
            lcd.crlf()
            lcd.write_string(f"Hum: {humedad}%")
            print(f"Temp: {temperatura}C, Hum: {humedad}%")
            if 21 <= temperatura <= 25:
                GPIO.output(IN1, GPIO.HIGH)
                lcd.clear()
                lcd.write_string("Bomba On")
            else:
                GPIO.output(IN1, GPIO.LOW)
                lcd.clear()
                lcd.write_string("Bomba Off")
        else:
            lcd.clear()
            lcd.write_string("Error DHT11")
        time.sleep(5)

# Sensor de humedad de suelo
def sensor_humedad():
    GPIO.setup(SENSOR_PIN, GPIO.IN)
    while True:
        estado = GPIO.input(SENSOR_PIN)
        if estado == GPIO.HIGH:
            lcd.clear()
            lcd.write_string("Suelo seco")
            print("Tierra seca")
        else:
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

        if distancia <= 3:
            lcd.clear()
            lcd.write_string("30% Agua")
            print("Nivel: 30%. Llenar bomba.")
            time.sleep(1)
            lcd.clear()
            lcd.write_string("Llenar Bomba")
        else:
            porcentaje = max(0, min(100, 100 - (distancia / 10 * 100)))
            lcd.clear()
            lcd.write_string(f"Agua: {porcentaje:.0f}%")
            print(f"Nivel de agua: {porcentaje:.0f}%")
        time.sleep(5)

# Programa principal
if __name__ == "__main__":
    configurar_gpio()
    iniciar_lcd()

    try:
        # Crear hilos para cada tarea
        motor_thread = threading.Thread(target=motor_control)
        dht11_thread = threading.Thread(target=dht11_lcd)
        humedad_thread = threading.Thread(target=sensor_humedad)
        distancia_thread = threading.Thread(target=medir_distancia)

        # Iniciar hilos
        motor_thread.start()
        dht11_thread.start()
        humedad_thread.start()
        distancia_thread.start()

        # Esperar a que terminen los hilos
        motor_thread.join()
        dht11_thread.join()
        humedad_thread.join()
        distancia_thread.join()

    except KeyboardInterrupt:
        print("\nPrograma finalizado por el usuario.")
    finally:
        GPIO.cleanup()
        SENSOR.exit()
        lcd.clear()
        print("Recursos liberados.")
