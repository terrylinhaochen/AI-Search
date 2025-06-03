import streamlit as st
import os
from llm_service import LLMService
from ui_components import (
    render_suggestion_card, 
    render_content_card, 
    render_book_recommendation,
    render_analysis_debug
)
from models import QueryType

# Page configuration
st.set_page_config(
    page_title="AI Search",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Notion-like minimalistic styling
st.markdown("""
<style>
    .main .block-container {
        max-width: 800px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    .main-header {
        text-align: center;
        background: #f7f6f3;
        padding: 24px;
        border-radius: 8px;
        border: 1px solid #e9e9e7;
        margin-bottom: 24px;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.2em;
        color: #2d2d2d;
        font-weight: 600;
    }
    
    .main-header p {
        margin: 8px 0 0 0;
        font-size: 1em;
        color: #6b6b6b;
    }
    
    .stTextInput input {
        border-radius: 6px;
        border: 1px solid #e9e9e7;
        padding: 12px 16px;
        font-size: 14px;
        height: 44px;
        background-color: white;
    }
    
    .stTextInput input:focus {
        border-color: #2383e2;
        box-shadow: 0 0 0 1px #2383e2;
    }
    
    .stButton button {
        background: #2383e2;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 16px;
        font-weight: 500;
        font-size: 14px;
        width: 100%;
        height: 44px;
        transition: background-color 0.2s;
    }
    
    .stButton button:hover {
        background: #1a73d1;
    }
    
    .results-section {
        margin-top: 32px;
    }
    
    /* Make overall content more compact */
    .element-container {
        margin-bottom: 0.75rem !important;
    }
    
    .stMarkdown {
        margin-bottom: 0.75rem !important;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        color: #8b8b8b;
        font-size: 14px;
        margin: 40px 0 20px 0;
        padding-top: 24px;
        border-top: 1px solid #e9e9e7;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        st.error("🔑 Please set your OpenAI API key in the .env file!")
        st.info("Edit the `.env` file and replace `your_openai_api_key_here` with your actual OpenAI API key.")
        st.stop()
    
    # Initialize LLM service
    if 'llm_service' not in st.session_state:
        st.session_state.llm_service = LLMService()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔍 AI Search</h1>
        <p>Discover content through intelligent understanding of your needs</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main search interface
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_query = st.text_input(
            "Search Query",
            placeholder="What content are you looking for? Books, podcasts, hosts... Try: 'How to deal with difficult colleagues'",
            key="search_input",
            label_visibility="collapsed"
        )
    
    with col2:
        search_clicked = st.button("Search", key="search_button")
    
    # Suggestion card (always visible when no results)
    if not user_query and 'search_results' not in st.session_state:
        render_suggestion_card()
    
    # Process search when button clicked or Enter pressed
    if (search_clicked or user_query) and user_query.strip():
        with st.spinner("Analyzing your query and finding relevant content..."):
            try:
                # Process the search query
                search_results = st.session_state.llm_service.process_search_query(user_query)
                st.session_state.search_results = search_results
                
                # Don't try to clear the input - this causes the error
                
            except Exception as e:
                st.error(f"❌ Search failed: {str(e)}")
                st.info("💡 Make sure your OpenAI API key is valid and you have sufficient credits.")
                return
    
    # Display results
    if 'search_results' in st.session_state:
        results = st.session_state.search_results
        
        st.markdown('<div class="results-section">', unsafe_allow_html=True)
        
        # Show analysis debug info (collapsible)
        render_analysis_debug(results.analysis)
        
        # Display results based on query type
        if results.analysis.query_type == QueryType.SPECIFIC_BOOK and results.book_recommendation:
            st.markdown("### 📖 Content Recommendation")
            render_book_recommendation(results.book_recommendation)
            
        elif results.content_cards:
            st.markdown("### 🎯 Relevant Content")
            
            # Display main card (first one) as large block
            if len(results.content_cards) > 0:
                render_content_card(results.content_cards[0], is_main=True)
            
            # Add expand button for additional results if there are more cards
            if len(results.content_cards) > 1:
                # Initialize expand state in session state if not exists
                if 'show_all_results' not in st.session_state:
                    st.session_state.show_all_results = False
                
                # Expand button
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button(
                        f"📚 Show {len(results.content_cards) - 1} more results" if not st.session_state.show_all_results else "📚 Show less",
                        key="expand_results",
                        type="secondary"
                    ):
                        st.session_state.show_all_results = not st.session_state.show_all_results
                        st.rerun()
                
                # Show additional cards if expanded
                if st.session_state.show_all_results:
                    st.markdown("---")
                    st.markdown("#### More Content")
                    
                    # Display remaining cards in full width with proper formatting
                    remaining_cards = results.content_cards[1:4]  # Show up to 3 more
                    for card in remaining_cards:
                        render_content_card(card, is_main=False)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Option to search again
        if st.button("🔄 New Search", key="new_search"):
            if 'search_results' in st.session_state:
                del st.session_state.search_results
            st.rerun()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p><strong>Tip:</strong> Try different types of queries to see how the AI adapts to your needs!</p>
        <p>Problem-solving • Exploration • Quotes • Plot memories • Characters • Emotions • Comparisons</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 