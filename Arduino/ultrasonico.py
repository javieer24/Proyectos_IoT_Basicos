import RPi.GPIO as GPIO
import time
from RPLCD.i2c import CharLCD

# Configuración inicial de los pines GPIO
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 5
GPIO_ECHO = 6
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# Configuración del LCD
lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)

# Constantes
VEL_SONIDO = 34000.0  # cm/s
NUM_LECTURAS = 100
ALTURA_MAXIMA = 12.0  # Altura total del bote en cm
DISTANCIA_100 = 1.0   # Distancia mínima medida para 100% (aproximadamente 11 cm de altura del líquido)
DISTANCIA_VACIO = 12.0  # Distancia máxima medida para 0% (bote vacío)

# Variables
lecturas = [0.0] * NUM_LECTURAS
total = 0.0
lectura_actual = 0
primera_media = False

# Función para medir distancia
def medir_distancia():
    # Enviar pulso de disparo
    GPIO.output(GPIO_TRIGGER, GPIO.LOW)
    time.sleep(0.000002)
    GPIO.output(GPIO_TRIGGER, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, GPIO.LOW)

    # Esperar a la respuesta del Echo
    while GPIO.input(GPIO_ECHO) == 0:
        inicio_pulso = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        fin_pulso = time.time()

    # Calcular duración del pulso
    duracion_pulso = fin_pulso - inicio_pulso

    # Calcular distancia en cm
    distancia = (duracion_pulso * VEL_SONIDO) / 2.0
    return distancia

# Inicialización del LCD
lcd.clear()
lcd.write_string("Nivel LiQuido")
lcd.cursor_pos = (1, 0)
lcd.write_string("Ultrasonico")
time.sleep(2)
lcd.clear()

try:
    while True:
        # Eliminar la última medida
        total -= lecturas[lectura_actual]

        # Obtener una nueva distancia
        distancia = medir_distancia()
        lecturas[lectura_actual] = distancia

        # Actualizar el total
        total += lecturas[lectura_actual]
        lectura_actual += 1

        # Reiniciar si se llega al final del array
        if lectura_actual >= NUM_LECTURAS:
            primera_media = True
            lectura_actual = 0

        # Calcular la media
        media = total / NUM_LECTURAS

        # Mostrar resultados si hay suficientes datos
        if primera_media:
            if media <= DISTANCIA_100:
                porcentaje = 100
            elif media >= DISTANCIA_VACIO:
                porcentaje = 0
            else:
                porcentaje = int((DISTANCIA_VACIO - media) / (DISTANCIA_VACIO - DISTANCIA_100) * 100)

            lcd.clear()
            lcd.cursor_pos = (0, 0)
            lcd.write_string(f"Altura: {ALTURA_MAXIMA - media:.1f} cm")
            lcd.cursor_pos = (1, 0)
            lcd.write_string(f"{porcentaje} %")

            print(f"Media: {media:.2f} cm")
            print(f"Altura del liquido: {ALTURA_MAXIMA - media:.1f} cm")
            print(f"Porcentaje: {porcentaje} %")
        else:
            lcd.cursor_pos = (0, 0)
            lcd.write_string(f"Calculando: {lectura_actual}")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nSaliendo del programa...")
    lcd.clear()
    GPIO.cleanup()
