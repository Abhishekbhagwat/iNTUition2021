waitForElementToDisplay("#top-level-buttons", main());

function main() {
    // add code here
}

function waitForElementToDisplay(selector, callback) {
    const startTimeInMs = Date.now();
    (function loopSearch() {
        if (document.querySelector(selector) != null) {
            callback();
            return;
        }
        else {
            setTimeout(function () {
                if (Date.now() - startTimeInMs > 10000)
                    return;
                loopSearch();
            }, 200);
        }
    })();
}