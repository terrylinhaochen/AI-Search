from pydantic import BaseModel
from typing import List, Optional, Literal
from enum import Enum

class QueryType(str, Enum):
    SPECIFIC_BOOK = "specific_book"
    GENERAL = "general"

class UserIntentCategory(str, Enum):
    PROBLEM_SOLVING = "problem_solving"
    EXPLORATION_DISCOVERY = "exploration_discovery"
    QUOTE_CONCEPT_MEMORY = "quote_concept_memory"
    PLOT_FRAGMENT_MEMORY = "plot_fragment_memory"
    CHARACTER_SCENE_DESCRIPTION = "character_scene_description"
    EMOTIONAL_THEME = "emotional_theme"
    COMPARATIVE_SEARCH = "comparative_search"

class BookRecommendation(BaseModel):
    title: str
    author: str
    reason: str
    relevance_score: float

class ContentCard(BaseModel):
    type: str
    title: str
    description: str
    book_title: Optional[str] = None
    book_author: Optional[str] = None
    quote: Optional[str] = None
    source_page: Optional[str] = None
    clickable_link: Optional[str] = None

class QueryAnalysis(BaseModel):
    query_type: QueryType
    user_intent_category: Optional[UserIntentCategory] = None
    confidence_score: float
    reasoning: str

class SearchResponse(BaseModel):
    analysis: QueryAnalysis
    book_recommendation: Optional[BookRecommendation] = None
    content_cards: List[ContentCard] = []
    
class PlaceholderFeature(BaseModel):
    name: str
    description: str
    status: str
    estimated_completion: str
    preview_data: dict 