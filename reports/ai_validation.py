import random
from PIL import Image
import os

def validate_image(image_path, incident_type):
    """
    Simulates AI validation of an image.
    In a real implementation, this would use a machine learning model.
    """
    try:
        # Simulate image processing
        with Image.open(image_path) as img:
            width, height = img.size
            
            # Simulate different confidence levels based on image properties and incident type
            if incident_type == 'cutting':
                # Favor images with more horizontal lines (simulating cut trees)
                confidence = min(0.3 + (width/height * 0.1) + random.uniform(0.1, 0.4), 0.95)
            elif incident_type == 'dumping':
                # Favor images with more varied colors (simulating trash)
                confidence = min(0.4 + random.uniform(0.1, 0.5), 0.95)
            else:
                confidence = random.uniform(0.3, 0.8)
                
        return round(confidence, 2)
    except Exception as e:
        print(f"Error processing image: {e}")
        return round(random.uniform(0.3, 0.6), 2)