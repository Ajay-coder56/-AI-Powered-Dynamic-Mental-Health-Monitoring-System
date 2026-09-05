class NLPConfig:
    MODEL_NAME = "cardiffnlp/twitter-xlm-roberta-base-sentiment-multilingual"
    MODEL_VERSION = "1.0"
    MAX_LENGTH = 512
    SUPPORTED_LANGUAGES = ["en", "hi", "ur", "mr", "gu", "pa", "bn", "ta", "te", "ml", "kn", "or", "as"]
    TIMEOUT_SECONDS = 10.0

config = NLPConfig()
