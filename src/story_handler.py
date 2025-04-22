import os
import json
from typing import Dict, List, Any, Optional
import re
from llm_utils import llm_handler
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import torch

class StoryHandler:
    def __init__(self, data_dir: str = "data/stories"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # Cache for story data to avoid frequent disk reads
        self.story_cache = {}
        
        # Initialize the LLM handler
        self.llm_handler = llm_handler
        
        # Initialize RAG components
        print("Initializing RAG system...")
        self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.story_embeddings = None
        self.story_texts = []
        self.faiss_index = None
        
        # Load and index all stories for RAG
        self._initialize_rag()
        
    def _initialize_rag(self):
        """Initialize the RAG system by loading and indexing all stories."""
        print("Loading stories for RAG indexing...")
        stories = self.get_all_stories()
        
        # Collect all story contents
        for story in stories:
            story_content = self.get_story_content(story['id'])
            if story_content and 'content' in story_content:
                # Split content into smaller chunks for better retrieval
                chunks = self._split_into_chunks(story_content['content'])
                for chunk in chunks:
                    self.story_texts.append({
                        'text': chunk,
                        'story_id': story['id'],
                        'title': story_content.get('title', 'Untitled')
                    })
        
        if not self.story_texts:
            print("No stories found for indexing!")
            return
            
        print(f"Creating embeddings for {len(self.story_texts)} story chunks...")
        texts = [item['text'] for item in self.story_texts]
        self.story_embeddings = self.embedding_model.encode(texts)
        
        # Create FAISS index
        dimension = self.story_embeddings.shape[1]
        self.faiss_index = faiss.IndexFlatL2(dimension)
        self.faiss_index.add(np.array(self.story_embeddings).astype('float32'))
        print("RAG system initialized successfully!")
        
    def _split_into_chunks(self, text: str, chunk_size: int = 200) -> List[str]:
        """Split text into smaller chunks for better retrieval."""
        # Split by sentences (assuming sentences end with ۔)
        sentences = text.split('۔')
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence = sentence.strip() + '۔'
            sentence_length = len(sentence.split())
            
            if current_length + sentence_length > chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_length = sentence_length
            else:
                current_chunk.append(sentence)
                current_length += sentence_length
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
            
        return chunks
    
    def get_all_stories(self) -> List[Dict[str, Any]]:
        """
        Get metadata for all available stories
        
        Returns:
            List of story metadata objects
        """
        stories = []
        
        # First look for stories directly in the data directory
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.json') and os.path.isfile(os.path.join(self.data_dir, filename)):
                file_path = os.path.join(self.data_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        story_data = json.load(f)
                        
                    # Add metadata for the story list
                    stories.append({
                        "id": f"root/{filename[:-5]}",  # Remove .json extension
                        "title": story_data.get("title", "Untitled"),
                        "age_group": story_data.get("ageGroup", story_data.get("age_group", "")),
                        "language": story_data.get("language", "urdu"),
                        "type": story_data.get("type", "story").lower()  # Default to story if not specified
                    })
                except Exception as e:
                    print(f"Error loading story {file_path}: {e}")
        
        # Walk through all subdirectories
        for subdir in os.listdir(self.data_dir):
            subdir_path = os.path.join(self.data_dir, subdir)
            if not os.path.isdir(subdir_path):
                continue
                
            # Look for story files in this subdirectory
            for filename in os.listdir(subdir_path):
                if filename.endswith('.json'):
                    file_path = os.path.join(subdir_path, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            story_data = json.load(f)
                            
                        # Add metadata for the story list
                        stories.append({
                            "id": f"{subdir}/{filename[:-5]}",  # Remove .json extension
                            "title": story_data.get("title", "Untitled"),
                            "age_group": story_data.get("ageGroup", story_data.get("age_group", "")),
                            "language": story_data.get("language", "urdu"),
                            "type": story_data.get("type", "story").lower()  # Default to story if not specified
                        })
                    except Exception as e:
                        print(f"Error loading story {file_path}: {e}")
        
        return stories
    
    def get_stories_by_age(self, age_group: str) -> List[Dict[str, Any]]:
        """
        Get stories filtered by age group
        
        Args:
            age_group: Age group to filter by
            
        Returns:
            List of story metadata objects
        """
        return [s for s in self.get_all_stories() if s["age_group"] == age_group]
    
    def get_story_content(self, story_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the full content of a story by its ID
        
        Args:
            story_id: Story ID in format 'root/story_name' or just 'story_name'
            
        Returns:
            Story data or None if not found
        """
        # Check if in cache first
        if story_id in self.story_cache:
            return self.story_cache[story_id]
            
        # Parse story ID to get file path
        parts = story_id.split('/')
        if len(parts) == 2:
            # Format: root/story_name or subdirectory/story_name
            location, story_name = parts
        else:
            # Format: story_name
            story_name = story_id
            
        # Convert underscores to hyphens in the story name
        story_name = story_name.replace('_', '-')
        
        # Try loading from root directory first
        file_path = os.path.join(self.data_dir, f"{story_name}.json")
        
        if not os.path.exists(file_path) and len(parts) == 2:
            # If not found in root and we have a location, try the subdirectory
            file_path = os.path.join(self.data_dir, parts[0], f"{story_name}.json")
        
        # If still not found, try with different spellings or formats
        if not os.path.exists(file_path):
            # Try with different spellings (e.g., jheel vs hheel)
            alt_name = story_name.replace('jheel', 'hheel').replace('hheel', 'jheel')
            alt_path = os.path.join(self.data_dir, f"{alt_name}.json")
            
            if os.path.exists(alt_path):
                file_path = alt_path
            else:
                # Try with different formats (e.g., with or without hyphens)
                alt_name = story_name.replace('-', '_')
                alt_path = os.path.join(self.data_dir, f"{alt_name}.json")
                
                if os.path.exists(alt_path):
                    file_path = alt_path
        
        if not os.path.exists(file_path):
            print(f"Story not found: {file_path}")
            return None
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                story_data = json.load(f)
                
            # Cache the story data
            self.story_cache[story_id] = story_data
            return story_data
        except Exception as e:
            print(f"Error loading story {file_path}: {e}")
            return None
    
    def answer_question(self, story_id: str, question: str) -> dict:
        """Answer a question about a specific story using RAG."""
        try:
            if not self.faiss_index:
                return {
                    'error': 'RAG system not initialized',
                    'success': False,
                    'found': False
                }
            
            # Get question embedding
            question_embedding = self.embedding_model.encode([question])
            
            # Search for relevant chunks
            k = 3  # Number of chunks to retrieve
            distances, indices = self.faiss_index.search(
                np.array(question_embedding).astype('float32'), k
            )
            
            # Get relevant chunks from the same story
            relevant_chunks = []
            for idx in indices[0]:
                chunk_data = self.story_texts[idx]
                if chunk_data['story_id'] == story_id:
                    relevant_chunks.append(chunk_data['text'])
            
            if not relevant_chunks:
                # If no chunks from the specific story found, return error
                return {
                    'error': 'No relevant content found in the story',
                    'success': False,
                    'found': True
                }
            
            # Combine relevant chunks as context
            context = ' '.join(relevant_chunks)
            
            # Use the LLM handler to answer the question with the retrieved context
            llm_response = self.llm_handler.chat_about_story(context, question)
            
            if not llm_response.get('success'):
                return {
                    'error': 'Failed to generate response',
                    'success': False,
                    'found': True
                }
            
            return {
                'success': True,
                'found': True,
                'response': llm_response.get('response', ''),
                'story_title': self.story_texts[indices[0][0]]['title']
            }
            
        except Exception as e:
            print(f"Error in answer_question: {e}")
            return {
                'error': str(e),
                'success': False,
                'found': False,
                'response': 'معذرت، میں اس وقت سوالات کا جواب نہیں دے سکتا۔'
            }

# Initialize the story handler
story_handler = StoryHandler() 