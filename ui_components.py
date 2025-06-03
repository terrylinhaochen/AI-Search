import streamlit as st
from models import ContentCard, BookRecommendation, PlaceholderFeature, UserIntentCategory

def render_suggestion_card():
    """Render the suggestion card showing query types"""
    
    st.markdown("""
    <div style="
        background: #f7f6f3;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #e9e9e7;
        margin: 20px 0;
        color: #2d2d2d;
    ">
        <h4 style="margin-top: 0; margin-bottom: 16px; color: #2d2d2d; font-weight: 600;">💡 What can you search for?</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; font-size: 0.9em;">
            <div style="background: white; padding: 12px; border-radius: 6px; border: 1px solid #e9e9e7;">
                <strong style="color: #2d2d2d;">🎯 Problem Solving</strong><br>
                <span style="color: #6b6b6b; font-size: 0.85em;">"How to deal with difficult colleagues"</span>
            </div>
            <div style="background: white; padding: 12px; border-radius: 6px; border: 1px solid #e9e9e7;">
                <strong style="color: #2d2d2d;">🔍 Exploration</strong><br>
                <span style="color: #6b6b6b; font-size: 0.85em;">"Mind-bending science podcasts"</span>
            </div>
            <div style="background: white; padding: 12px; border-radius: 6px; border: 1px solid #e9e9e7;">
                <strong style="color: #2d2d2d;">💭 Quotes & Concepts</strong><br>
                <span style="color: #6b6b6b; font-size: 0.85em;">"Content about 'flow state'"</span>
            </div>
            <div style="background: white; padding: 12px; border-radius: 6px; border: 1px solid #e9e9e7;">
                <strong style="color: #2d2d2d;">📖 Plot Memories</strong><br>
                <span style="color: #6b6b6b; font-size: 0.85em;">"Book with a girl counting prime numbers"</span>
            </div>
            <div style="background: white; padding: 12px; border-radius: 6px; border: 1px solid #e9e9e7;">
                <strong style="color: #2d2d2d;">👥 Characters & Scenes</strong><br>
                <span style="color: #6b6b6b; font-size: 0.85em;">"London autistic detective"</span>
            </div>
            <div style="background: white; padding: 12px; border-radius: 6px; border: 1px solid #e9e9e7;">
                <strong style="color: #2d2d2d;">❤️ Emotional Themes</strong><br>
                <span style="color: #6b6b6b; font-size: 0.85em;">"Content that will make me cry (in a good way)"</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_content_card(card: ContentCard, is_main: bool = False):
    """Render individual content card with three simple components: title, reason, book info"""
    
    # Card styling configuration for colors and icons
    card_styles = {
        "quote": {"icon": "💬", "color": "#2383e2"},
        "summary": {"icon": "📄", "color": "#10b981"},
        "recommendation": {"icon": "⭐", "color": "#8b5cf6"},
        "theme": {"icon": "🎭", "color": "#f59e0b"},
        "podcast": {"icon": "🎧", "color": "#e74c3c"},
        "error": {"icon": "⚠️", "color": "#ef4444"}
    }
    
    style = card_styles.get(card.type, card_styles["recommendation"])
    
    # 1. TITLE COMPONENT
    with st.container():
        st.markdown(f"## {style['icon']} {card.title}")
    
    # 2. RECOMMENDATION REASON COMPONENT  
    with st.container():
        st.markdown(f"**Why this content:** {card.description}")
    
    # 3. BOOK/CONTENT COMPONENT
    with st.container():
        if card.book_title:
            st.markdown(f"**📖 {card.book_title}**")
            if card.book_author:
                st.markdown(f"*by {card.book_author}*")
            if card.source_page:
                st.markdown(f"*{card.source_page}*")
        
        # Quote section (if applicable)
        if card.type == "quote" and card.quote:
            st.markdown(f"> *\"{card.quote}\"*")
    
    # Add some spacing
    st.markdown("---")

def render_book_recommendation(recommendation: BookRecommendation):
    """Render specific content recommendation"""
    
    # Determine confidence color based on relevance score
    if recommendation.relevance_score > 0.7:
        confidence_color = "#10b981"
    elif recommendation.relevance_score > 0.4:
        confidence_color = "#f59e0b"
    else:
        confidence_color = "#ef4444"
    
    # Build the recommendation HTML
    recommendation_html = f"""
    <div style="background: white; border: 1px solid #e9e9e7; border-left: 4px solid #2383e2; 
                padding: 24px; border-radius: 8px; margin: 20px 0;">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <span style="font-size: 1.5em; margin-right: 15px;">📚</span>
            <div>
                <h2 style="margin: 0; color: #2d2d2d; font-weight: 700; font-size: 1.4em;">
                    {recommendation.title}
                </h2>
                <h4 style="margin: 5px 0; color: #6b6b6b; font-weight: 500;">
                    by {recommendation.author}
                </h4>
            </div>
        </div>
        
        <div style="background: #f8f9fa; padding: 16px; border-radius: 6px; margin: 15px 0;">
            <h4 style="color: #2d2d2d; margin-top: 0; margin-bottom: 8px; font-weight: 600;">
                Why this content?
            </h4>
            <p style="line-height: 1.6; margin-bottom: 0; color: #6b6b6b; font-size: 0.9em;">
                {recommendation.reason}
            </p>
        </div>
        
        <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 20px;">
            <div style="background: {confidence_color}; color: white; padding: 6px 12px; 
                        border-radius: 20px; font-weight: 600; font-size: 0.8em;">
                Relevance: {recommendation.relevance_score:.0%}
            </div>
            <div style="background: #2383e2; color: white; padding: 8px 16px; border-radius: 6px; 
                        cursor: pointer; font-weight: 500; font-size: 0.85em;">
                View Details
            </div>
        </div>
    </div>
    """
    
    st.markdown(recommendation_html, unsafe_allow_html=True)

def render_placeholder_feature(feature: PlaceholderFeature):
    """Render work-in-progress placeholder feature"""
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        color: white;
        border: 2px dashed rgba(255, 255, 255, 0.3);
    ">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <span style="font-size: 1.8em; margin-right: 15px;">🚧</span>
            <div>
                <h3 style="margin: 0; color: white;">{feature.name}</h3>
                <span style="
                    background: rgba(255, 255, 255, 0.2);
                    padding: 4px 12px;
                    border-radius: 15px;
                    font-size: 0.9em;
                    margin-top: 5px;
                    display: inline-block;
                ">{feature.status}</span>
            </div>
        </div>
        
        <p style="opacity: 0.9; margin-bottom: 15px;">{feature.description}</p>
        
        <div style="
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        ">
            <h5 style="color: #e8f4f8; margin-top: 0;">Preview Data:</h5>
            <ul style="margin: 0; padding-left: 20px;">
    """, unsafe_allow_html=True)
    
    for key, value in feature.preview_data.items():
        st.markdown(f"<li><strong>{key.replace('_', ' ').title()}:</strong> {value}</li>", unsafe_allow_html=True)
    
    st.markdown(f"""
            </ul>
        </div>
        
        <div style="text-align: center; margin-top: 20px;">
            <span style="
                background: rgba(255, 255, 255, 0.2);
                padding: 8px 15px;
                border-radius: 20px;
                font-size: 0.9em;
            ">
                🕐 ETA: {feature.estimated_completion}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_analysis_debug(analysis):
    """Render query analysis for debugging (optional)"""
    
    with st.expander("🔍 Query Analysis (Debug)"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Query Type:**", analysis.query_type.value)
            st.write("**Confidence:**", f"{analysis.confidence_score:.0%}")
        
        with col2:
            if analysis.user_intent_category:
                st.write("**Intent Category:**", analysis.user_intent_category.value.replace('_', ' ').title())
            st.write("**Reasoning:**", analysis.reasoning) 