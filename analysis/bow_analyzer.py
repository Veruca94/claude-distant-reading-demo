"""
Bag-of-words analyzer for Shakespeare plays.
Computes word frequencies, TF-IDF scores, and distinctive vocabulary.
"""

from collections import Counter
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


def compute_word_frequencies(tokens: List[str]) -> Dict[str, int]:
    """
    Compute word frequency counts.

    Args:
        tokens: List of word tokens

    Returns:
        Dictionary mapping words to their frequencies
    """
    return dict(Counter(tokens))


def get_top_words(word_freq: Dict[str, int], n: int = 50) -> List[Tuple[str, int]]:
    """
    Get the top N most frequent words.

    Args:
        word_freq: Dictionary of word frequencies
        n: Number of top words to return

    Returns:
        List of (word, frequency) tuples, sorted by frequency descending
    """
    return sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:n]


def compute_tfidf(documents: Dict[str, List[str]]) -> Dict[str, List[Tuple[str, float]]]:
    """
    Compute TF-IDF scores across multiple documents to identify distinctive words.

    Args:
        documents: Dictionary mapping document names to token lists

    Returns:
        Dictionary mapping document names to lists of (word, tfidf_score) tuples
    """
    # Prepare documents as space-separated strings
    doc_names = list(documents.keys())
    doc_texts = [' '.join(documents[name]) for name in doc_names]

    # Compute TF-IDF
    vectorizer = TfidfVectorizer(max_features=100)
    tfidf_matrix = vectorizer.fit_transform(doc_texts)
    feature_names = vectorizer.get_feature_names_out()

    # Extract top TF-IDF words for each document
    results = {}
    for idx, doc_name in enumerate(doc_names):
        # Get TF-IDF scores for this document
        scores = tfidf_matrix[idx].toarray()[0]
        # Sort by score
        word_scores = [(feature_names[i], scores[i]) for i in range(len(scores)) if scores[i] > 0]
        word_scores.sort(key=lambda x: x[1], reverse=True)
        results[doc_name] = word_scores[:50]  # Top 50 distinctive words

    return results


def compute_vocabulary_stats(tokens: List[str]) -> Dict[str, any]:
    """
    Compute vocabulary statistics.

    Args:
        tokens: List of word tokens

    Returns:
        Dictionary of vocabulary statistics
    """
    total_words = len(tokens)
    unique_words = len(set(tokens))
    word_freq = Counter(tokens)

    # Hapax legomena (words appearing exactly once)
    hapax = sum(1 for count in word_freq.values() if count == 1)

    return {
        'total_words': total_words,
        'unique_words': unique_words,
        'hapax_legomena': hapax,
        'type_token_ratio': unique_words / total_words if total_words > 0 else 0
    }


def analyze_bag_of_words(tokens: List[str], top_n: int = 100) -> Dict[str, any]:
    """
    Complete bag-of-words analysis for a single document.

    Args:
        tokens: List of word tokens (stopwords removed)
        top_n: Number of top words to include

    Returns:
        Dictionary containing word frequencies and statistics
    """
    word_freq = compute_word_frequencies(tokens)
    top_words = get_top_words(word_freq, top_n)
    vocab_stats = compute_vocabulary_stats(tokens)

    return {
        'word_frequencies': word_freq,
        'top_words': top_words,
        'vocabulary_stats': vocab_stats
    }


if __name__ == "__main__":
    # Test the analyzer
    test_tokens = ['love', 'hate', 'love', 'death', 'life', 'love', 'death']
    result = analyze_bag_of_words(test_tokens)
    print("Word frequencies:", result['word_frequencies'])
    print("Top words:", result['top_words'])
    print("Vocabulary stats:", result['vocabulary_stats'])
