#!/bin/bash

# DMG Creation Script for BuymaLister macOS App
# This script creates a DMG file for easy distribution

set -e  # Exit on any error

echo "📦 Creating DMG for BuymaLister..."

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Error: This script must be run on macOS"
    exit 1
fi

# Check if the app exists
if [ ! -d "dist/BuymaLister.app" ]; then
    echo "❌ Error: BuymaLister.app not found in dist/ directory"
    echo "Please run the build script first: ./build_macos.sh"
    exit 1
fi

# Check if create-dmg is installed
if ! command -v create-dmg &> /dev/null; then
    echo "📥 Installing create-dmg..."
    if command -v brew &> /dev/null; then
        brew install create-dmg
    else
        echo "❌ Error: Homebrew not found. Please install Homebrew first:"
        echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        echo "   Then run: brew install create-dmg"
        exit 1
    fi
fi

# Clean up previous DMG
if [ -f "BuymaLister.dmg" ]; then
    echo "🧹 Removing previous DMG..."
    rm "BuymaLister.dmg"
fi

# Create DMG
echo "🔨 Creating DMG file..."
create-dmg \
    --volname "BuymaLister" \
    --volicon "assets/icon.icns" \
    --window-pos 200 120 \
    --window-size 600 400 \
    --icon-size 100 \
    --icon "BuymaLister.app" 175 120 \
    --hide-extension "BuymaLister.app" \
    --app-drop-link 425 120 \
    "BuymaLister.dmg" \
    "dist/"

# Check if DMG was created successfully
if [ -f "BuymaLister.dmg" ]; then
    echo "✅ DMG created successfully! 🎉"
    echo "📁 Your DMG file: BuymaLister.dmg"
    echo "📏 DMG size:"
    du -sh "BuymaLister.dmg"
    echo ""
    echo "🚀 To install:"
    echo "   1. Double-click BuymaLister.dmg"
    echo "   2. Drag BuymaLister.app to Applications folder"
    echo "   3. Eject the DMG"
    echo ""
    echo "📤 Ready for distribution!"
else
    echo "❌ DMG creation failed!"
    exit 1
fi 