"""Main application."""

from __future__ import annotations

import os
import pathlib
import shutil
import uuid
from audio_splitter.main import split_audio  # type: ignore[import]
from flask import Flask, Response, abort, make_response, request
import json
from model.audio.predict import Speech2EmotionModel  # type: ignore[import]
from model.face.src.emotions import EmotionDetector

s2e = Speech2EmotionModel()

detector = EmotionDetector()
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


@app.route("/classify_video", methods=["POST"])
def classify_video() -> Response:
    """Classify emotions in a video file.

    Returns
    -------
    flask.Response: JSON response containing emotion durations

    """
    input_file = request.files.get("file")
    if input_file is None or input_file.filename == "":
        abort(400)

    uploaded_path = f"data/videos/{uuid.uuid4()}" + input_file.filename
    input_file.save(uploaded_path)

    result_path = f"data/results/{uuid.uuid4()}.json"

    # Detect emotions and save results to JSON file
    detector.detect_emotions_to_json(uploaded_path, result_path)

    # Remove uploaded video file
    pathlib.Path(uploaded_path).unlink()

    # Read results from JSON file
    with open(result_path, "r") as f:
        result = json.load(f)

    # Remove result JSON file
    pathlib.Path(result_path).unlink()

    return make_response(json.dumps(result), 200)


if __name__ == "__main__":
    app.run("0.0.0.0", port=8080)  # noqa: S104
