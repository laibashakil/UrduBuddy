from typing import Dict, Any
import re
from .rag_handler import RAGHandler

class LLMHandler:
    def __init__(self):
        # Initialize RAG handler
        self.rag_handler = RAGHandler()
        print("LLM Handler initialized with RAG system")
        
    def _create_prompt(self, story_content: str, question: str) -> str:
        # Create a simple prompt for context
        prompt = f"""
        کہانی: {story_content}
        
        سوال: {question}
        
        جواب: """
        return prompt
        
    def _extract_answer(self, generated_text: str) -> str:
        # Simple answer extraction
        try:
            # Remove the prompt and any extra text
            answer = generated_text.split("جواب:")[-1].strip()
            # Remove any extra newlines or spaces
            answer = re.sub(r'\s+', ' ', answer)
            return answer.strip()
        except Exception as e:
            print(f"Error extracting answer: {e}")
            return "معذرت، میں آپ کے سوال کا جواب نہیں دے سکا۔"
        
    def chat_about_story(self, story_content: str, user_message: str) -> Dict[str, Any]:
        try:
            print(f"Processing question: {user_message}")
            
            # Use RAG system to get the answer
            response = self.rag_handler.get_answer(story_content, user_message)
            
            return {
                'response': response,
                'success': True
            }
            
        except Exception as e:
            print(f"Error in chat_about_story: {e}")
            return {
                'response': 'معذرت، میں آپ کے سوال کا جواب نہیں دے سکا۔ براہ کرم دوبارہ کوشش کریں۔',
                'success': False
            }

# Initialize the LLM handler
llm_handler = LLMHandler() 