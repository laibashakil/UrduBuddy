import json
import torch
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Dict
import os

class UrduRAG:
    def __init__(self, stories_path: str, poems_path: str):
        # Initialize lightweight multilingual model for embeddings
        self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        
        # Load and process data
        self.data = self._load_data(stories_path, poems_path)
        self.index = self._create_index()
        
    def _load_data(self, stories_path: str, poems_path: str) -> List[Dict]:
        """Load and preprocess both stories and poems data."""
        data = []
        
        # Load stories
        if os.path.exists(stories_path):
            with open(stories_path, 'r', encoding='utf-8') as f:
                stories = json.load(f)
                for story in stories:
                    story['type'] = 'story'
                    data.append(story)
        
        # Load poems
        if os.path.exists(poems_path):
            for poem_file in os.listdir(poems_path):
                if poem_file.endswith('.json'):
                    with open(os.path.join(poems_path, poem_file), 'r', encoding='utf-8') as f:
                        poem = json.load(f)
                        poem['type'] = 'poem'
                        # Add poem content to text field for consistency
                        poem['text'] = poem['content']
                        data.append(poem)
        
        return data
    
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
    
    def query(self, question: str, k: int = 3) -> Dict:
        """Query the RAG system and return structured response."""
        # Get question embedding
        question_embedding = self.embedding_model.encode([question])
        
        # Search for relevant documents
        distances, indices = self.index.search(
            np.array(question_embedding).astype('float32'), k
        )
        
        # Get relevant contexts
        contexts = [self.data[idx] for idx in indices[0]]
        
        # Format response
        response = {
            'answer': contexts[0]['text'],
            'confidence': float(1 / (1 + distances[0][0])),  # Convert distance to confidence score
            'sources': [
                {
                    'text': ctx['text'],
                    'relevance': float(1 / (1 + dist)),
                    'type': ctx['type'],
                    'title': ctx.get('title', '')
                }
                for ctx, dist in zip(contexts, distances[0])
            ]
        }
        
        return response

# Example usage
if __name__ == "__main__":
    # Initialize the RAG system
    rag = UrduRAG("data/stories/urdu_stories.json", "data/poems")
    
    # Example query
    question = "What is the capital of Pakistan?"
    response = rag.query(question)
    print(f"Question: {question}")
    print(f"Response: {response}") 