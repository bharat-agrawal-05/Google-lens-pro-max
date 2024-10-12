from flask import Flask, request, render_template
from PIL import Image
import os
from transformers import BlipProcessor, BlipForConditionalGeneration
import pandas as pd
from duckduckgo_search import DDGS

app = Flask(__name__)

# Load the BLIP model and processor
model_name = "Salesforce/blip-image-captioning-base"
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
    results_df.to_csv(f'{''.join(search_query.split())}.csv', index=True)

    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        prompt = request.form['prompt']
        image_path = f"./static/{file.filename}"
        
        # Ensure the directory exists
        if not os.path.exists('./static'):
            os.makedirs('./static')
        
        file.save(image_path)
        
        # Generate caption
        caption = generate_caption(image_path)
        caption = f"I have a image with content:{caption} and I want to search for {prompt}"
        print(caption)
        # Search using the generated caption
        results = search(caption)
        
        return render_template('results.html', caption=caption, results=results)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
