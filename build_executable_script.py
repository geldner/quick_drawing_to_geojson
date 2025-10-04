"""
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
    print("✓ PyInstaller installed\n")

def build_executable():
    """Build the executable using PyInstaller"""
    print("🔨 Building executable...\n")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window (comment out if you want to see logs)
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
        print("\n" + "="*60)
        print("✓ BUILD SUCCESSFUL!")
        print("="*60)
        print("\n📁 Your executable is located in the 'dist' folder:")
        
        if sys.platform == "win32":
            print("   → dist/PolygonMapper.exe")
        elif sys.platform == "darwin":
            print("   → dist/PolygonMapper")
        else:
            print("   → dist/PolygonMapper")
        
        print("\n📝 Instructions:")
        print("   1. Navigate to the 'dist' folder")
        print("   2. Double-click the executable to run")
        print("   3. Your browser will open automatically")
        print("   4. Draw polygons and export as GeoJSON")
        print("\n💡 You can distribute this executable to users")
        print("   They don't need Python or any dependencies!\n")
        
    except subprocess.CalledProcessError as e:
        print("\n❌ Build failed!")
        print(f"Error: {e}")
        sys.exit(1)

def main():
    print("\n" + "="*60)
    print("POLYGON MAPPER - EXECUTABLE BUILDER")
    print("="*60 + "\n")
    
    # Check if polygon_mapper.py exists
    if not os.path.exists("polygon_mapper.py"):
        print("❌ Error: polygon_mapper.py not found!")
        print("   Make sure you're running this script in the same directory")
        sys.exit(1)
    
    # Check if templates directory exists
    if not os.path.exists("templates"):
        print("⚠️  Warning: templates directory not found")
        print("   It will be created when you run polygon_mapper.py first")
        print("\n   Running polygon_mapper.py once to create templates...")
        subprocess.check_call([sys.executable, "polygon_mapper.py"])
    
    # Install PyInstaller
    try:
        import PyInstaller
        print("✓ PyInstaller already installed\n")
    except ImportError:
        install_pyinstaller()
    
    # Build executable
    build_executable()

if __name__ == "__main__":
    main()
