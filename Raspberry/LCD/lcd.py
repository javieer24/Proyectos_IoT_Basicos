from RPLCD.i2c import CharLCD
import time

# Inicializa el LCD con el chip PCF8574 y la dirección I2C
lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)  # Ajusta cols y rows si es necesario

# Tiempo total de ejecución en segundos
tiempo_total = 180  # 3 minutos
tiempo_inicio = time.time()  # Marca de tiempo inicial

# Cuento en forma de mensajes
cuento = [
    "Había una vez",
    "un robot curioso",
    "que amaba leer",
    "y contar historias.",
    "Un día decidió",
    "explorar el mundo",
    "y compartir sus",
    "aventuras en LCD.",
    "El tiempo pasaba",
    "y nunca se cansó",
    "de aprender y",
    "enseñar a otros.",
    "Fin del cuento",
    "Gracias por leer"
]

# Iterar los mensajes del cuento mientras no se exceda el tiempo total
indice = 0  # Índice para recorrer el cuento

while time.time() - tiempo_inicio < tiempo_total:
    mensaje_actual = cuento[indice % len(cuento)]  # Repite mensajes si es necesario
    lcd.write_string(mensaje_actual)  # Muestra el mensaje en el LCD
    print(mensaje_actual)  # Imprime en la consola

    time.sleep(5)  # Espera 5 segundos
    lcd.clear()  # Limpia el LCD

    indice += 1  # Avanza al siguiente mensaje

# Finaliza el programa limpiando el LCD
lcd.clear()
print("El programa ha terminado.")  # Mensaje final en consola
