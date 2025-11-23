// Shakespeare Distant Reading Application

// Global state
const state = {
    plays: {},
    selectedPlays: new Set(),
    currentView: 'single',
    currentPlayId: null
};

// Initialize the application
document.addEventListener('DOMContentLoaded', async () => {
    await loadAllPlays();
    setupEventListeners();
});

// Load all play data from JSON files
async function loadAllPlays() {
    const playIds = ['romeo_juliet', 'hamlet', 'macbeth', 'midsummer', 'much_ado'];

    for (const playId of playIds) {
        try {
            const response = await fetch(`../output/data/${playId}.json`);
            if (response.ok) {
                state.plays[playId] = await response.json();
            } else {
                console.error(`Failed to load ${playId}.json`);
            }
        } catch (error) {
            console.error(`Error loading ${playId}:`, error);
        }
    }
}

// Setup event listeners
function setupEventListeners() {
    // Play selection checkboxes
    document.querySelectorAll('.play-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', handlePlaySelection);
    });

    // View toggle buttons
    document.getElementById('btn-single-view').addEventListener('click', () => switchView('single'));
    document.getElementById('btn-compare-view').addEventListener('click', () => switchView('compare'));

    // Tab navigation
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const tabName = e.target.dataset.tab;
            switchTab(tabName);
        });
    });

    // Wordcloud regeneration
    const regenerateBtn = document.getElementById('btn-regenerate-wordcloud');
    if (regenerateBtn) {
        regenerateBtn.addEventListener('click', regenerateWordcloud);
    }

    // Wordcloud max words slider
    const maxWordsSlider = document.getElementById('wc-max-words');
    if (maxWordsSlider) {
        maxWordsSlider.addEventListener('input', (e) => {
            document.getElementById('wc-max-words-value').textContent = e.target.value;
        });
    }
}

// Handle play selection
function handlePlaySelection(e) {
    const playId = e.target.id.replace('play-', '');

    if (e.target.checked) {
        state.selectedPlays.add(playId);
    } else {
        state.selectedPlays.delete(playId);
    }

    updateView();
}

// Update the view based on selection
function updateView() {
    if (state.currentView === 'single') {
        if (state.selectedPlays.size === 1) {
            const playId = Array.from(state.selectedPlays)[0];
            displaySinglePlay(playId);
        } else if (state.selectedPlays.size > 1) {
            // Auto-switch to compare view
            switchView('compare');
        } else {
            showWelcomeMessage();
        }
    } else if (state.currentView === 'compare') {
        if (state.selectedPlays.size >= 2) {
            displayComparison();
        } else {
            showComparePlaceholder();
        }
    }
}

// Switch between views
function switchView(view) {
    state.currentView = view;

    // Update button states
    document.getElementById('btn-single-view').classList.toggle('active', view === 'single');
    document.getElementById('btn-compare-view').classList.toggle('active', view === 'compare');

    // Update view containers
    document.getElementById('single-view').classList.toggle('active', view === 'single');
    document.getElementById('compare-view').classList.toggle('active', view === 'compare');

    updateView();
}

// Show welcome message
function showWelcomeMessage() {
    document.querySelector('.welcome-message').style.display = 'block';
    document.getElementById('play-detail').style.display = 'none';
}

// Display a single play
function displaySinglePlay(playId) {
    const play = state.plays[playId];
    if (!play) return;

    state.currentPlayId = playId;

    // Hide welcome, show play detail
    document.querySelector('.welcome-message').style.display = 'none';
    document.getElementById('play-detail').style.display = 'block';

    // Update metadata
    document.getElementById('play-title').textContent = play.metadata.title;
    document.getElementById('play-genre').textContent = play.metadata.genre;
    document.getElementById('play-genre').className = `genre ${play.metadata.genre.toLowerCase()}`;
    document.getElementById('play-stats').textContent =
        `${play.statistics.total_words.toLocaleString()} words, ${play.statistics.sentences.toLocaleString()} sentences`;

    // Update overview tab
    updateOverviewTab(play);

    // Update wordcloud tab
    updateWordcloudTab(play);

    // Update sentiment tab
    updateSentimentTab(play);

    // Update style tab
    updateStyleTab(play);
}

