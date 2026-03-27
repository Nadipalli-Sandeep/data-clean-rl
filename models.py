from typing import Dict, Optional
from openenv.core.env_server.types import Action, Observation
from pydantic import Field


# -------------------------------
# ACTION (What agent can do)
# -------------------------------
class MyAction(Action):
    action_type: str = Field(
        ..., description="Type of action: fill_missing, remove_outliers, drop_duplicates, normalize, do_nothing"
    )

    column: Optional[str] = Field(
        None, description="Target column (if applicable)"
    )


# -------------------------------
# OBSERVATION (What agent sees)
# -------------------------------
class MyObservation(Observation):
    missing: Dict[str, int] = Field(default_factory=dict)
    outliers: Dict[str, int] = Field(default_factory=dict)
    duplicates: int = Field(default=0)

    # NEW FIELDS
    total_missing: int = 0
    total_outliers: int = 0
    step_count: int = 0
    message: str = ""