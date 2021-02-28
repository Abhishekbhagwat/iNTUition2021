function callback(tabs) {
    alert(currentTab.url);
}

function updateURL(newUrl) {
    chrome.tabs.update(currentTab.id, {url: newUrl});
}

function search() {
    const term = document.getElementById("search").value;
    fetch('http://localhost:8000/api/searcher', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
        // body: JSON.stringify({ term })
    })
        .then(response => response.json())
        .then(data => {
            results = data;
            render();
        });
}

function timestampOnClick() {
    alert('timestamped clicked');
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
        // const timestamp = document.createElement('a');
        // const timestamp = document.createElement('div');
        const timestamp = document.createElement('p');
        timestamp.setAttribute('class', 'text-sm underline resultsLink');
        // timestamp.setAttribute('href', result[1]);
        // timestamp.setAttribute('href', '#');
        // timestamp.setAttribute('onclick', () => alert('timestamp'))
        // timestamp.setAttribute('onclick', timestampOnClick)
        
        timestamp.innerText = `${result[1]}s`;
        li.appendChild(header);
        li.appendChild(timestamp);
        resultsList.appendChild(li);
        timestamp.addEventListener('click', skipToTimestamp);
    });
}

async function skipToTimestamp(e) {
    // alert(e.srcElement.attributes.href.textContent);
    // e.preventDefault();
    // window.parent.postMessage(
    //     {
    //         type: 'SKIP_TO_TIME',
    //         time: e.srcElement.attributes.href.textContent
    //     },
    //     '*'
    // );
    // updateURL(e.srcElement.attributes.href.textContent);

    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: () => {
        // console.log(e.srcElement.innerText)
        let myPlayer = document.getElementsByClassName('video-stream html5-main-video')[0];
        myPlayer.currentTime = 2513.4;
      },
    });
}

var currentTab;
var results = [
    // ['memory', 12]
    ['google the word idiot', '2513.4'],
    ['said it doesn\'t mean that you\'re not', '5336.44'],
    ['be a fair statement if you did it', '6539.51'],
    ['recently so when did it become available','9141.14'],
    ['broadcasting and conservative talk radio','618.82'],
    ['use the android operating system it\'s','1415.339'],
];
const query = { active: true, currentWindow: true };

chrome.tabs.query(query, (tabs) => {
    currentTab = tabs[0];
    // document.getElementById('search').addEventListener('input', search);
    // document.getElementById('search').addEventListener('input', (e) => console.log(e.target.value));
    document.getElementById('search')
    // .addEventListener('input', (e) => alert('hello'));
    let form = document.getElementById('form')
    form.addEventListener('submit', () => {
        chrome.scripting.executeScript({
            target: { tabId: currentTab.id },
            function: () => console.log('submit')
          });
        render()
    })
    // render();
});