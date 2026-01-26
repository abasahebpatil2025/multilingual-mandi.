"""
Translation Service for Multilingual Mandi
Provides high-level translation management with caching and optimization
"""

from typing import List, Dict, Optional
import streamlit as st
from .gemini_client import GeminiClient
import sys
import os

# Add project root to path for config import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import ConfigManager

class TranslationService:
    """High-level translation service with session caching"""
    
    def __init__(self):
        self.config = ConfigManager()
        self.gemini_client = None
        self.supported_languages = ['marathi', 'hindi', 'english']
        self.language_codes = {
            'marathi': 'mr',
            'hindi': 'hi', 
            'english': 'en'
        }
        
        # Initialize session state for caching
        if 'translation_cache' not in st.session_state:
            st.session_state.translation_cache = {}
            
        # Initialize Gemini client if API key is available
        try:
            api_key = self.config.get_gemini_api_key()
            if api_key:
                self.gemini_client = GeminiClient(api_key)
        except Exception as e:
            st.warning(f"Translation service unavailable: {str(e)}")
    
    def translate(self, text: str, target_language: str) -> str:
        """
        Translate text to target language with caching
        
        Args:
            text: Text to translate
            target_language: Target language (marathi, hindi, english)
            
        Returns:
            Translated text or original text if translation fails
        """
        if not text or not text.strip():
            return text
            
        # Normalize language name
        target_language = target_language.lower()
        if target_language not in self.supported_languages:
            return text
            
        # Check cache first
        cache_key = f"{text}_{target_language}"
        if cache_key in st.session_state.translation_cache:
            return st.session_state.translation_cache[cache_key]
        
        # If no Gemini client, return original text
        if not self.gemini_client:
            return text
            
        try:
            # Detect source language (simplified)
            source_lang = self.detect_language(text)
            
            # Skip translation if already in target language
            if source_lang == target_language:
                return text
                
            # Translate using Gemini
            translated = self.gemini_client.translate_text(
                text, 
                source_lang, 
                target_language
            )
            
            # Cache the result
            st.session_state.translation_cache[cache_key] = translated
            return translated
            
        except Exception as e:
            st.error(f"Translation failed: {str(e)}")
            return text
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        return self.supported_languages.copy()
    
    def detect_language(self, text: str) -> str:
        """
        Simple language detection (can be enhanced)
        
        Args:
            text: Text to analyze
            
        Returns:
            Detected language code
        """
        # Simple heuristic - can be improved with actual detection
        # For now, assume English if contains mostly Latin characters
        if text and any(ord(char) < 128 for char in text if char.isalpha()):
            return 'english'
        return 'marathi'  # Default to Marathi
    
    def batch_translate(self, texts: List[str], target_language: str) -> List[str]:
        """
        Translate multiple texts efficiently
        
        Args:
            texts: List of texts to translate
            target_language: Target language
            
        Returns:
            List of translated texts
        """
        return [self.translate(text, target_language) for text in texts]
    
    def clear_cache(self):
        """Clear translation cache"""
        if 'translation_cache' in st.session_state:
            st.session_state.translation_cache.clear()