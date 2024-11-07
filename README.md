# Mini Weather Station
Mini station météo très basique utilisant une Raspberry Pi 3 B+ et une Arduino Uno.
Voici comment faire fonctionner le projet :

Ce fichier explique comment lancer le projet et récupérer les données de température et d’humidité depuis un capteur DHT11, connecté à un Arduino (lui-même relié en série (filaire) avec la Raspberry Pi 3 B+), vers une base de données MariaDB (existante dans la Raspberry).


Prérequis

1. Arduino : Assurez-vous d’avoir un Arduino connecté, avec un capteur DHT11 branché sur le pin numérique 2.
2. Base de données MariaDB : Un serveur MariaDB doit être configuré et accessible. Vous aurez besoin des identifiants (hôte, utilisateur, mot de passe, nom de base de données) pour vous connecter.




Étapes d’installation


1. Injection du code Arduino

Avant de lancer le code Python, il est nécessaire d’injecter le code Arduino dans votre carte Arduino. Assurez-vous que :
	•	Le capteur DHT11 est connecté sur le pin numérique 2 de l’Arduino.
	•	Le code Arduino est configuré pour lire les données de température et d’humidité à partir du capteur et pour les transmettre au Raspberry Pi (ou à l’ordinateur utilisé).

Pour injecter le code Arduino :
	•	Ouvrez l’IDE Arduino.
	•	Chargez le fichier arduino.ino fourni avec ce projet.
	•	Branchez votre Arduino via USB.
	•	Téléversez le code sur l’Arduino.


2. Configuration de la base de données dans app.py

Ouvrez le fichier app.py et vérifiez les identifiants de connexion à la base de données. Vous devrez peut-être ajuster les paramètres suivants :
    host="localhost",		# Adresse de la base de données (par défaut, localhost)
    user="root",			#  Votre nom d'utilisateur pour MariaDB
    password="pi",			# Votre mot passe pour MariaDB
    database="SensorData"	# Nom de la base de données

Modifiez ces valeurs avec vos informations MariaDB pour que le programme puisse se connecter.


3. Lancement des scripts Python

Pour lancer le programme, suivez ces étapes :
1.	Démarrez app.py : Ce script initialise la connexion à la base de données et prépare l’application pour recevoir des données. Pour cela, ouvrez un terminal, placez-vous dans le dossier du projet et exécutez la commande suivante :

python3 app.py

2.	Lancez donnees_arduino.py en parallèle : Ce script récupère les données de température et d’humidité envoyées par l’Arduino et les transmet au programme principal. Ouvrez un autre terminal dans le même dossier, et exécutez :

python3 donnees_arduino.py

Ce script enverra automatiquement les relevés de température et d’humidité du capteur DHT11 connecté à l’Arduino.




Notes

•	Assurez-vous que votre Arduino est bien branché et que le capteur DHT11 fonctionne correctement.
•	Si vous rencontrez des erreurs de connexion avec MariaDB, vérifiez les identifiants et que le serveur MariaDB est bien accessible.
