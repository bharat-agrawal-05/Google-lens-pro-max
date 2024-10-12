from PIL import Image
import requests
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load the BLIP model and processor
model_name = "Salesforce/blip-image-captioning-base"
processor = BlipProcessor.from_pretrained(model_name)
model = BlipForConditionalGeneration.from_pretrained(model_name)

# Load the image
image_url = "path_to_your_image.jpg"  # Replace with your image path or URL
image = Image.open("download.jpeg")

# Preprocess the image
inputs = processor(images=image, return_tensors="pt")

# Generate captions
outputs = model.generate(**inputs)
caption = processor.decode(outputs[0], skip_special_tokens=True)

print("Generated Caption:", caption)
