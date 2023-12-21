import json
import os
from flask import Flask, render_template, request, send_file
import exiftool


app = Flask(__name__)

images_path = "F:/images_without_background".split("/")


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
        if request.json and request.json["filename"] and request.json["tags"]:
            filename = request.json["filename"]
            tags = request.json["tags"]
            print(f"setting tags for {filename} to {tags}")

    return ""


@app.route("/get_tags/<string:filename>")
def get_tags(filename: str):
    data = {"tags": ["human", "person", "angry"]}

    return json.dumps(data)


@app.route("/all_tags/")
def all_tags():
    data = {"tags": ["human", "person", "angry"]}

    return json.dumps(data)
