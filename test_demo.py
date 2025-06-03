#!/usr/bin/env python3
"""
Demo script to test the AI Book Search functionality
Run this to verify everything is working before launching the Streamlit app
"""

import os
import json
from dotenv import load_dotenv
from llm_service import LLMService
from models import QueryType

def test_queries():
    """Test various query types"""
    
    # Load environment
    load_dotenv()
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("❌ Please set your OpenAI API key in the .env file!")
        return
    
    print("🚀 Testing AI Book Search...")
    print("=" * 50)
    
    # Initialize service
    llm_service = LLMService()
    
    # Test queries
    test_cases = [
        {
            "query": "How to deal with difficult colleagues",
            "expected_type": "problem_solving"
        },
        {
            "query": "London autistic detective",
            "expected_type": "character_scene_description"
        },
        {
            "query": "Books about flow state",
            "expected_type": "quote_concept_memory"
        },
        {
            "query": "What is the book Atomic Habits about?",
            "expected_type": "specific_book"
        },
        {
            "query": "Like Harry Potter but for adults",
            "expected_type": "comparative_search"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test_case['query']}")
        print("-" * 40)
        
        try:
            # Process query
            result = llm_service.process_search_query(test_case['query'])
            
            # Display analysis
            print(f"📊 Query Type: {result.analysis.query_type.value}")
            print(f"🎯 Intent: {result.analysis.user_intent_category.value if result.analysis.user_intent_category else 'N/A'}")
            print(f"🔍 Confidence: {result.analysis.confidence_score:.0%}")
            print(f"💭 Reasoning: {result.analysis.reasoning}")
            
            # Display results
            if result.analysis.query_type == QueryType.SPECIFIC_BOOK:
                if result.book_recommendation:
                    print(f"\n📚 Book: {result.book_recommendation.title}")
                    print(f"👤 Author: {result.book_recommendation.author}")
                    print(f"⭐ Relevance: {result.book_recommendation.relevance_score:.0%}")
                    print(f"💡 Reason: {result.book_recommendation.reason}")
            else:
                print(f"\n🎴 Generated {len(result.content_cards)} content cards:")
                for j, card in enumerate(result.content_cards, 1):
                    print(f"  {j}. {card.type.upper()}: {card.title}")
                    if card.book_title:
                        print(f"     📖 {card.book_title} by {card.book_author}")
            
            print("✅ Success!")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    # Test placeholder feature
    print("\n" + "=" * 50)
    print("🚧 Testing Placeholder Feature...")
    try:
        placeholder = llm_service.get_placeholder_feature()
        print(f"📦 Feature: {placeholder.name}")
        print(f"📝 Description: {placeholder.description}")
        print(f"⏰ Status: {placeholder.status}")
        print(f"📅 ETA: {placeholder.estimated_completion}")
        print("✅ Success!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 Demo complete! If all tests passed, run: streamlit run app.py")

if __name__ == "__main__":
    test_queries() 