#!/bin/bash

# macOS Build Script for BuymaLister
# This script will build a macOS desktop app from the Python source code

set -e  # Exit on any error

echo "🚀 Starting macOS build process for BuymaLister..."

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Error: This script must be run on macOS"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/downloads/"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 is not installed"
    exit 1
fi

echo "✅ Python and pip found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install macOS-specific requirements
echo "📚 Installing macOS dependencies..."
pip install -r requirements_macos.txt

# Check if assets directory exists
if [ ! -d "assets" ]; then
    echo "📁 Creating assets directory..."
    mkdir -p assets
fi

# Create app icon if it doesn't exist
if [ ! -f "assets/icon.icns" ]; then
    echo "🎨 Creating app icon..."
    
    # Create a simple icon using sips (macOS built-in tool)
    # First, create a temporary PNG from the background.png if it exists
    if [ -f "background.png" ]; then
        echo "🖼️ Converting background.png to icon..."
        # Create different sizes for the icon
        sips -z 16 16 background.png --out assets/icon_16.png
        sips -z 32 32 background.png --out assets/icon_32.png
        sips -z 64 64 background.png --out assets/icon_64.png
        sips -z 128 128 background.png --out assets/icon_128.png
        sips -z 256 256 background.png --out assets/icon_256.png
        sips -z 512 512 background.png --out assets/icon_512.png
        
        # Create .icns file using iconutil (requires .iconset directory)
        mkdir -p assets/BuymaLister.iconset
        
        # Copy icons to iconset with proper naming
        cp assets/icon_16.png assets/BuymaLister.iconset/icon_16x16.png
        cp assets/icon_32.png assets/BuymaLister.iconset/icon_16x16@2x.png
        cp assets/icon_32.png assets/BuymaLister.iconset/icon_32x32.png
        cp assets/icon_64.png assets/BuymaLister.iconset/icon_32x32@2x.png
        cp assets/icon_64.png assets/BuymaLister.iconset/icon_64x64.png
        cp assets/icon_128.png assets/BuymaLister.iconset/icon_64x64@2x.png
        cp assets/icon_128.png assets/BuymaLister.iconset/icon_128x128.png
        cp assets/icon_256.png assets/BuymaLister.iconset/icon_128x128@2x.png
        cp assets/icon_256.png assets/BuymaLister.iconset/icon_256x256.png
        cp assets/icon_512.png assets/BuymaLister.iconset/icon_256x256@2x.png
        cp assets/icon_512.png assets/BuymaLister.iconset/icon_512x512.png
        cp assets/icon_512.png assets/BuymaLister.iconset/icon_512x512@2x.png
        
        # Create .icns file
        iconutil -c icns assets/BuymaLister.iconset -o assets/icon.icns
        
        # Clean up temporary files
        rm -rf assets/BuymaLister.iconset
        rm assets/icon_*.png
        
        echo "✅ App icon created successfully"
    else
        echo "⚠️ Warning: background.png not found, creating default icon..."
        # Create a simple colored square as default icon
        python3 -c "
import os
from PIL import Image, ImageDraw

# Create a simple icon
size = 512
img = Image.new('RGB', (size, size), color='#007AFF')
draw = ImageDraw.Draw(img)

# Draw a simple design
draw.rectangle([size//4, size//4, 3*size//4, 3*size//4], fill='white')
draw.text((size//2-50, size//2-20), 'BL', fill='#007AFF')

# Save as PNG first
img.save('assets/icon.png')

# Convert to different sizes and create .icns
os.system('sips -z 16 16 assets/icon.png --out assets/icon_16.png')
os.system('sips -z 32 32 assets/icon.png --out assets/icon_32.png')
os.system('sips -z 64 64 assets/icon.png --out assets/icon_64.png')
os.system('sips -z 128 128 assets/icon.png --out assets/icon_128.png')
os.system('sips -z 256 256 assets/icon.png --out assets/icon_256.png')
os.system('sips -z 512 512 assets/icon.png --out assets/icon_512.png')

# Create iconset directory
os.makedirs('assets/BuymaLister.iconset', exist_ok=True)

# Copy icons to iconset
os.system('cp assets/icon_16.png assets/BuymaLister.iconset/icon_16x16.png')
os.system('cp assets/icon_32.png assets/BuymaLister.iconset/icon_16x16@2x.png')
os.system('cp assets/icon_32.png assets/BuymaLister.iconset/icon_32x32.png')
os.system('cp assets/icon_64.png assets/BuymaLister.iconset/icon_32x32@2x.png')
os.system('cp assets/icon_64.png assets/BuymaLister.iconset/icon_64x64.png')
os.system('cp assets/icon_128.png assets/BuymaLister.iconset/icon_64x64@2x.png')
os.system('cp assets/icon_128.png assets/BuymaLister.iconset/icon_128x128.png')
os.system('cp assets/icon_256.png assets/BuymaLister.iconset/icon_128x128@2x.png')
os.system('cp assets/icon_256.png assets/BuymaLister.iconset/icon_256x256.png')
os.system('cp assets/icon_512.png assets/BuymaLister.iconset/icon_256x256@2x.png')
os.system('cp assets/icon_512.png assets/BuymaLister.iconset/icon_512x512.png')
os.system('cp assets/icon_512.png assets/BuymaLister.iconset/icon_512x512@2x.png')

# Create .icns file
os.system('iconutil -c icns assets/BuymaLister.iconset -o assets/icon.icns')

# Clean up
os.system('rm -rf assets/BuymaLister.iconset')
os.system('rm assets/icon*.png')
print('Default icon created successfully')
"
    fi
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist

# Build the macOS app
echo "🔨 Building macOS app with PyInstaller..."
pyinstaller index_macos.spec

# Check if build was successful
if [ -d "dist/BuymaLister.app" ]; then
    echo "✅ Build successful! 🎉"
    echo "📱 Your macOS app is located at: dist/BuymaLister.app"
    echo ""
    echo "🚀 To run the app:"
    echo "   open dist/BuymaLister.app"
    echo ""
    echo "📦 To distribute:"
    echo "   - Copy dist/BuymaLister.app to Applications folder"
    echo "   - Or create a DMG file for distribution"
    echo ""
    echo "🔍 App size:"
    du -sh dist/BuymaLister.app
    
    # Optional: Open the app
    read -p "Would you like to open the app now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🚀 Opening BuymaLister app..."
        open dist/BuymaLister.app
    fi
    
else
    echo "❌ Build failed! Check the error messages above."
    exit 1
fi

echo ""
echo "🎯 Build process completed!"
echo "📁 Check the 'dist' folder for your macOS app bundle" 