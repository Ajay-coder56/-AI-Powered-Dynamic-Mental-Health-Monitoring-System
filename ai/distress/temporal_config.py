from pydantic_settings import BaseSettings

class TemporalConfig(BaseSettings):
    """Configuration for Phase 3E Temporal Risk Engine."""
    
    # Analysis Windows
    SHORT_WINDOW_DAYS: int = 7
    LONG_WINDOW_DAYS: int = 14
    
    # Observation thresholds
    MIN_OBSERVATIONS_TREND: int = 2
    MIN_OBSERVATIONS_STRONG: int = 5
    
    # Trend thresholds (change per day to be considered stable vs worsening/improving)
    # A slope of 1.0 means risk_score increases by 1 point per day.
    TREND_THRESHOLD: float = 0.5
    
    # Early Warning Weights (engineering values, NOT clinical)
    CURRENT_RISK_WEIGHT: float = 0.35
    TREND_WEIGHT: float = 0.30
    PERSISTENCE_WEIGHT: float = 0.20
    RECENT_CHANGE_WEIGHT: float = 0.15
    
    # Status Thresholds (0-100 scale for early warning score)
    STATUS_NO_SIGNAL_MAX: int = 24
    STATUS_WATCH_MAX: int = 49
    STATUS_ELEVATED_MAX: int = 74

    class Config:
        env_prefix = "TEMPORAL_"

config = TemporalConfig()
