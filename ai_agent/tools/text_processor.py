# tools/text_processor.py - Example of a custom text processing module

import re
from typing import Dict, List, Union


def summarize(text: str, max_length: int = 200) -> str:
    """
    Summarize a text to a specified maximum length.
    
    Args:
        text: The text to summarize
        max_length: Maximum length of the summary in characters
        
    Returns:
        A summarized version of the text
    """
    # In a real implementation, you would use an LLM or NLP library
    # This is a very basic implementation for demonstration
    if len(text) <= max_length:
        return text
    
    # Simple summarization: first sentence + truncate to max_length
    sentences = re.split(r'(?<=[.!?])\s+', text)
    if sentences:
        summary = sentences[0]
        if len(summary) > max_length:
            summary = summary[:max_length-3] + "..."
        return summary
    
    return text[:max_length-3] + "..."


def extract_entities(text: str) -> Dict[str, List[str]]:
    """
    Extract named entities from text.
    
    Args:
        text: The text to analyze
        
    Returns:
        Dictionary with entity types and lists of entities
    """
    # In a real implementation, you would use an NLP library like spaCy
    # This is a simple pattern matching for demonstration
    
    # Very basic patterns
    patterns = {
        "emails": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "urls": r'https?://[^\s]+',
        "dates": r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
        "numbers": r'\b\d+(?:\.\d+)?\b'
    }
    
    results = {}
    for entity_type, pattern in patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            results[entity_type] = matches
    
    return results


def sentiment_analysis(text: str) -> Dict[str, Union[str, float]]:
    """
    Analyze the sentiment of the text.
    
    Args:
        text: The text to analyze
        
    Returns:
        Dictionary with sentiment label and score
    """
    # In a real implementation, you would use an NLP library or API
    # This is a naive implementation for demonstration
    
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'best', 'love', 'happy']
    negative_words = ['bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'sad', 'disappointed']
    
    # Convert to lowercase for matching
    text_lower = text.lower()
    
    # Count positive and negative words
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    # Calculate sentiment score (-1 to 1)
    total = positive_count + negative_count
    if total == 0:
        score = 0.0
    else:
        score = (positive_count - negative_count) / total
    
    # Determine sentiment label
    if score > 0.3:
        label = "positive"
    elif score < -0.3:
        label = "negative"
    else:
        label = "neutral"
    
    return {
        "label": label,
        "score": score,
        "positive_count": positive_count,
        "negative_count": negative_count
    }


def translate(text: str, target_language: str = "es") -> str:
    """
    Translate text to the target language.
    
    Args:
        text: The text to translate
        target_language: Language code to translate to (default: Spanish)
        
    Returns:
        Translated text
    """
    # In a real implementation, you would use a translation API
    # This is a placeholder with some basic translations for demonstration
    
    translations = {
        "es": {
            "hello": "hola",
            "world": "mundo",
            "goodbye": "adiós",
            "thank you": "gracias",
            "yes": "sí",
            "no": "no"
        },
        "fr": {
            "hello": "bonjour",
            "world": "monde",
            "goodbye": "au revoir",
            "thank you": "merci",
            "yes": "oui",
            "no": "non"
        },
        "de": {
            "hello": "hallo",
            "world": "welt",
            "goodbye": "auf wiedersehen",
            "thank you": "danke",
            "yes": "ja",
            "no": "nein"
        }
    }
    
    if target_language not in translations:
        return f"Error: Unsupported target language '{target_language}'. Supported languages: {', '.join(translations.keys())}"
    
    # Very basic word-by-word replacement
    result = text.lower()
    for eng, translated in translations[target_language].items():
        result = re.sub(r'\b' + re.escape(eng) + r'\b', translated, result)
    
    return result + f" [Note: This is a simplified translation to {target_language}]"


# Example of how to integrate this module in main.py:
"""
from tools import web_search, calculator, file_operations, text_processor

def main():
    # Initialize agent with available tools
    agent = Agent(
        tools={
            "web_search": web_search.search,
            "calculator": calculator.calculate,
            "read_file": file_operations.read_file,
            "write_file": file_operations.write_file,
            "summarize_text": text_processor.summarize,
            "extract_entities": text_processor.extract_entities,
            "analyze_sentiment": text_processor.sentiment_analysis,
            "translate_text": text_processor.translate
        }
    )
"""