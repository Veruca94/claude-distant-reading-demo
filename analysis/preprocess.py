"""
Text preprocessing module for Shakespeare plays.
Strips Project Gutenberg headers/footers and prepares text for analysis.
"""

import re
from typing import List, Tuple
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

ENGLISH_STOPWORDS = set(stopwords.words('english'))


def strip_gutenberg_headers(text: str) -> str:
    """
    Remove Project Gutenberg headers and footers.

    Args:
        text: Raw text from Project Gutenberg file

    Returns:
        Clean text content without headers/footers
    """
    # Find start marker
    start_pattern = r'\*\*\* START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK[^\*]*\*\*\*'
    start_match = re.search(start_pattern, text, re.IGNORECASE)

    # Find end marker
    end_pattern = r'\*\*\* END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK[^\*]*\*\*\*'
    end_match = re.search(end_pattern, text, re.IGNORECASE)

    if start_match and end_match:
        return text[start_match.end():end_match.start()].strip()
    elif start_match:
        # If no end marker, take everything after start
        return text[start_match.end():].strip()
    else:
        # Fallback: return original text
        return text.strip()


def tokenize_text(text: str) -> List[str]:
    """
    Tokenize text into words, removing punctuation and converting to lowercase.

    Args:
        text: Clean text to tokenize

    Returns:
        List of lowercase word tokens
    """
    # Tokenize into words
    tokens = word_tokenize(text.lower())

    # Keep only alphabetic tokens (removes punctuation and numbers)
    words = [token for token in tokens if token.isalpha()]

    return words


def remove_stopwords(tokens: List[str]) -> List[str]:
    """
    Remove English stopwords from token list.

    Args:
        tokens: List of word tokens

    Returns:
        List of tokens with stopwords removed
    """
    return [word for word in tokens if word not in ENGLISH_STOPWORDS]


def get_sentences(text: str) -> List[str]:
    """
    Extract sentences from text.

    Args:
        text: Clean text

    Returns:
        List of sentences
    """
    return sent_tokenize(text)


def preprocess_file(filepath: str) -> Tuple[str, List[str], List[str], List[str]]:
    """
    Complete preprocessing pipeline for a text file.

    Args:
        filepath: Path to text file

    Returns:
        Tuple of (clean_text, all_tokens, tokens_without_stopwords, sentences)
    """
    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    # Strip headers
    clean_text = strip_gutenberg_headers(raw_text)

    # Get sentences
    sentences = get_sentences(clean_text)

    # Tokenize
    all_tokens = tokenize_text(clean_text)

    # Remove stopwords
    tokens_without_stopwords = remove_stopwords(all_tokens)

    return clean_text, all_tokens, tokens_without_stopwords, sentences


if __name__ == "__main__":
    # Test the preprocessing
    import sys
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        clean_text, all_tokens, filtered_tokens, sentences = preprocess_file(filepath)
        print(f"Total words: {len(all_tokens)}")
        print(f"Words (no stopwords): {len(filtered_tokens)}")
        print(f"Unique words: {len(set(all_tokens))}")
        print(f"Sentences: {len(sentences)}")
        print(f"\nFirst 50 words (no stopwords): {' '.join(filtered_tokens[:50])}")
