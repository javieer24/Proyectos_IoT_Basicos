# Monitor de Presión Atmosférica con BMP280
Este proyecto se centra en el sensor BMP280, un dispositivo utilizado para medir la altura, la presión barométrica y la temperatura. Los datos obtenidos de este sensor pueden ser utilizados en diversas aplicaciones, como meteorología, agricultura y control ambiental.

## Funcionamiento del Sensor BMP280
El sensor BMP280 es un dispositivo electrónico que combina un sensor de presión barométrica y un sensor de temperatura en un solo chip. Es ampliamente utilizado en aplicaciones que requieren medir la presión atmosférica y la temperatura con alta precisión, como estaciones meteorológicas caseras, drones, sistemas de control ambiental y más.
##  ¿Cómo funciona?
- **Principio de funcionamiento:** El sensor mide la deformación de un elemento sensible a la presión cuando varía la presión atmosférica. A partir de esta deformación, calcula la presión en hectopascales (hPa). La temperatura se mide mediante un termistor integrado.
- **CComunicación:** Se comunica con un microcontrolador (como la Raspberry Pi) a través de dos interfaces principales: I2C y SPI. En tu código, estás utilizando la interfaz I2C.
- **Configuración:** Puedes configurar varios parámetros del sensor, como la sobremuestreo de los datos, el filtro y la frecuencia de medición, para optimizar el rendimiento según tus necesidades.
## Datasheet

<p align="center">
    <img src="IMG\bmp280.png">
</p>
El datasheet del BMP280 proporcionará información detallada sobre las características técnicas del sensor, como:

- **Rango de medición:** Los valores mínimo y máximo que puede medir el sensor para la presión y la temperatura.
- **Consumo de corriente:** La cantidad de corriente que consume el sensor.(Recomendado de alimentar con 5VC)
- **Regímenes de funcionamiento:** Diferentes modos de operación del sensor para optimizar el consumo de energía y la frecuencia de muestreo.
- **Instrucciones de configuración:** Cómo configurar los diferentes parámetros del sensor a través de los registros I2C.


## Conexión Raspberry
<p align="center">
    <img src="IMG\bmp280_esquemático.png">
    <img src="IMG\Conexion.png">
</p>

## Explicación código
- **Importación de librerías:** Se importan las librerías necesarias para trabajar con el sensor y realizar operaciones de tiempo.
- **Creación de la conexión I2C:** Se establece una conexión I2C con el sensor utilizando los pines SCL y SDA de la Raspberry Pi.
- **Creación del objeto BMP280:** Se crea un objeto de la clase `Adafruit_BMP280_I2C` para interactuar con el sensor.
- **Configuración del nivel del mar:** Se establece la presión al nivel del mar para calcular la altitud de forma más precisa.
- **Función `obtener_datos_bmp280:`**
    - Lee los valores de temperatura, presión y altitud del sensor.
    - Imprime los valores formateados en la consola.
- **Bucle principal:**
    - Llama repetidamente a la función `obtener_datos_bmp280` para realizar mediciones periódicas.
  