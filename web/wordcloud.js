// Dynamic Wordcloud Generator using Canvas
// A simple canvas-based word cloud implementation

class WordCloudGenerator {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.words = [];
        this.placements = [];
    }

    // Generate word cloud from frequency data
    generate(wordFrequencies, options = {}) {
        const {
            maxWords = 100,
            minFontSize = 12,
            maxFontSize = 60,
            fontFamily = 'Arial',
            colors = ['#764ba2', '#667eea', '#ff6b6b', '#51cf66', '#ffd43b']
        } = options;

        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.placements = [];

        // Convert to array and sort by frequency
        const wordArray = Object.entries(wordFrequencies)
            .sort((a, b) => b[1] - a[1])
            .slice(0, maxWords);

        if (wordArray.length === 0) return;

        // Calculate font sizes
        const maxFreq = wordArray[0][1];
        const minFreq = wordArray[wordArray.length - 1][1];

        this.words = wordArray.map(([word, freq]) => {
            // Scale font size based on frequency
            const normalizedFreq = (freq - minFreq) / (maxFreq - minFreq);
            const fontSize = minFontSize + (normalizedFreq * (maxFontSize - minFontSize));

            return {
                text: word,
                size: fontSize,
                color: colors[Math.floor(Math.random() * colors.length)],
                frequency: freq
            };
        });

        // Place words on canvas
        this.placeWords(fontFamily);
    }

    // Place words on canvas using spiral placement
    placeWords(fontFamily) {
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;

        this.words.forEach((word, index) => {
            this.ctx.font = `${word.size}px ${fontFamily}`;
            this.ctx.fillStyle = word.color;

            const metrics = this.ctx.measureText(word.text);
            const wordWidth = metrics.width;
            const wordHeight = word.size;

            // Try to place word using spiral pattern
            let placed = false;
            let angle = 0;
            let radius = 0;
            const spiralStep = 2;
            const angleStep = 0.1;

            // Start from center and spiral outward
            for (let attempt = 0; attempt < 1000 && !placed; attempt++) {
                const x = centerX + radius * Math.cos(angle) - wordWidth / 2;
                const y = centerY + radius * Math.sin(angle) + wordHeight / 2;

                if (this.canPlaceWord(x, y, wordWidth, wordHeight)) {
                    // Draw the word
                    this.ctx.fillText(word.text, x, y);

                    // Store placement
                    this.placements.push({
                        x, y,
                        width: wordWidth,
                        height: wordHeight
                    });

                    placed = true;
                } else {
                    // Move along spiral
                    angle += angleStep;
                    radius += spiralStep * angleStep / (2 * Math.PI);
                }
            }

            // If we couldn't place the word, skip it
            if (!placed) {
                console.log(`Could not place word: ${word.text}`);
            }
        });
    }

    // Check if a word can be placed at given position
    canPlaceWord(x, y, width, height) {
        // Check canvas bounds
        if (x < 0 || y < height || x + width > this.canvas.width || y > this.canvas.height) {
            return false;
        }

        // Check collision with existing words
        for (const placement of this.placements) {
            if (this.rectsOverlap(
                x, y - height, width, height,
                placement.x, placement.y - placement.height, placement.width, placement.height
            )) {
                return false;
            }
        }

        return true;
    }

    // Check if two rectangles overlap
    rectsOverlap(x1, y1, w1, h1, x2, y2, w2, h2) {
        const padding = 5; // Add some padding between words
        return !(
            x1 + w1 + padding < x2 ||
            x2 + w2 + padding < x1 ||
            y1 + h1 + padding < y2 ||
            y2 + h2 + padding < y1
        );
    }
}

// Global word cloud generator instance
let wordCloudGenerator = null;

// Initialize word cloud generator
document.addEventListener('DOMContentLoaded', () => {
    wordCloudGenerator = new WordCloudGenerator('dynamic-wordcloud');
});

// Override the generateDynamicWordcloud function from app.js
window.generateDynamicWordcloud = function(play) {
    if (!wordCloudGenerator) {
        wordCloudGenerator = new WordCloudGenerator('dynamic-wordcloud');
    }

    // Convert top words to frequency object
    const frequencies = {};
    play.bag_of_words.top_words.forEach(([word, freq]) => {
        frequencies[word] = freq;
    });

    // Get max words from slider
    const maxWords = parseInt(document.getElementById('wc-max-words').value) || 100;

    // Generate word cloud
    wordCloudGenerator.generate(frequencies, {
        maxWords: maxWords,
        minFontSize: 14,
        maxFontSize: 50,
        fontFamily: 'Georgia, serif',
        colors: ['#764ba2', '#667eea', '#9775fa', '#b197fc', '#da77f2']
    });
};

// Export for use in app.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WordCloudGenerator;
}
