

import json
import sys
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def load_corpus(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, 'r') as f:
        return json.load(f)

def preprocess_corpus(corpus: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    processed_corpus = []
    for doc in corpus:
        processed_doc = {
            'title': doc['title'],
            'author': doc['author'],
            'url': doc['url'],
            'source': doc['source'],
            'category': doc['category'],
            'published_at': doc['published_at'],
            'content': doc['title'] + ' ' + doc['body']
        }
        processed_corpus.append(processed_doc)
    return processed_corpus

def create_embeddings(corpus: List[Dict[str, Any]], model_name: str = 'sentence-transformers/all-MiniLM-L6-v2') -> np.ndarray:
    model = SentenceTransformer(model_name)
    return model.encode([doc['content'] for doc in corpus])

def retrieve_documents(query: str, corpus: List[Dict[str, Any]], embeddings: np.ndarray, model_name: str = 'sentence-transformers/all-MiniLM-L6-v2', top_k: int = 4) -> List[Dict[str, Any]]:
    model = SentenceTransformer(model_name)
    query_embedding = model.encode([query])
    similarities = cosine_similarity(query_embedding, embeddings)[0]
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    return [corpus[i] for i in top_indices]

def generate_answer(query: str, relevant_docs: List[Dict[str, Any]], model_name: str = 'google/flan-t5-base') -> str:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    context = " ".join([doc['content'] for doc in relevant_docs])
    input_text = f"Query: {query}\nContext: {context}\nAnswer:"
    
    inputs = tokenizer(input_text, return_tensors="pt", max_length=1024, truncation=True)
    outputs = model.generate(**inputs, max_length=150, num_return_sequences=1, temperature=0.7)
    
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Main RAG pipeline
def rag_pipeline(query: str, corpus: List[Dict[str, Any]], embeddings: np.ndarray) -> Dict[str, Any]:
    relevant_docs = retrieve_documents(query, corpus, embeddings)
    answer = generate_answer(query, relevant_docs)
    
    evidence_list = []
    for doc in relevant_docs:
        evidence = {
            'title': doc['title'],
            'author': doc['author'],
            'url': doc['url'],
            'source': doc['source'],
            'category': doc['category'],
            'published_at': doc['published_at'],
            'fact': doc['content'][:200] + '...'
        }
        evidence_list.append(evidence)
    
    return {
        'query': query,
        'answer': answer,
        'question_type': 'inference_query',
        'evidence_list': evidence_list
    }

# Example usage
def query(query: str):
    corpus = load_corpus('corpus.json')
    processed_corpus = preprocess_corpus(corpus)
    embeddings = create_embeddings(processed_corpus)
    result = rag_pipeline(query, processed_corpus, embeddings)
    print(json.dumps(result, indent=2))

q = "What is the impact of COVID-19 on the economy?"
query(q)