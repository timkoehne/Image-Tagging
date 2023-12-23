
let currentImage = 0

function loadNextImage() {
    currentImage += 1;
    loadImage();
}

function loadPrevImage() {
    currentImage -= 1;
    loadImage();

}

function setTags() {
    let value = document.querySelector('input[name="tags"]').value;
    if (value != "") {
        value = JSON.parse(value);
    }


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
        loadPopularTags()
    })
}

function loadTags() {
    filename = document.getElementById("filename").textContent;

    const tagContainer = document.getElementById("tagContainer")
    while (tagContainer.firstChild) {
        tagContainer.removeChild(tagContainer.firstChild)
    }

    tagify.loading(true).dropdown.hide()

    fetch("/get_tags/" + filename).then(response => {
        return response.json();
    }).then(data => {
        let tags = data["tags"];

        document.querySelector('input[name="tags"]').value = tags;
        tagify.loading(false) // render the suggestions dropdown
    })
    loadPossibleTags()
}

function loadPossibleTags() {
    fetch("/all_tags/").then(response => {
        return response.json();
    }).then(data => {
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

function loadTagCategories() {
    fetch("/get_tag_categories/").then(response => {
        return response.json()
    }).then(categories_arr => {
        for (i in categories_arr) {
            option = document.createElement("option")
            option.textContent = categories_arr[i]
            option.value = categories_arr[i]
            document.getElementById("tagCategories").appendChild(option)
        }
        onCategorySelection(categories_arr[0])

    })
}

function onCategorySelection(selected_category) {
    const tagsInCategory = document.getElementById("tagsInCategory")
    while (tagsInCategory.firstChild) {
        tagsInCategory.removeChild(tagsInCategory.firstChild)
    }

    fetch("/get_tag_category/" + selected_category).then(response => {
        return response.json()
    }).then(tagsInCategoryArr => {
        for (i in tagsInCategoryArr) {
            entry = document.createElement("button")
            entry.onclick = function () {
                addTagToTagInput(this.textContent)
            }
            entry.textContent = tagsInCategoryArr[i]
            document.getElementById("tagsInCategory").appendChild(entry)
        }
    })

}

function addTagToTagInput(value) {

    let currentTags = document.getElementById("tags").value
    console.log(currentTags)
    if (currentTags != "") {
        currentTagsArr = JSON.parse(currentTags)
    } else { currentTagsArr = [] }

    let tags = []
    for (i in currentTagsArr) {
        tags.push(currentTagsArr[i]["value"])
    }

    tags.push(value)

    const tagsStr = tags.join(",")
    document.getElementById("tags").value = tagsStr
}

function loadPopularTags() {

    const popularTags = document.getElementById("popularTags")
    while (popularTags.firstChild) {
        popularTags.removeChild(popularTags.firstChild)
    }


    fetch("/get_most_popular_tags/").then(response => {
        return response.json()
    }).then(popularTagsArr => {
        // console.log("Loading popular Tags:")
        // console.log(popularTagsArr)
        for (i in popularTagsArr) {
            entry = document.createElement("button")
            entry.onclick = function () {
                addTagToTagInput(this.textContent)
            }
            entry.textContent = popularTagsArr[i].tag
            document.getElementById("popularTags").appendChild(entry)
        }
    })
}

loadImage()
loadTagCategories()
loadPopularTags()