# Control de Sensor de Humedad de Suelo YL-69 con Raspberry Pi
Este proyecto demuestra cómo utilizar una Raspberry Pi y un sensor de humedad de suelo YL-69 para detectar el nivel de humedad en la tierra. El código proporcionado permite leer el estado del sensor y determinar si la tierra está húmeda o seca.

## ¿Cómo Funciona?
### Funcionamiento del Sensor YL-69
El sensor YL-69 detecta la humedad del suelo mediante la resistencia eléctrica. A través de su pin de datos, envía un estado lógico alto o bajo que indica el nivel de humedad:
- Salida Alta (HIGH): La tierra está seca.
- Salida Baja (LOW): La tierra está húmeda

El sensor consta de dos partes principales:
1. Sonda: Insertada en la tierra para medir la humedad.
2. Módulo: Convierte la señal de la sonda en un dato legible por la Raspberry Pi.

## Datasheet

<p align="center">
    <img src="IMG\yl-69.png">
</p>

## Conexión Raspberry 

<p align="center">
    <img src="IMG\sensoryl69.png">
</p>
<p align="center">
    <img src="IMG\yl69_esquemático.png">
</p>

## Explicación código
- Importación de librerías: Se utilizan las librerías `RPi.GPIO` para manejar los pines GPIO y `time` para introducir pausas en el programa.
- Definición del pin GPIO: El pin GPIO 17 está configurado para leer datos del sensor.
- Configuración de GPIO: Se establece el modo BCM y el pin de entrada para el sensor.
- Función de lectura: Se define una función para leer el estado del sensor:
    - Devuelve "Húmeda" si la señal es baja (LOW).
    - Devuelve "Seca" si la señal es alta (HIGH).
    - Muestra un error si no puede leer el sensor.
- Bucle principal: El programa entra en un bucle infinito que lee el estado del sensor y muestra el nivel de humedad cada segundo.
    - Puede detenerse con `Ctrl+C`, limpiando los GPIO antes de finalizar.
