"""
Risk Engine Registry — Centralized engine metadata and versioning.

Tracks all registered risk engine implementations and their metadata.
Prevents hardcoded version logic throughout the application.

Usage:
    registry = EngineRegistry()
    registry.register(DeterministicBaselineEngine())
    engine = registry.get_engine("deterministic_baseline")
    info = registry.list_engines()
"""

from typing import Dict, List, Optional

from app.risk_engine.interface import RiskEngine


class EngineInfo:
    """Metadata about a registered engine."""

    def __init__(self, engine: RiskEngine, is_active: bool = False) -> None:
        self.engine = engine
        self.name = engine.engine_name
        self.version = engine.engine_version
        self.engine_id = engine.engine_id()
        self.is_active = is_active

    def to_dict(self) -> dict:
        return {
            "engine_name": self.name,
            "engine_version": self.version,
            "engine_id": self.engine_id,
            "is_active": self.is_active,
        }


class EngineRegistry:
    """
    Registry of available risk engine implementations.

    Allows registering multiple engines by name@version and selecting
    the active engine. Future phases can register NLP, speech, temporal,
    and multimodal engines alongside the baseline.
    """

    def __init__(self) -> None:
        self._engines: Dict[str, EngineInfo] = {}
        self._active_engine_id: Optional[str] = None

    def register(self, engine: RiskEngine, set_active: bool = False) -> None:
        """
        Register an engine implementation.

        Args:
            engine: A RiskEngine implementation to register.
            set_active: If True, set this engine as the active engine.
        """
        engine_id = engine.engine_id()

        if engine_id in self._engines:
            raise ValueError(
                f"Engine '{engine_id}' is already registered. "
                f"Use a different version to register a new variant."
            )

        info = EngineInfo(engine=engine, is_active=set_active)
        self._engines[engine_id] = info

        if set_active:
            # Deactivate any previously active engine
            if self._active_engine_id and self._active_engine_id in self._engines:
                self._engines[self._active_engine_id].is_active = False
            self._active_engine_id = engine_id

    def get_engine(self, engine_name: str, version: Optional[str] = None) -> RiskEngine:
        """
        Retrieve a registered engine by name and optional version.

        If version is not specified, returns the first engine matching the name.

        Args:
            engine_name: The engine name (e.g. 'deterministic_baseline').
            version: Optional version string (e.g. '1.0').

        Returns:
            The registered RiskEngine implementation.

        Raises:
            KeyError: If no matching engine is found.
        """
        if version:
            engine_id = f"{engine_name}@{version}"
            if engine_id not in self._engines:
                raise KeyError(f"Engine '{engine_id}' is not registered.")
            return self._engines[engine_id].engine

        # Find first engine matching the name
        for info in self._engines.values():
            if info.name == engine_name:
                return info.engine

        raise KeyError(f"No engine with name '{engine_name}' is registered.")

    def get_active_engine(self) -> RiskEngine:
        """
        Return the currently active engine.

        Raises:
            RuntimeError: If no active engine is set.
        """
        if not self._active_engine_id or self._active_engine_id not in self._engines:
            raise RuntimeError(
                "No active risk engine is set. "
                "Register an engine with set_active=True."
            )
        return self._engines[self._active_engine_id].engine

    def list_engines(self) -> List[dict]:
        """Return metadata for all registered engines."""
        return [info.to_dict() for info in self._engines.values()]

    @property
    def active_engine_id(self) -> Optional[str]:
        """The engine_id of the currently active engine, or None."""
        return self._active_engine_id