// Update overview tab
function updateOverviewTab(play) {
    document.getElementById('stat-total-words').textContent = play.statistics.total_words.toLocaleString();
    document.getElementById('stat-unique-words').textContent = play.statistics.unique_words.toLocaleString();
    document.getElementById('stat-lexical-diversity').textContent =
        (play.style.lexical_diversity * 100).toFixed(2) + '%';
    document.getElementById('stat-sentiment').textContent = play.sentiment.summary;

    // Top words chart
    renderTopWordsChart(play.bag_of_words.top_words.slice(0, 20));

    // Distinctive words
    renderDistinctiveWords(play.bag_of_words.distinctive_words || []);
}

// Render top words chart
function renderTopWordsChart(topWords) {
    const container = document.getElementById('top-words-chart');
    container.innerHTML = '<div class="bar-chart"></div>';
    const chart = container.querySelector('.bar-chart');

    const maxCount = topWords[0][1];

    topWords.forEach(([word, count]) => {
        const percentage = (count / maxCount) * 100;
        const item = document.createElement('div');
        item.className = 'bar-chart-item';
        item.innerHTML = `
            <div class="bar-chart-label">${word}</div>
            <div class="bar-chart-bar" style="width: ${percentage}%">
                <span class="bar-chart-value">${count}</span>
            </div>
        `;
        chart.appendChild(item);
    });
}

// Render distinctive words
function renderDistinctiveWords(distinctiveWords) {
    const container = document.getElementById('distinctive-words');
    container.innerHTML = '';

    distinctiveWords.slice(0, 30).forEach(([word, score]) => {
        const tag = document.createElement('span');
        tag.className = 'word-tag';
        tag.textContent = word;
        tag.title = `TF-IDF Score: ${score.toFixed(4)}`;
        container.appendChild(tag);
    });
}

// Update wordcloud tab
function updateWordcloudTab(play) {
    const imgPath = `../${play.wordcloud.path}`;
    document.getElementById('wordcloud-image').src = imgPath;
    document.getElementById('wordcloud-image').alt = `${play.metadata.title} Word Cloud`;

    // Generate dynamic wordcloud
    generateDynamicWordcloud(play);
}

// Generate dynamic wordcloud (placeholder until wordcloud.js is loaded)
function generateDynamicWordcloud(play) {
    // This will be enhanced by wordcloud.js
    const canvas = document.getElementById('dynamic-wordcloud');
    const ctx = canvas.getContext('2d');

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Simple placeholder - will be replaced by proper wordcloud
    ctx.fillStyle = '#764ba2';
    ctx.font = '20px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('Dynamic word cloud will render here', canvas.width / 2, canvas.height / 2);
}

// Regenerate wordcloud
function regenerateWordcloud() {
    if (state.currentPlayId) {
        const play = state.plays[state.currentPlayId];
        generateDynamicWordcloud(play);
    }
}

// Update sentiment tab
function updateSentimentTab(play) {
    const scores = play.sentiment.overall_scores;

    // Sentiment bars
    const barsContainer = document.getElementById('sentiment-bars');
    barsContainer.innerHTML = '';

    const sentiments = [
        { label: 'Positive', value: scores.pos, class: 'positive' },
        { label: 'Neutral', value: scores.neu, class: 'neutral' },
        { label: 'Negative', value: scores.neg, class: 'negative' }
    ];

    sentiments.forEach(sentiment => {
        const barDiv = document.createElement('div');
        barDiv.className = 'sentiment-bar';
        barDiv.innerHTML = `
            <span class="sentiment-label">${sentiment.label}</span>
            <div class="bar-container">
                <div class="bar-fill ${sentiment.class}" style="width: ${sentiment.value * 100}%"></div>
            </div>
            <span class="bar-value">${(sentiment.value * 100).toFixed(1)}%</span>
        `;
        barsContainer.appendChild(barDiv);
    });

    // Sentiment summary
    document.getElementById('sentiment-summary-text').textContent =
        `This play has an overall ${play.sentiment.summary.toLowerCase()} sentiment.`;

    const compoundScore = document.getElementById('compound-score');
    compoundScore.textContent = `Compound Score: ${scores.compound.toFixed(3)}`;
    compoundScore.style.color = scores.compound >= 0.05 ? '#51cf66' :
                                 scores.compound <= -0.05 ? '#ff6b6b' : '#ffd43b';

    // Act sentiment (if available)
    if (play.sentiment.by_act) {
        renderActSentiment(play.sentiment.by_act);
    } else {
        document.getElementById('act-sentiment-section').style.display = 'none';
    }
}

