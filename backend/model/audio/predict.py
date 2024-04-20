"""model audio predict."""

from __future__ import annotations

from speechbrain.inference.interfaces import foreign_class  # type: ignore[import]


class Speech2EmotionModel:
    """Speech2EmotionModel class."""

    def __init__(self: Speech2EmotionModel) -> None:
        """Initialize Speech2EmotionModel class."""
        self.classifier = foreign_class(
            source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP",
            pymodule_file="custom_interface.py",
            classname="CustomEncoderWav2vec2Classifier",
            savedir="model/audio/wav2vec2",
            huggingface_cache_dir="model/audio/model_cache",
        )

    def predict(self: Speech2EmotionModel, audio_path: str) -> tuple:
        """Predict emotion from audio file."""
        return self.classifier.classify_file(audio_path)  # type: ignore[no-any-return]
