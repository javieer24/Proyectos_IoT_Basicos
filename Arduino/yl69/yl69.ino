#define SOIL_SENSOR_PIN 7 // Pin digital conectado a la salida D0 del módulo

void setup() {
  pinMode(SOIL_SENSOR_PIN, INPUT); // Configura el pin como entrada
  Serial.begin(9600); 
  Serial.println("Iniciando medición de humedad del suelo...");
}

void loop() {
  // Leer el estado digital del sensor
  int soilState = digitalRead(SOIL_SENSOR_PIN);

  // Interpretar la lectura
  if (soilState == HIGH) {
    // Señal alta: el suelo está seco
    Serial.println("El suelo está seco.");
  } else {
    // Señal baja: el suelo está húmedo
    Serial.println("El suelo está húmedo.");
  }

  delay(2000); // Pausa entre lecturas
}

