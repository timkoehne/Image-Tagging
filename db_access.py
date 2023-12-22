from calendar import c
import sqlite3
from typing import Tuple


class DB_Controller:
    def __init__(self, db_filename: str) -> None:
        self.db_filename = db_filename
        connection = sqlite3.connect(self.db_filename)
        self._create_tables(connection)
        connection.close()

    def _create_tables(self, connection: sqlite3.Connection):
        cursor = connection.cursor()

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS images (
            image_id INTEGER PRIMARY KEY,
            filename TEXT NOT NULL UNIQUE
        );"""
        )

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS tags (
            tag_id INTEGER PRIMARY KEY,
            tag TEXT NOT NULL UNIQUE
        );"""
        )

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS image_tags (
            image_id INTEGER,
            tag_id INTEGER,
            PRIMARY KEY (image_id, tag_id),
            FOREIGN KEY (image_id) REFERENCES images (image_id),
            FOREIGN KEY (tag_id) REFERENCES tags (tag_id)
        );"""
        )

    def _insert_image(self, filename: str, connection: sqlite3.Connection):
        cursor = connection.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO images (filename) VALUES (?);", (filename,)
        )

    def _insert_tag(self, tag: str, connection: sqlite3.Connection):
        cursor = connection.cursor()
        cursor.execute("INSERT OR IGNORE  INTO tags (tag) VALUES (?);", (tag,))

    def _get_image_name(self, image_id: int, connection: sqlite3.Connection) -> str:
        cursor = connection.cursor()
        cursor.execute("SELECT filename FROM images WHERE image_id=?", (image_id,))
        filename: str = cursor.fetchone()[0]
        return filename

    def _get_tag_name(self, tag_id: int, connection: sqlite3.Connection) -> str:
        cursor = connection.cursor()
        cursor.execute("SELECT tag FROM tags WHERE tag_id=?", (tag_id,))
        tag: str = cursor.fetchone()[0]
        return tag

    def _get_image_id(self, image: str, connection: sqlite3.Connection) -> int:
        cursor = connection.cursor()
        self._insert_image(image, connection)
        cursor.execute("SELECT image_id FROM images WHERE filename=?", (image,))
        image_id: int = cursor.fetchone()[0]

        return image_id

    def _get_tag_id(self, tag: str, connection: sqlite3.Connection) -> int:
        cursor = connection.cursor()
        self._insert_tag(tag, connection)
        cursor.execute("SELECT tag_id FROM tags WHERE tag=?", (tag,))
        tag_id: int = cursor.fetchone()[0]
        return tag_id

    def _print_everything(self, connection: sqlite3.Connection):
        cursor = connection.cursor()
        print("------Tables-----")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(cursor.fetchall())

        print("------Images-----")
        cursor.execute("SELECT * FROM images;")
        print(cursor.fetchall())

        print("------Tags-----")
        cursor.execute("SELECT * FROM tags;")
        print(cursor.fetchall())

        print("------Image_Tags-----")
        cursor.execute("SELECT * FROM image_tags;")
        print(cursor.fetchall())

    def get_all_tags(self) -> list[str]:
        connection = sqlite3.connect(self.db_filename)
        cursor = connection.cursor()

        tags = []
        cursor.execute("SELECT tag from tags")
        for entry in cursor.fetchall():
            tags.append(entry[0])

        connection.close()
        return tags

    def get_image_tags(self, image: str) -> list[str]:
        connection = sqlite3.connect(self.db_filename)
        cursor = connection.cursor()

        print(image)
        image_id = self._get_image_id(image, connection)
        print(image_id)
        cursor.execute("SELECT tag_id FROM image_tags WHERE image_id=?", (image_id,))
        result = cursor.fetchall()
        # print(result)

        tags = []
        for tag in result:
            # print(self._get_tag_name(tag[0]))
            tags.append(self._get_tag_name(tag[0], connection))

        connection.close()
        return tags

    def tag_image(
        self, image: str, tag: str, connection: sqlite3.Connection | None = None
    ):
        if connection:
            passedInConnection = True
        else:
            # create, commit and close connection only if the connection wasnt passed into this method
            passedInConnection = False
            connection = sqlite3.connect(self.db_filename)

        cursor = connection.cursor()

        self._insert_image(image, connection)
        self._insert_tag(tag, connection)
        image_id = self._get_image_id(image, connection)
        tag_id = self._get_tag_id(tag, connection)

        cursor.execute(
            "INSERT OR IGNORE INTO image_tags (image_id, tag_id) VALUES (?, ?);",
            (image_id, tag_id),
        )

        if not passedInConnection:
            connection.commit()
            connection.close()

    def tag_images(self, image_tags: list[Tuple[str, list[str]]]):
        connection = sqlite3.connect(self.db_filename)

        for entry in image_tags:
            filename = entry[0]
            tags = entry[1]

            for tag in tags:
                self.tag_image(filename, tag, connection)

        connection.close()

    def remove_tags_from_image(self, image: str):
        connection = sqlite3.connect(self.db_filename)
        cursor = connection.cursor()

        image_id = self._get_image_id(image, connection)
        cursor.execute("DELETE FROM image_tags WHERE image_id=?", (image_id,))

        connection.commit()
        connection.close()

    def get_most_popular_tags(self):
        connection = sqlite3.connect(self.db_filename)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT tag, COUNT(tag) AS amount FROM image_tags JOIN tags ON image_tags.tag_id=tags.tag_id GROUP BY tag ORDER BY amount DESC LIMIT 10"
        )
        popularity = cursor.fetchall()
        popularity = [{"tag": entry[0], "amount": entry[1]} for entry in popularity]

        connection.close()
        return popularity
