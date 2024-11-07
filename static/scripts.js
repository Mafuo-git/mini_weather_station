document.addEventListener('DOMContentLoaded', (event) => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    // Configuration des graphiques Chart.js
    var ctxTemp = document.getElementById('temperatureChart').getContext('2d');
    var temperatureChart = new Chart(ctxTemp, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Température (°C)',
                data: [],
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Temps' } },
                y: { title: { display: true, text: 'Température (°C)' }, beginAtZero: true }
            }
        }
    });

    var ctxHum = document.getElementById('humidityChart').getContext('2d');
    var humidityChart = new Chart(ctxHum, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Humidité (%)',
                data: [],
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Temps' } },
                y: { title: { display: true, text: 'Humidité (%)' }, beginAtZero: true }
            }
        }
    });

    // Réception des données du serveur
    socket.on('update_data', (data) => {
        // Mettre à jour les valeurs actuelles
        document.getElementById('current-temperature').textContent = data.latest_temperature;
        document.getElementById('current-humidity').textContent = data.latest_humidity;
        document.getElementById('last-update').textContent = data.latest_time;

        // Mettre à jour les graphiques
        temperatureChart.data.labels = data.timestamps;
        temperatureChart.data.datasets[0].data = data.temperatures;
        temperatureChart.update();

        humidityChart.data.labels = data.timestamps;
        humidityChart.data.datasets[0].data = data.humidities;
        humidityChart.update();
    });
});
