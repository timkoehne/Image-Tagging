import json
import os
from typing import Set, Tuple
from flask import Flask, render_template, request, send_file
import exiftool
import db_access

db_controller = db_access.DB_Controller("database.db")

app = Flask(__name__)

images_path = "F:\\/images_without_background".split("/")  # this is ugly


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/get_image/<int:image_id>")
def get_image(image_id: int):
    images = os.listdir(os.path.join(*images_path))

    image_id = image_id % len(images)
    print(image_id)
    print(images[image_id])

    print(os.path.join(*images_path, images[image_id]))

    return send_file(os.path.join(*images_path, images[image_id]))


@app.route("/set_tags/", methods=["POST"])
def set_tags():
    if request.method == "POST":
        if request.json and request.json["filename"] and "tags" in request.json:
            filename = request.json["filename"]
            tags = request.json["tags"]

            db_controller.remove_tags_from_image(filename)
            for tag in tags:
                print(f"adding {filename} has tag {tag} into db")
                db_controller.tag_image(filename, tag)

            keywords_string = ",".join(tags)
            print(keywords_string)
            with exiftool.ExifToolHelper() as et:
                et.set_tags(
                    os.path.join(*images_path, filename),
                    {"XMP:Subject": keywords_string},
                    "-overwrite_original",
                )
            print(f"setting tags for {filename} to {keywords_string}")

    return ""


@app.route("/get_tags/<string:filename>")
def get_tags(filename: str):
    tags = db_controller.get_image_tags(filename)
    tags = ",".join(tags)

    if len(tags) == 0:
        print("looking into exif because there is no data in database")
        with exiftool.ExifToolHelper() as et:
            print(f"accessing file {os.path.join(*images_path, filename)}")
            metadata: dict = et.get_metadata(os.path.join(*images_path, filename))[0]
            # print(metadata)

            if "XMP:Subject" in metadata:
                tags = metadata.get("XMP:Subject").split(",")  # type: ignore

    data = {"tags": tags}

    return json.dumps(data)


@app.route("/get_tags_exif/<string:filename>")
def get_tags_exif(filename: str):
    with exiftool.ExifToolHelper() as et:
        metadata: dict = et.get_metadata(os.path.join(*images_path, filename))[0]
        print(metadata)
        if "XMP:Subject" in metadata:
            tags = metadata.get("XMP:Subject")
        else:
            tags = []

    print(f"Tags: {tags}")
    data = {"tags": tags}
    return json.dumps(data)


@app.route("/all_tags/")
def all_tags():
    tags = db_controller.get_all_tags()
    with open("saved_tags.json") as file:
        categories = json.loads(file.read())
        for category, entries in categories.items():
            for entry in entries:
                tags.append(entry)
    
    tags = set(tags)
    data = {"tags": ",".join(tags)}
    return json.dumps(data)


@app.route("/read_tags_from_xmp/")
def read_tags_from_xmp():
    images_tags: list[Tuple[str, list[str]]] = []

    for file in os.listdir(os.path.join(*images_path)):
        filename = os.path.join(*images_path, file)
        print(f"{file}")

        with exiftool.ExifToolHelper() as et:
            print(f"accessing file {os.path.join(*images_path, filename)}")
            metadata: dict = et.get_metadata(os.path.join(*images_path, filename))[0]
            # print(metadata)

            if "XMP:Subject" in metadata:
                tags: list[str] = metadata.get("XMP:Subject").split(",")  # type: ignore
                images_tags.append((file, tags))  # type: ignore
    db_controller.tag_images(images_tags)
    return ""


@app.route("/get_most_popular_tags/")
def get_most_popular_tags():
    popularity = db_controller.get_most_popular_tags()
    print("Most popular tags are:")
    print(popularity)

    return popularity


@app.route("/get_tag_categories/")
def get_tag_categories():
    with open("saved_tags.json", "r") as file:
        content: dict[str, list[str]] = json.loads(file.read())
    keys = list(content.keys())
    print(list(content.keys()))
    return keys


@app.route("/get_tag_category/<string:category>")
def get_tag_category(category: str):
    with open("saved_tags.json", "r") as file:
        content: dict[str, list[str]] = json.loads(file.read())
    keys = list(content.keys())
    
    if category in keys:
        return content[category]
    return ""
