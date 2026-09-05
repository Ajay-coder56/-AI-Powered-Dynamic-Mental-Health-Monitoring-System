# NLP Data Handling & Security

**Version**: 1.0
**Phase**: 3B — NLP

## Data Processing
- Text provided via `text_content` is processed strictly in-memory during the request lifecycle.
- The NLP engine (`MultilingualSentimentEngine`) runs inference locally via Hugging Face Transformers.
- NO external API calls are made for inference (no OpenAI, no Google Cloud).

## Storage & Logging
- **Database**: Raw text is NOT persisted in PostgreSQL by default in Phase 3B. The `check_ins` table was not modified to store raw text.
- **Logging**: Text is stripped/redacted from logs. `nlp_analysis` logs only report model load status, errors, and availability, NOT the text content itself.
- **Errors**: Model errors do not include the raw text in the HTTP response or logs.

## Clinical Disclaimer
The system does not store diagnoses, as the NLP output is an engineering baseline distress signal, not a clinical psychiatric diagnosis.
