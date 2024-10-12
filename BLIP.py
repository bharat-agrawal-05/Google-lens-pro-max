from PIL import Image
import requests
from transformers import BlipProcessor, BlipForConditionalGeneration

def generate(image_url):
    model_name = "Salesforce/blip-image-captioning-base"
    processor = BlipProcessor.from_pretrained(model_name)
    model = BlipForConditionalGeneration.from_pretrained(model_name)

    # Load the image
    image = Image.open(image_url)

    # Preprocess the image
    inputs = processor(images=image, return_tensors="pt")

    # Generate captions
    outputs = model.generate(**inputs)
    caption = processor.decode(outputs[0], skip_special_tokens=True)

    return caption
