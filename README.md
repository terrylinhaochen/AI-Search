# 📚 AI Book Search Prototype

An intelligent book search system that understands your needs and provides personalized recommendations using GPT-4o.

## ✨ Features

### 🧠 Smart Query Analysis
- **Specific Book Detection**: Identifies when you're asking about a particular book
- **Intent Classification**: Categorizes general queries into 7 types:
  - 🎯 **Problem Solving**: "How to deal with difficult colleagues"
  - 🔍 **Exploration/Discovery**: "Mind-bending science books (not too technical)"
  - 💭 **Quote/Concept Memory**: "Books about 'flow state'"
  - 📖 **Plot Fragment Memory**: "Book with a girl counting prime numbers"
  - 👥 **Character/Scene Description**: "London autistic detective"
  - ❤️ **Emotional/Theme**: "Books that will make me cry (in a good way)"
  - 🔄 **Comparative Search**: "Like Harry Potter but for adults"

### 🎨 Dynamic UI Components
- **Responsive Cards**: Different designs for quotes, summaries, recommendations, and themes
- **Book Recommendations**: Rich cards with relevance scores and detailed reasoning
- **Quote Cards**: Special formatting with book attribution and page numbers
- **Placeholder Features**: Work-in-progress components with preview data

### 🤖 AI-Powered Responses
- Real GPT-4o integration for query analysis and content generation
- Structured JSON responses rendered into beautiful UI components
- Fallback handling for API errors
- Debug mode to understand query analysis

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd /path/to/your/ai_search
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key:**
   Edit the `.env` file and replace `your_openai_api_key_here` with your actual OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser:**
   The app will open at `http://localhost:8501`

## 🏗️ Architecture

### Core Components

- **`models.py`**: Pydantic models for structured data handling
- **`llm_service.py`**: OpenAI GPT-4o integration and query processing
- **`ui_components.py`**: Reusable Streamlit UI components
- **`app.py`**: Main Streamlit application

### Data Flow

1. **User Input** → Query entered in search box
2. **Query Analysis** → GPT-4o determines query type and intent
3. **Content Generation** → Based on analysis, generates appropriate responses
4. **UI Rendering** → Structured data rendered into appropriate card types

## 🎯 Example Queries

### Problem Solving
- "How to understand my teenage children"
- "Investment books without jargon"
- "Dealing with impostor syndrome"

### Exploration
- "Books that will change how I think about science"
- "Engaging books for long flights"
- "Books that will make me smarter"

### Quote/Concept Memory
- "Books about 'flow state'"
- "Where does 'all happy families' come from"
- "The marshmallow experiment book"

### Plot Fragment Memory
- "Book with a girl using prime numbers"
- "Story where everyone goes blind"
- "Book where death takes a vacation"

### Character/Scene Description
- "London autistic detective"
- "Assassin training school"
- "Novel about Japanese American internment camps"

### Emotional/Theme
- "Books that will make me cry (cathartic)"
- "Finding yourself after divorce"
- "Dark academia vibes"

### Comparative Search
- "Like Harry Potter but for adults"
- "Like Atomic Habits but more practical"
- "Malcolm Gladwell style but about technology"

## 🛠️ Technical Details

### Models and Types
- **QueryType**: SPECIFIC_BOOK | GENERAL
- **UserIntentCategory**: 7 predefined categories
- **ContentCard**: Flexible card system with type-specific rendering
- **BookRecommendation**: Rich recommendation with reasoning
- **PlaceholderFeature**: Work-in-progress features

### API Integration
- Uses OpenAI GPT-4o for all AI processing
- Structured JSON responses with Pydantic validation
- Error handling and fallback responses
- Temperature controls for different use cases

### UI Features
- Custom CSS styling with gradients and animations
- Responsive card layouts
- Debug mode for development
- Loading states and error handling

## 🔧 Customization

### Adding New Intent Categories
1. Update `UserIntentCategory` enum in `models.py`
2. Add category-specific prompts in `llm_service.py`
3. Update suggestion card in `ui_components.py`

### Creating New Card Types
1. Add new card type to `card_styles` in `ui_components.py`
2. Implement special rendering logic if needed
3. Update LLM prompts to generate the new type

### Styling Modifications
- Update CSS in `app.py` for global styles
- Modify individual component styles in `ui_components.py`
- Customize gradients and colors throughout

## 🚧 Roadmap

### Planned Features
- **Semantic Vector Search**: Advanced embedding-based search
- **User Preferences**: Learning from search history
- **Book Database Integration**: Real book data and availability
- **Social Features**: Sharing and collaborative recommendations
- **Mobile Optimization**: Progressive web app features

## 📝 Notes

- This is a prototype focused on the AI interaction layer
- No actual book database integration yet (uses AI-generated content)
- Designed for easy deployment on Streamlit Cloud
- Modular architecture for easy extension

## 🤝 Contributing

Feel free to extend this prototype! Key areas for improvement:
- Book database integration
- Advanced search algorithms
- User preference learning
- Performance optimization
- UI/UX enhancements

---

**Built with ❤️ using Streamlit and GPT-4o**
