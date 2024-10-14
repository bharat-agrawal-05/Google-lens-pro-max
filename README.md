
# Google Lens Pro Max 

## How to run the repository for inference : 

### Clone the repository:

```bash
git clone https://github.com/yourusername/google-lens-pro-max.git
cd Google-lens-pro-max
```

### Install dependancies

```bash
pip install -r requirements.txt
npm install
```

### Go to WebPage Folder 

```bash
cd Webpage
```

### Start the backend server 

```bash
cd backend
node index.js
```

### Start the frontend server 

```bash
cd frontend
npm run dev
```

## Folder Structure 
```bash
WebPage/
│
├── backend/
│   ├── app.py
│   └── index.js
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   └── index.jsx
│
├── requirements.txt
└── README.md
```


## Tech Stack

### Backend:
- Python
- BLIP (Bootstrapping Language-Image Pre-training) model
- DuckDuckGo API for web search

### Frontend:
- React.js
- Tailwind
- HTML

## Problem Solution Explanation

Our project addresses the challenge of developing an intelligent pipeline that processes an image and a user-defined prompt to return relevant web search results. Here's a detailed explanation of how our solution works:

### Image Input and Prompt:
The system takes two inputs:
- An image file path (`image_path`)
- A user-defined prompt (`prompt`)

### Image Caption Generation:
We use the **BLIP (Bootstrapping Language-Image Pre-training)** model for image captioning.  
The `generate_caption()` function:
- Loads the image using **PIL (Python Imaging Library)**
- Preprocesses the image using the BLIP processor
- Generates a caption using the BLIP model
- Decodes the output to get a human-readable caption

### Combining Caption with User Prompt:
The generated caption is combined with the user's prompt to create a comprehensive search query.  
Format:  
`I have an image with content: {caption} and I want to search for {prompt}`  
This combined query is saved to a `caption.txt` file for reference.

### Web Search:
The `search()` function uses the **DuckDuckGo Search API** (via the `duckduckgo_search` library) to perform a web search.  
It uses the combined caption and prompt as the search query.  
The search is configured to:
- Use the 'wt-wt' region (Worldwide)
- Turn off safe search
- Retrieve a maximum of 20 results

### Results Processing:
- Search results are converted into a **pandas DataFrame**.
- The DataFrame is then saved as a CSV file named `output.csv`.

### This pipeline effectively solves the problem by:
- Using AI (**BLIP model**) to understand and describe the content of the input image.
- Combining this AI-generated description with the user's specific requirements (**prompt**).
- Leveraging a powerful web search engine (**DuckDuckGo**) to find relevant results based on this comprehensive query.
- Providing results in a structured format (**CSV**) for easy analysis and further processing.

The solution enhances search efficiency by bridging the gap between visual inputs and textual queries, allowing for more context-aware and specific search results that align closely with the user's needs.




