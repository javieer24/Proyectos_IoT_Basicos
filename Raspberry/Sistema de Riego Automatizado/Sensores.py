import RPi.GPIO as GPIO
import time
import threading
import adafruit_dht
import board
from RPLCD.i2c import CharLCD
from datetime import datetime
import db as _db

# Configuración de GPIO
def configurar_gpio():
    GPIO.setmode(GPIO.BCM)

# Configuración inicial
IN1 = 24
EN = 25
TRIGGER = 5
ECHO = 6
SENSOR_PIN = 17
ALTURA_BOTELLA = 13.0  # Altura de la botella para el sensor ultrasónico

# Pines para el ventilador
IN1_VENTILADOR = 27
EN_VENTILADOR = 23

# Inicialización de sensores y LCD
SENSOR_INTERIOR = adafruit_dht.DHT11(board.D4)
SENSOR_EXTERIOR = adafruit_dht.DHT11(board.D22)
lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)

# Bloqueo para sincronizar el acceso al LCD
lcd_lock = threading.Lock()

# Variables para almacenar datos
datos_temperatura_interior = []
datos_humedad_interior = []
datos_temperatura_exterior = []
datos_humedad_exterior = []
datos_humedad_suelo = []
datos_distancia = []

# Variables para guardar tiempos de activación/desactivación
bomba_activaciones = []
bomba_desactivaciones = []
ventilador_activaciones = []
ventilador_desactivaciones = []

# Eventos para sincronización
eventos_sensores = {
    "interior": threading.Event(),
    "exterior": threading.Event(),
    "humedad": threading.Event(),
    "distancia": threading.Event()
}

# Variable de control para detener los hilos
programa_en_ejecucion = True

#estado manual
control_manual = False

def actualizar_lcd(linea1, linea2=""):
    with lcd_lock:
        lcd.clear()
        lcd.write_string(linea1)
        if linea2:
            lcd.crlf()
            lcd.write_string(linea2)

def iniciar_lcd():
    actualizar_lcd("Iniciando...")
    print("Iniciando...")
    time.sleep(5)
    actualizar_lcd("Bienvenido")
    print("Bienvenido")
    time.sleep(5)

def registrar_evento(lista, evento):
    lista.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def control_bomba_y_ventilador(temperatura):
    global control_manual
    
    if control_manual:
        print("Control manual activado.Ignorando lògica automàtica")
        return

    if 40 <= temperatura <= 70:
        if GPIO.input(IN1) == GPIO.LOW:  # La bomba estaba apagada
            registrar_evento(bomba_activaciones, "Bomba encendida")
        if GPIO.input(IN1_VENTILADOR) == GPIO.LOW:  # El ventilador estaba apagado
            registrar_evento(ventilador_activaciones, "Ventilador encendido")

        GPIO.output(IN1, GPIO.HIGH)  # Enciende la bomba
        GPIO.output(IN1_VENTILADOR, GPIO.HIGH)  # Enciende el ventilador
        GPIO.output(EN, GPIO.HIGH)  # Activa la bomba
        GPIO.output(EN_VENTILADOR, GPIO.HIGH)  # Activa el ventilador
        
        actualizar_lcd("Bomba y Ventilador On")
        print("Bomba y Ventilador encendidos")
    else:
        if GPIO.input(IN1) == GPIO.HIGH:  # La bomba estaba encendida
            registrar_evento(bomba_desactivaciones, "Bomba apagada")
        if GPIO.input(IN1_VENTILADOR) == GPIO.HIGH:  # El ventilador estaba encendido
            registrar_evento(ventilador_desactivaciones, "Ventilador apagado")

        GPIO.output(IN1, GPIO.LOW)  # Apaga la bomba
        GPIO.output(IN1_VENTILADOR, GPIO.LOW)  # Apaga el ventilador
        GPIO.output(EN, GPIO.LOW)  # Desactiva la bomba
        GPIO.output(EN_VENTILADOR, GPIO.LOW)  # Desactiva el ventilador
        actualizar_lcd("Bomba y Ventilador Off")
        print("Bomba y Ventilador apagados")

def control_manual_ventilador_bomba():
    global control_manual

    while programa_en_ejecucion:
        comando = input("Ingrese 'on', 'off' o 'auto' para controlar los dispositivos: ").strip().lower()
        if comando == 'on':
            control_manual = True
            GPIO.output(IN1, GPIO.HIGH)
            GPIO.output(IN1_VENTILADOR, GPIO.HIGH)
            actualizar_lcd("Modo manual:", "Encendido")
            _db.insert_aire(1)
            _db.insert_bomba(1)
            print("Ventilador y bomba encendidos manualmente.")
        elif comando == 'off':
            control_manual = True
            GPIO.output(IN1, GPIO.LOW)
            GPIO.output(IN1_VENTILADOR, GPIO.LOW)
            actualizar_lcd("Modo manual:", "Apagado")
            _db.insert_aire(0)
            _db.insert_bomba(0)
            print("Ventilador y bomba apagados manualmente.")
        elif comando == 'auto':
            control_manual = False
            actualizar_lcd("Modo automatico")
            print("Modo automático activado.")
        else:
            print("Comando no reconocido. Use 'on', 'off' o 'auto'.")

