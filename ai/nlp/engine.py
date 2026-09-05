import time
import logging
from typing import Optional

from app.risk_engine.interface import TextAnalysisEngine
from ai.nlp.schemas import TextAnalysisInput, TextAnalysisResult
from ai.nlp.config import config

logger = logging.getLogger(__name__)

class MultilingualSentimentEngine(TextAnalysisEngine):
    """
    NLP engine for analyzing mental health check-in text.
    
    Uses XLM-RoBERTa multilingual sentiment to derive a distress signal.
    Distress signal is mapped to the 'Negative' sentiment probability.
    """
    
    def __init__(self):
        self._pipeline = None
        self._is_loaded = False
        self._load_error = None
        
    @property
    def engine_name(self) -> str:
        return "text_nlp"
        
    @property
    def engine_version(self) -> str:
        return config.MODEL_VERSION

    def _load_model(self):
        """Lazy load the model to avoid blocking startup."""
        if self._is_loaded or self._load_error:
            return
            
        try:
            from transformers import pipeline
            # Use sentiment-analysis pipeline. The model predicts 3 labels:
            # 0: Negative, 1: Neutral, 2: Positive (labels depend on the specific model,
            # cardiffnlp uses Negative, Neutral, Positive typically).
            self._pipeline = pipeline(
                "sentiment-analysis", 
                model=config.MODEL_NAME, 
                tokenizer=config.MODEL_NAME,
                return_all_scores=True,
                device=-1 # CPU
            )
            self._is_loaded = True
            logger.info(f"Successfully loaded NLP model {config.MODEL_NAME}")
        except Exception as e:
            self._load_error = str(e)
            logger.error(f"Failed to load NLP model {config.MODEL_NAME}: {self._load_error}")

    def analyze_text(self, text: str, language: Optional[str] = None) -> dict:
        """Internal interface matching TextAnalysisEngine ABC."""
        input_data = TextAnalysisInput(text=text, language=language)
        result = self.analyze(input_data)
        return result.model_dump()

    def analyze(self, input_data: TextAnalysisInput) -> TextAnalysisResult:
        """
        Analyze text and produce an NLP distress signal.
        """
        start_time = time.time()
        
        # Validate text
        text = input_data.text.strip()
        if not text:
            return self._build_unavailable_result(
                "Text is empty.", start_time
            )
            
        if len(text) > 2000:
             return self._build_unavailable_result(
                "Text exceeds maximum length.", start_time
            )

        # Ensure model is loaded
        self._load_model()
        if not self._is_loaded:
            return self._build_unavailable_result(
                f"Model failed to load: {self._load_error}", start_time
            )

        try:
            # Inference
            # XLM-R max length is 512 tokens. Truncate text roughly by chars.
            truncated_text = text[:config.MAX_LENGTH * 4] 
            raw_output = self._pipeline(truncated_text)
            
            # Extract scores. Output format: [[{'label': 'Negative', 'score': 0.8}, ...]]
            scores = {item['label'].lower(): item['score'] for item in raw_output[0]}
            
            # Map Negative sentiment to distress signal
            # Handle variations in label naming from different models
            negative_score = scores.get('negative', scores.get('label_0', 0.0))
            positive_score = scores.get('positive', scores.get('label_2', 0.0))
            neutral_score = scores.get('neutral', scores.get('label_1', 0.0))
            
            distress_signal = negative_score
            confidence = max(negative_score, positive_score, neutral_score)
            
            # Determine dominant label
            sentiment_label = max(scores.items(), key=lambda x: x[1])[0]

            inference_time = (time.time() - start_time) * 1000

            explanation = (
                f"Analyzed {len(text)} characters. "
                f"Detected '{sentiment_label}' primary sentiment with {confidence:.2f} confidence. "
                f"Distress signal (derived from negative sentiment probability) is {distress_signal:.2f}."
            )
            
            return TextAnalysisResult(
                available=True,
                language_detected=input_data.language or "unknown",
                distress_signal=distress_signal,
                sentiment_label=sentiment_label,
                sentiment_scores=scores,
                confidence=confidence,
                model_name=config.MODEL_NAME,
                model_version=self.engine_version,
                inference_time_ms=inference_time,
                explanation=explanation,
                limitations="Model may not perfectly understand code-mixed Hinglish or clinical context."
            )

        except Exception as e:
            logger.error(f"NLP inference failed: {e}")
            return self._build_unavailable_result(
                f"Inference error: {str(e)}", start_time
            )
            
    def _build_unavailable_result(self, reason: str, start_time: float) -> TextAnalysisResult:
        inference_time = (time.time() - start_time) * 1000
        return TextAnalysisResult(
            available=False,
            model_name=config.MODEL_NAME,
            model_version=self.engine_version,
            inference_time_ms=inference_time,
            explanation=f"NLP analysis unavailable: {reason}",
            limitations="Analysis skipped."
        )
