function callback(tabs) {
    alert(currentTab.url);
}

function updateURL(newUrl) {
    chrome.tabs.update(currentTab.id, {url: newUrl});
}

function search() {
    const term = document.getElementById("search").value;
    fetch('http://localhost:8000/api/searcher', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ term })
    })
        .then(response => response.json())
        .then(data => {
            results = data;
            render();
        });
}

function render() {
    const resultsList = document.getElementById("resultsList");
    resultsList.innerHTML = '';
    results.forEach(function (result) {
        const li = document.createElement('li');
        li.setAttribute('class', 'flex justify-between items-center px-1 py-2');
        li.setAttribute('style', 'color: blue;');
        const header = document.createElement('div');
        header.setAttribute('class', 'text-medium text-sm');
        header.innerText = result[0];
        const timestamp = document.createElement('a');
        timestamp.setAttribute('class', 'text-sm underline resultsLink');
        timestamp.setAttribute('href', result[1]);
        timestamp.innerText = `${result[1]}s`;
        li.appendChild(header);
        li.appendChild(timestamp);
        resultsList.appendChild(li);
        timestamp.addEventListener('click', skipToTimestamp);
    });
}

function skipToTimestamp(e) {
    e.preventDefault();
    window.parent.postMessage(
        {
            type: 'SKIP_TO_TIME',
            time: e.srcElement.attributes.href.textContent
        },
        '*'
    );
    // updateURL(e.srcElement.attributes.href.textContent);
}

var currentTab;
var results = [
    ['memory', 12]
];
const query = { active: true, currentWindow: true };

chrome.tabs.query(query, (tabs) => {
    document.getElementById('search').addEventListener('input', search);
    currentTab = tabs[0];
    render();
});