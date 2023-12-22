
let currentImage = 0

function loadNextImage() {
    currentImage += 1;
    loadImage();
}

function loadPrevImage() {
    currentImage -= 1;
    loadImage();

}

function addTag() {
    let data = {
        tag: "test"
    }

    fetch("/add_tag/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    }).then(response => {
        console.log(response)
    })
}

function setTags() {
    let value = JSON.parse(document.querySelector('input[name="tags"]').value);
    let tags = [];
    let filename = document.getElementById("filename").textContent
    for (i in value) {
        tags.push(value[i]["value"]);
    }

    console.log("Setting image tags to " + tags);

    fetch("/set_tags/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "filename": filename,
            "tags": tags
        }),
    }).then(response => {
        console.log(response)
    })
}


function loadTags() {

    filename = document.getElementById("filename").textContent;
    tagify.loading(true).dropdown.hide()

    fetch("/get_tags/" + filename).then(response => {
        return response.json();
    }).then(data => {
        let tags = data["tags"];

        const tagContainer = document.getElementById("tagContainer")
        while (tagContainer.firstChild) {
            tagContainer.removeChild(tagContainer.firstChild)
        }
        document.querySelector('input[name="tags"]').value = tags;
        tagify.loading(false) // render the suggestions dropdown
    })
}


function loadPossibleTags() {
    fetch("/all_tags/").then(response => {
        return response.json();
    }).then(data => {
        console.log(data)
        tagify.whitelist = data["tags"].split(",")
    })
}

function loadImage() {
    fetch("/get_image/" + currentImage).then(response => {

        let arr = response.headers.get("content-disposition").split("=")
        let filename = arr[arr.length - 1]
        console.log(filename)
        document.getElementById("filename").textContent = filename

        return response.blob()
    }).then(imageData => {
        document.getElementById("currentImage").src = URL.createObjectURL(imageData)
        loadTags()
    })

}


loadImage()