#!/bin/bash

# macOS Setup Script for BuymaLister
# This script prepares your macOS environment for building the desktop app

set -e  # Exit on any error

echo "🚀 Setting up macOS environment for BuymaLister..."
echo "=" * 50

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Error: This script must be run on macOS"
    exit 1
fi

# Check macOS version
MACOS_VERSION=$(sw_vers -productVersion)
echo "📱 macOS Version: $MACOS_VERSION"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "🐍 Installing Python 3..."
    if command -v brew &> /dev/null; then
        brew install python3
    else
        echo "📥 Installing Homebrew first..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        echo "🐍 Installing Python 3..."
        brew install python3
    fi
else
    echo "✅ Python 3 already installed: $(python3 --version)"
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "📦 Installing pip3..."
    python3 -m ensurepip --upgrade
else
    echo "✅ pip3 already installed: $(pip3 --version)"
fi

# Upgrade pip
echo "⬆️ Upgrading pip..."
python3 -m pip install --upgrade pip

# Install Homebrew if not present
if ! command -v brew &> /dev/null; then
    echo "🍺 Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for current session
    eval "$(/opt/homebrew/bin/brew shellenv)"
    
    echo "✅ Homebrew installed successfully"
else
    echo "✅ Homebrew already installed: $(brew --version)"
fi

# Install additional tools
echo "🔧 Installing additional tools..."
brew install create-dmg || echo "⚠️ create-dmg installation failed (will install later if needed)"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements_macos.txt

# Make scripts executable
echo "🔐 Making scripts executable..."
chmod +x build_macos.sh create_dmg.sh create_icon.py

# Create assets directory
echo "📁 Creating assets directory..."
mkdir -p assets

# Check if icon exists
if [ ! -f "assets/icon.icns" ]; then
    echo "🎨 Creating app icon..."
    python3 create_icon.py
else
    echo "✅ App icon already exists"
fi

echo ""
echo "🎯 Setup completed successfully! 🎉"
echo ""
echo "🚀 Next steps:"
echo "   1. Build the app: ./build_macos.sh"
echo "   2. Install: Drag dist/BuymaLister.app to Applications"
echo "   3. Create DMG (optional): ./create_dmg.sh"
echo ""
echo "📚 For more information, see README_macOS.md"
echo ""
echo "Happy building! 🎨" 