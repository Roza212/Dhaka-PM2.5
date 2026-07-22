// Initialize Leaflet Map centered on Dhaka
const map = L.map('gis-map', {
    zoomControl: false // Customizing UI
}).setView([23.8103, 90.4125], 13);

L.control.zoom({ position: 'bottomright' }).addTo(map);

// Dark themed tiles for premium aesthetic (CartoDB Dark Matter)
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
    subdomains: 'abcd',
    maxZoom: 20
}).addTo(map);

// Chart.js Global Setup
const ctx = document.getElementById('predictionChart').getContext('2d');
Chart.defaults.color = '#8b949e';
Chart.defaults.font.family = 'Inter';

let predictionChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Current', '+1h', '+3h', '+6h'],
        datasets: [{
            label: 'Predicted PM2.5 (µg/m³)',
            data: [0, 0, 0, 0],
            borderColor: '#00f2fe',
            backgroundColor: 'rgba(0, 242, 254, 0.1)',
            borderWidth: 3,
            fill: true,
            tension: 0.4, // Smooth curve
            pointBackgroundColor: '#fff',
            pointRadius: 5,
            pointHoverRadius: 8
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: {
                backgroundColor: 'rgba(0,0,0,0.8)',
                titleFont: { size: 14, family: 'Inter' },
                bodyFont: { size: 14, family: 'Inter' },
                padding: 10,
                displayColors: false
            }
        },
        scales: {
            y: {
                beginAtZero: false,
                grid: { color: 'rgba(255, 255, 255, 0.05)' }
            },
            x: {
                grid: { display: false }
            }
        }
    }
});

let currentMarker = null;

// Mock Data Fetcher (Simulating FastAPI connection)
async function fetchPredictions() {
    const horizon = document.getElementById('horizon-select').value;
    const aqiElement = document.getElementById('current-aqi');
    
    // Simulate UI loading state
    aqiElement.innerText = 'Syncing...';
    aqiElement.style.color = '#8b949e';
    
    // Simulate network delay for effect
    await new Promise(r => setTimeout(r, 600));

    // Mock API Response matching FastAPI /api/v1/predictions/hyperlocal schema
    const baseValue = 140 + (Math.random() * 30 - 10);
    const mockData = {
        current_pm25: baseValue,
        confidence_score: 0.88 + (Math.random() * 0.1),
        predictions: [
            { hour_offset: 1, predicted_pm25: baseValue + 12 },
            { hour_offset: 3, predicted_pm25: baseValue + 25 },
            { hour_offset: 6, predicted_pm25: baseValue - 5 }
        ]
    };

    updateDashboard(mockData);
}

function updateDashboard(data) {
    // 1. Update Sidebar Stats
    const currentPm25 = data.current_pm25.toFixed(1);
    const aqiElement = document.getElementById('current-aqi');
    
    aqiElement.innerText = currentPm25;
    // Dynamic color change based on pollution severity
    const severityColor = currentPm25 > 150 ? '#ff4757' : (currentPm25 > 100 ? '#ffa502' : '#2ed573');
    aqiElement.style.color = severityColor;
    
    document.getElementById('confidence-score').innerText = (data.confidence_score * 100).toFixed(1) + '%';

    // 2. Update Chart.js Data
    predictionChart.data.datasets[0].data = [
        data.current_pm25,
        data.predictions[0].predicted_pm25,
        data.predictions[1].predicted_pm25,
        data.predictions[2].predicted_pm25
    ];
    // Match line color to severity
    predictionChart.data.datasets[0].borderColor = severityColor;
    predictionChart.data.datasets[0].backgroundColor = severityColor + '20'; // 20 hex is ~12% opacity
    predictionChart.update();

    // 3. Update GIS Map
    const lat = 23.7383 + (Math.random() * 0.02 - 0.01); // Randomize slightly in Dhaka
    const lng = 90.3957 + (Math.random() * 0.02 - 0.01);
    
    // Custom glowing HTML marker
    const markerHtml = `
        <div style="
            background: ${severityColor};
            width: 18px;
            height: 18px;
            border-radius: 50%;
            box-shadow: 0 0 20px ${severityColor};
            border: 2px solid #fff;
            animation: pulse 2s infinite;
        "></div>
    `;
    const customIcon = L.divIcon({
        className: 'custom-div-icon',
        html: markerHtml,
        iconSize: [18, 18],
        iconAnchor: [9, 9]
    });

    if(currentMarker) {
        map.removeLayer(currentMarker);
    }

    currentMarker = L.marker([lat, lng], {icon: customIcon})
        .addTo(map)
        .bindPopup(`
            <div style="font-family: 'Inter'; text-align: center;">
                <strong style="color: #000; font-size: 1.1em;">Gridlock Intersection</strong><br>
                <span style="color: #666;">Predicted AQI: <b style="color: ${severityColor}">${data.predictions[2].predicted_pm25.toFixed(1)}</b></span>
            </div>
        `, { closeButton: false })
        .openPopup();
        
    // Smooth cinematic fly-to animation
    map.flyTo([lat, lng], 15, { 
        duration: 2.0,
        easeLinearity: 0.25
    });
}

// Event Listeners
document.getElementById('refresh-btn').addEventListener('click', fetchPredictions);
document.getElementById('horizon-select').addEventListener('change', fetchPredictions);

// Initial Load Trigger
window.onload = fetchPredictions;
