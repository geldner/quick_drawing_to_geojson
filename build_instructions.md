# Building Polygon Mapper Executables

This guide will walk you through creating standalone executables for Windows, macOS, and Linux.

## 📋 Prerequisites

- Python 3.8 or higher installed
- Terminal/Command Prompt access
- Internet connection (for downloading dependencies)

---

## 🎯 Quick Start - Creating the Project Files

### Step 1: Create Project Directory

```bash
# Create a new folder for the project
mkdir polygon-mapper
cd polygon-mapper
```

### Step 2: Create All Required Files

You need to create 3 files. Copy the content for each:

#### File 1: `polygon_mapper.py`
Copy the entire content from the "polygon_mapper.py" artifact I provided above.

#### File 2: `requirements.txt`
```
flask==3.0.0
```

#### File 3: `build_executable.py`
Copy the entire content from the "build_executable.py" artifact I provided above.

---

## 🪟 Building for Windows

### On a Windows Machine:

1. **Open Command Prompt or PowerShell**

2. **Navigate to your project folder:**
   ```cmd
   cd path\to\polygon-mapper
   ```

3. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   pip install pyinstaller
   ```

4. **Build the executable:**
   ```cmd
   python build_executable.py
   ```
   
   OR manually:
   ```cmd
   pyinstaller --onefile --windowed --name=PolygonMapper --add-data="templates;templates" --hidden-import=flask --hidden-import=werkzeug --collect-all=flask polygon_mapper.py
   ```

5. **Find your executable:**
   - Location: `dist\PolygonMapper.exe`
   - Size: ~15-25 MB
   - This is the file you distribute to Windows users!

### Testing the Windows Executable:

```cmd
cd dist
PolygonMapper.exe
```

Your browser should open automatically to `http://localhost:5000`

---

## 🍎 Building for macOS

### On a Mac:

1. **Open Terminal**

2. **Navigate to your project folder:**
   ```bash
   cd path/to/polygon-mapper
   ```

3. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   pip3 install pyinstaller
   ```

4. **Build the executable:**
   ```bash
   python3 build_executable.py
   ```
   
   OR manually:
   ```bash
   pyinstaller --onefile --windowed --name=PolygonMapper --add-data="templates:templates" --hidden-import=flask --hidden-import=werkzeug --collect-all=flask polygon_mapper.py
   ```

5. **Find your executable:**
   - Location: `dist/PolygonMapper`
   - This is a Unix executable file
   - This is the file you distribute to Mac users!

### Testing the macOS Executable:

```bash
cd dist
./PolygonMapper
```

### Note for macOS Users:
When distributing to macOS users, they may need to:
1. Right-click the app → "Open" (first time only)
2. Click "Open" in the security dialog
3. Or run: `chmod +x PolygonMapper` to make it executable

---

## 🐧 Building for Linux

### On a Linux Machine:

1. **Open Terminal**

2. **Navigate to your project folder:**
   ```bash
   cd path/to/polygon-mapper
   ```

3. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   pip3 install pyinstaller
   ```

4. **Build the executable:**
   ```bash
   python3 build_executable.py
   ```
   
   OR manually:
   ```bash
   pyinstaller --onefile --windowed --name=PolygonMapper --add-data="templates:templates" --hidden-import=flask --hidden-import=werkzeug --collect-all=flask polygon_mapper.py
   ```

5. **Find your executable:**
   - Location: `dist/PolygonMapper`
   - This is a Linux executable
   - This is the file you distribute to Linux users!

### Testing the Linux Executable:

```bash
cd dist
chmod +x PolygonMapper
./PolygonMapper
```

---

## 📦 Creating Distribution Packages

### For Windows Users:

Create a simple ZIP file:
```
PolygonMapper-Windows.zip
├── PolygonMapper.exe
└── README.txt (simple instructions)
```

