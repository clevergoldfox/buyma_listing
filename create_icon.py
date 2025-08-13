#!/usr/bin/env python3
"""
Icon Creation Script for BuymaLister macOS App
This script creates a proper .icns file for the macOS app bundle
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
import subprocess

def create_icon():
    """Create the app icon for macOS"""
    
    # Ensure assets directory exists
    os.makedirs('assets', exist_ok=True)
    
    # Check if we already have an icon
    if os.path.exists('assets/icon.icns'):
        print("✅ App icon already exists at assets/icon.icns")
        return
    
    print("🎨 Creating app icon for BuymaLister...")
    
    # Try to use background.png if it exists
    if os.path.exists('background.png'):
        print("🖼️ Using background.png as base for icon...")
        create_icon_from_image('background.png')
    else:
        print("🎨 Creating default icon...")
        create_default_icon()
    
    print("✅ App icon created successfully!")

def create_icon_from_image(image_path):
    """Create icon from existing image"""
    try:
        # Open the base image
        base_img = Image.open(image_path)
        
        # Create different sizes
        sizes = [16, 32, 64, 128, 256, 512]
        iconset_dir = 'assets/BuymaLister.iconset'
        os.makedirs(iconset_dir, exist_ok=True)
        
        for size in sizes:
            # Resize image maintaining aspect ratio
            resized = base_img.resize((size, size), Image.Resampling.LANCZOS)
            
            # Save with proper naming for iconset
            if size == 16:
                resized.save(f'{iconset_dir}/icon_16x16.png')
            elif size == 32:
                resized.save(f'{iconset_dir}/icon_16x16@2x.png')
            elif size == 64:
                resized.save(f'{iconset_dir}/icon_32x32.png')
            elif size == 128:
                resized.save(f'{iconset_dir}/icon_32x32@2x.png')
            elif size == 256:
                resized.save(f'{iconset_dir}/icon_128x128.png')
            elif size == 512:
                resized.save(f'{iconset_dir}/icon_128x128@2x.png')
        
        # Create .icns file using iconutil
        create_icns_from_iconset(iconset_dir)
        
        # Clean up
        import shutil
        shutil.rmtree(iconset_dir)
        
    except Exception as e:
        print(f"❌ Error creating icon from image: {e}")
        print("🔄 Falling back to default icon...")
        create_default_icon()

def create_default_icon():
    """Create a default icon with text"""
    try:
        # Create a simple icon
        size = 512
        img = Image.new('RGB', (size, size), color='#007AFF')  # macOS blue
        draw = ImageDraw.Draw(img)
        
        # Draw a rounded rectangle background
        margin = size // 8
        draw.rounded_rectangle(
            [margin, margin, size - margin, size - margin],
            radius=size // 8,
            fill='white'
        )
        
        # Try to use a system font, fallback to default
        try:
            # Try to use SF Pro (macOS system font)
            font_size = size // 4
            font = ImageFont.truetype("/System/Library/Fonts/SF-Pro-Display-Bold.otf", font_size)
        except:
            try:
                # Try Arial
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
            except:
                # Use default font
                font = ImageFont.load_default()
                font_size = size // 6
        
        # Draw text
        text = "BL"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        
        draw.text((x, y), text, fill='#007AFF', font=font)
        
        # Save as PNG first
        img.save('assets/icon.png')
        
        # Create iconset directory
        iconset_dir = 'assets/BuymaLister.iconset'
        os.makedirs(iconset_dir, exist_ok=True)
        
        # Create different sizes
        sizes = [16, 32, 64, 128, 256, 512]
        for size in sizes:
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            
            if size == 16:
                resized.save(f'{iconset_dir}/icon_16x16.png')
            elif size == 32:
                resized.save(f'{iconset_dir}/icon_16x16@2x.png')
            elif size == 64:
                resized.save(f'{iconset_dir}/icon_32x32.png')
            elif size == 128:
                resized.save(f'{iconset_dir}/icon_32x32@2x.png')
            elif size == 256:
                resized.save(f'{iconset_dir}/icon_128x128.png')
            elif size == 512:
                resized.save(f'{iconset_dir}/icon_128x128@2x.png')
        
        # Create .icns file
        create_icns_from_iconset(iconset_dir)
        
        # Clean up
        import shutil
        shutil.rmtree(iconset_dir)
        os.remove('assets/icon.png')
        
    except Exception as e:
        print(f"❌ Error creating default icon: {e}")
        sys.exit(1)

def create_icns_from_iconset(iconset_dir):
    """Create .icns file from iconset directory using iconutil"""
    try:
        # Use iconutil to create .icns file
        result = subprocess.run([
            'iconutil', '-c', 'icns', iconset_dir, '-o', 'assets/icon.icns'
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Error running iconutil: {result.stderr}")
            raise Exception("iconutil failed")
            
    except FileNotFoundError:
        print("❌ Error: iconutil not found. This script must be run on macOS.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error creating .icns file: {e}")
        sys.exit(1)

def main():
    """Main function"""
    print("🚀 BuymaLister Icon Creator")
    print("=" * 40)
    
    # Check if we're on macOS
    if sys.platform != 'darwin':
        print("❌ This script must be run on macOS")
        print("   iconutil is a macOS-specific tool")
        sys.exit(1)
    
    create_icon()
    
    print("\n🎯 Icon creation completed!")
    print("📁 Check assets/icon.icns")

if __name__ == "__main__":
    main() 