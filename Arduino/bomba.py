import RPi.GPIO as GPIO
import time

# Pines del L298N
IN1 = 17  # GPIO para IN1
IN2 = 27  # GPIO para IN2

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

def encender_bomba():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)  # Corriente en un sentido

def apagar_bomba():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)  # Sin corriente

try:
    print("Encendiendo la bomba...")
    encender_bomba()
    time.sleep(5)  # La bomba funciona por 5 segundos
    print("Apagando la bomba...")
    apagar_bomba()

finally:
    GPIO.cleanup()
