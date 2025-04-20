import json
import torch
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Dict
import os

class UrduRAG:
    def __init__(self, data_path: str):
        # Initialize lightweight multilingual model for embeddings
        self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        
        # Load and process data
        self.data = self._load_data(data_path)
        self.index = self._create_index()
        
    def _load_data(self, data_path: str) -> List[Dict]:
        """Load and preprocess the JSON data."""
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _create_index(self) -> faiss.Index:
        """Create FAISS index from the data."""
        # Extract text from data
        texts = [item['text'] for item in self.data]
        
        # Create embeddings
        embeddings = self.embedding_model.encode(texts)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings).astype('float32'))
        
        return index
    
    def query(self, question: str, k: int = 3) -> str:
        """Query the RAG system and return response in Urdu."""
        # Get question embedding
        question_embedding = self.embedding_model.encode([question])
        
        # Search for relevant documents
        distances, indices = self.index.search(
            np.array(question_embedding).astype('float32'), k
        )
        
        # Get relevant contexts
        contexts = [self.data[idx] for idx in indices[0]]
        
        # Return the most relevant context
        return contexts[0]['text']

# Example usage
if __name__ == "__main__":
    # Initialize the RAG system
    rag = UrduRAG("data/urdu_data.json")
    
    # Example query
    question = "What is the capital of Pakistan?"
    response = rag.query(question)
    print(f"Question: {question}")
    print(f"Response: {response}") 