# Voice Model Selection

**Phase**: 3C — Speech Analysis

## Selected Pipeline
**Pipeline**: PyAV (`av`) + `librosa`

## Rationale
- **Acoustic Features vs ASR/Wav2Vec2**: Instead of using a heavy speech representation model like Wav2Vec2 (which is primarily designed for speech-to-text / phoneme extraction), we use deterministic acoustic feature extraction.
- **Features**: Pitch (F0), Pitch Variability (std), and RMS Energy.
- **Signal**: We derive a purely experimental `voice_signal` from pitch variability and energy inversion. This is fully explainable, unlike a black-box Wav2Vec2 embedding.
- **Decoding**: Since system `ffmpeg` is unavailable, `av` safely decodes browser-native `audio/webm` Opus streams entirely in-memory.

## Alternatives Considered
- **Wav2Vec2 / Whisper**: Rejected because they require significantly more RAM/CPU, are better suited for speech-to-text (ASR), and using their embeddings for mental health without fine-tuning is scientifically unsupported.
- **OpenSMILE**: Heavy integration requirement. `librosa` provides the exact necessary features natively in Python.
