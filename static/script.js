async function searchYouTube() {
    const queryText = document.getElementById('query').value;
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = '';

    const response = await fetch(`/query/?query_text=${encodeURIComponent(queryText)}`);
    const data = await response.json();

    const results = data.results;

    results.forEach(result => {
        const resultDiv = document.createElement('div');
        resultDiv.classList.add('result');

        resultDiv.innerHTML = `
            <a href="${result.video_url}" target="_blank">
                <img src="${result.thumbnail}" alt="Video Thumbnail">
            </a>
            <div class="result-text">
                <h3><a href="${result.video_url}" target="_blank">${result.Title}</a></h3>
                <p>${result.text}</p>
            </div>
        `;

        resultsContainer.appendChild(resultDiv);
    });
}
