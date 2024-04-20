"""Main application."""

import pathlib
import shutil
import uuid

import flask

from model.audio.predict import Speech2EmotionModel
from modules.audioprocessing import to_chunks, to_wav

s2e = Speech2EmotionModel()

app = flask.Flask(__name__)


@app.route("/classify_audio", methods=["POST"])
def classify() -> flask.Response:
    """Classify audio file.

    Returns
    -------
        flask.Response: JSON response

    """
    input_file = flask.request.files.get("file")
    if input_file is None or input_file.filename == "":
        flask.abort(400)

    uploaded_path = f"data/audios/{uuid.uuid4()}" + input_file.filename
    input_file.save(uploaded_path)

    new_path = to_wav(pathlib.Path(uploaded_path))
    pathlib.Path(uploaded_path).unlink()

    result = []
    folder_id = str(uuid.uuid4())
    parent_path = f"model/audio/{folder_id}"

    for path in to_chunks(audio_file=new_path, parent_path=parent_path):
        result.append(s2e.predict(path))
        pathlib.Path(path).unlink()

    new_path.unlink()
    shutil.rmtree(parent_path)

    return flask.make_response({"result": result}, 200)


if __name__ == "__main__":
    app.run("0.0.0.0", port=8080)  # noqa: S104
