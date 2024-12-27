import RPi.GPIO as GPIO
from time import sleep

# Pines de control del ventilador
in1 = 27
en = 23

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)

# Configuración inicial para máxima potencia
GPIO.output(in2, GPIO.HIGH)  # Activa la dirección del ventilador
GPIO.output(en, GPIO.HIGH)  # Conecta el pin de habilitación directamente a HIGH

print("\n")
print("Ventilador funcionando a máxima potencia.")
print("Opciones: r-run s-stop e-exit")
print("\n")

while True:
    x = input()

    if x == 'r':
        print("run")
        GPIO.output(in2, GPIO.HIGH)  # Vuelve a encender el ventilador
        GPIO.output(en, GPIO.HIGH)

    elif x == 's':
        print("stop")
        GPIO.output(in2, GPIO.LOW)  # Apaga el ventilador

    elif x == 'e':
        GPIO.cleanup()
        print("GPIO Clean up")
        break

    else:
        print("<<<  dato incorrecto  >>>")
        print("por favor ingresa 'r', 's' o 'e'.")
