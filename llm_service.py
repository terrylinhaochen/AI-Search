import openai
import json
import os
from typing import Dict, Any
from dotenv import load_dotenv
from models import (
    QueryAnalysis, QueryType, UserIntentCategory, 
    SearchResponse, BookRecommendation, ContentCard, PlaceholderFeature
)

load_dotenv()

class LLMService:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI()
    
    def analyze_query(self, user_query: str) -> QueryAnalysis:
        """Analyze user query to determine type and intent category"""
        
        system_prompt = """
        You are an expert at analyzing search queries for content (books, podcasts, hosts, articles). Your task is to:
        1. Determine if the query is about a SPECIFIC item or GENERAL
        2. If GENERAL, categorize the user intent into one of these categories:
           - problem_solving: User has a specific problem and believes content can provide solutions
           - exploration_discovery: User wants to explore within specific parameters
           - quote_concept_memory: User is touched by a specific concept/quote
           - plot_fragment_memory: User wants to relive a specific story fragment
           - character_scene_description: User has strong resonance with characters/worlds
           - emotional_theme: User seeks specific emotional experiences related to current life situation
           - comparative_search: User likes specific aspects of a work and wants similar variants
        
        You MUST respond with valid JSON only. No other text.
        Return a JSON object with:
        - query_type: "specific_book" or "general"
        - user_intent_category: (only if general) one of the categories above
        - confidence_score: float between 0-1
        - reasoning: explanation of your analysis
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze this query: '{user_query}'"}
                ],
                temperature=0.3
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Clean the response to ensure it's valid JSON
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            if not response_text:
                raise ValueError("Empty response from OpenAI")
            
            result = json.loads(response_text)
            
            return QueryAnalysis(
                query_type=QueryType(result["query_type"]),
                user_intent_category=UserIntentCategory(result["user_intent_category"]) if result.get("user_intent_category") else None,
                confidence_score=result["confidence_score"],
                reasoning=result["reasoning"]
            )
        except Exception as e:
            print(f"Error in query analysis: {str(e)}")
            # Fallback analysis
            return QueryAnalysis(
                query_type=QueryType.GENERAL,
                user_intent_category=UserIntentCategory.EXPLORATION_DISCOVERY,
                confidence_score=0.5,
                reasoning=f"Error in analysis: {str(e)}"
            )
    
    def generate_book_recommendation(self, query: str) -> BookRecommendation:
        """Generate recommendation for specific content queries"""
        
        system_prompt = """
        You are a knowledgeable content curator. The user is asking about specific content (books, podcasts, etc.).
        Provide a recommendation with title, creator, and detailed reasoning.
        
        You MUST respond with valid JSON only. No other text.
        Return JSON with: title, author, reason, relevance_score (0-1)
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0.4
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Clean the response
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            if not response_text:
                raise ValueError("Empty response from OpenAI")
            
            result = json.loads(response_text)
            return BookRecommendation(**result)
        except Exception as e:
            print(f"Error in recommendation generation: {str(e)}")
            return BookRecommendation(
                title="Content Analysis Error",
                author="System",
                reason=f"Unable to analyze: {str(e)}",
                relevance_score=0.0
            )
    
    def generate_content_cards(self, query: str, intent_category: UserIntentCategory) -> list[ContentCard]:
        """Generate relevant content cards based on query and intent"""
        
        category_prompts = {
            UserIntentCategory.PROBLEM_SOLVING: "Generate practical content recommendations (books, podcasts, articles) that solve real problems",
            UserIntentCategory.EXPLORATION_DISCOVERY: "Generate content that offers new perspectives and discoveries",
            UserIntentCategory.QUOTE_CONCEPT_MEMORY: "Generate content cards with memorable quotes and concepts",
            UserIntentCategory.PLOT_FRAGMENT_MEMORY: "Generate cards focusing on specific story elements and plot points",
            UserIntentCategory.CHARACTER_SCENE_DESCRIPTION: "Generate cards highlighting character development and vivid scenes",
            UserIntentCategory.EMOTIONAL_THEME: "Generate emotionally resonant content that matches the user's current state",
            UserIntentCategory.COMPARATIVE_SEARCH: "Generate recommendations similar to what the user already likes"
        }
        
        system_prompt = f"""
        You are creating content cards for a search system. 
        Focus on: {category_prompts.get(intent_category, "general recommendations")}
        
        Generate 1-5 content cards that form a COHESIVE PROGRESSION and are logically related to each other.
        The cards should build upon each other or explore different aspects of the same topic.
        
        Decision criteria for number of cards:
        - 1 card: Very specific query with one clear answer
        - 2-3 cards: Query with a few complementary perspectives 
        - 4-5 cards: Complex topic that benefits from multiple angles
        
        Include diverse content types (books, podcasts, audiobooks, articles) when multiple cards are warranted.
        
        For each card:
        
        You MUST respond with valid JSON only. No other text.
        Return an array of objects with:
        - type: EXACTLY one of: "quote", "summary", "recommendation", "theme"
        - title: engaging title that relates to the overall theme
        - description: compelling description (max 100 words) showing how this fits the progression
        - book_title: (if applicable) content title - for podcasts use format "Podcast Name" or "Episode Title"
        - book_author: (if applicable) creator name - for podcasts use host names
        - quote: (only if type is "quote") the actual quote text
        - source_page: (optional) string like "Page 143" or "23:45" for timestamps
        - clickable_link: always use "#"
        
        Important: 
        - Each card should logically connect to or build upon the others
        - For podcasts, include words like "Podcast", "Episode", "Interview", "Talk" in the book_title
        - source_page should be a string, not a number
        - Ensure cards form a coherent learning journey or exploration path
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Query: '{query}' | Category: {intent_category.value}"}
                ],
                temperature=0.6
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Clean the response
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            if not response_text:
                raise ValueError("Empty response from OpenAI")
            
            print(f"Raw response: {response_text}")  # Debug print
            
            cards_data = json.loads(response_text)
            return [ContentCard(**card) for card in cards_data]
        except Exception as e:
            print(f"Error in content generation: {str(e)}")
            print(f"Raw response was: {response_text if 'response_text' in locals() else 'No response'}")
            # Fallback cards
            return [
                ContentCard(
                    type="recommendation",
                    title="Content Discovery",
                    description="We're finding the best content for your query. Please try again or refine your search.",
                    clickable_link="#"
                )
            ]
    
    def process_search_query(self, user_query: str) -> SearchResponse:
        """Main method to process a search query end-to-end"""
        
        # Step 1: Analyze the query
        analysis = self.analyze_query(user_query)
        
        # Step 2: Generate appropriate response
        if analysis.query_type == QueryType.SPECIFIC_BOOK:
            book_rec = self.generate_book_recommendation(user_query)
            return SearchResponse(
                analysis=analysis,
                book_recommendation=book_rec,
                content_cards=[]
            )
        else:
            content_cards = self.generate_content_cards(user_query, analysis.user_intent_category)
            return SearchResponse(
                analysis=analysis,
                book_recommendation=None,
                content_cards=content_cards
            )
    
    def get_placeholder_feature(self) -> PlaceholderFeature:
        """Generate a work-in-progress placeholder feature"""
        return PlaceholderFeature(
            name="Semantic Vector Search",
            description="Advanced semantic matching using embeddings to find books with similar themes, writing styles, and emotional resonance.",
            status="In Development",
            estimated_completion="Next Sprint",
            preview_data={
                "similarity_threshold": 0.85,
                "embedding_dimensions": 1536,
                "indexed_books": 15000,
                "search_modes": ["semantic", "hybrid", "contextual"]
            }
        ) 