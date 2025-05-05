from ctransformers import AutoModelForCausalLM
import sys
import time
import psutil
import os
from typing import Tuple, Dict, List
import json
from datetime import datetime
import re
from nltk.tokenize import sent_tokenize
import nltk
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import traceback
import numpy as np

def get_memory_usage() -> float:
    """Get current memory usage in MB"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

def count_tokens(text: str) -> int:
    """Rough estimation of tokens (words + punctuation)"""
    return len(text.split()) + len([c for c in text if c in '.,!?;:'])

def truncate_context(context: str, max_tokens: int = 100) -> str:
    """Truncate context to fit within token limit"""
    sentences = sent_tokenize(context)
    result = []
    total_tokens = 0
    
    for sentence in sentences:
        sentence_tokens = count_tokens(sentence)
        if total_tokens + sentence_tokens > max_tokens:
            break
        result.append(sentence)
        total_tokens += sentence_tokens
    
    return " ".join(result)

def measure_response(response: str, expected: str, embedding_model) -> Tuple[float, int, float]:
    """Measure hallucination level, response length, and semantic similarity"""
    # Word overlap check
    response_words = set(response.lower().split())
    expected_words = set(expected.lower().split())
    word_overlap = len(response_words.intersection(expected_words))
    total = len(expected_words)
    word_similarity = word_overlap / total if total > 0 else 0
    
    # Semantic similarity check
    response_embedding = embedding_model.encode(response)
    expected_embedding = embedding_model.encode(expected)
    semantic_similarity = float(cosine_similarity([response_embedding], [expected_embedding])[0][0])
    
    # Combined score
    hallucination_level = 1 - ((word_similarity * 0.7) + (semantic_similarity * 0.3))
    return float(hallucination_level), len(response), float(semantic_similarity)

def load_test_story() -> Dict:
    """Load a single test story"""
    file_path = "data/khachwa-aur-khargosh.json"
    print(f"Loading test story: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)
        
    # Create test questions
    questions = [
        {"question": "کہانی کا عنوان کیا ہے؟", "expected": story_data.get("title", "")},
        {"question": "کہانی سے کیا سبق ملتا ہے؟", "expected": story_data.get("lesson", "")},
        {"question": "کہانی کا خلاصہ کیا ہے؟", "expected": story_data.get("summary", "")}
    ]
    
    return {
        "story": story_data.get("content", ""),
        "questions": questions
    }

def save_results(results: Dict):
    """Save test results to JSON file"""
    # Convert numpy types to Python native types
    def convert_types(obj):
        if isinstance(obj, np.float32):
            return float(obj)
        elif isinstance(obj, dict):
            return {k: convert_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_types(item) for item in obj]
        return obj
    
    results = convert_types(results)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_results_{timestamp}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to {filename}")

try:
    print("Loading models...")
    initial_memory = get_memory_usage()
    start_time = time.time()
    
    # Load embedding model
    embedding_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    
    # Load LLM
    model = AutoModelForCausalLM.from_pretrained(
        "models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
        model_type="llama",
        max_new_tokens=128,
        temperature=0.2
    )
    
    load_time = time.time() - start_time
    model_memory = get_memory_usage() - initial_memory
    print(f"Models loaded successfully in {load_time:.2f} seconds!")
    print(f"Model memory usage: {model_memory:.2f} MB")

    # Load test story
    story_data = load_test_story()
    print(f"\nLoaded test story with {len(story_data['questions'])} questions")
    
    # Initialize metrics
    metrics = {
        "model_load_time": load_time,
        "model_memory_usage": model_memory,
        "total_questions": 0,
        "total_time": 0,
        "total_hallucination": 0,
        "total_length": 0,
        "total_accuracy": 0,
        "errors": 0,
        "detailed_results": []
    }

    print("\nStarting to process questions...")
    
    story = story_data["story"]
    for q_data in story_data["questions"]:
        question = q_data["question"]
        expected = q_data["expected"]
        
        print(f"\nProcessing question: {question}")
        
        # Truncate context to fit token limits
        truncated_story = truncate_context(story, max_tokens=100)
        
        # Create prompt in the same format as RAGHandler with Urdu language enforcement
        prompt = f"""<|system|>You are an Urdu language assistant. You MUST ONLY respond in Urdu. NEVER use English or any other language. If you cannot answer in Urdu, respond with "معذرت، میں جواب نہیں دے سکتا۔". Answer based ONLY on this context. If unsure, say: "کہانی میں ذکر نہیں۔"
<|user|>{question}
<|context|>{truncated_story}
<|assistant|>"""

        try:
            # Check total tokens before generation
            total_tokens = count_tokens(prompt)
            print(f"Prompt tokens: {total_tokens}")
            
            # Measure response time
            start_time = time.time()
            response = model(prompt)
            response_time = time.time() - start_time
            
            # Format response
            response = re.sub(r'\n\s*\n', '\n', response)
            response = response.strip()
            response = re.sub(r'```.*?```', '', response, flags=re.DOTALL)
            response = re.sub(r'<.*?>', '', response)
            
            if not response:
                print("No valid response received")
                metrics["errors"] += 1
                continue
            
            # Measure metrics
            hallucination, length, accuracy = measure_response(response, expected, embedding_model)
            
            # Update metrics
            metrics["total_questions"] += 1
            metrics["total_time"] += response_time
            metrics["total_hallucination"] += hallucination
            metrics["total_length"] += length
            metrics["total_accuracy"] += accuracy
            
            # Store detailed results
            metrics["detailed_results"].append({
                "question": question,
                "expected": expected,
                "response": response,
                "time": response_time,
                "hallucination": float(hallucination),
                "length": length,
                "accuracy": float(accuracy),
                "prompt_tokens": total_tokens
            })
            
            print(f"Answer: {response}")
            print(f"Time: {response_time:.2f} seconds")
            print(f"Hallucination Level: {hallucination:.2%}")
            print(f"Accuracy: {accuracy:.2%}")
            print(f"Response Length: {length} characters")

        except Exception as e:
            print(f"Error: {str(e)}")
            metrics["errors"] += 1

    # Calculate averages
    num_questions = metrics["total_questions"]
    if num_questions > 0:
        metrics["average_time"] = metrics["total_time"] / num_questions
        metrics["average_hallucination"] = metrics["total_hallucination"] / num_questions
        metrics["average_length"] = metrics["total_length"] / num_questions
        metrics["average_accuracy"] = metrics["total_accuracy"] / num_questions
        metrics["error_rate"] = metrics["errors"] / num_questions

    # Print summary
    print("\nSummary:")
    print(f"Total Questions: {metrics['total_questions']}")
    print(f"Average Response Time: {metrics['average_time']:.2f} seconds")
    print(f"Average Hallucination Level: {metrics['average_hallucination']:.2%}")
    print(f"Average Accuracy: {metrics['average_accuracy']:.2%}")
    print(f"Average Response Length: {metrics['average_length']:.0f} characters")
    print(f"Error Rate: {metrics['error_rate']:.2%}")
    print(f"Total Memory Usage: {get_memory_usage():.2f} MB")

    # Save results
    save_results(metrics)

except Exception as e:
    print(f"An error occurred: {str(e)}")
    print(traceback.format_exc())
