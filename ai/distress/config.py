from pydantic_settings import BaseSettings

class FusionConfig(BaseSettings):
    """Configuration for Multimodal Risk Fusion."""
    
    # Base weights for each modality
    BASELINE_WEIGHT: float = 0.60
    NLP_WEIGHT: float = 0.20
    SPEECH_WEIGHT: float = 0.20
    
    # Conflict threshold
    CONFLICT_THRESHOLD: float = 30.0

    class Config:
        env_prefix = "FUSION_"

config = FusionConfig()