def leer_sensor_interior():
    try:
        temperatura = SENSOR_INTERIOR.temperature
        humedad = SENSOR_INTERIOR.humidity
        if temperatura is not None and humedad is not None:
            return (temperatura, humedad)
    except RuntimeError:
        pass
    return None

def dht11_interior():
    while programa_en_ejecucion:
        try:
            lectura = leer_sensor_interior()
            actualizar_lcd("Interior")
            print("Interior:")
            time.sleep(2)

            if lectura:
                temperatura, humedad = lectura
                datos_temperatura_interior.append(temperatura)
                datos_humedad_interior.append(humedad)
                actualizar_lcd(f"Temp: {temperatura}C", f"Hum: {humedad}%")
                print(f"Temp: {temperatura}C, Hum: {humedad}%")
                control_bomba_y_ventilador(temperatura)
                _db.insert_datos_int(temperatura, humedad)
            else:
                actualizar_lcd("Error Interior")
                print("Error al leer DHT11 interior")

            eventos_sensores["interior"].set()
            time.sleep(8)
        except Exception as e:
            print(f"Error en dht11_interior: {e}")

def leer_sensor_exterior():
    try:
        temperatura = SENSOR_EXTERIOR.temperature
        humedad = SENSOR_EXTERIOR.humidity
        if temperatura is not None and humedad is not None:
            return (temperatura, humedad)
    except RuntimeError:
        pass
    return None

def dht11_exterior():
    while programa_en_ejecucion:
        try:
            lectura = leer_sensor_exterior()
            actualizar_lcd("Exterior")
            print("Exterior:")
            time.sleep(2)

            if lectura:
                temperatura, humedad = lectura
                datos_temperatura_exterior.append(temperatura)
                datos_humedad_exterior.append(humedad)
                actualizar_lcd(f"Temp: {temperatura}C", f"Hum: {humedad}%")
                _db.insert_datos_ext(temperatura, humedad)
                print(f"Temp: {temperatura}C, Hum: {humedad}%")
            else:
                actualizar_lcd("Error Exterior")
                print("Error al leer DHT11 exterior")

            eventos_sensores["exterior"].set()
            time.sleep(10)
        except Exception as e:
            print(f"Error en dht11_exterior: {e}")

def sensor_humedad():
    GPIO.setup(SENSOR_PIN, GPIO.IN)
    while programa_en_ejecucion:
        try:
            estado = GPIO.input(SENSOR_PIN)
            if estado == GPIO.HIGH:
                datos_humedad_suelo.append("Seco")
                actualizar_lcd("Suelo seco")
                _db.insert_humedad_tierra(0)
                print("Tierra seca")
            else:
                datos_humedad_suelo.append("Humedo")
                actualizar_lcd("Suelo humedo")
                _db.insert_humedad_tierra(1)
                print("Tierra humeda")

            eventos_sensores["humedad"].set()
            time.sleep(5)
        except Exception as e:
            print(f"Error en sensor_humedad: {e}")

def medir_distancia():
    GPIO.setup(TRIGGER, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    while programa_en_ejecucion:
        try:
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
            actualizar_lcd(f"Agua: {nivel_agua:.1f}cm")
            _db.insert_nivel_agua(nivel_agua)
            print(f"Nivel de agua: {nivel_agua:.1f} cm, Distancia: {distancia:.1f} cm")

            eventos_sensores["distancia"].set()
            time.sleep(5)
        except Exception as e:
            print(f"Error en medir_distancia: {e}")

if __name__ == "__main__":
    configurar_gpio()
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(EN, GPIO.OUT)
    GPIO.setup(IN1_VENTILADOR, GPIO.OUT)
    GPIO.setup(EN_VENTILADOR, GPIO.OUT)
    
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(EN, GPIO.HIGH)
    GPIO.output(IN1_VENTILADOR, GPIO.LOW)
    GPIO.output(EN_VENTILADOR, GPIO.HIGH)

    iniciar_lcd()

    try:
        dht11_interior_thread = threading.Thread(target=dht11_interior)
        dht11_exterior_thread = threading.Thread(target=dht11_exterior)
        humedad_thread = threading.Thread(target=sensor_humedad)
        distancia_thread = threading.Thread(target=medir_distancia)

        dht11_interior_thread.start()
        dht11_exterior_thread.start()
        humedad_thread.start()
        distancia_thread.start()

        while True:
            for evento in eventos_sensores.values():
                evento.wait()
            print("Todas las lecturas completadas")
            for evento in eventos_sensores.values():
                evento.clear()

    except KeyboardInterrupt:
        print("\nPrograma finalizado por el usuario.")
        programa_en_ejecucion = False
        dht11_interior_thread.join()
        dht11_exterior_thread.join()
        humedad_thread.join()
        distancia_thread.join()
    finally:
        GPIO.cleanup()
        SENSOR_INTERIOR.exit()
        SENSOR_EXTERIOR.exit()
        actualizar_lcd("Adios")
        print("Recursos liberados.")