**README.txt content:**
```
POLYGON MAPPER - Windows

How to use:
1. Double-click PolygonMapper.exe
2. Your browser will open automatically
3. Draw polygons on the map
4. Click "Export GeoJSON" to save

Exported files are saved in the "output" folder.

Troubleshooting:
- If Windows Defender blocks it, click "More info" → "Run anyway"
- If it doesn't start, make sure no other app is using port 5000
```

### For macOS Users:

Create a ZIP or DMG:
```
PolygonMapper-macOS.zip
├── PolygonMapper
└── README.txt
```

**README.txt content:**
```
POLYGON MAPPER - macOS

How to use:
1. Right-click PolygonMapper and select "Open"
2. Click "Open" in the security dialog
3. Your browser will open automatically
4. Draw polygons on the map
5. Click "Export GeoJSON" to save

Exported files are saved in the "output" folder.

Note: You only need to right-click → Open the first time.
After that, you can double-click normally.
```

### For Linux Users:

Create a tarball:
```bash
tar -czf PolygonMapper-Linux.tar.gz PolygonMapper README.txt
```

**README.txt content:**
```
POLYGON MAPPER - Linux

How to use:
1. Make executable: chmod +x PolygonMapper
2. Run: ./PolygonMapper
3. Your browser will open automatically
4. Draw polygons on the map
5. Click "Export GeoJSON" to save

Exported files are saved in the "output" folder.
```

---

## 🔍 Troubleshooting Build Issues

### "PyInstaller not found"
```bash
pip install pyinstaller
# or
pip3 install pyinstaller
```

### "templates folder not found"
The templates folder is auto-created when you first run `polygon_mapper.py`. Run it once:
```bash
python polygon_mapper.py
# Wait for it to start, then press Ctrl+C
# Now the templates folder exists
```

### Build creates multiple files instead of one
Make sure you're using the `--onefile` flag in the PyInstaller command.

### Executable is too large (>50MB)
This is normal. PyInstaller bundles Python and all dependencies. 15-25MB is typical.

### Antivirus flags the executable
This is common with PyInstaller. Solutions:
- Build on the target OS
- Sign the executable with a code signing certificate
- Users can add an exception in their antivirus

### macOS "damaged" error
This happens with unsigned apps. Users should:
- Right-click → Open (not double-click)
- Or disable Gatekeeper temporarily: `sudo spctl --master-disable`

---

## 📝 Complete Build Checklist

- [ ] Create project folder
- [ ] Create `polygon_mapper.py`
- [ ] Create `requirements.txt`
- [ ] Create `build_executable.py`
- [ ] Install Python dependencies
- [ ] Run build script
- [ ] Test executable
- [ ] Create distribution package
- [ ] Write simple user instructions
- [ ] Test on clean system (if possible)

---

## 🎁 Alternative: Create Everything in One Go

Save this as `setup_project.py` and run it to auto-create all files:

```python
import os

# Create project structure
os.makedirs("polygon-mapper", exist_ok=True)
os.chdir("polygon-mapper")

# Create requirements.txt
with open("requirements.txt", "w") as f:
    f.write("flask==3.0.0\n")

print("✓ Created requirements.txt")
print("\nNext steps:")
print("1. Copy polygon_mapper.py content into a new file")
print("2. Copy build_executable.py content into a new file")
print("3. Run: python build_executable.py")
```

---

## 💡 Tips

- **Build on the target OS** for best compatibility (Windows exe on Windows, etc.)
- **Test thoroughly** on a clean machine without Python installed
- **Keep file size down** by using `--onefile` and excluding unnecessary imports
- **Version your releases** (e.g., PolygonMapper-v1.0-Windows.zip)
- **Sign your executables** if distributing widely (prevents security warnings)

---

## 🆘 Still Having Issues?

1. Make sure Python 3.8+ is installed: `python --version`
2. Check pip is working: `pip --version`
3. Try running the Python script directly first: `python polygon_mapper.py`
4. Check PyInstaller documentation: https://pyinstaller.org
5. Search for your specific error message

---

**Ready to build? Start with the Quick Start section above!** 🚀