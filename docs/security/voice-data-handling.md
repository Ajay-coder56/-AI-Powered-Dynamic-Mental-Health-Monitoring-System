# Voice Data Handling & Security

**Version**: 1.0
**Phase**: 3C — Speech Analysis

## Data Processing
- Audio is uploaded directly to the backend as `multipart/form-data`.
- The bytes are processed strictly in-memory using `av` (PyAV).
- Audio is decoded, converted to a mono numpy array, and passed to `librosa` for feature extraction.

## Storage & Logging
- **Database**: Raw audio is NOT persisted to PostgreSQL or disk. It is immediately garbage collected after feature extraction.
- **Logging**: No raw audio bytes or base64 strings are logged.

## Privacy Limits
- Maximum duration: 180 seconds.
- Maximum size: 10 MB.
- The derived signal is an engineering prototype and not a clinical diagnosis.
