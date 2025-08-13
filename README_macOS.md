# BuymaLister macOS Desktop App

This guide will help you convert your Python project into a native macOS desktop application.

## 🚀 Quick Start

1. **Clone/Download** this project to your Mac
2. **Run the build script**: `./build_macos.sh`
3. **Install the app**: Drag `dist/BuymaLister.app` to Applications folder
4. **Create DMG** (optional): `./create_dmg.sh`

## 📋 Prerequisites

### System Requirements
- **macOS 10.13 (High Sierra) or later**
- **Python 3.8+** (3.9+ recommended)
- **8GB RAM minimum** (16GB recommended for building)
- **2GB free disk space**

### Required Software
- **Python 3**: Download from [python.org](https://www.python.org/downloads/)
- **Homebrew** (for additional tools): Install with:
  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```

## 🛠️ Installation & Setup

### 1. Install Dependencies
```bash
# Install macOS-specific requirements
pip3 install -r requirements_macos.txt

# Or install PyInstaller globally
pip3 install pyinstaller
```

### 2. Create App Icon
```bash
# Option 1: Use the Python script
python3 create_icon.py

# Option 2: Use the shell script (includes icon creation)
./build_macos.sh
```

### 3. Build the App
```bash
# Make scripts executable
chmod +x build_macos.sh create_dmg.sh

# Build the macOS app
./build_macos.sh
```

## 📁 Project Structure

```
buyma_2.01_app/
├── index.py                 # Main application entry point
├── index_macos.spec        # PyInstaller spec for macOS
├── requirements_macos.txt   # macOS-specific dependencies
├── build_macos.sh          # Build script
├── create_icon.py          # Icon creation script
├── create_dmg.sh           # DMG creation script
├── assets/                 # App assets (icons, images)
├── views/                  # UI components
├── controllers/            # Business logic
└── dist/                   # Built application (after build)
    └── BuymaLister.app     # macOS app bundle
```

## 🔧 Build Process

### What the Build Script Does

1. **Environment Setup**
   - Creates virtual environment
   - Installs dependencies
   - Checks system requirements

2. **Icon Creation**
   - Converts `background.png` to `.icns` format
   - Creates multiple icon sizes for different resolutions
   - Generates proper macOS app icon

3. **App Building**
   - Runs PyInstaller with macOS-specific configuration
   - Bundles all dependencies
   - Creates `.app` bundle

4. **Post-Build**
   - Verifies build success
   - Shows app location and size
   - Optionally opens the app

### Manual Build (Alternative)

If you prefer to build manually:

```bash
# 1. Create icon
python3 create_icon.py

# 2. Build with PyInstaller
pyinstaller index_macos.spec

# 3. Check result
ls -la dist/
```

## 📱 App Features

### macOS Integration
- **Native app bundle** (`.app` format)
- **Retina display support**
- **Dark mode compatibility**
- **Proper app icon**
- **System notifications support**
- **App Store ready** (with additional signing)

### User Experience
- **No terminal window** (pure GUI)
- **Proper window management**
- **macOS-style window behavior**
- **Responsive design**

## 🚀 Distribution

### Option 1: Direct Installation
```bash
# Copy app to Applications
cp -r dist/BuymaLister.app /Applications/

# Or drag and drop in Finder
open dist/
```

### Option 2: Create DMG
```bash
# Install create-dmg tool
brew install create-dmg

# Create distribution DMG
./create_dmg.sh
```

### Option 3: App Store (Advanced)
For App Store distribution, you'll need:
- **Apple Developer Account** ($99/year)
- **Code signing certificates**
- **App Store Connect setup**
- **Additional metadata files**

## 🔍 Troubleshooting

### Common Issues

#### 1. "Python not found"
```bash
# Install Python 3
brew install python3

# Verify installation
python3 --version
```

#### 2. "PyInstaller not found"
```bash
# Install PyInstaller
pip3 install pyinstaller

# Or use requirements
pip3 install -r requirements_macos.txt
```

#### 3. "Permission denied" on scripts
```bash
# Make scripts executable
chmod +x build_macos.sh create_dmg.sh create_icon.py
```

#### 4. "Icon creation failed"
```bash
# Check if PIL/Pillow is installed
pip3 install Pillow

# Try manual icon creation
python3 create_icon.py
```

#### 5. "Build failed"
```bash
# Check error messages
tail -f build.log

# Clean and retry
rm -rf build dist
./build_macos.sh
```

#### 6. "App won't open"
```bash
# Check app permissions
ls -la dist/BuymaLister.app/Contents/MacOS/

# Run from terminal to see errors
./dist/BuymaLister.app/Contents/MacOS/BuymaLister
```

### Performance Issues

#### Large App Size
- **Exclude unnecessary packages** in `index_macos.spec`
- **Use UPX compression** (already enabled)
- **Remove unused dependencies**

#### Slow Startup
- **Optimize imports** in your code
- **Use lazy loading** for heavy modules
- **Profile startup time**

## 🎯 Customization

### App Metadata
Edit `index_macos.spec` to change:
- **App name**: `name='BuymaLister'`
- **Bundle ID**: `bundle_identifier='com.buyma.lister'`
- **Version**: `CFBundleVersion`
- **Minimum macOS version**: `LSMinimumSystemVersion`

### Icon Customization
1. **Replace** `assets/icon.icns`
2. **Or modify** `create_icon.py`
3. **Use your own** `.png` or `.jpg` files

### UI Customization
- **Edit** `views/` files for UI changes
- **Modify** `index.py` for app behavior
- **Add** custom themes and styles

## 📚 Advanced Topics

### Code Signing
```bash
# Sign the app (requires Developer ID)
codesign --force --deep --sign "Developer ID Application: Your Name" dist/BuymaLister.app

# Verify signature
codesign -dv dist/BuymaLister.app
```

### Notarization (for distribution outside App Store)
```bash
# Submit for notarization
xcrun altool --notarize-app --primary-bundle-id "com.buyma.lister" \
  --username "your-apple-id@example.com" \
  --password "app-specific-password" \
  --file BuymaLister.dmg

# Staple notarization ticket
xcrun stapler staple dist/BuymaLister.app
```

### Automated Builds
```bash
# Add to CI/CD pipeline
#!/bin/bash
set -e
./build_macos.sh
./create_dmg.sh
# Upload to distribution server
```

## 🤝 Support

### Getting Help
1. **Check** this README first
2. **Review** error messages carefully
3. **Search** for similar issues online
4. **Ask** in relevant forums/communities

### Contributing
- **Report bugs** with detailed information
- **Suggest improvements** for macOS compatibility
- **Share** your customizations and tips

## 📄 License

This project is licensed under the same terms as the original BuymaLister project.

---

**Happy Building! 🎉**

Your macOS desktop app is just a few commands away! 