from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import torch
import re

class RAGHandler:
    def __init__(self):
        print("Initializing RAG Handler...")
        
        # Initialize the embedding model
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        print("Embedding model loaded")
        
        # Initialize FAISS index
        self.dimension = 384  # Dimension of embeddings from all-MiniLM-L6-v2
        self.index = faiss.IndexFlatL2(self.dimension)
        self.texts = []  # Store the original text chunks
        
    def _chunk_text(self, text: str, chunk_size: int = 200) -> List[str]:
        """Split text into chunks of approximately equal size."""
        # Split by sentences (assuming sentences end with ۔)
        sentences = text.split('۔')
        chunks = []
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            sentence = sentence.strip() + '۔'
            sentence_length = len(sentence.split())
            
            if current_size + sentence_length > chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_size = sentence_length
            else:
                current_chunk.append(sentence)
                current_size += sentence_length
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
            
        return chunks
        
    def _create_embeddings(self, texts: List[str]) -> np.ndarray:
        """Create embeddings for the given texts."""
        embeddings = self.embedding_model.encode(texts, convert_to_numpy=True)
        return embeddings
        
    def _search_relevant_chunks(self, query: str, k: int = 5) -> List[str]:
        """Search for the most relevant text chunks for the given query."""
        query_embedding = self.embedding_model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_embedding, k)
        
        relevant_chunks = [self.texts[i] for i in indices[0]]
        return relevant_chunks
        
    def _extract_relevant_sentences(self, context: str, question: str) -> List[str]:
        """Extract sentences that are most relevant to the question."""
        # Split context into sentences
        sentences = context.split('۔')
        
        # Create embeddings for each sentence
        sentence_embeddings = self.embedding_model.encode(sentences, convert_to_numpy=True)
        
        # Create embedding for the question
        question_embedding = self.embedding_model.encode([question], convert_to_numpy=True)
        
        # Calculate similarity scores
        similarities = np.dot(sentence_embeddings, question_embedding.T).flatten()
        
        # Get top 3 most similar sentences
        top_indices = np.argsort(similarities)[-3:][::-1]
        
        # Return the sentences in order of relevance
        return [sentences[i].strip() + '۔' for i in top_indices]
        
    def _generate_response(self, context: str, question: str) -> str:
        """Generate a response based on the context and question."""
        # Extract the most relevant sentences from the context
        relevant_sentences = self._extract_relevant_sentences(context, question)
        
        # If we have relevant sentences, use them to form a response
        if relevant_sentences:
            # Simply return the most relevant sentence
            return relevant_sentences[0]
        
        # If no relevant sentences found, return a generic response
        return "معذرت، میں آپ کے سوال کا جواب نہیں دے سکا۔ براہ کرم دوبارہ کوشش کریں۔"
        
    def process_story(self, story_content: str):
        """Process a story and store its chunks in the index."""
        # Clear previous data
        self.index = faiss.IndexFlatL2(self.dimension)
        self.texts = []
        
        # Create chunks
        chunks = self._chunk_text(story_content)
        self.texts = chunks
        
        # Create and store embeddings
        embeddings = self._create_embeddings(chunks)
        self.index.add(embeddings)
        
    def get_answer(self, story_content: str, question: str) -> str:
        """Get an answer for the given question about the story."""
        try:
            # Process the story if not already processed
            self.process_story(story_content)
            
            # Get relevant chunks
            relevant_chunks = self._search_relevant_chunks(question)
            context = " ".join(relevant_chunks)
            
            # Generate response
            response = self._generate_response(context, question)
            return response
            
        except Exception as e:
            print(f"Error in get_answer: {e}")
            return "معذرت، میں آپ کے سوال کا جواب نہیں دے سکا۔ براہ کرم دوبارہ کوشش کریں۔" 