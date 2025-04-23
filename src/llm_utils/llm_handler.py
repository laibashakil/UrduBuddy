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
            prompt = f"""Read this story. A child will ask a question about this story.
Please:
1. Answer only based on the story content
2. Keep the answer short and simple
3. Do not provide any additional information
4. Only tell what is mentioned in the story

Story:
{story_content}

Child's question: {question}

Please provide your answer in Urdu language.
"""
            
            # Get response from Cohere
            response = self.co.generate(
                model="command",  # Using Cohere's Command model
                prompt=prompt,
                max_tokens=200,  # Reduced for shorter responses
                temperature=0.3,  # Lower temperature for more focused responses
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