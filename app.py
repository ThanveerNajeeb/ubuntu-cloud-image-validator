from flask import Flask, render_template_string, request, jsonify
import folium
import itertools
import math

app = Flask(__name__)

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def optimize_route(locations):
    if len(locations) <= 2:
        return locations, round(calculate_distance(
            locations[0]['lat'], locations[0]['lon'],
            locations[1]['lat'], locations[1]['lon']), 2)
    best_route = None
    best_distance = float('inf')
    start = locations[0]
    stops = locations[1:]
    for perm in itertools.permutations(stops):
        route = [start] + list(perm)
        distance = sum(calculate_distance(
            route[i]['lat'], route[i]['lon'],
            route[i+1]['lat'], route[i+1]['lon']
        ) for i in range(len(route)-1))
        if distance < best_distance:
            best_distance = distance
            best_route = route
    return best_route, round(best_distance, 2)

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clicks Express - Route Optimizer</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', sans-serif; background: #0f0f1a; color: #ffffff; min-height: 100vh; }

        /* Header */
        .header {
            background: linear-gradient(135deg, #e63946 0%, #c1121f 100%);
            padding: 20px 40px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 4px 20px rgba(230, 57, 70, 0.4);
        }
        .header-left { display: flex; align-items: center; gap: 15px; }
        .logo { font-size: 28px; }
        .header h1 { font-size: 22px; font-weight: 700; letter-spacing: 0.5px; }
        .header p { font-size: 13px; opacity: 0.85; margin-top: 2px; }
        .badge { background: rgba(255,255,255,0.2); padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 600; }

        /* Main layout */
        .main { display: grid; grid-template-columns: 400px 1fr; gap: 0; min-height: calc(100vh - 80px); }

        /* Sidebar */
        .sidebar { background: #1a1a2e; padding: 30px; border-right: 1px solid #2a2a3e; overflow-y: auto; }
        .section-title { font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; color: #e63946; margin-bottom: 20px; display: flex; align-items: center; gap: 8px; }

        /* Input card */
        .input-card { background: #16213e; border-radius: 12px; padding: 20px; margin-bottom: 20px; border: 1px solid #2a2a3e; }
        .input-group { margin-bottom: 14px; }
        .input-group label { display: block; font-size: 12px; font-weight: 500; color: #8888aa; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.8px; }
        .input-group input {
            width: 100%; padding: 10px 14px;
            background: #0f0f1a; border: 1px solid #2a2a3e;
            border-radius: 8px; color: #ffffff; font-size: 14px;
            transition: all 0.2s;
            font-family: 'Inter', sans-serif;
        }
        .input-group input:focus { outline: none; border-color: #e63946; box-shadow: 0 0 0 3px rgba(230,57,70,0.15); }
        .input-group input::placeholder { color: #444466; }

        .btn-add {
            width: 100%; padding: 12px;
            background: linear-gradient(135deg, #e63946, #c1121f);
            color: white; border: none; border-radius: 8px;
            font-size: 14px; font-weight: 600; cursor: pointer;
            transition: all 0.2s; letter-spacing: 0.5px;
        }
        .btn-add:hover { transform: translateY(-1px); box-shadow: 0 4px 15px rgba(230,57,70,0.4); }

        /* Stops list */
        .stops-container { margin-bottom: 20px; }
        .stop-item {
            background: #16213e; border-radius: 10px; padding: 12px 16px;
            margin-bottom: 8px; border: 1px solid #2a2a3e;
            display: flex; align-items: center; gap: 12px;
            animation: slideIn 0.3s ease;
        }
        @keyframes slideIn { from { opacity: 0; transform: translateX(-10px); } to { opacity: 1; transform: translateX(0); } }
        .stop-number {
            width: 28px; height: 28px; border-radius: 50%;
            background: linear-gradient(135deg, #e63946, #c1121f);
            display: flex; align-items: center; justify-content: center;
            font-size: 12px; font-weight: 700; flex-shrink: 0;
        }
        .stop-number.start { background: linear-gradient(135deg, #06d6a0, #048a81); }
        .stop-info { flex: 1; }
        .stop-name { font-size: 14px; font-weight: 600; }
        .stop-coords { font-size: 11px; color: #666688; margin-top: 2px; }
        .stop-delete { background: none; border: none; color: #444466; cursor: pointer; font-size: 16px; padding: 4px; border-radius: 4px; transition: color 0.2s; }
        .stop-delete:hover { color: #e63946; }

        /* Action buttons */
        .btn-optimize {
            width: 100%; padding: 14px;
            background: linear-gradient(135deg, #06d6a0, #048a81);
            color: white; border: none; border-radius: 10px;
            font-size: 15px; font-weight: 700; cursor: pointer;
            transition: all 0.2s; margin-bottom: 10px; letter-spacing: 0.5px;
        }
        .btn-optimize:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(6,214,160,0.35); }
        .btn-clear {
            width: 100%; padding: 11px;
            background: transparent; color: #666688;
            border: 1px solid #2a2a3e; border-radius: 10px;
            font-size: 13px; font-weight: 500; cursor: pointer;
            transition: all 0.2s;
        }
        .btn-clear:hover { border-color: #e63946; color: #e63946; }

        /* Result card */
        .result-card {
            background: #16213e; border-radius: 12px; padding: 20px;
            border: 1px solid #06d6a0; margin-top: 20px; display: none;
        }
        .result-title { font-size: 13px; font-weight: 600; color: #06d6a0; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px; }
        .result-step { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
        .step-num { width: 22px; height: 22px; border-radius: 50%; background: #e63946; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; flex-shrink: 0; }
        .step-name { font-size: 13px; font-weight: 500; }
        .result-divider { height: 1px; background: #2a2a3e; margin: 15px 0; }
        .distance-badge {
            display: flex; align-items: center; justify-content: space-between;
            background: #0f0f1a; border-radius: 8px; padding: 12px 16px;
        }
        .distance-label { font-size: 12px; color: #666688; }
        .distance-value { font-size: 20px; font-weight: 700; color: #06d6a0; }

        /* Map area */
        .map-area { position: relative; background: #0f0f1a; }
        .map-placeholder {
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            height: 100%; color: #333355; gap: 15px;
        }
        .map-placeholder .icon { font-size: 60px; }
        .map-placeholder p { font-size: 16px; font-weight: 500; }
        .map-placeholder small { font-size: 13px; color: #222244; }
        #map-frame { width: 100%; height: 100%; border: none; display: none; }

        /* Loading */
        .loading { display: none; text-align: center; padding: 20px; color: #06d6a0; font-size: 13px; }
        .spinner { display: inline-block; width: 20px; height: 20px; border: 2px solid #2a2a3e; border-top-color: #06d6a0; border-radius: 50%; animation: spin 0.8s linear infinite; margin-right: 8px; vertical-align: middle; }
        @keyframes spin { to { transform: rotate(360deg); } }

        .empty-state { text-align: center; color: #333355; padding: 20px; font-size: 13px; }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-left">
            <div class="logo">🚚</div>
            <div>
                <h1>Clicks Express</h1>
                <p>AI-Powered Route Optimizer</p>
            </div>
        </div>
        <div class="badge">Qatar Delivery Network</div>
    </div>

    <div class="main">
        <!-- Sidebar -->
        <div class="sidebar">
            <div class="section-title">📍 Add Delivery Stop</div>

            <div class="input-card">
                <div class="input-group">
                    <label>Location Name</label>
                    <input id="name" placeholder="e.g. Villaggio Mall" />
                </div>
                <div class="input-group">
                    <label>Latitude</label>
                    <input id="lat" placeholder="e.g. 25.2948" type="number" step="any" />
                </div>
                <div class="input-group">
                    <label>Longitude</label>
                    <input id="lon" placeholder="e.g. 51.4450" type="number" step="any" />
                </div>
                <button class="btn-add" onclick="addStop()">+ Add Stop</button>
            </div>

            <div class="section-title">🗂️ Delivery Stops</div>
            <div class="stops-container" id="stops-list">
                <div class="empty-state">No stops added yet.<br>Add at least 2 to optimize.</div>
            </div>

            <div class="loading" id="loading"><span class="spinner"></span>Calculating best route...</div>

            <button class="btn-optimize" onclick="optimizeRoute()">🗺️ Optimize Route</button>
            <button class="btn-clear" onclick="clearAll()">🗑️ Clear All Stops</button>

            <div class="result-card" id="result-card">
                <div class="result-title">✅ Optimized Route</div>
                <div id="route-steps"></div>
                <div class="result-divider"></div>
                <div class="distance-badge">
                    <div>
                        <div class="distance-label">Total Distance</div>
                        <div class="distance-value" id="distance-value">-- km</div>
                    </div>
                    <div style="font-size:28px">📏</div>
                </div>
            </div>
        </div>

        <!-- Map -->
        <div class="map-area">
            <div class="map-placeholder" id="map-placeholder">
                <div class="icon">🗺️</div>
                <p>Your optimized route will appear here</p>
                <small>Add stops and click Optimize Route</small>
            </div>
            <iframe id="map-frame" src=""></iframe>
        </div>
    </div>

    <script>
        let stops = [];

        function addStop() {
            const name = document.getElementById('name').value.trim();
            const lat = parseFloat(document.getElementById('lat').value);
            const lon = parseFloat(document.getElementById('lon').value);
            if (!name || isNaN(lat) || isNaN(lon)) { alert('Please fill all fields correctly!'); return; }
            stops.push({ name, lat, lon });
            renderStops();
            document.getElementById('name').value = '';
            document.getElementById('lat').value = '';
            document.getElementById('lon').value = '';
            document.getElementById('name').focus();
        }

        document.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') addStop();
        });

        function renderStops() {
            const list = document.getElementById('stops-list');
            if (stops.length === 0) {
                list.innerHTML = '<div class="empty-state">No stops added yet.<br>Add at least 2 to optimize.</div>';
                return;
            }
            list.innerHTML = stops.map((s, i) => `
                <div class="stop-item">
                    <div class="stop-number ${i === 0 ? 'start' : ''}">${i === 0 ? '🏠' : i}</div>
                    <div class="stop-info">
                        <div class="stop-name">${s.name}</div>
                        <div class="stop-coords">${s.lat}, ${s.lon}</div>
                    </div>
                    <button class="stop-delete" onclick="deleteStop(${i})">✕</button>
                </div>
            `).join('');
        }

        function deleteStop(index) {
            stops.splice(index, 1);
            renderStops();
        }

        function clearAll() {
            stops = [];
            renderStops();
            document.getElementById('result-card').style.display = 'none';
            document.getElementById('map-frame').style.display = 'none';
            document.getElementById('map-placeholder').style.display = 'flex';
            document.getElementById('map-frame').src = '';
        }

        async function optimizeRoute() {
            if (stops.length < 2) { alert('Please add at least 2 stops!'); return; }
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result-card').style.display = 'none';
            const response = await fetch('/optimize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ stops })
            });
            const data = await response.json();
            document.getElementById('loading').style.display = 'none';
            document.getElementById('result-card').style.display = 'block';
            document.getElementById('route-steps').innerHTML = data.route.map((s, i) => `
                <div class="result-step">
                    <div class="step-num">${i + 1}</div>
                    <div class="step-name">${s.name}</div>
                </div>
            `).join('');
            document.getElementById('distance-value').textContent = data.distance + ' km';
            document.getElementById('map-placeholder').style.display = 'none';
            document.getElementById('map-frame').style.display = 'block';
            document.getElementById('map-frame').src = '/map?' + new Date().getTime();
        }
    </script>
</body>
</html>
'''

optimized = []
total_dist = 0

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/optimize', methods=['POST'])
def optimize():
    global optimized, total_dist
    data = request.json
    result, total_dist = optimize_route(data['stops'])
    optimized = result
    return jsonify({'route': result, 'distance': total_dist})

@app.route('/map')
def show_map():
    if not optimized:
        return "No route yet"
    m = folium.Map(location=[optimized[0]['lat'], optimized[0]['lon']], zoom_start=13,
                   tiles='CartoDB dark_matter')
    for i, loc in enumerate(optimized):
        color = 'green' if i == 0 else 'red'
        folium.Marker(
            [loc['lat'], loc['lon']],
            popup=folium.Popup(f"<b>{loc['name']}</b>", max_width=200),
            icon=folium.Icon(color=color, icon='info-sign')
        ).add_to(m)
    points = [[loc['lat'], loc['lon']] for loc in optimized]
    folium.PolyLine(points, color='#06d6a0', weight=4, opacity=0.8, dash_array='10').add_to(m)
    return m._repr_html_()

if __name__ == '__main__':
    app.run(debug=True)
