# NLP Model Selection

**Phase**: 3B — NLP

## Selected Model
**Model**: `cardiffnlp/twitter-xlm-roberta-base-sentiment-multilingual`

## Rationale
- **Multilingual Support**: Trained on 8 languages including Hindi, English. Handles Hinglish (code-mixed) decently.
- **Task**: Sentiment classification (Negative/Neutral/Positive). Negative sentiment maps directly to a conceptual `distress_signal`.
- **Performance**: Base XLM-RoBERTa (278M parameters) runs smoothly on modern CPU environments (approx. 500ms latency).
- **Environment Fit**: Requires `transformers` and `torch`, fits inside the 15GB RAM availability.

## Alternatives Considered
- `ai4bharat/IndicBERTv2`: Excellent for Indic languages, but requires custom fine-tuning for sentiment/distress as it is an MLM pre-trained model. Phase 3B restricts fine-tuning.
- `nlptown/bert-base-multilingual-uncased-sentiment`: 5-star ratings output is less optimal for mental health distress signals compared to negative sentiment probability.

## Limitations
- The model is trained on Twitter data, not clinical text.
- It detects negative sentiment, which is a proxy for distress but NOT a clinical diagnosis.
