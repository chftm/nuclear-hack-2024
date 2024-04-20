"""audio processing module."""

import pathlib
from typing import Iterator

from pydub import AudioSegment  # type: ignore[import-untyped]
from pydub.silence import split_on_silence  # type: ignore[import-untyped]


def to_wav(path: pathlib.Path) -> pathlib.Path:
    """Convert audio file to wav format."""
    path = path.with_suffix(".wav")
    AudioSegment.from_file(path).export(path, format="wav")
    return path


def to_chunks(audio_file: pathlib.Path, parent_path: str) -> Iterator[str]:
    """Split audio file into chunks."""
    chunks = split_on_silence(
        AudioSegment.from_file(audio_file),
        min_silence_len=500,
        silence_thresh=-40,
    )

    for i, chunk in enumerate(chunks):
        chunk_path = parent_path + f"/chunk{i}.wav"
        chunk.export(chunk_path, format="wav")
        yield chunk_path
