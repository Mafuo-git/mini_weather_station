from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import mysql.connector
import time
import threading
import folium

app = Flask(__name__)
socketio = SocketIO(app)

# Configuration de la base de données
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'pi',
    'database': 'SensorData',
}

# Fonction pour récupérer les dernières données et les envoyer au client
def fetch_latest_data():
    while True:
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            # Récupération de la dernière donnée
            latest_query = "SELECT temperature, humidite, horodatage FROM mesures ORDER BY horodatage DESC LIMIT 1"
            cursor.execute(latest_query)
            latest_row = cursor.fetchone()

            # Récupération des 10 dernières données pour les graphiques
            history_query = "SELECT temperature, humidite, horodatage, latitude, longitude FROM mesures ORDER BY horodatage DESC LIMIT 10"
            cursor.execute(history_query)
            latest_data = cursor.fetchall()

            cursor.close()
            connection.close()

            if latest_row and latest_data:
                # Extraction des données pour les graphiques
                temperatures = [row[0] for row in latest_data][::-1]
                humidities = [row[1] for row in latest_data][::-1]
                timestamps = [row[2].strftime('%H:%M:%S') for row in latest_data][::-1]
                latitude = latest_data[0][3]
                longitude = latest_data[0][4]

                # Création de la carte avec Folium
                m = folium.Map(location=[latitude, longitude], zoom_start=15)
                folium.Marker([latitude, longitude], popup="Localisation actuelle").add_to(m)
                m.save("templates/map.html")

                # Émission des données via SocketIO
                socketio.emit('update_data', {
                    'latest_temperature': latest_row[0],
                    'latest_humidity': latest_row[1],
                    'latest_time': latest_row[2].strftime('%Y-%m-%d %H:%M:%S'),
                    'temperatures': temperatures,
                    'humidities': humidities,
                    'timestamps': timestamps,
                    'latitude': latitude,
                    'longitude': longitude
                })

            time.sleep(6)

        except mysql.connector.Error as err:
            print(f"Erreur: {err}")

# Lancer le thread pour l'extraction des données
thread = threading.Thread(target=fetch_latest_data)
thread.daemon = True
thread.start()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
