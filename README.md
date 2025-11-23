# Shakespeare Distant Reading Analysis

A computational literary analysis project demonstrating "distant reading" techniques on five Shakespeare plays. This project combines Python-based text analysis with an interactive web visualization interface.

## Overview

This project performs distant reading analysis on five Shakespeare plays from Project Gutenberg:
- Romeo and Juliet (Tragedy)
- Hamlet (Tragedy)
- Macbeth (Tragedy)
- A Midsummer Night's Dream (Comedy)
- Much Ado about Nothing (Comedy)

## Features

### Python Analysis Pipeline
- **Text Preprocessing**: Strips Project Gutenberg headers and tokenizes text
- **Bag of Words Analysis**: Word frequency distributions and TF-IDF scores for distinctive words
- **Sentiment Analysis**: VADER sentiment scoring at play and act levels
- **Stylometric Analysis**: Lexical diversity, readability scores, vocabulary richness
- **Word Cloud Generation**: Visual representations of word frequencies

### Interactive Web Interface
- **Single Play View**: Detailed analysis for individual plays
- **Comparative Analysis**: Side-by-side comparison of multiple plays
- **Visualizations**: Word clouds, sentiment charts, style metrics
- **Dynamic Features**: Interactive word cloud regeneration with customizable parameters

## Installation

### Requirements
- Python 3.8 or higher
- Web browser with JavaScript support

### Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the analysis pipeline:
```bash
python3 analysis/analyze_all.py
```

This will:
- Process all five Shakespeare plays
- Generate JSON data files in `output/data/`
- Create word cloud images in `output/wordclouds/`

## Usage

### Running the Analysis
```bash
# Run complete analysis on all plays
python3 analysis/analyze_all.py
```

### Viewing the Web Interface

Option 1 - Simple HTTP Server (Python):
```bash
cd web
python3 -m http.server 8000
```
Then open http://localhost:8000 in your browser.

Option 2 - Direct File Access:
Open `web/index.html` directly in your browser (may have CORS restrictions with some browsers).

### Using the Web Interface

1. **Select Plays**: Click checkboxes in the sidebar to select plays
2. **Single View**: Analyze one play in depth with tabs for:
   - Overview (statistics, top words, distinctive words)
   - Word Cloud (static and dynamic generation)
   - Sentiment (scores, act-level analysis)
   - Style (readability, vocabulary, metrics)
3. **Compare View**: Select 2+ plays to compare:
   - Sentiment comparison
   - Stylometric comparison table
   - Vocabulary overlap analysis
   - Side-by-side word clouds
   - Top words comparison

## Project Structure

```
.
├── analysis/                  # Python analysis modules
│   ├── preprocess.py         # Text preprocessing
│   ├── bow_analyzer.py       # Bag of words analysis
│   ├── sentiment_analyzer.py # Sentiment analysis
│   ├── style_analyzer.py     # Stylometric analysis
│   ├── wordcloud_generator.py# Word cloud generation
│   └── analyze_all.py        # Main orchestrator
├── output/                    # Generated analysis output
│   ├── data/                 # JSON analysis results
│   └── wordclouds/           # Word cloud images
├── web/                       # Web interface
│   ├── index.html            # Main HTML
│   ├── styles.css            # Styling
│   ├── app.js                # Application logic
│   └── wordcloud.js          # Dynamic word cloud
├── pg*.txt                    # Source Shakespeare texts
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Analysis Methods

### Bag of Words
- Computes word frequencies (stopwords removed)
- Uses TF-IDF to identify distinctive vocabulary
- Tracks top 100 most common words per play

### Sentiment Analysis
- VADER (Valence Aware Dictionary and sEntiment Reasoner)
- Provides positive, negative, neutral, and compound scores
- Analyzes sentiment at play and act levels

### Stylometric Features
- **Lexical Diversity**: Type-token ratio
- **Vocabulary Richness**: Hapax legomena (words used once)
- **Readability**: Flesch Reading Ease, Flesch-Kincaid Grade, Gunning Fog, etc.
- **Style Metrics**: Average word/sentence length

## Technologies Used

- **Python**: NLTK, scikit-learn, VADER, textstat, wordcloud, matplotlib
- **Web**: HTML5, CSS3, JavaScript (vanilla)
- **Data Format**: JSON for analysis results

## License

Shakespeare texts are from Project Gutenberg and are in the public domain.

## Acknowledgments

- Project Gutenberg for providing the Shakespeare texts
- NLTK and scikit-learn for NLP tools
- VADER sentiment analysis tool
