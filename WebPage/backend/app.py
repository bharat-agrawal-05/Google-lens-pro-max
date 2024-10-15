from PIL import Image
import os
import sys
from transformers import BlipProcessor, BlipForConditionalGeneration
import pandas as pd
from duckduckgo_search import DDGS


# Load the BLIP model and processor
model_name = "Salesforce/blip-image-captioning-large"
processor = BlipProcessor.from_pretrained(model_name)
model = BlipForConditionalGeneration.from_pretrained(model_name)

def generate_caption(image_path):
    # Load and preprocess the image
    image = Image.open(image_path)
    inputs = processor(images=image, return_tensors="pt")
    
    # Generate captions
    outputs = model.generate(**inputs)
    caption = processor.decode(outputs[0], skip_special_tokens=True)
    
    return caption

def search(keywords):
    search_query = keywords

    # Fetch search results from DuckDuckGo
    results = DDGS().text(
        keywords=search_query,
        region='wt-wt',
        safesearch='off',
        max_results=20
    )

    # Convert results to DataFrame and save to CSV
    results_df = pd.DataFrame(results)
    results_df.to_csv('output.csv', index=True)

    return results

image_path = sys.argv[1]
prompt = sys.argv[2]

# Generate caption
caption = generate_caption(image_path)
caption = f"I have a image with content:{caption} and I want to search for {prompt}"
with open('caption.txt', 'w') as f:
    f.write(caption)
search(caption)

