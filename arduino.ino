#define DHTPIN 2  // Pin où le DHT11 est connecté

// Fonction pour lire les données brutes du DHT11
void readDHT11Data(uint8_t* data) {
  pinMode(DHTPIN, OUTPUT);
  digitalWrite(DHTPIN, LOW);  // Envoyer un signal de démarrage
  delay(18);                  // Attendre 18 ms
  digitalWrite(DHTPIN, HIGH); // Fin du signal de démarrage
  delayMicroseconds(40);
  
  pinMode(DHTPIN, INPUT);     // Passer en mode lecture

  // Attendre la réponse du capteur
  while (digitalRead(DHTPIN) == HIGH);
  while (digitalRead(DHTPIN) == LOW);
  while (digitalRead(DHTPIN) == HIGH);

  // Lire les 40 bits (5 octets) de données
  for (int i = 0; i < 5; i++) {
    data[i] = 0;
    for (int j = 0; j < 8; j++) {
      while (digitalRead(DHTPIN) == LOW);  // Attendre le début du bit
      delayMicroseconds(30);               // Après 30 µs, lire la valeur
      if (digitalRead(DHTPIN) == HIGH) {
        data[i] |= (1 << (7 - j));         // Stocker le bit
      }
      while (digitalRead(DHTPIN) == HIGH); // Attendre la fin du bit
    }
  }
}

void setup() {
  Serial.begin(9600); // Initialiser la communication série
}

void loop() {
  uint8_t data[5]; // Tableau pour stocker les données brutes
  
  readDHT11Data(data); // Lire les données du DHT11

  // Envoyer les données brutes à la Raspberry Pi
  for (int i = 0; i < 5; i++) {
    Serial.print(data[i], HEX);  // Envoyer chaque octet en hexadécimal
    Serial.print(" ");
  }
  Serial.println();  // Nouvelle ligne pour chaque série de données

  delay(6000);  // Attendre 2 secondes avant la prochaine lecture
}