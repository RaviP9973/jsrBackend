import requests
import sys
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
import json 
from io import BytesIO
import base64
import os
from datetime import datetime
# Step 1: Set your Roboflow API details
API_KEY = "msvaHK2lfsfvfg0VAKWZ"  # Replace with your actual Roboflow API Key
PROJECT_ID = "project-r-5e4dz"           # Replace with your project ID
MODEL_VERSION = "1"                # Replace with your model version
API_URL = f"https://detect.roboflow.com/{PROJECT_ID}/{MODEL_VERSION}?api_key={API_KEY}"

#step2: Load the image path passed as an argument
if len(sys.argv) != 2:
    # print("Usage: python segementImage.py <image-path>")
    sys.exit(1)

# Step 3: Load your image
IMAGE_PATH = sys.argv[1]  # Replace with your image path

# Step 4: Upload the image and get predictions
# print(IMAGE_PATH)
with open(IMAGE_PATH, "rb") as img_file:
    response = requests.post(API_URL, files={"file": img_file})

# Step 5: Parse predictions, overlay them, and calculate pixel counts
if response.status_code == 200:
    predictions = response.json()
    # print("Predictions received.")

    # Open the original image
    original_image = Image.open(IMAGE_PATH).convert("RGBA")
    overlay = Image.new("RGBA", original_image.size, (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)

    # Create a blank mask (same size as the original image)
    mask = Image.new("L", original_image.size, 0)  # "L" mode for grayscale
    draw_mask = ImageDraw.Draw(mask)

    # Loop through each prediction
    for prediction in predictions["predictions"]:
        # Extract polygon points
        points = prediction.get("points", [])  # Handle missing 'points' key gracefully
        if points:
            polygon = [(point["x"], point["y"]) for point in points]

            # Draw the polygon on the overlay (transparent red)
            draw_overlay.polygon(polygon, fill=(255, 0, 0, 100))

            # Draw the polygon on the mask (white)
            draw_mask.polygon(polygon, fill=255)

    # Combine original image with overlay
    segmented_image = Image.alpha_composite(original_image, overlay)

    buffered = BytesIO()
    segmented_image.save(buffered, format="PNG")
    segmented_image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # Convert mask to a NumPy array
    mask_array = np.array(mask)

    # Count non-zero pixels in the mask
    pixel_count = np.count_nonzero(mask_array)

    # Display the segmented image
    # plt.figure(figsize=(10, 10))
    # plt.imshow(segmented_image)
    # plt.axis("off")
    # plt.show()

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    segmented_image_path = f"uploads/{timestamp}_segmented_image.png"

    segmented_image.save(segmented_image_path)

    # Print pixel count and raw predictions
    # print(f"Number of pixels in the segmentation mask: {pixel_count}")
    #print("Predictions content:", predictions["predictions"])

    result = {
        "pixel_count": pixel_count,
        "segmented_image_path": segmented_image_path,   
        "segmented_image_base64":segmented_image_base64
    }
    print(json.dumps(result))
    
else:
    print(f"Failed to get predictions: {response.status_code} - {response.text}")