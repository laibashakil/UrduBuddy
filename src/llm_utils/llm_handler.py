from typing import Dict, Any
import re
import cohere
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMHandler:
    def __init__(self):
        print("LLM Handler initialized")
        # Initialize Cohere client
        self.co = cohere.Client(os.getenv('COHERE_API_KEY'))
        
    def chat_about_story(self, story_content: str, question: str) -> dict:
        """Generate a response about a story using the full story content."""
        try:
            # Input validation
            if not story_content or not question:
                return {
                    'success': False,
                    'error': 'Story content and question are required'
                }
            
            # Sanitize inputs
            story_content = story_content.strip()
            question = question.strip()
            
            # Create a focused prompt for children's questions
            prompt = f"""یہ کہانی پڑھیں۔ ایک بچہ اس کہانی کے بارے میں سوال پوچھے گا۔ 
براہ کرم:
1. صرف کہانی کے مطابق جواب دیں
2. مختصر اور آسان جواب دیں
3. کوئی اضافی معلومات نہ دیں
4. صرف وہی بتائیں جو کہانی میں ہے

کہانی:
{story_content}

بچے کا سوال: {question}

جواب:"""
            
            # Get response from Cohere
            response = self.co.generate(
                prompt=prompt,
                max_tokens=100,  # Reduced for shorter responses
                temperature=0.2,  # Lower temperature for more focused responses
                k=0,
                stop_sequences=["\n", "بچے کا سوال:", "کہانی:"],  # Stop at newlines or new questions
                return_likelihoods='NONE'
            )
            
            # Extract the generated text
            generated_text = response.generations[0].text.strip()
            
            # Validate response
            if not generated_text:
                return {
                    'success': False,
                    'error': 'Empty response generated'
                }
            
            # Basic content validation
            generated_text = generated_text.strip()
            if len(generated_text) > 1000:  # Limit response length
                generated_text = generated_text[:1000] + "..."
            
            return {
                'success': True,
                'response': generated_text
            }
            
        except Exception as e:
            print(f"Error in chat_about_story: {e}")
            return {
                'success': False,
                'error': str(e)
            }

# Create a single instance of LLMHandler
_handler = LLMHandler()

# Export the instance methods directly
def chat_about_story(story_content: str, question: str) -> dict:
    return _handler.chat_about_story(story_content, question)

# Export the handler instance for direct use
llm_handler = _handler 