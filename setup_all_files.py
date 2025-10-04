"""
This script creates all the files needed for the Polygon Mapper project.
Just run this script and it will set up everything for you!
"""

import os

def create_project():
    # Create project directory
    project_dir = "polygon-mapper"
    os.makedirs(project_dir, exist_ok=True)
    os.chdir(project_dir)
    
    print("Creating Polygon Mapper project files...")
    print("=" * 60)
    
    # Create requirements.txt
    requirements = """flask==3.0.0
"""
    with open("requirements.txt", "w") as f:
        f.write(requirements)
    print("✓ Created requirements.txt")
    
    # Create polygon_mapper.py
    polygon_mapper = '''"""
Polygon Mapper - Standalone Web Application
Draw polygons on a map and export as GeoJSON
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import os
from datetime import datetime
import webbrowser
import threading

app = Flask(__name__)

# Store polygons in memory
polygons = []

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/polygons', methods=['GET'])
def get_polygons():
    """Return all polygons"""
    return jsonify({
        'type': 'FeatureCollection',
        'features': polygons
    })

@app.route('/api/polygons', methods=['POST'])
def add_polygon():
    """Add a new polygon"""
    data = request.json
    polygons.append(data)
    return jsonify({'success': True, 'count': len(polygons)})

@app.route('/api/polygons', methods=['DELETE'])
def clear_polygons():
    """Clear all polygons"""
    global polygons
    polygons = []
    return jsonify({'success': True})

@app.route('/api/export', methods=['GET'])
def export_geojson():
    """Export polygons as GeoJSON file"""
    if not polygons:
        return jsonify({'error': 'No polygons to export'}), 400
    
    feature_collection = {
        'type': 'FeatureCollection',
        'features': polygons
    }
    
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'output/polygons_{timestamp}.geojson'
    
    # Save to file
    with open(filename, 'w') as f:
        json.dump(feature_collection, f, indent=2)
    
    return send_file(filename, as_attachment=True)

def open_browser():
    """Open the browser after a short delay"""
    import time
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Create the HTML template
    html_content = \'\'\'<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Polygon Mapper</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <link rel="stylesheet" href="https://unpkg.com/leaflet-draw@1.0.4/dist/leaflet.draw.css" />
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            font-size: 28px;
            margin-bottom: 10px;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 14px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .controls {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        .instructions {
            background: #e8f4f8;
            border-left: 4px solid #3388ff;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 15px;
        }
        
        .instructions h3 {
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 16px;
        }
        
        .instructions ol {
            margin-left: 20px;
            color: #555;
            font-size: 14px;
            line-height: 1.8;
        }
        
        .button-group {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .btn-primary {
            background: #3388ff;
            color: white;
        }
        
        .btn-success {
            background: #28a745;
            color: white;
        }
        
        .btn-warning {
            background: #ffc107;
            color: #333;
        }
        
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .btn:disabled:hover {
            transform: none;
            box-shadow: none;
        }
        
        #map {
            height: 600px;
            border-radius: 10px;
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
            border: 2px solid #ddd;
        }
        
        .status {
            margin-top: 15px;
            padding: 12px;
            border-radius: 6px;
            font-size: 14px;
            display: none;
        }
        
        .status.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
            display: block;
        }
        
        .status.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
            display: block;
        }
        
        .status.info {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
            display: block;
        }
        
        .counter {
            background: #667eea;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>📍 Polygon Mapper</h1>
            <p>Draw polygons on the map and export them as GeoJSON files</p>
        </div>
    </div>
    
    <div class="container">
        <div class="controls">
            <div class="instructions">
                <h3>📝 How to Use:</h3>
                <ol>
                    <li>Click the <strong>polygon tool</strong> (⬟) in the map\\'s left toolbar</li>
                    <li>Click on the map to create vertices for your polygon</li>
                    <li>Double-click or click the first point again to complete the polygon</li>
                    <li>Draw as many polygons as you need</li>
                    <li>Click <strong>"Export GeoJSON"</strong> to download all polygons</li>
                </ol>
            </div>
            
            <div class="button-group">
                <button class="btn btn-success" onclick="exportGeoJSON()" id="exportBtn">
                    📥 Export GeoJSON
                </button>
                <button class="btn btn-warning" onclick="clearAll()">
                    🗑️ Clear All
                </button>
                <span class="counter" id="counter">Polygons: 0</span>
            </div>
            
            <div id="status" class="status"></div>
        </div>
        
        <div id="map"></div>
    </div>

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://unpkg.com/leaflet-draw@1.0.4/dist/leaflet.draw.js"></script>
    <script>
        // Initialize map
        const map = L.map('map').setView([39.8283, -98.5795], 4);
        
        // Add OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(map);
        
        // Create feature group for drawn items
        const drawnItems = new L.FeatureGroup();
        map.addLayer(drawnItems);
        
        // Initialize draw control
        const drawControl = new L.Control.Draw({
            draw: {
                polygon: {
                    shapeOptions: {
                        color: '#3388ff',
                        weight: 3
                    }
                },
                polyline: false,
                rectangle: false,
                circle: false,
                marker: false,
                circlemarker: false
            },
            edit: {
                featureGroup: drawnItems,
                remove: true
            }
        });
        map.addControl(drawControl);
        
        let polygonCount = 0;
        
        // Handle polygon creation
        map.on(L.Draw.Event.CREATED, function(event) {
            const layer = event.layer;
            drawnItems.addLayer(layer);
            
            // Convert to GeoJSON
            const geojson = layer.toGeoJSON();
            
            // Send to server
            fetch('/api/polygons', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(geojson)
            })
            .then(response => response.json())
            .then(data => {
                polygonCount = data.count;
                updateCounter();
                showStatus(`✓ Polygon ${polygonCount} added successfully!`, 'success');
            });
        });
        
        // Handle polygon deletion
        map.on(L.Draw.Event.DELETED, function(event) {
            const layers = event.layers;
            layers.eachLayer(function(layer) {
                polygonCount--;
            });
            updateCounter();
            showStatus('Polygon(s) deleted', 'info');
        });
        
        function updateCounter() {
            document.getElementById('counter').textContent = `Polygons: ${polygonCount}`;
            document.getElementById('exportBtn').disabled = polygonCount === 0;
        }
        
        function showStatus(message, type) {
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = `status ${type}`;
            
            setTimeout(() => {
                status.className = 'status';
            }, 5000);
        }
        
        function exportGeoJSON() {
            if (polygonCount === 0) {
                showStatus('⚠ No polygons to export. Draw some polygons first!', 'error');
                return;
            }
            
            fetch('/api/export')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Export failed');
                    }
                    return response.blob();
                })
                .then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `polygons_${new Date().getTime()}.geojson`;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                    showStatus(`✓ Exported ${polygonCount} polygon(s) successfully!`, 'success');
                })
                .catch(error => {
                    showStatus('⚠ Export failed. Please try again.', 'error');
                });
        }
        
        function clearAll() {
            if (polygonCount === 0) {
                showStatus('No polygons to clear', 'info');
                return;
            }
            
            if (confirm(`Are you sure you want to clear all ${polygonCount} polygon(s)?`)) {
                drawnItems.clearLayers();
                
                fetch('/api/polygons', {
                    method: 'DELETE'
                })
                .then(response => response.json())
                .then(data => {
                    polygonCount = 0;
                    updateCounter();
                    showStatus('✓ All polygons cleared', 'success');
                });
            }
        }
        
        // Initialize counter
        updateCounter();
    </script>
</body>
</html>\'\'\'
    
    # Write HTML template
    with open('templates/index.html', 'w') as f:
        f.write(html_content)
    
    # Start browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    print("\\n" + "="*60)
    print("🗺️  POLYGON MAPPER - STARTING")
    print("="*60)
    print("\\n✓ Server starting at: http://127.0.0.1:5000")
    print("✓ Browser will open automatically...")
    print("\\n📁 Exported files will be saved in the 'output' folder")
    print("\\n⚠️  Press CTRL+C to stop the server\\n")
    print("="*60 + "\\n")
    
    # Run Flask app
    app.run(debug=False, port=5000)
'''
    
    with open("polygon_mapper.py", "w", encoding='utf-8') as f:
        f.write(polygon_mapper)
    print("✓ Created polygon_mapper.py")
    
    # Create build_executable.py
    build_script = '''"""
Build script to create standalone executables for Polygon Mapper
Run this script to generate executables for your platform
"""

import os
import sys
import subprocess

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    print("📦 Installing PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    print("✓ PyInstaller installed\\n")

def build_executable():
    """Build the executable using PyInstaller"""
    print("🔨 Building executable...\\n")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window
        "--name=PolygonMapper",         # Name of the executable
        "--add-data=templates:templates",  # Include templates folder
        "--hidden-import=flask",
        "--hidden-import=werkzeug",
        "--collect-all=flask",
        "polygon_mapper.py"
    ]
    
    # Adjust add-data syntax for Windows
    if sys.platform == "win32":
        cmd[4] = "--add-data=templates;templates"
    
    try:
        subprocess.check_call(cmd)
        print("\\n" + "="*60)
        print("✓ BUILD SUCCESSFUL!")
        print("="*60)
        print("\\n📁 Your executable is located in the 'dist' folder:")
        
        if sys.platform == "win32":
            print("   → dist/PolygonMapper.exe")
        elif sys.platform == "darwin":
            print("   → dist/PolygonMapper")
        else:
            print("   → dist/PolygonMapper")
        
        print("\\n📝 Instructions:")
        print("   1. Navigate to the 'dist' folder")
        print("   2. Double-click the executable to run")
        print("   3. Your browser will open automatically")
        print("   4. Draw polygons and export as GeoJSON")
        print("\\n💡 You can distribute this executable to users")
        print("   They don't need Python or any dependencies!\\n")
        
    except subprocess.CalledProcessError as e:
        print("\\n❌ Build failed!")
        print(f"Error: {e}")
        sys.exit(1)

def main():
    print("\\n" + "="*60)
    print("POLYGON MAPPER - EXECUTABLE BUILDER")
    print("="*60 + "\\n")
    
    # Check if polygon_mapper.py exists
    if not os.path.exists("polygon_mapper.py"):
        print("❌ Error: polygon_mapper.py not found!")
        print("   Make sure you're running this script in the same directory")
        sys.exit(1)
    
    # Check if templates directory exists, create if needed
    if not os.path.exists("templates"):
        print("📁 Creating templates directory...")
        os.makedirs("templates", exist_ok=True)
        print("   Run polygon_mapper.py once to generate the HTML template")
        print("   Then run this build script again\\n")
        sys.exit(0)
    
    # Install PyInstaller
    try:
        import PyInstaller
        print("✓ PyInstaller already installed\\n")
    except ImportError:
        install_pyinstaller()
    
    # Build executable
    build_executable()

if __name__ == "__main__":
    main()
'''
    
    with open("build_executable.py", "w") as f:
        f.write(build_script)
    print("✓ Created build_executable.py")
    
    # Create README
    readme = """# Polygon Mapper

Quick setup guide - see BUILD_INSTRUCTIONS.md for detailed build instructions.

## Quick Start

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the app directly:
   ```
   python polygon_mapper.py
   ```
   Opens at http://localhost:5000

3. Build executable:
   ```
   python build_executable.py
   ```
   Executable will be in the `dist/` folder

## Files Created

- polygon_mapper.py - Main application
- requirements.txt - Dependencies
- build_executable.py - Build script
- templates/index.html - Auto-generated UI

See BUILD_INSTRUCTIONS.md for platform-specific build guides.
"""
    
    with open("README.md", "w") as f:
        f.write(readme)
    print("✓ Created README.md")
    
    print("\n" + "=" * 60)
    print("✅ PROJECT SETUP COMPLETE!")
    print("=" * 60)
    print(f"\n📁 Project created in: {os.getcwd()}")
    print("\n🚀 Next steps:")
    print("   1. cd polygon-mapper")
    print("   2. pip install -r requirements.txt")
    print("   3. python polygon_mapper.py (to test)")
    print("   4. python build_executable.py (to create executable)")
    print("\n💡 Your executable will be in the 'dist' folder\n")

if __name__ == "__main__":
    create_project()
    print("Done! Check the polygon-mapper folder.")
