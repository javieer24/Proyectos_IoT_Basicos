# Bienvenido a la carpeta de proyectos con Raspberry Pi

**En esta carpeta encontrarás todos los proyectos desarrollados utilizando una Raspberry Pi como plataforma principal. ¡Explora el potencial de la Raspberry Pi y da vida a tus ideas! En este repositorio encontrarás una colección de proyectos diseñados para ayudarte a aprender y experimentar con la electrónica y la programación.**
## Estructura

~~~
├── Raspberry
│   ├── BMP280
│   │   ├── bmp280.py
│   │   ├── README.md
│   ├── bombadc
│   │   ├── bombadc.py
│   │   ├── README.md
│   ├── LCD
│   │   ├── lcd.py
│   │   ├── README.md
│   ├── Sistema de Monitoreo Climatico
│   │   ├── README.md
│   │   ├── sensores.py
│   ├── Sistema dde Riego Autoomatizado
│   │   ├── README.md
│   │   ├── Sensores.py
│   ├── ultra_sonico
│   │   ├── README.md
│   │   ├── ultrasonic.py
│   ├── Ventilador
│   │   ├── README.md
│   │   ├── ventiladordc.py
│   ├── Yl-69
│   │   ├── README.md
│   │   ├── yl-69.py
└── README.md
~~~
### ¿Qué encontrarás aquí?
- Proyectos prácticos: Desde estaciones meteorológicas hasta sistemas de riego automatizado, cada proyecto te ofrece una experiencia de aprendizaje completa.
- Código abierto: Todo el código es de acceso libre, lo que te permite modificarlo y adaptarlo a tus necesidades.
- Documentación detallada: Cada proyecto viene acompañado de una guía paso a paso que te ayudará a reproducir los resultados.
- Ejemplos de uso: Aprende cómo utilizar cada sensor y componente de forma práctica.

## Proyectos Destacados 
- Sistema de Monitoreo Climático
- Sistema de Riego Automatizado

## **Requisitos previos**
- Raspberry Pi: Con sistema operativo Raspberry Pi OS instalado.
- Conexión a internet: Para descargar las librerías.
- Terminal: Acceder a la terminal de la Raspberry Pi.
## Instalación Raspberry pi OS
Raspberry Pi OS es el sistema operativo oficial para las Raspberry Pi y es el más recomendado para la mayoría de los usuarios. Su instalación es sencilla y se realiza a través de una herramienta gráfica llamada Raspberry Pi Imager.
### Pasos:
1. **Descargar Raspberry Pi Imager:**  
   - Visita la página oficial de [Raspberry Pi](https://www.raspberrypi.com/software/) y descarga la versión de Raspberry Pi Imager compatible con tu sistema operativo (Windows, macOS o Linux).

2. **Preparar la tarjeta SD:**
   - Inserta una tarjeta SD con suficiente capacidad (mínimo 8GB) en tu ordenador.
   - Ejecuta Raspberry Pi Imager.
3. **Seleccionar la imagen del SO**
   - En Raspberry Pi Imager, seleccionar la imagen de Raspberry Pi OS que se  desea instalar. Puede elegir entre la versión de 32 bits o 64 bits, dependiendo del modelo de tu Raspberry Pi.
4. **Seleccionar la tarjeta SD:**
   - Elige la tarjeta SD que has insertado en tu ordenador.
5. **Escribir la imagen:**
   - Haga clic en el botón "Escribir" para comenzar el proceso de escritura de la imagen en la tarjeta SD. ¡Atención! Este proceso formateará la tarjeta SD y eliminará todos los datos que contenga.
6. **Configurar la Raspberry Pi:**
   -   Una vez finalizada la escritura, inserta la tarjeta SD en tu Raspberry Pi.
   -   Opcional
       -   Conecta tu Raspberry Pi a un monitor, teclado y mouse.
       -   Conecta tu Raspberry Pi a un monitor, teclado y mouse.
### Configuración inicial
- **Idioma y zona horaria:** Se te pedirá que configures el idioma y la zona horaria de tu sistema.
- **Contraseña:** Establece una contraseña para el usuario principal (por defecto, "pi").
- **Expandir el sistema de archivos:** Se recomienda expandir el sistema de archivos para utilizar toda la capacidad de la tarjeta SD.

### Acces
- **Habilitar SSH:** Si quieres acceder a tu Raspberry Pi de forma remota, habilita SSH durante el proceso de instalación o edita el archivo /boot/config.txt en la tarjeta SD antes de escribir la imagen.

### Recurso Adicional
-  [**Documentación Oficial**](https://www.raspberrypi.com/documentation/computers/getting-started.html)
- [**Raspberry Conect**](https://www.raspberrypi.com/software/connect/)


## **Instalación requerimientos previos**

Verificar la versión de Python 3:

Abre una terminal en tu Raspberry Pi y ejecuta el siguiente comando:
```bash
python3 --version
```
Esto te mostrará la versión de Python 3 actualmente instalada.

Actualizar Python 3 (si es necesario):
Normalmente, la versión de Python 3 que viene preinstalada en Raspberry Pi OS es bastante estable. Sin embargo, si se desea actualizar a una versión más reciente, se puede hacer siguiendo estos pasos:

1. Actualizar la lista de paquetes
   ```bash
    sudo apt-get update
    ```
2. Instalar la version deseada
   ```bash
    sudo apt-get install python3.10
    ```
3. Añadir repositorios de terceros
   ```bash
    sudo apt-add-repository ppa:deadsnakes/ppa
    ```
### Instalar Librerias deseadas
Comandos de instalación
1. I2C
   ```bash
    sudo apt-get update
    ```
   ```bash
    sudo apt-get install python3-rpi.gpio i2c-tools
    ```
2. Instalar librerias con pip
   ```bash
    sudo pip3 install Adafruit-DHT Adafruit-BMP280 RPLCD pytz
    ```
### Explicación librerias:

-  `sudo apt-get update`: Actualiza la lista de paquetes disponibles en los repositorios de software.

- `sudo apt-get install python3-rpi.gpio i2c-tools:`  Instala las librerías RPi.GPIO (para controlar los pines GPIO) y i2c-tools (para comunicación I2C).
- `sudo pip3 install Adafruit-DHT Adafruit-BMP280 RPLCD pytz: `   Instala las librerías específicas utilizadas en los códigos ejemplo del presente repositorio:
  - `Adafruit-DHT:` Para trabajar con sensores DHT11, DHT22, etc.
  - `Adafruit-BMP280:` Para trabajar con el sensor de presión y temperatura BMP280.
  - `RPLCD:`  Para controlar pantallas LCD.
  -  `pytz:`  Para trabajar con zonas horarias.