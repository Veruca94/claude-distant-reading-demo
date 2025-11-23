"""
Wordcloud generation module.
Creates visual wordcloud images from word frequency data.
"""

from typing import Dict
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend


def generate_wordcloud(word_frequencies: Dict[str, int],
                       output_path: str,
                       width: int = 800,
                       height: int = 400,
                       background_color: str = 'white',
                       colormap: str = 'viridis') -> str:
    """
    Generate a wordcloud image from word frequencies.

    Args:
        word_frequencies: Dictionary mapping words to frequencies
        output_path: Path to save the wordcloud image
        width: Width of the image in pixels
        height: Height of the image in pixels
        background_color: Background color for the wordcloud
        colormap: Matplotlib colormap name

    Returns:
        Path to the saved wordcloud image
    """
    if not word_frequencies:
        # Create empty wordcloud if no data
        word_frequencies = {'no': 1, 'data': 1}

    # Create wordcloud object
    wc = WordCloud(
        width=width,
        height=height,
        background_color=background_color,
        colormap=colormap,
        max_words=200,
        relative_scaling=0.5,
        min_font_size=10
    )

    # Generate wordcloud from frequencies
    wc.generate_from_frequencies(word_frequencies)

    # Save to file
    plt.figure(figsize=(width/100, height/100), dpi=100)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig(output_path, format='png', bbox_inches='tight', dpi=100)
    plt.close()

    return output_path


def generate_play_wordcloud(play_name: str,
                           word_frequencies: Dict[str, int],
                           output_dir: str) -> str:
    """
    Generate a wordcloud for a Shakespeare play.

    Args:
        play_name: Name of the play (for filename)
        word_frequencies: Dictionary of word frequencies
        output_dir: Directory to save the wordcloud

    Returns:
        Path to the saved wordcloud image
    """
    # Create filename
    filename = f"{play_name.lower().replace(' ', '_')}_wordcloud.png"
    output_path = f"{output_dir}/{filename}"

    # Generate wordcloud with play-appropriate styling
    generate_wordcloud(
        word_frequencies,
        output_path,
        width=1200,
        height=600,
        background_color='white',
        colormap='RdPu'  # Purple/red colormap for Shakespeare
    )

    return output_path


if __name__ == "__main__":
    # Test the wordcloud generator
    test_frequencies = {
        'love': 50,
        'death': 30,
        'life': 25,
        'hate': 20,
        'fortune': 15,
        'time': 12,
        'fair': 10
    }

    import os
    os.makedirs('output/wordclouds', exist_ok=True)
    output = generate_play_wordcloud('Test Play', test_frequencies, 'output/wordclouds')
    print(f"Wordcloud saved to: {output}")
