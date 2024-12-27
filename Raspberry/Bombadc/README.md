 # Control de Bomba de Agua DC con L298N y Raspberry Pi

 Este proyecto demuestra cómo utilizar una Raspberry Pi y un módulo L298N para controlar una bomba de agua DC. El código proporcionado permite una interacción básica con la bomba, incluyendo el encendido, apagado y, en futuras implementaciones, la regulación de la velocidad.

 ## ¿Cómo Funciona?
 ### Funcionamiento del L298N
 El L298N es un circuito integrado que actúa como un puente H, permitiendo controlar la dirección y la velocidad de un motor DC. En este caso, se utiliza para controlar una bomba de agua DC.

- **Pines IN1 y IN2:** Controlan la dirección del motor. Al cambiar el estado lógico de estos pines, se invierte el sentido de giro del motor.
- **Pin EN:** Controla la velocidad del motor mediante modulación por ancho de pulso (PWM). Al variar el ciclo de trabajo de este pin, se modifica la velocidad del motor.

## Datasheet

<p align="center">
    <img src="IMG\L298N.png">
</p>

## Conexión Raspberry 

<p align="center">
    <img src="IMG\bombadc.png">
</p>
<p align="center">
    <img src="IMG\bombadc_esquemático.png">
</p>

## Explicación código

- **Importación de librerías:** Se importan las librerías `RPi.GPIO`  para controlar los pines GPIO de la Raspberry Pi y `time` para introducir pausas en el programa.
- **Definición de pines:** Se asignan los pines GPIO 24 y 25 a las variables`in1` y `en`, respectivamente.
- **Configuración de GPIO:** Se configura el modo de numeración de los pines GPIO (BCM) y se establecen los pines `in1` y `en` como salidas.
- **Configuración inicial:** Se establece el pin `in1` en alto para activar la dirección del motor y el pin `en` en alto para conectar el pin de habilitación directamente a la alimentación, lo que hace que el motor funcione a máxima potencia.
- **Bucle principal:** El programa entra en un bucle infinito donde espera una entrada del usuario.
    - **'r':** Enciende el motor a máxima potencia.
    - **'s':** Apaga el motor.
    - **'e':** Limpia los GPIO y termina el programa.


