# Control de Nivel de Agua con Sensor Ultrasónico y Raspberry Pi
Este proyecto utiliza un sensor ultrasónico para medir la distancia y calcular el nivel de agua en un recipiente utilizando una Raspberry Pi. El código calcula la distancia del sensor al agua y determina el nivel en función de la altura del recipiente.

## ¿Cómo Funciona?
### Funcionamiento del Sensor Ultrasónico
El sensor ultrasónico mide distancias mediante la emisión de ondas de sonido y la recepción de los ecos reflejados por un objeto. La distancia se calcula con la fórmula:

La fórmula para calcular la distancia es:

$$
\text{Distancia} = \frac{\text{Tiempo de ida y vuelta} \times \text{Velocidad del sonido}}{2}
$$

- **Trigger:** Pin de salida que envía un pulso ultrasónico
- **Echo:** Pin de entrada que detecta el eco del pulso.

## Especificaciones usada (Referencia)
- **Velocidad del sonido:** 340 m/s (34,000 cm/s) a temperatura ambiente.
- **Altura de la botella:** 13 cm (modificable según el recipiente usado).

## Datasheet

<p align="center">
    <img src="IMG\sonic.png">
</p>

## Conexión Raspberry 

<p align="center">
    <img src="IMG\ultrasonic.png">
</p>
<p align="center">
    <img src="IMG\Ultrasonic_esquemático.png">
</p>

## Explicación código

- Importación de librerías: Se utilizan `RPi.GPIO` para controlar los pines GPIO y `time` para medir intervalos con precisión.
- Definición de pines GPIO: Se asignan los pines GPIO 5 y 6 para el Trigger y Echo, respectivamente.
- Altura del recipiente: La constante `ALTURA_BOTELLA` define la altura del recipiente en cm.
- Función medir: Realiza las siguientes acciones:
    1. Envía un pulso ultrasónico.
    2. Calcula la duración del pulso recibido.
    3. Convierte la duración en distancia.
    4. Calcula el nivel de agua restando la distancia medida de la altura del recipiente.
- Bucle principal: Realiza mediciones en tiempo real, mostrando:
    - Nivel de agua en cm.
    - Distancia medida por el sensor.
- Limpieza de GPIO: Al terminar el programa (interrumpido con `Ctrl+C`), limpia los pines GPIO para evitar conflictos futuros.