"""
The Multilingual Mandi - Main Streamlit Application
A linguistic bridge for local agricultural traders
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import streamlit as st
from datetime import datetime
import pandas as pd

# Import services
from services.translation_service import TranslationService
from services.market_service import MarketRateService
from config import ConfigManager

# Page configuration
st.set_page_config(
    page_title="The Multilingual Mandi",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize services
@st.cache_resource
def initialize_services():
    """Initialize all services"""
    translation_service = TranslationService()
    market_service = MarketRateService()
    config = ConfigManager()
    return translation_service, market_service, config

# Initialize session state
def initialize_session_state():
    """Initialize session state variables"""
    if 'language' not in st.session_state:
        st.session_state.language = 'marathi'  # Default language
    if 'user_role' not in st.session_state:
        st.session_state.user_role = 'buyer'
    if 'negotiation_history' not in st.session_state:
        st.session_state.negotiation_history = []

# Language translations for UI
UI_TRANSLATIONS = {
    'marathi': {
        'title': 'बहुभाषिक मंडी',
        'subtitle': 'स्थानिक व्यापाऱ्यांसाठी भाषिक सेतू',
        'market_rates': 'बाजार भाव',
        'negotiation': 'वाटाघाटी',
        'language_settings': 'भाषा सेटिंग्ज',
        'select_language': 'भाषा निवडा',
        'current_prices': 'सध्याचे भाव',
        'crop_name': 'पिकाचे नाव',
        'price': 'भाव',
        'unit': 'एकक',
        'market': 'मंडी',
        'trend': 'ट्रेंड',
        'last_updated': 'शेवटचे अपडेट',
        'buyer': 'खरेदीदार',
        'seller': 'विक्रेता',
        'select_role': 'तुमची भूमिका निवडा',
        'chat_placeholder': 'तुमचा संदेश येथे टाइप करा...',
        'send': 'पाठवा',
        'ai_assistant': 'AI सहाय्यक',
        'price_suggestion': 'भाव सुचवणे'
    },
    'hindi': {
        'title': 'बहुभाषी मंडी',
        'subtitle': 'स्थानीय व्यापारियों के लिए भाषाई सेतु',
        'market_rates': 'बाजार भाव',
        'negotiation': 'बातचीत',
        'language_settings': 'भाषा सेटिंग्स',
        'select_language': 'भाषा चुनें',
        'current_prices': 'वर्तमान भाव',
        'crop_name': 'फसल का नाम',
        'price': 'भाव',
        'unit': 'इकाई',
        'market': 'मंडी',
        'trend': 'रुझान',
        'last_updated': 'अंतिम अपडेट',
        'buyer': 'खरीदार',
        'seller': 'विक्रेता',
        'select_role': 'अपनी भूमिका चुनें',
        'chat_placeholder': 'यहाँ अपना संदेश टाइप करें...',
        'send': 'भेजें',
        'ai_assistant': 'AI सहायक',
        'price_suggestion': 'भाव सुझाव'
    },
    'english': {
        'title': 'The Multilingual Mandi',
        'subtitle': 'Linguistic bridge for local traders',
        'market_rates': 'Market Rates',
        'negotiation': 'Negotiation',
        'language_settings': 'Language Settings',
        'select_language': 'Select Language',
        'current_prices': 'Current Prices',
        'crop_name': 'Crop Name',
        'price': 'Price',
        'unit': 'Unit',
        'market': 'Market',
        'trend': 'Trend',
        'last_updated': 'Last Updated',
        'buyer': 'Buyer',
        'seller': 'Seller',
        'select_role': 'Select Your Role',
        'chat_placeholder': 'Type your message here...',
        'send': 'Send',
        'ai_assistant': 'AI Assistant',
        'price_suggestion': 'Price Suggestion'
    }
}

def get_text(key: str) -> str:
    """Get translated text for current language"""
    return UI_TRANSLATIONS.get(st.session_state.language, UI_TRANSLATIONS['english']).get(key, key)

def render_sidebar():
    """Render sidebar with navigation and language settings"""
    st.sidebar.title(get_text('title'))
    st.sidebar.markdown(f"*{get_text('subtitle')}*")
    
    # Language selector
    st.sidebar.subheader(get_text('language_settings'))
    languages = {
        'marathi': 'मराठी',
        'hindi': 'हिंदी', 
        'english': 'English'
    }
    
    selected_lang = st.sidebar.selectbox(
        get_text('select_language'),
        options=list(languages.keys()),
        format_func=lambda x: languages[x],
        index=list(languages.keys()).index(st.session_state.language)
    )
    
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.rerun()
    
    # Role selector
    st.sidebar.subheader(get_text('select_role'))
    roles = {
        'buyer': get_text('buyer'),
        'seller': get_text('seller')
    }
    
    selected_role = st.sidebar.selectbox(
        "",
        options=list(roles.keys()),
        format_func=lambda x: roles[x],
        index=list(roles.keys()).index(st.session_state.user_role)
    )
    
    if selected_role != st.session_state.user_role:
        st.session_state.user_role = selected_role
        st.rerun()
    
    # Navigation
    st.sidebar.markdown("---")
    return st.sidebar.radio(
        "Navigation",
        [get_text('market_rates'), get_text('negotiation')],
        label_visibility="collapsed"
    )

def render_market_rates_page(market_service):
    """Render market rates page"""
    st.header(get_text('market_rates'))
    st.subheader(get_text('current_prices'))
    
    # Get current rates
    rates = market_service.get_current_rates()
    
    # Create DataFrame for display
    data = []
    for crop in rates.values():
        trend_emoji = {"up": "📈", "down": "📉", "stable": "➡️"}
        data.append({
            get_text('crop_name'): crop.crop_name,
            get_text('price'): f"₹{crop.current_price:,.2f}",
            get_text('unit'): crop.unit,
            get_text('market'): crop.market_location,
            get_text('trend'): f"{trend_emoji.get(crop.trend, '➡️')} {crop.trend.title()}",
            get_text('last_updated'): crop.last_updated.strftime("%H:%M")
        })
    
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Trending crops section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📈 Rising Prices")
        rising = market_service.get_trending_crops("up")
        for crop in rising[:3]:
            st.write(f"**{crop.crop_name}**: ₹{crop.current_price:,.2f}")
    
    with col2:
        st.subheader("📉 Falling Prices") 
        falling = market_service.get_trending_crops("down")
        for crop in falling[:3]:
            st.write(f"**{crop.crop_name}**: ₹{crop.current_price:,.2f}")
    
    with col3:
        st.subheader("➡️ Stable Prices")
        stable = market_service.get_trending_crops("stable")
        for crop in stable[:3]:
            st.write(f"**{crop.crop_name}**: ₹{crop.current_price:,.2f}")

def render_negotiation_page(translation_service, market_service):
    """Render negotiation page"""
    st.header(get_text('negotiation'))
    
    # Crop selection for negotiation
    rates = market_service.get_current_rates()
    crop_options = {k: v.crop_name for k, v in rates.items()}
    
    selected_crop_key = st.selectbox(
        "Select Crop for Negotiation:",
        options=list(crop_options.keys()),
        format_func=lambda x: crop_options[x]
    )
    
    if selected_crop_key:
        selected_crop = rates[selected_crop_key]
        
        # Display crop info
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(f"Negotiating: {selected_crop.crop_name}")
            st.write(f"**Current Market Rate**: ₹{selected_crop.current_price:,.2f} per {selected_crop.unit}")
            st.write(f"**Market**: {selected_crop.market_location}")
            st.write(f"**Trend**: {selected_crop.trend.title()}")
        
        with col2:
            st.subheader(get_text('ai_assistant'))
            # AI price suggestion
            suggested_price = selected_crop.current_price
            if st.session_state.user_role == 'buyer':
                suggested_price *= 0.95  # 5% below market rate
                st.success(f"💡 **{get_text('price_suggestion')}**: ₹{suggested_price:,.2f}")
                st.write("*As a buyer, consider starting 5% below market rate*")
            else:
                suggested_price *= 1.05  # 5% above market rate  
                st.success(f"💡 **{get_text('price_suggestion')}**: ₹{suggested_price:,.2f}")
                st.write("*As a seller, consider starting 5% above market rate*")
        
        # Chat interface
        st.markdown("---")
        st.subheader("💬 Negotiation Chat")
        
        # Chat history
        chat_container = st.container()
        with chat_container:
            if st.session_state.negotiation_history:
                for i, message in enumerate(st.session_state.negotiation_history):
                    if message['role'] == st.session_state.user_role:
                        st.chat_message("user").write(message['content'])
                    else:
                        st.chat_message("assistant").write(message['content'])
        
        # Chat input
        user_input = st.chat_input(get_text('chat_placeholder'))
        
        if user_input:
            # Add user message
            st.session_state.negotiation_history.append({
                'role': st.session_state.user_role,
                'content': user_input,
                'timestamp': datetime.now()
            })
            
            # Simple AI response (mock)
            ai_responses = [
                f"I understand you're interested in {selected_crop.crop_name}. The current market rate is ₹{selected_crop.current_price:,.2f}.",
                f"Based on market trends, a fair price range would be ₹{selected_crop.current_price*0.95:,.2f} to ₹{selected_crop.current_price*1.05:,.2f}.",
                "Let me help you find a mutually beneficial price point.",
                f"Considering the {selected_crop.trend} trend, this seems like a good time to negotiate."
            ]
            
            import random
            ai_response = random.choice(ai_responses)
            
            # Translate AI response if needed
            if st.session_state.language != 'english':
                try:
                    ai_response = translation_service.translate(ai_response, st.session_state.language)
                except:
                    pass  # Keep original if translation fails
            
            st.session_state.negotiation_history.append({
                'role': 'ai_assistant',
                'content': ai_response,
                'timestamp': datetime.now()
            })
            
            st.rerun()

def main():
    """Main application function"""
    # Initialize
    initialize_session_state()
    
    try:
        translation_service, market_service, config = initialize_services()
    except Exception as e:
        st.error(f"Failed to initialize services: {str(e)}")
        st.info("The application will run with limited functionality.")
        # Create fallback services
        market_service = MarketRateService()
        translation_service = None
    
    # Render sidebar and get selected page
    selected_page = render_sidebar()
    
    # Main content area
    if selected_page == get_text('market_rates'):
        render_market_rates_page(market_service)
    elif selected_page == get_text('negotiation'):
        render_negotiation_page(translation_service, market_service)
    
    # Footer
    st.markdown("---")
    st.markdown(
        f"<div style='text-align: center; color: gray;'>"
        f"🌾 {get_text('title')} | Powered by Google Gemini AI | "
        f"Current Language: {st.session_state.language.title()}"
        f"</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()