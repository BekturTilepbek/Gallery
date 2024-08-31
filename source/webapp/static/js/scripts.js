async function makeRequest(url, method = "GET") {
    let response = await fetch(url, {"method": method});
    if (response.ok) {
        return await response.json();
    } else {
        let error = new Error(response.text);
        console.log(error);
        throw error;
    }
}

async function onClick(event) {
    event.preventDefault();
    let a = event.target;

    let url = a.href;

    let response = await makeRequest(url);

    if (response['in_favorites']) {
        a.innerHTML = '<i class="bi bi-bookmark-fill" style="pointer-events: none"></i>';
    } else {
        a.innerHTML = '<i class="bi bi-bookmark" style="pointer-events: none"></i>';
    }
}

function onLoad() {
    let links = document.querySelectorAll('[data-js="favorite"]')
    for (let link of links) {
        link.addEventListener("click", onClick);
    }
}

window.addEventListener("load", onLoad);