// Render act sentiment
function renderActSentiment(actData) {
    const section = document.getElementById('act-sentiment-section');
    section.style.display = 'block';

    const container = document.getElementById('act-sentiment-chart');
    container.innerHTML = '<div class="bar-chart"></div>';
    const chart = container.querySelector('.bar-chart');

    actData.forEach(act => {
        const compound = act.scores.compound;
        const actLabel = act.act_number ? `Act ${act.act_number}` : 'Full Text';

        const item = document.createElement('div');
        item.className = 'bar-chart-item';
        item.innerHTML = `
            <div class="bar-chart-label">${actLabel}</div>
            <div class="bar-container">
                <div class="bar-fill ${compound >= 0.05 ? 'positive' : compound <= -0.05 ? 'negative' : 'neutral'}"
                     style="width: ${Math.abs(compound) * 100}%"></div>
            </div>
            <span class="bar-value">${compound.toFixed(3)}</span>
        `;
        chart.appendChild(item);
    });
}

// Update style tab
function updateStyleTab(play) {
    // Readability scores
    renderMetricGrid('readability-scores', play.style.readability_scores);

    // Vocabulary richness
    renderMetricGrid('vocabulary-richness', play.style.vocabulary_richness);

    // Style metrics
    const styleMetrics = {
        'Lexical Diversity': (play.style.lexical_diversity * 100).toFixed(2) + '%',
        'Average Word Length': play.style.average_word_length.toFixed(2) + ' chars',
        'Avg Sentence Length (words)': play.style.sentence_statistics.avg_sentence_length_words.toFixed(1),
        'Avg Sentence Length (chars)': play.style.sentence_statistics.avg_sentence_length_chars.toFixed(1)
    };
    renderMetricGrid('style-metrics', styleMetrics);
}

// Render metric grid
function renderMetricGrid(containerId, metrics) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';

    for (const [key, value] of Object.entries(metrics)) {
        const item = document.createElement('div');
        item.className = 'metric-item';

        const displayName = key.replace(/_/g, ' ')
            .replace(/\b\w/g, l => l.toUpperCase());

        const displayValue = typeof value === 'number' ? value.toFixed(2) : value;

        item.innerHTML = `
            <div class="metric-name">${displayName}</div>
            <div class="metric-value">${displayValue}</div>
        `;
        container.appendChild(item);
    }
}

// Switch tabs
function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabName);
    });

    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.toggle('active', content.id === `tab-${tabName}`);
    });
}

// Show compare placeholder
function showComparePlaceholder() {
    document.querySelector('.compare-placeholder').style.display = 'block';
    document.getElementById('comparison-results').style.display = 'none';
}

// Display comparison
function displayComparison() {
    document.querySelector('.compare-placeholder').style.display = 'none';
    document.getElementById('comparison-results').style.display = 'block';

    const selectedPlayIds = Array.from(state.selectedPlays);
    document.getElementById('compare-play-count').textContent = selectedPlayIds.length;

    // Sentiment comparison
    renderSentimentComparison(selectedPlayIds);

    // Style comparison table
    renderStyleComparisonTable(selectedPlayIds);

    // Vocabulary overlap
    renderVocabularyOverlap(selectedPlayIds);

    // Wordclouds comparison
    renderWordcloudsComparison(selectedPlayIds);

    // Top words comparison
    renderTopWordsComparison(selectedPlayIds);
}

// Render sentiment comparison
function renderSentimentComparison(playIds) {
    const container = document.getElementById('compare-sentiment-chart');
    container.innerHTML = '<div class="bar-chart"></div>';
    const chart = container.querySelector('.bar-chart');

    playIds.forEach(playId => {
        const play = state.plays[playId];
        const compound = play.sentiment.overall_scores.compound;

        const item = document.createElement('div');
        item.className = 'bar-chart-item';
        item.innerHTML = `
            <div class="bar-chart-label">${play.metadata.title}</div>
            <div class="bar-container">
                <div class="bar-fill ${compound >= 0.05 ? 'positive' : compound <= -0.05 ? 'negative' : 'neutral'}"
                     style="width: ${Math.abs(compound) * 100}%"></div>
            </div>
            <span class="bar-value">${compound.toFixed(3)}</span>
        `;
        chart.appendChild(item);
    });
}

