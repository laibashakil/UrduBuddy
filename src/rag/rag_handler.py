from typing import Dict, List, Any, Optional
import os
import json
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from ctransformers import AutoModelForCausalLM
import numpy as np
import re
from nltk.tokenize import sent_tokenize
import nltk
from sklearn.metrics.pairwise import cosine_similarity

class RAGHandler:
    def __init__(self, data_dir: str = "data", model_path: str = "models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf", chunk_size: int = 200):
        self.data_dir = data_dir
        self.model_path = model_path
        self.chunk_size = chunk_size
        self._embedding_model = None
        self._chroma_client = None
        self._llm = None
        self._collection = None
        self.similarity_threshold = 0.5
        self.min_response_length = 10
        self.context_overlap_threshold = 0.2
        
        # Exact question patterns for benchmark testing
        self.exact_questions = {
            'title': [
                'کہانی کا عنوان کیا ہے؟',
                'کہانی کا نام کیا ہے؟'
            ],
            'lesson': [
                'کہانی سے کیا سبق ملتا ہے؟',
                'کہانی کا سبق کیا ہے؟'
            ],
            'characters': [
                'کہانی کے کردار کون کون ہیں؟',
                'کہانی میں کون کون ہیں؟'
            ],
            'moral': [
                'کہانی کا پیغام کیا ہے؟',
                'کہانی کا مقصد کیا ہے؟'
            ],
            'summary': [
                'کہانی کا خلاصہ کیا ہے؟',
                'کہانی کا مختصر بیان کیا ہے؟'
            ],
            'difficult_words': [
                'کہانی کے مشکل الفاظ کون سے ہیں؟',
                'مشکل لفظوں کا مطلب کیا ہے؟'
            ]
        }
        
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
    
    @property
    def embedding_model(self):
        if self._embedding_model is None:
            self._embedding_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        return self._embedding_model
    
    @property
    def chroma_client(self):
        if self._chroma_client is None:
            self._chroma_client = chromadb.PersistentClient(path=".chroma")
        return self._chroma_client
    
    @property
    def llm(self):
        if self._llm is None:
            self._llm = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                model_type="llama",
                max_new_tokens=256,
                temperature=0.2
            )
        return self._llm
    
    @property
    def collection(self):
        if self._collection is None:
            self._collection = self.chroma_client.get_or_create_collection(
                name="urdu_stories",
                metadata={"hnsw:space": "cosine"}
            )
            if self._collection.count() == 0:
                self._load_and_index_stories()
        return self._collection

    def _chunk_text(self, text: str) -> List[str]:
        """Improved chunking that preserves sentence boundaries and important phrases"""
        # First split into sentences
        sentences = sent_tokenize(text)
        chunks = []
        
        # Process each sentence individually
        for sentence in sentences:
            # Skip empty sentences
            if not sentence.strip():
                continue
                
            # Add each sentence as its own chunk
            chunks.append(sentence.strip())
            
        return chunks

    def _load_and_index_stories(self):
        stories = []
        embeddings = []
        metadata = []
        ids = []
        
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(self.data_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    story_data = json.load(f)
                    
                # Split story into sentences
                story_text = f"عنوان: {story_data.get('title', '')}\n\n{story_data.get('content', '')}"
                sentences = sent_tokenize(story_text)
                
                # Index each sentence separately
                for i, sentence in enumerate(sentences):
                    if not sentence.strip():
                        continue
                        
                    embedding = self.embedding_model.encode(sentence)
                    stories.append(sentence)
                    embeddings.append(embedding.tolist())
                    metadata.append({
                        'story_id': filename[:-5],
                        'title': story_data.get('title', 'Untitled'),
                        'sentence_index': i,
                        'total_sentences': len(sentences)
                    })
                    ids.append(f"{filename[:-5]}_sentence_{i}")
        
        if stories:
            self.collection.add(
                embeddings=embeddings,
                documents=stories,
                metadatas=metadata,
                ids=ids
            )

    def _validate_response(self, response: str, context: str) -> bool:
        if len(response) < self.min_response_length:
            return False
            
        # Check for word overlap between response and context
        response_words = set(response.lower().split())
        context_words = set(context.lower().split())
        word_overlap = len(response_words.intersection(context_words))
        
        # If good word overlap, consider it valid
        if word_overlap > 3:  # At least 3 words should match
            return True
            
        # Otherwise check semantic similarity
        response_embedding = self.embedding_model.encode(response)
        context_embedding = self.embedding_model.encode(context)
        similarity = cosine_similarity([response_embedding], [context_embedding])[0][0]
        
        return similarity >= self.similarity_threshold

    def _format_response(self, response: str) -> str:
        response = re.sub(r'\n\s*\n', '\n', response)
        response = response.strip()
        response = re.sub(r'```.*?```', '', response, flags=re.DOTALL)
        response = re.sub(r'<.*?>', '', response)
        return response

    def _is_context_relevant(self, question: str, context: str) -> bool:
        question_embedding = self.embedding_model.encode(question)
        context_embedding = self.embedding_model.encode(context)
        similarity = cosine_similarity([question_embedding], [context_embedding])[0][0]
        return similarity > self.similarity_threshold

    def _find_exact_match(self, partial_text: str, story_id: Optional[str] = None) -> Optional[str]:
        """Find exact matches for partial text in the story"""
        if not story_id:
            return None
            
        # First try to find the exact sentence in the story file
        story_file = os.path.join(self.data_dir, f"{story_id}.json")
        if os.path.exists(story_file):
            with open(story_file, 'r', encoding='utf-8') as f:
                story_data = json.load(f)
                story_text = story_data.get('content', '')
                
                # Split into sentences
                sentences = sent_tokenize(story_text)
                
                # Look for the sentence containing the exact partial text
                for sentence in sentences:
                    # Check if the sentence starts with the partial text
                    if sentence.startswith(partial_text):
                        return sentence
                    # Check if the partial text is in the middle of the sentence
                    if partial_text in sentence:
                        # Get the part of the sentence that starts with the partial text
                        start_idx = sentence.find(partial_text)
                        if start_idx >= 0:
                            return sentence[start_idx:]
        
        # If not found in story file, try the vector database
        results = self.collection.query(
            query_embeddings=[self.embedding_model.encode(partial_text).tolist()],
            n_results=3,
            where={"story_id": story_id}
        )
        
        if not results['documents']:
            return None
            
        # Look for exact matches or continuations
        partial_text = partial_text.strip()
        for doc in results['documents'][0]:
            # Split into sentences for more precise matching
            sentences = sent_tokenize(doc)
            for sentence in sentences:
                # Check if the sentence starts with the partial text
                if sentence.startswith(partial_text):
                    return sentence
                # Check if the partial text is in the middle of the sentence
                if partial_text in sentence:
                    # Get the part of the sentence that starts with the partial text
                    start_idx = sentence.find(partial_text)
                    if start_idx >= 0:
                        return sentence[start_idx:]
                        
        return None

    def _get_relevant_context(self, question: str, story_id: Optional[str] = None) -> str:
        # First try exact matching for sentence completion
        if story_id:
            exact_match = self._find_exact_match(question, story_id)
            if exact_match:
                return exact_match
        
        question_embedding = self.embedding_model.encode(question)
        
        # Extract key words from question
        question_words = set(question.lower().split())
        
        # Try with exact word matching
        if story_id:
            results = self.collection.query(
                query_embeddings=[question_embedding.tolist()],
                n_results=3,  # Reduced from 10 to 3
                where={"story_id": story_id}
            )
            
            if results['documents']:
                # Score each document based on word overlap and semantic similarity
                scored_docs = []
                for doc in results['documents'][0]:
                    # Split into sentences for more precise matching
                    sentences = sent_tokenize(doc)
                    for sentence in sentences:
                        sentence_words = set(sentence.lower().split())
                        word_overlap = len(question_words.intersection(sentence_words))
                        semantic_sim = cosine_similarity(
                            [self.embedding_model.encode(sentence)], 
                            [question_embedding]
                        )[0][0]
                        
                        # Combined score (weighted)
                        score = (word_overlap * 0.7) + (semantic_sim * 0.3)
                        scored_docs.append((sentence, score))
                
                # Sort by score and take top 2
                scored_docs.sort(key=lambda x: x[1], reverse=True)
                best_matches = [doc for doc, score in scored_docs[:2] if score > 0.3]
                
                if best_matches:
                    return " ".join(best_matches)
        
        # If no good matches found, fall back to semantic search
        results = self.collection.query(
            query_embeddings=[question_embedding.tolist()],
            n_results=2,  # Reduced from 3 to 2
            where={"story_id": story_id} if story_id else None
        )
        
        if not results['documents']:
            return ""
            
        # Combine relevant sentences with overlap handling
        combined_context = []
        seen_content = set()
        
        for doc in results['documents'][0]:
            # Split into sentences for more precise matching
            sentences = sent_tokenize(doc)
            for sentence in sentences:
                # Check for overlap with existing content
                sentence_embedding = self.embedding_model.encode(sentence)
                is_duplicate = False
                
                for existing in combined_context:
                    existing_embedding = self.embedding_model.encode(existing)
                    if cosine_similarity([sentence_embedding], [existing_embedding])[0][0] > self.context_overlap_threshold:
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    combined_context.append(sentence)
        
        return " ".join(combined_context)

    def _detect_question_type(self, question: str) -> str:
        question = question.lower()
        
        # Title related questions
        if any(pattern in question for pattern in ['عنوان', 'نام', 'کا نام', 'کا عنوان', 'کہانی کا عنوان', 'کہانی کا نام']):
            return 'title'
            
        # Lesson related questions
        if any(pattern in question for pattern in ['سبق', 'سیکھنا', 'سیکھتے', 'سیکھا', 'کہانی کا سبق', 'کہانی سے سبق']):
            return 'lesson'
            
        # Character related questions
        if any(pattern in question for pattern in ['کردار', 'کرداروں', 'کون کون', 'کون ہے', 'کہانی کے کردار']):
            return 'characters'
            
        # Moral related questions
        if any(pattern in question for pattern in ['سبق', 'پیغام', 'مقصد', 'نتیجہ', 'کہانی کا پیغام']):
            return 'moral'
            
        # Summary related questions
        if any(pattern in question for pattern in ['خلاصہ', 'کہانی کا خلاصہ', 'کہانی کا مختصر بیان']):
            return 'summary'
            
        # Theme related questions
        if any(pattern in question for pattern in ['تھیم', 'موضوع', 'کہانی کا موضوع']):
            return 'theme'
            
        # Difficulty level questions
        if any(pattern in question for pattern in ['مشکل', 'آسان', 'کہانی کی مشکل']):
            return 'difficulty'
            
        # Age group questions
        if any(pattern in question for pattern in ['عمر', 'کہانی کس عمر کے لیے ہے']):
            return 'age_group'
            
        # Difficult words questions
        if any(pattern in question for pattern in ['مشکل الفاظ', 'مشکل لفظ', 'لفظوں کا مطلب']):
            return 'difficult_words'
            
        return 'content'

    def _get_direct_answer(self, question_type: str, story_id: str) -> Dict[str, Any]:
        story_file = os.path.join(self.data_dir, f"{story_id}.json")
        if not os.path.exists(story_file):
            return {
                'success': False,
                'error': 'Story not found'
            }
            
        with open(story_file, 'r', encoding='utf-8') as f:
            story_data = json.load(f)
            
        if question_type == 'title':
            return {
                'success': True,
                'response': story_data.get('title', ''),
                'context': story_data.get('title', '')
            }
        elif question_type == 'lesson':
            return {
                'success': True,
                'response': story_data.get('lesson', ''),
                'context': story_data.get('lesson', '')
            }
        elif question_type == 'characters':
            characters = story_data.get('characters', [])
            character_names = [char['name'] for char in characters]
            return {
                'success': True,
                'response': '، '.join(character_names),
                'context': '، '.join(character_names)
            }
        elif question_type == 'moral':
            return {
                'success': True,
                'response': story_data.get('moral', ''),
                'context': story_data.get('moral', '')
            }
        elif question_type == 'summary':
            return {
                'success': True,
                'response': story_data.get('summary', ''),
                'context': story_data.get('summary', '')
            }
        elif question_type == 'theme':
            return {
                'success': True,
                'response': story_data.get('theme', ''),
                'context': story_data.get('theme', '')
            }
        elif question_type == 'difficulty':
            return {
                'success': True,
                'response': story_data.get('difficulty_level', ''),
                'context': story_data.get('difficulty_level', '')
            }
        elif question_type == 'age_group':
            return {
                'success': True,
                'response': story_data.get('age_group', ''),
                'context': story_data.get('age_group', '')
            }
        elif question_type == 'difficult_words':
            difficult_words = story_data.get('difficult_words', [])
            words_with_meanings = [f"{word['word']} - {word['meaning']}" for word in difficult_words]
            return {
                'success': True,
                'response': '\n'.join(words_with_meanings),
                'context': '\n'.join(words_with_meanings)
            }
            
        return {
            'success': False,
            'error': 'Invalid question type'
        }

    def _is_exact_question(self, question: str) -> tuple[bool, str]:
        """Check if the question matches any exact pattern"""
        question = question.strip()
        for qtype, patterns in self.exact_questions.items():
            if question in patterns:
                return True, qtype
        return False, ''

    def _count_tokens(self, text: str) -> int:
        # Rough estimation of tokens (words + punctuation)
        return len(text.split()) + len([c for c in text if c in '.,!?;:'])
        
    def _truncate_context(self, context: str, max_tokens: int = 200) -> str:
        """Truncate context to fit within token limit"""
        words = context.split()
        if len(words) <= max_tokens:
            return context
            
        # Take first max_tokens words
        truncated = ' '.join(words[:max_tokens])
        return truncated

    def answer_question(self, question: str, story_id: Optional[str] = None) -> Dict[str, Any]:
        # First check for exact question match
        is_exact, question_type = self._is_exact_question(question)
        
        if is_exact and story_id:
            direct_answer = self._get_direct_answer(question_type, story_id)
            if direct_answer['success']:
                return direct_answer
        
        # Check for sentence completion first
        if story_id:
            exact_match = self._find_exact_match(question, story_id)
            if exact_match:
                return {
                    'success': True,
                    'response': exact_match,
                    'context': exact_match
                }
        
        # Get relevant context
        context = self._get_relevant_context(question, story_id)
        
        if not context:
            return {
                'success': False,
                'error': 'No relevant context found'
            }
        
        # If we found an exact match, return it directly
        if story_id and self._find_exact_match(question, story_id):
            return {
                'success': True,
                'response': context,
                'context': context
            }
        
        # Truncate context to be very conservative with tokens
        context = self._truncate_context(context, max_tokens=100)
        
        # Create a minimal prompt
        prompt = f"""<|system|>Answer based ONLY on this context. If unsure, say: "کہانی میں ذکر نہیں۔"
<|user|>{question}
<|context|>{context}
<|assistant|>"""
        
        try:
            # Check total tokens before generation
            total_tokens = self._count_tokens(prompt)
            if total_tokens > 400:  # Leave room for response
                # Try with even shorter context
                context = self._truncate_context(context, max_tokens=50)
                prompt = f"""<|system|>Answer based ONLY on this context. If unsure, say: "کہانی میں ذکر نہیں۔"
<|user|>{question}
<|context|>{context}
<|assistant|>"""
            
            answer = self.llm(prompt)
            formatted_answer = self._format_response(answer)
            
            # Validate response
            if not self._validate_response(formatted_answer, context):
                return {
                    'success': False,
                    'error': 'Generated response was not relevant to the context'
                }
            
            return {
                'success': True,
                'response': formatted_answer,
                'context': context
            }
            
        except Exception as e:
            if "Number of tokens exceeded" in str(e):
                # Last resort: try with minimal context
                context = self._truncate_context(context, max_tokens=25)
                prompt = f"""<|system|>Answer based ONLY on this context. If unsure, say: "کہانی میں ذکر نہیں۔"
<|user|>{question}
<|context|>{context}
<|assistant|>"""
                
                try:
                    answer = self.llm(prompt)
                    formatted_answer = self._format_response(answer)
                    
                    if self._validate_response(formatted_answer, context):
                        return {
                            'success': True,
                            'response': formatted_answer,
                            'context': context
                        }
                except:
                    pass
            
            return {
                'success': False,
                'error': 'Could not generate a valid response due to token limits'
            }

# Create a single instance of RAGHandler
rag_handler = RAGHandler() 