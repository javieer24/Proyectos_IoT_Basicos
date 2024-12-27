# Historias en una Pantalla: Proyecto de LCD con Raspberry Pi
Este proyecto te guiará en la creación de un pequeño lector de cuentos digital utilizando una Raspberry Pi y una pantalla LCD. Aprenderás a configurar la pantalla LCD, a programar en Python y a crear una sencilla aplicación que muestre una historia línea por línea.

## LCD 
Las pantallas LCD funcionan controlando la orientación de los cristales líquidos para permitir o bloquear el paso de la luz. Al combinar millones de estos píxeles y utilizando filtros de color, se pueden crear imágenes a todo color.

### ¿Qué es una pantalla LCD?
LCD son las siglas en inglés de "Liquid Crystal Display", que en español significa "pantalla de cristal líquido". Es un tipo de pantalla que utiliza cristales líquidos para mostrar imágenes. Estos cristales líquidos son moléculas orgánicas que cambian su orientación cuando se les aplica un campo eléctrico, permitiendo el paso o bloqueo de la luz.

### ¿Qué es I2C?
I2C (Inter-Integrated Circuit) es un protocolo de comunicación serial que permite conectar múltiples dispositivos a un bus común utilizando solo dos hilos: uno de datos (SDA) y otro de reloj (SCL). Esto lo hace muy eficiente en términos de cableado, especialmente cuando se tienen varios dispositivos como sensores o pantallas LCD.

## ¿Cómo funciona la LCD con I2C?
1. **Módulo adaptador:**
   - Entre la Raspberry Pi y la LCD, generalmente se utiliza un módulo adaptador como el PCF8574. Este módulo actúa como un puente, traduciendo las señales I2C de la Raspberry Pi a los comandos que la LCD entiende.
    - El módulo PCF8574 tiene una dirección I2C específica que se puede configurar mediante puentes. Esta dirección es la que se utiliza en el código para identificar la pantalla LCD y enviar comandos.
  
2. **Comandos:**
   - Para controlar la LCD, se envían comandos a través del bus I2C. Estos comandos pueden ser para:
        - Limpiar la pantalla: Borrar todo el contenido de la pantalla.
        - Escribir caracteres: Mostrar caracteres en la posición actual del cursor.

3. **Librería RPLCD.i2c**
   -Esta librería en Python facilita la interacción con la pantalla LCD. Abstrae los detalles de bajo nivel del protocolo I2C y proporciona una interfaz sencilla para enviar comandos a la pantalla


## Datasheet

<p align="center">
    <img src="IMG\lcd.png">
</p>

## Conexión Raspberry 

<p align="center">
    <img src="IMG\Lcdi2c.jpg">
</p>
<p align="center">
    <img src="IMG\Lcdi2c_esquemático.jpg">
</p>

## Explicación código

### ¿Cómo funciona el código?

```bash
lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)
```
hace lo siguiente:
- `PCF8574`: Especifica que se está utilizando un módulo PCF8574 como adaptador I2C.
- **0x27:** Indica la dirección I2C del módulo. Asegúrate de que esta dirección coincida con la configuración física de tu módulo.
- **cols=16, rows=2:** Define las dimensiones de la pantalla LCD (16 columnas y 2 filas).
Luego, en el bucle while, se utilizan métodos de la clase CharLCD para:

- **Escribir_string:** Envía una cadena de texto a la pantalla.
- **clear:** Limpia la pantalla.

1. Importa las librerías necesarias:`RPLCD.i2c` para interactuar con la pantalla LCD y `time` para manejar el tiempo.
2. Inicializa la pantalla LCD: Configura la pantalla LCD con las dimensiones correctas y la dirección I2C.
3. Define un cuento: Crea una lista de cadenas de texto que representarán las líneas del cuento.
4. Bucle principal:
    - Obtiene el mensaje actual del cuento.
    - Muestra el mensaje en la pantalla LCD y en la consola.
    - Espera 5 segundos.
    - Limpia la pantalla LCD.
    - Incrementa el índice para pasar al siguiente mensaje.
5. Finaliza el programa: Limpia la pantalla LCD y muestra un mensaje final en la consola.

### Visualización del Funcionamiento
Imagina que la pantalla LCD es una hoja de papel cuadriculado. Cada cuadrado es un píxel que puede mostrar un carácter. El cursor es como un lápiz que se mueve por la hoja y escribe los caracteres en la posición actual. Los comandos que se envían a la LCD le indican al cursor dónde moverse y qué caracteres escribir.
