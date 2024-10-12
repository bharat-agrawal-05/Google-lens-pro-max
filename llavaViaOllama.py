import ollama

def chat(images):
    res = ollama.chat(
        model="llava",
        messages=[
            {
                "role": "user",
                "content": "what is in this image?",
                "images": images
            }
        ],
    )
    return res['message']['content']

print(chat(['pizza.jpg']))