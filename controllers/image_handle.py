import cv2
from PIL import Image
import numpy as np
import io
import requests
import os
import sys
from rembg import remove
REMBG_AVAILABLE = True

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Use OpenCV's built-in haarcascades path
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)

if face_cascade.empty():
    raise IOError('Cannot load cascade classifier xml file at ' + cascade_path)

def simple_background_removal(image):
    """Simple background removal using color-based segmentation"""
    # Convert to RGBA
    image_rgba = image.convert("RGBA")
    data = np.array(image_rgba)
    
    # Create a mask based on white/light background
    # This is a simple approach - you might need to adjust thresholds
    r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]
    
    # Create mask for white/light pixels
    mask = (r > 240) & (g > 240) & (b > 240)
    
    # Set alpha channel based on mask
    data[:, :, 3] = np.where(mask, 0, 255)
    
    return Image.fromarray(data, "RGBA")

def image_handle(input_image_path, background_image_path, output_image_path):
    # Step 1: Face Removal - Crop from top to face
    if input_image_path.startswith('http://') or input_image_path.startswith('https://'):
        response = requests.get(input_image_path)
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    else:
        image = cv2.imread(input_image_path)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 0:
        # Take the first detected face (you can adjust this logic for multiple faces)
        (x, y, w, h) = faces[0]
        # Crop the image from the bottom of the face down
        cropped_image = image[y + h:]
        # Convert the cropped image to PIL Image for easier background blending
        cropped_pil_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
    else:
        # No face detected: use the whole image as PIL Image
        cropped_pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        #print("No face detected in the image.")
    
    # Step 2: Background Removal
    if REMBG_AVAILABLE:
        try:
            buffer = io.BytesIO()
            cropped_pil_image.save(buffer, format="PNG")
            cropped_image_bytes = buffer.getvalue()
            output_data = remove(cropped_image_bytes)
            background_removed_image = Image.open(io.BytesIO(output_data))
        except Exception as e:
            #print(f"Background removal failed: {e}. Using simple method.")
            background_removed_image = simple_background_removal(cropped_pil_image)
    else:
        #print("Using simple background removal method.")
        background_removed_image = simple_background_removal(cropped_pil_image)

    # Step 3: Background Addition
    if background_image_path:
        # Load the new background image
        background = Image.open(background_image_path)

        # Resize the background to match the size of the cropped image
        background_resized = background.resize(background_removed_image.size)

        # Composite the cropped image (with background removed) on top of the resized background
        background_resized.paste(background_removed_image, (0, 0), background_removed_image)
        final_image = background_resized
    else:
        # Create a white background
        white_bg = Image.new("RGB", background_removed_image.size, (255, 255, 255))
        white_bg.paste(background_removed_image, (0, 0), background_removed_image)
        final_image = white_bg

    final_image = final_image.convert("RGB")
    final_image.save(output_image_path, format="JPEG", quality=98, subsampling=0)
    #print(f"Image saved as {output_image_path}")
    return output_image_path

# Example usage
# remove_face_and_background_and_add_new_background('https://assets.hermes.com/is/image/hermesproduct/5H1151D702_worn_1?size=3000,3000&extend=0,0,0,0&align=0,0&$product_item_grid_g$&wid=400&hei=400', 'background_image.png', 'output_image.png')
# remove_face_and_background_and_add_new_background('input_image.png', 'background_image.png', 'output_image.png')
