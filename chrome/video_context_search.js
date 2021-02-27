fetch('http://localhost:8000/api/searcher')
.then(response => response.json())
.then(data => console.log(data));