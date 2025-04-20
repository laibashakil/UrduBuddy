from rag_system import UrduRAG
import json

def test_rag_system():
    # Initialize the RAG system
    rag = UrduRAG("data/urdu_data.json")
    
    # Test questions in English
    english_questions = [
        "What is the capital of Pakistan?",
        "What is the national language of Pakistan?",
        "Which city is the economic center of Pakistan?"
    ]
    
    # Test questions in Urdu
    urdu_questions = [
        "پاکستان کا دارالحکومت کیا ہے؟",
        "پاکستان کی قومی زبان کیا ہے؟",
        "پاکستان کا معاشی مرکز کون سا شہر ہے؟"
    ]
    
    print("Testing English questions:")
    for question in english_questions:
        response = rag.query(question)
        print(f"\nQuestion: {question}")
        print(f"Response: {response}")
    
    print("\nTesting Urdu questions:")
    for question in urdu_questions:
        response = rag.query(question)
        print(f"\nQuestion: {question}")
        print(f"Response: {response}")

if __name__ == "__main__":
    test_rag_system() 