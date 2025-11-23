"""
Stylometric analysis module.
Computes readability scores, lexical diversity, and other style metrics.
"""

from typing import List, Dict
import textstat
from collections import Counter


def compute_lexical_diversity(tokens: List[str]) -> float:
    """
    Compute type-token ratio (lexical diversity).

    Args:
        tokens: List of word tokens

    Returns:
        Type-token ratio (unique words / total words)
    """
    if len(tokens) == 0:
        return 0.0
    return len(set(tokens)) / len(tokens)


def compute_vocabulary_richness(tokens: List[str]) -> Dict[str, any]:
    """
    Compute vocabulary richness metrics.

    Args:
        tokens: List of word tokens

    Returns:
        Dictionary of vocabulary richness metrics
    """
    if len(tokens) == 0:
        return {
            'total_words': 0,
            'unique_words': 0,
            'hapax_legomena': 0,
            'hapax_percentage': 0.0
        }

    word_freq = Counter(tokens)
    hapax = sum(1 for count in word_freq.values() if count == 1)

    return {
        'total_words': len(tokens),
        'unique_words': len(set(tokens)),
        'hapax_legomena': hapax,
        'hapax_percentage': (hapax / len(set(tokens)) * 100) if len(set(tokens)) > 0 else 0.0
    }


def compute_readability_scores(text: str) -> Dict[str, float]:
    """
    Compute various readability scores.

    Args:
        text: Clean text

    Returns:
        Dictionary of readability scores
    """
    return {
        'flesch_reading_ease': textstat.flesch_reading_ease(text),
        'flesch_kincaid_grade': textstat.flesch_kincaid_grade(text),
        'gunning_fog': textstat.gunning_fog(text),
        'smog_index': textstat.smog_index(text),
        'automated_readability_index': textstat.automated_readability_index(text),
        'coleman_liau_index': textstat.coleman_liau_index(text),
        'dale_chall_readability': textstat.dale_chall_readability_score(text)
    }


def compute_average_word_length(tokens: List[str]) -> float:
    """
    Compute average word length.

    Args:
        tokens: List of word tokens

    Returns:
        Average word length in characters
    """
    if len(tokens) == 0:
        return 0.0
    return sum(len(word) for word in tokens) / len(tokens)


def compute_average_sentence_length(sentences: List[str]) -> Dict[str, float]:
    """
    Compute average sentence length metrics.

    Args:
        sentences: List of sentences

    Returns:
        Dictionary with sentence length statistics
    """
    if len(sentences) == 0:
        return {
            'avg_sentence_length_words': 0.0,
            'avg_sentence_length_chars': 0.0
        }

    word_counts = [len(sent.split()) for sent in sentences]
    char_counts = [len(sent) for sent in sentences]

    return {
        'avg_sentence_length_words': sum(word_counts) / len(sentences),
        'avg_sentence_length_chars': sum(char_counts) / len(sentences)
    }


def analyze_style(text: str, tokens: List[str], sentences: List[str]) -> Dict[str, any]:
    """
    Complete stylometric analysis pipeline.

    Args:
        text: Clean text
        tokens: List of word tokens
        sentences: List of sentences

    Returns:
        Dictionary containing all style metrics
    """
    lexical_diversity = compute_lexical_diversity(tokens)
    vocab_richness = compute_vocabulary_richness(tokens)
    readability = compute_readability_scores(text)
    avg_word_length = compute_average_word_length(tokens)
    sentence_stats = compute_average_sentence_length(sentences)

    return {
        'lexical_diversity': lexical_diversity,
        'vocabulary_richness': vocab_richness,
        'readability_scores': readability,
        'average_word_length': avg_word_length,
        'sentence_statistics': sentence_stats
    }


if __name__ == "__main__":
    # Test the analyzer
    test_text = "This is a test. This is another test sentence with more words."
    test_tokens = ['test', 'another', 'test', 'sentence', 'words']
    test_sentences = ["This is a test.", "This is another test sentence with more words."]

    result = analyze_style(test_text, test_tokens, test_sentences)
    print("Lexical diversity:", result['lexical_diversity'])
    print("Vocabulary richness:", result['vocabulary_richness'])
    print("Readability:", result['readability_scores'])
