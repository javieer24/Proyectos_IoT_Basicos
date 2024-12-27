import RPi.GPIO as GPIO
from time import sleep

# Pines de control del motor
in1 = 24
en = 25

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)

# Configuración inicial para máxima potencia
GPIO.output(in1, GPIO.HIGH)  # Activa la dirección del motor
GPIO.output(en, GPIO.HIGH)  # Conecta el pin de habilitación directamente a HIGH

print("\n")
print("Bomba funcionando a máxima potencia.")
print("Opciones: r-run s-stop e-exit")
print("\n")

while True:
    x = input()

    if x == 'r':
        print("run")
        GPIO.output(in1, GPIO.HIGH)  # Vuelve a encender la bomba
        GPIO.output(en, GPIO.HIGH)

    elif x == 's':
        print("stop")
        GPIO.output(in1, GPIO.LOW)  # Apaga la bomba

    elif x == 'e':
        GPIO.cleanup()
        print("GPIO Clean up")
        break

    else:
        print("<<<  dato incorrecto  >>>")
        print("por favor ingresa 'r', 's' o 'e'.")
