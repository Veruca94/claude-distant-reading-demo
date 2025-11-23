#!/usr/bin/env python3
"""
Main analysis orchestrator.
Runs complete distant reading analysis on all Shakespeare plays.
"""

import json
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from preprocess import preprocess_file
from bow_analyzer import analyze_bag_of_words, compute_tfidf
from sentiment_analyzer import analyze_sentiment
from style_analyzer import analyze_style
from wordcloud_generator import generate_play_wordcloud


# Play metadata
PLAYS = {
    'pg1513.txt': {
        'id': 'romeo_juliet',
        'title': 'Romeo and Juliet',
        'genre': 'Tragedy'
    },
    'pg1514.txt': {
        'id': 'midsummer',
        'title': "A Midsummer Night's Dream",
        'genre': 'Comedy'
    },
    'pg1519.txt': {
        'id': 'much_ado',
        'title': 'Much Ado about Nothing',
        'genre': 'Comedy'
    },
    'pg1524.txt': {
        'id': 'hamlet',
        'title': 'Hamlet',
        'genre': 'Tragedy'
    },
    'pg1533.txt': {
        'id': 'macbeth',
        'title': 'Macbeth',
        'genre': 'Tragedy'
    }
}


def analyze_play(filepath: str, play_info: dict, output_dir: str, wordcloud_dir: str) -> dict:
    """
    Run complete analysis on a single play.

    Args:
        filepath: Path to the play text file
        play_info: Dictionary with play metadata
        output_dir: Directory for JSON output
        wordcloud_dir: Directory for wordcloud images

    Returns:
        Dictionary containing all analysis results
    """
    print(f"Analyzing {play_info['title']}...")

    # Preprocess
    clean_text, all_tokens, filtered_tokens, sentences = preprocess_file(filepath)

    # Bag of words analysis
    print("  - Bag of words analysis...")
    bow_results = analyze_bag_of_words(filtered_tokens, top_n=100)

    # Sentiment analysis
    print("  - Sentiment analysis...")
    sentiment_results = analyze_sentiment(clean_text, sentences)

    # Style analysis
    print("  - Stylometric analysis...")
    style_results = analyze_style(clean_text, all_tokens, sentences)

    # Generate wordcloud
    print("  - Generating wordcloud...")
    wordcloud_path = generate_play_wordcloud(
        play_info['id'],
        bow_results['word_frequencies'],
        wordcloud_dir
    )

    # Compile results
    results = {
        'metadata': {
            'id': play_info['id'],
            'title': play_info['title'],
            'genre': play_info['genre'],
            'source_file': os.path.basename(filepath)
        },
        'statistics': {
            'total_words': len(all_tokens),
            'words_without_stopwords': len(filtered_tokens),
            'unique_words': len(set(all_tokens)),
            'sentences': len(sentences)
        },
        'bag_of_words': {
            'top_words': bow_results['top_words'][:50],  # Top 50 for JSON
            'vocabulary_stats': bow_results['vocabulary_stats']
        },
        'sentiment': sentiment_results,
        'style': style_results,
        'wordcloud': {
            'filename': os.path.basename(wordcloud_path),
            'path': f"output/wordclouds/{os.path.basename(wordcloud_path)}"
        }
    }

    # Save individual JSON
    output_file = f"{output_dir}/{play_info['id']}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print(f"  - Results saved to {output_file}")

    return results, bow_results['word_frequencies'], filtered_tokens


def compute_distinctive_words(all_plays_data: dict) -> dict:
    """
    Compute TF-IDF scores to find distinctive words for each play.

    Args:
        all_plays_data: Dictionary mapping play IDs to token lists

    Returns:
        Dictionary mapping play IDs to distinctive words
    """
    print("\nComputing distinctive words using TF-IDF...")
    tfidf_results = compute_tfidf(all_plays_data)
    return tfidf_results


def update_results_with_tfidf(output_dir: str, tfidf_results: dict):
    """
    Update individual JSON files with distinctive words.

    Args:
        output_dir: Directory containing JSON files
        tfidf_results: TF-IDF results from compute_distinctive_words
    """
    for play_id, distinctive_words in tfidf_results.items():
        json_file = f"{output_dir}/{play_id}.json"

        if os.path.exists(json_file):
            # Load existing data
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Add distinctive words
            data['bag_of_words']['distinctive_words'] = distinctive_words[:30]

            # Save updated data
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

            print(f"  - Updated {play_id}.json with distinctive words")


def main():
    """
    Main execution function.
    """
    # Setup directories
    base_dir = Path(__file__).parent.parent
    output_dir = base_dir / 'output' / 'data'
    wordcloud_dir = base_dir / 'output' / 'wordclouds'

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(wordcloud_dir, exist_ok=True)

    print("=== Shakespeare Distant Reading Analysis ===\n")

    # Analyze all plays
    all_tokens = {}
    for filename, play_info in PLAYS.items():
        filepath = base_dir / filename
        if filepath.exists():
            results, word_freq, tokens = analyze_play(
                str(filepath),
                play_info,
                str(output_dir),
                str(wordcloud_dir)
            )
            all_tokens[play_info['id']] = tokens
        else:
            print(f"Warning: {filename} not found, skipping...")

    # Compute distinctive words across corpus
    if all_tokens:
        tfidf_results = compute_distinctive_words(all_tokens)
        update_results_with_tfidf(str(output_dir), tfidf_results)

    print("\n=== Analysis Complete ===")
    print(f"JSON data saved to: {output_dir}")
    print(f"Wordclouds saved to: {wordcloud_dir}")
    print("\nYou can now open web/index.html to view the visualization.")


if __name__ == "__main__":
    main()
