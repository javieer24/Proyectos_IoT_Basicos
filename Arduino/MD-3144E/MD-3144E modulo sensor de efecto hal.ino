const int hallSensorPin = 2; // Pin digital conectado al OUT del sensor
volatile int pulseCount = 0; // Contador de pulsos (debe ser volatile para interrupciones)
unsigned long previousMillis = 0;
const long interval = 2000; // Intervalo de 1 segundo

// Radio del molino (en metros)
const float radius = 0.0125; // 1.25 cm convertido a metros

void setup() {
  pinMode(hallSensorPin, INPUT); // Configurar el pin como entrada
  attachInterrupt(digitalPinToInterrupt(hallSensorPin), countPulse, FALLING); // Interrupción al detectar un pulso
  Serial.begin(9600); // Iniciar la comunicación serial
}

void loop() {
  unsigned long currentMillis = millis();

  // Calcular y mostrar RPM y velocidad cada segundo
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    // Calcular RPM
    float rpm = pulseCount * 60.0;

    // Calcular velocidad angular en rad/s
    float omega = rpm * (2 * PI / 60);

    // Calcular velocidad lineal en m/s
    float velocity = omega * radius;

    // Mostrar resultados en el monitor serial
    Serial.print("RPM: ");
    Serial.println(rpm);

    Serial.print("Velocidad angular (rad/s): ");
    Serial.println(omega);

    Serial.print("Velocidad lineal (m/s): ");
    Serial.println(velocity);

    pulseCount = 0; // Reiniciar el contador de pulsos
  }
}

// Función de interrupción para contar pulsos
void countPulse() {
  pulseCount++;
}