// Render style comparison table
function renderStyleComparisonTable(playIds) {
    const container = document.getElementById('compare-style-table');

    const table = document.createElement('table');
    table.innerHTML = `
        <thead>
            <tr>
                <th>Play</th>
                <th>Total Words</th>
                <th>Unique Words</th>
                <th>Lexical Diversity</th>
                <th>Flesch Reading Ease</th>
                <th>Avg Word Length</th>
            </tr>
        </thead>
        <tbody></tbody>
    `;

    const tbody = table.querySelector('tbody');

    playIds.forEach(playId => {
        const play = state.plays[playId];
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${play.metadata.title}</strong></td>
            <td>${play.statistics.total_words.toLocaleString()}</td>
            <td>${play.statistics.unique_words.toLocaleString()}</td>
            <td>${(play.style.lexical_diversity * 100).toFixed(2)}%</td>
            <td>${play.style.readability_scores.flesch_reading_ease.toFixed(2)}</td>
            <td>${play.style.average_word_length.toFixed(2)}</td>
        `;
        tbody.appendChild(row);
    });

    container.innerHTML = '';
    container.appendChild(table);
}

// Render vocabulary overlap
function renderVocabularyOverlap(playIds) {
    const container = document.getElementById('vocab-overlap');

    if (playIds.length !== 2) {
        container.innerHTML = '<p>Select exactly 2 plays to see vocabulary overlap.</p>';
        return;
    }

    const play1 = state.plays[playIds[0]];
    const play2 = state.plays[playIds[1]];

    const words1 = new Set(play1.bag_of_words.top_words.map(([word]) => word));
    const words2 = new Set(play2.bag_of_words.top_words.map(([word]) => word));

    const overlap = new Set([...words1].filter(word => words2.has(word)));
    const unique1 = new Set([...words1].filter(word => !words2.has(word)));
    const unique2 = new Set([...words2].filter(word => !words1.has(word)));

    container.innerHTML = `
        <div class="vocab-stats">
            <h4>Vocabulary Overlap Analysis (Top 100 Words)</h4>
            <p><strong>Common words:</strong> ${overlap.size}</p>
            <p><strong>Unique to ${play1.metadata.title}:</strong> ${unique1.size}</p>
            <p><strong>Unique to ${play2.metadata.title}:</strong> ${unique2.size}</p>
            <div class="word-tags" style="margin-top: 15px;">
                <strong>Shared words:</strong> ${Array.from(overlap).slice(0, 20).map(word =>
                    `<span class="word-tag">${word}</span>`).join('')}
            </div>
        </div>
    `;
}

// Render wordclouds comparison
function renderWordcloudsComparison(playIds) {
    const container = document.getElementById('compare-wordclouds');
    container.innerHTML = '';

    playIds.forEach(playId => {
        const play = state.plays[playId];
        const item = document.createElement('div');
        item.className = 'wordcloud-grid-item';
        item.innerHTML = `
            <h4>${play.metadata.title}</h4>
            <img src="../${play.wordcloud.path}" alt="${play.metadata.title} Word Cloud">
        `;
        container.appendChild(item);
    });
}

// Render top words comparison
function renderTopWordsComparison(playIds) {
    const container = document.getElementById('compare-top-words');
    container.innerHTML = '<h4>Top 10 Words in Each Play</h4>';

    playIds.forEach(playId => {
        const play = state.plays[playId];
        const section = document.createElement('div');
        section.style.marginBottom = '20px';

        const title = document.createElement('h5');
        title.textContent = play.metadata.title;
        title.style.color = '#764ba2';
        section.appendChild(title);

        const chart = document.createElement('div');
        chart.className = 'bar-chart';

        const topWords = play.bag_of_words.top_words.slice(0, 10);
        const maxCount = topWords[0][1];

        topWords.forEach(([word, count]) => {
            const percentage = (count / maxCount) * 100;
            const item = document.createElement('div');
            item.className = 'bar-chart-item';
            item.innerHTML = `
                <div class="bar-chart-label">${word}</div>
                <div class="bar-chart-bar" style="width: ${percentage}%">
                    <span class="bar-chart-value">${count}</span>
                </div>
            `;
            chart.appendChild(item);
        });

        section.appendChild(chart);
        container.appendChild(section);
    });
}
