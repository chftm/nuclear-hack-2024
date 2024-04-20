"""Main application."""

from __future__ import annotations

import os
import pathlib
import shutil
import uuid

from audio_splitter.main import split_audio  # type: ignore[import]
from flask import Flask, Response, abort, make_response, request

from model.audio.predict import Speech2EmotionModel  # type: ignore[import]

s2e = Speech2EmotionModel()

app = Flask(__name__)


@app.route("/classify_audio", methods=["POST"])
def classify() -> Response:
    """Classify audio file.

    Returns
    -------
        flask.Response: JSON response

    """
    chunk_len = 10  # in seconds

    input_file = request.files.get("file")
    if input_file is None or input_file.filename == "":
        abort(400)

    input_file_path = "data/audios/" + str(uuid.uuid4()) + input_file.filename
    input_file.save(input_file_path)

    dir_path = f"data/audios/{uuid.uuid4()}/"

    split_audio(
        input_file_path,
        dir_path,
        chunk_len * 1000,
        output_format="wav",
        silence_based=False,
    )

    pathlib.Path(input_file_path).unlink()
    result: list[tuple[int, str]] = []

    for ind, chunk in enumerate(os.listdir(dir_path)):
        time = ind * 10
        result.append((time, s2e.predict(dir_path + chunk)))

    shutil.rmtree(dir_path)

    return make_response(result, 200)


if __name__ == "__main__":
    app.run("0.0.0.0", port=8080)  # noqa: S104
