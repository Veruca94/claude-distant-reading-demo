"""
Sentiment analysis module using VADER.
Analyzes overall sentiment and sentiment by structural divisions.
"""

from typing import List, Dict
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re


def get_vader_analyzer():
    """
    Get VADER sentiment analyzer instance.

    Returns:
        SentimentIntensityAnalyzer instance
    """
    return SentimentIntensityAnalyzer()


def analyze_text_sentiment(text: str) -> Dict[str, float]:
    """
    Analyze sentiment of a text.

    Args:
        text: Text to analyze

    Returns:
        Dictionary with sentiment scores (neg, neu, pos, compound)
    """
    analyzer = get_vader_analyzer()
    scores = analyzer.polarity_scores(text)
    return scores


def analyze_sentence_sentiments(sentences: List[str]) -> List[Dict[str, any]]:
    """
    Analyze sentiment for each sentence.

    Args:
        sentences: List of sentences

    Returns:
        List of dictionaries containing sentence and sentiment scores
    """
    analyzer = get_vader_analyzer()
    results = []

    for sentence in sentences:
        scores = analyzer.polarity_scores(sentence)
        results.append({
            'sentence': sentence[:100],  # Truncate for storage
            'scores': scores
        })

    return results


def extract_acts(text: str) -> List[str]:
    """
    Attempt to extract acts from Shakespeare play text.

    Args:
        text: Clean play text

    Returns:
        List of act texts (if acts can be identified)
    """
    # Look for ACT markers (e.g., "ACT I", "ACT II", etc.)
    act_pattern = r'ACT\s+[IVX]+'
    act_positions = [(m.start(), m.group()) for m in re.finditer(act_pattern, text, re.IGNORECASE)]

    if len(act_positions) < 2:
        # Can't reliably split into acts
        return [text]

    acts = []
    for i in range(len(act_positions)):
        start = act_positions[i][0]
        end = act_positions[i + 1][0] if i + 1 < len(act_positions) else len(text)
        act_text = text[start:end]
        acts.append(act_text)

    return acts


def analyze_by_structure(text: str) -> Dict[str, any]:
    """
    Analyze sentiment by structural divisions (acts).

    Args:
        text: Clean play text

    Returns:
        Dictionary with overall and act-level sentiment
    """
    analyzer = get_vader_analyzer()

    # Overall sentiment
    overall_scores = analyzer.polarity_scores(text)

    # Try to extract acts
    acts = extract_acts(text)

    # Analyze each act
    act_sentiments = []
    for i, act_text in enumerate(acts):
        act_scores = analyzer.polarity_scores(act_text)
        act_sentiments.append({
            'act_number': i + 1 if len(acts) > 1 else None,
            'scores': act_scores
        })

    return {
        'overall': overall_scores,
        'by_act': act_sentiments if len(acts) > 1 else None,
        'num_acts': len(acts) if len(acts) > 1 else None
    }


def compute_sentiment_summary(scores: Dict[str, float]) -> str:
    """
    Generate a human-readable sentiment summary.

    Args:
        scores: VADER sentiment scores

    Returns:
        Summary string (e.g., "Positive", "Negative", "Neutral")
    """
    compound = scores['compound']

    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"


def analyze_sentiment(text: str, sentences: List[str] = None) -> Dict[str, any]:
    """
    Complete sentiment analysis pipeline.

    Args:
        text: Clean play text
        sentences: Optional list of sentences for sentence-level analysis

    Returns:
        Dictionary containing all sentiment analysis results
    """
    # Structural analysis
    structural_analysis = analyze_by_structure(text)

    # Overall summary
    summary = compute_sentiment_summary(structural_analysis['overall'])

    # Sentence-level analysis (limit to first 100 for performance)
    sentence_sentiments = None
    if sentences:
        sentence_sentiments = analyze_sentence_sentiments(sentences[:100])

    return {
        'overall_scores': structural_analysis['overall'],
        'summary': summary,
        'by_act': structural_analysis['by_act'],
        'sentence_sentiments': sentence_sentiments
    }


if __name__ == "__main__":
    # Test the analyzer
    test_text = "I love this beautiful day! But I hate the rain."
    result = analyze_sentiment(test_text)
    print("Overall scores:", result['overall_scores'])
    print("Summary:", result['summary'])
