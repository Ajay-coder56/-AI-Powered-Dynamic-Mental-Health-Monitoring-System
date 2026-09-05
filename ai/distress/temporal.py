from datetime import datetime, timezone
from typing import List, Tuple
from ai.distress.temporal_schemas import TemporalInput, TemporalRiskResult
from ai.distress.temporal_config import config

class TemporalRiskEngine:
    """
    Deterministic Temporal Risk Engine (Phase 3E).
    Produces longitudinal early-warning signals from historical fused risk scores.
    """
    
    def analyze(self, temporal_input: TemporalInput) -> TemporalRiskResult:
        # 1. Deduplicate and sort chronologically
        obs_dict = {}
        for obs in temporal_input.observations:
            # use timestamp as key to effectively deduplicate identical times
            obs_dict[obs.timestamp] = obs
            
        sorted_times = sorted(obs_dict.keys())
        valid_obs = [obs_dict[t] for t in sorted_times if 0 <= obs_dict[t].risk_score <= 100]
        count = len(valid_obs)
        
        # Base case: 0 observations
        if count == 0:
            return self._build_unavailable_result()
            
        current_score = valid_obs[-1].risk_score
        
        # Base case: 1 observation
        if count == 1:
            return self._build_single_observation_result(current_score)
            
        # 2. Extract time and score series
        scores = [obs.risk_score for obs in valid_obs]
        first_time = sorted_times[0]
        last_time = sorted_times[-1]
        
        elapsed_seconds = (last_time - first_time).total_seconds()
        elapsed_days = max(elapsed_seconds / 86400.0, 0.0001)  # Prevent division by zero
        
        # 3. Deterministic features
        previous_score = scores[-2]
        mean_score = int(round(sum(scores) / count))
        minimum_score = min(scores)
        maximum_score = max(scores)
        score_range = maximum_score - minimum_score
        
        # Simple Linear Regression for slope (Δrisk / Δdays)
        # Using actual elapsed time for each point
        x_days = [(t - first_time).total_seconds() / 86400.0 for t in sorted_times]
        if count == 2:
            slope_per_day = (scores[-1] - scores[0]) / max(x_days[-1] - x_days[0], 0.0001)
        else:
            # standard least squares
            mean_x = sum(x_days) / count
            mean_y = sum(scores) / count
            numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_days, scores))
            denominator = sum((x - mean_x) ** 2 for x in x_days)
            slope_per_day = numerator / denominator if denominator > 0.0001 else 0.0
            
        slope_per_day = round(slope_per_day, 2)
        
        # 4. Trend classification
        if slope_per_day < -config.TREND_THRESHOLD:
            trend = "improving"
        elif abs(slope_per_day) <= config.TREND_THRESHOLD:
            trend = "stable"
        else:
            trend = "worsening"
            
        # 5. Persistence logic
        # Count consecutive increases ending at the latest observation
        consecutive_increases = 0
        for i in range(count - 1, 0, -1):
            if scores[i] > scores[i-1]:
                consecutive_increases += 1
            else:
                break
                
        # Boolean persistent flag (multiple consecutive worsening observations)
        persistence = consecutive_increases >= 2
        
        # Determine if this is just a single spike
        is_single_spike = False
        if count >= 3:
            # Spike = went up recently, but was previously low, and only 1 increase
            if scores[-1] > scores[-2] and scores[-2] <= scores[-3] and consecutive_increases == 1:
                # significant jump
                if (scores[-1] - scores[-2]) >= 15:
                    is_single_spike = True
                    
        # 6. Early-warning engineering score (0-100)
        # A. Current Risk (0-100)
        c_risk = current_score
        
        # B. Trend Component (0-100). Max out at 5 points per day worsening
        if slope_per_day <= 0:
            c_trend = 0.0
        else:
            c_trend = min((slope_per_day / 5.0) * 100.0, 100.0)
            
        # C. Persistence Component (0-100)
        if persistence:
            c_persist = 100.0
        elif is_single_spike:
            c_persist = 0.0  # actively suppress single spikes
        else:
            c_persist = 50.0 if consecutive_increases == 1 else 0.0
            
        # D. Recent Change Component (0-100)
        recent_change = current_score - previous_score
        c_change = min(max(recent_change * 2.0, 0.0), 100.0)
        
        ew_score_raw = (
            (c_risk * config.CURRENT_RISK_WEIGHT) +
            (c_trend * config.TREND_WEIGHT) +
            (c_persist * config.PERSISTENCE_WEIGHT) +
            (c_change * config.RECENT_CHANGE_WEIGHT)
        )
        early_warning_score = int(round(max(0, min(100, ew_score_raw))))
        
        # 7. Temporal Status
        if early_warning_score <= config.STATUS_NO_SIGNAL_MAX:
            temporal_status = "no_signal"
        elif early_warning_score <= config.STATUS_WATCH_MAX:
            temporal_status = "watch"
        elif early_warning_score <= config.STATUS_ELEVATED_MAX:
            temporal_status = "elevated"
        else:
            temporal_status = "strong"
            
        # 8. Data Quality
        if count < config.MIN_OBSERVATIONS_TREND:
            data_quality = "insufficient"
        elif count < config.MIN_OBSERVATIONS_STRONG:
            data_quality = "limited"
        elif elapsed_days >= config.SHORT_WINDOW_DAYS:
            data_quality = "strong"
        else:
            data_quality = "adequate"
            
        # 9. Explanation
        if trend == "stable":
            explanation = "Recent risk scores have remained relatively stable over the available observation window."
        elif trend == "improving":
            explanation = "Recent observations indicate an improving risk trajectory."
        else:
            if is_single_spike:
                explanation = "The latest observation shows an elevated risk spike, but lacks persistence across previous check-ins."
            elif persistence:
                explanation = "Recent observations show elevated risk together with a persistent worsening trajectory. Human review may be appropriate."
            else:
                explanation = "Recent observations show a worsening risk trajectory."
                
        return TemporalRiskResult(
            available=True,
            observation_count=count,
            analysis_window_days=round(elapsed_days, 2),
            current_score=current_score,
            previous_score=previous_score,
            mean_score=mean_score,
            minimum_score=minimum_score,
            maximum_score=maximum_score,
            range=score_range,
            slope_per_day=slope_per_day,
            trend=trend,
            persistence=persistence,
            early_warning_score=early_warning_score,
            temporal_status=temporal_status,
            data_quality=data_quality,
            explanation=explanation
        )
        
    def _build_unavailable_result(self) -> TemporalRiskResult:
        return TemporalRiskResult(
            available=False,
            observation_count=0,
            trend="insufficient_data",
            temporal_status="unavailable",
            data_quality="insufficient",
            explanation="No historical observations available for temporal analysis."
        )
        
    def _build_single_observation_result(self, current_score: int) -> TemporalRiskResult:
        return TemporalRiskResult(
            available=False,
            observation_count=1,
            current_score=current_score,
            trend="insufficient_data",
            temporal_status="unavailable",
            data_quality="insufficient",
            explanation="Additional check-ins are needed before a reliable temporal trend can be estimated."
        )
