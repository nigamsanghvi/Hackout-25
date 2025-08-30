// Initialize the map
function initMap() {
    const map = L.map('map').setView([-2.5, 118.0], 5);
    
    // Add base layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    // Add satellite imagery layer
    const satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
    });
    
    // Add layer control
    const baseMaps = {
        "Street Map": L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }),
        "Satellite": satelliteLayer
    };
    
    L.control.layers(baseMaps).addTo(map);
    
    // Add incidents to map
    if (typeof reportsData !== 'undefined') {
        reportsData.forEach(report => {
            const marker = L.marker([report.latitude, report.longitude]).addTo(map);
            
            let statusClass = 'secondary';
            if (report.status === 'validated') statusClass = 'success';
            else if (report.status === 'reported') statusClass = 'warning';
            else if (report.status === 'action_taken') statusClass = 'info';
            
            marker.bindPopup(`
                <div class="popup-content">
                    <h5>${report.incident_type}</h5>
                    ${report.photo_url ? `<img src="${report.photo_url}" class="img-fluid mb-2" alt="Incident photo">` : ''}
                    <p><strong>Status:</strong> <span class="badge bg-${statusClass}">${report.status}</span></p>
                    <p><strong>Reported:</strong> ${report.created_at}</p>
                    <a href="/reports/${report.id}" class="btn btn-sm btn-primary">View Details</a>
                </div>
            `);
        });
    }
    
    // Add location control
    const locateControl = L.control.locate({
        position: 'topright',
        drawCircle: true,
        follow: true,
        setView: true,
        keepCurrentZoomLevel: true,
        markerStyle: {
            weight: 1,
            opacity: 0.8,
            fillOpacity: 0.8
        },
        circleStyle: {
            weight: 1,
            clickable: false
        },
        icon: 'bi bi-geo-fill',
        metric: true,
        strings: {
            title: "Show my location",
            popup: "You are within {distance} {unit} from this point",
            outsideMapBoundsMsg: "You seem located outside the map boundaries"
        },
        locateOptions: {
            maxZoom: 16,
            watch: true,
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        }
    }).addTo(map);
    
    // Handle map clicks for report creation
    if (document.getElementById('report-form-map')) {
        const reportMap = L.map('report-form-map').setView([-2.5, 118.0], 5);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(reportMap);
        
        let marker = null;
        
        reportMap.on('click', function(e) {
            const { lat, lng } = e.latlng;
            
            // Update form fields
            document.getElementById('id_latitude').value = lat;
            document.getElementById('id_longitude').value = lng;
            
            // Update marker position
            if (marker) {
                reportMap.removeLayer(marker);
            }
            
            marker = L.marker([lat, lng]).addTo(reportMap)
                .bindPopup('Incident location<br>Lat: ' + lat.toFixed(4) + '<br>Lng: ' + lng.toFixed(4))
                .openPopup();
        });
        
        // Add locate control to report form map
        locateControl.addTo(reportMap);
    }
}

// Initialize map when page loads
document.addEventListener('DOMContentLoaded', initMap);