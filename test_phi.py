from ctransformers import AutoModelForCausalLM
import sys
import time
from typing import Dict, List, Tuple

def measure_response(response: str, expected: str) -> Tuple[float, int]:
    """Measure hallucination level and response length"""
    # Simple word overlap measurement
    response_words = set(response.lower().split())
    expected_words = set(expected.lower().split())
    overlap = len(response_words.intersection(expected_words))
    total = len(expected_words)
    hallucination_level = 1 - (overlap / total) if total > 0 else 1.0
    return hallucination_level, len(response)

try:
    print("Loading Phi-2 model...")
    start_time = time.time()
    model = AutoModelForCausalLM.from_pretrained(
        "models/phi-2.Q4_K_M.gguf",
        model_type="gpt2",
        max_new_tokens=128,
        context_length=512,
        temperature=0.3
    )
    load_time = time.time() - start_time
    print(f"Model loaded successfully in {load_time:.2f} seconds!")

    # Urdu story
    story = """علی ایک اچھا بچہ تھا۔ ایک دن اس نے ایک زخمی پرندہ دیکھا۔ اس نے پرندے کو گھر لایا اور اس کی دیکھ بھال کی۔ جب پرندہ ٹھیک ہوا تو علی نے اسے آزاد کر دیا۔"""

    # Questions with expected answers
    questions = [
        ("بچے کا نام کیا تھا؟", "علی"),
        ("علی نے کیا دیکھا؟", "زخمی پرندہ"),
        ("پرندے کے ساتھ کیا ہوا؟", "ٹھیک ہوا اور آزاد کر دیا گیا")
    ]

    print("\nStarting to process questions...")
    total_time = 0
    total_hallucination = 0
    total_length = 0
    
    # Ask each question
    for i, (question, expected) in enumerate(questions, 1):
        print(f"\nProcessing question {i}...")
        # Phi instruction format
        prompt = f"""Instruct: You are a helpful Urdu language assistant. Please read this story and answer the question in Urdu.

Story: {story}

Question: {question}

Output:"""
        
        print(f"Question: {question}")
        try:
            start_time = time.time()
            response = model(prompt)
            response_time = time.time() - start_time
            total_time += response_time
            
            # Measure hallucination and length
            hallucination, length = measure_response(response, expected)
            total_hallucination += hallucination
            total_length += length
            
            print(f"Answer: {response}")
            print(f"Time: {response_time:.2f} seconds")
            print(f"Hallucination Level: {hallucination:.2%}")
            print(f"Response Length: {length} characters\n")
        except Exception as e:
            print(f"Error: {str(e)}\n")

    # Print summary
    num_questions = len(questions)
    print("\nSummary:")
    print(f"Average Response Time: {total_time/num_questions:.2f} seconds")
    print(f"Average Hallucination Level: {total_hallucination/num_questions:.2%}")
    print(f"Average Response Length: {total_length/num_questions:.0f} characters")

except Exception as e:
    print(f"An error occurred: {str(e)}", file=sys.stderr) 