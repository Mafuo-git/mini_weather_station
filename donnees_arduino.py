import serial
import time
import mysql.connector
from datetime import datetime

# Fonction pour convertir les données brutes du DHT11
def convert_data(data):
    humidity = data[0] + data[1] / 256.0
    temperature = data[2] + data[3] / 256.0
    checksum = data[4]
    
    # Vérification du checksum
    if (data[0] + data[1] + data[2] + data[3]) & 0xFF != checksum:
        return None, None, "Checksum invalide"
    
    return humidity, temperature, None

# Initialiser la communication série avec l'Arduino
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # Pause pour que la connexion série s'initialise


# Connexion a la base de donnees
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pi",
    database="SensorData",
)

cursor = db_connection.cursor()

# Création de la base de données si elle n'existe pas
cursor.execute("CREATE DATABASE IF NOT EXISTS SensorData")
db_connection.database = "SensorData"

# Création de la table mesures si elle n'existe pas
create_table_query = """
CREATE TABLE IF NOT EXISTS mesures (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    temperature FLOAT(5,2) DEFAULT NULL,
    humidite FLOAT(5,2) DEFAULT NULL,
    horodatage DATETIME DEFAULT CURRENT_TIMESTAMP,
    latitude FLOAT(9,6) DEFAULT NULL,
    longitude FLOAT(9,6) DEFAULT NULL
)
"""
cursor.execute(create_table_query)

while True:
    # Lire les données envoyées par l'Arduino
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        if line:
            # Split des données reçues en octets (en hexadécimal)
            data_hex = line.split()
            data = [int(x, 16) for x in data_hex]  # Convertir en valeurs décimales
            
            if len(data) == 5:  # Si on reçoit bien les 5 octets
                humidity, temperature, error = convert_data(data)
                if error:
                    print(error)
                else:
                    print(f'Humidité : {humidity} %')
                    print(f'Température : {temperature} °C')
                    
                    #Recuperer horodatage actuel
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                    latitude = 50.63420410
                    longitude = 3.04876040 #coordonnées gps de l'isen
                    # Insertion des donnees dans la DB
                    insert_query = "INSERT INTO mesures (temperature, humidite, horodatage,latitude,longitude) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(insert_query, (temperature, humidity, current_time,latitude,longitude))
                    db_connection.commit()     # valider la transaction
                    
    time.sleep(6)

# Fermer la connexion a la DB
cursor.close()
db_connection.close()
