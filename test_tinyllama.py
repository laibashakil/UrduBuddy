from ctransformers import AutoModelForCausalLM
import sys
import time
from typing import Tuple

def measure_response(response: str, expected: str) -> Tuple[float, int]:
    """Measure hallucination level and response length"""
    response_words = set(response.lower().split())
    expected_words = set(expected.lower().split())
    overlap = len(response_words.intersection(expected_words))
    total = len(expected_words)
    hallucination_level = 1 - (overlap / total) if total > 0 else 1.0
    return hallucination_level, len(response)

try:
    print("Loading TinyLlama model...")
    start_time = time.time()
    model = AutoModelForCausalLM.from_pretrained(
        "models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
        model_type="llama",
        max_new_tokens=64,
        context_length=512,
        temperature=0.2,
        repetition_penalty=1.2,
        stop=["سوال:", "\nسوال:"]
    )
    load_time = time.time() - start_time
    print(f"Model loaded successfully in {load_time:.2f} seconds!")

    # Urdu story
    story = """علی ایک اچھا بچہ تھا۔ ایک دن اس نے ایک زخمی پرندہ دیکھا۔ اس نے پرندے کو گھر لایا اور اس کی دیکھ بھال کی۔ جب پرندہ ٹھیک ہوا تو علی نے اسے آزاد کر دیا۔"""

    # Questions and expected answers
    questions = [
        ("بچے کا نام کیا تھا؟", "علی"),
        ("علی نے کیا دیکھا؟", "زخمی پرندہ"),
        ("پرندے کے ساتھ کیا ہوا؟", "ٹھیک ہوا اور آزاد کر دیا گیا")
    ]

    print("\nStarting to process questions...")
    total_time = 0
    total_hallucination = 0
    total_length = 0

    for i, (question, expected) in enumerate(questions, 1):
        print(f"\nProcessing question {i}...")
        prompt = f"""یہ ایک کہانی ہے:
{story}

سوال: کہانی میں بچے کا نام کیا ہے؟
جواب: علی

سوال: علی نے کیا دیکھا؟
جواب: زخمی پرندہ

سوال: پرندے کے ساتھ کیا ہوا؟
جواب: ٹھیک ہوا اور آزاد کر دیا گیا

سوال: {question}
جواب:"""

        # Optional: Uncomment to debug prompt
        # print(f"\nFull Prompt:\n{prompt}\n")

        try:
            start_time = time.time()
            response = model(prompt)
            response_time = time.time() - start_time
            total_time += response_time

            hallucination, length = measure_response(response, expected)
            total_hallucination += hallucination
            total_length += length

            print(f"Question: {question}")
            print(f"Answer: {response}")
            print(f"Time: {response_time:.2f} seconds")
            print(f"Hallucination Level: {hallucination:.2%}")
            print(f"Response Length: {length} characters\n")

        except Exception as e:
            print(f"Error during question {i}: {str(e)}\n")

    # Summary
    num_questions = len(questions)
    print("\nSummary:")
    print(f"Average Response Time: {total_time / num_questions:.2f} seconds")
    print(f"Average Hallucination Level: {total_hallucination / num_questions:.2%}")
    print(f"Average Response Length: {total_length / num_questions:.0f} characters")

except Exception as e:
    print(f"An error occurred: {str(e)}", file=sys.stderr)
