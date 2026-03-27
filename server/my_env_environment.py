# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
My Env Environment Implementation.

A simple test environment that echoes back messages sent to it.
Perfect for testing HTTP server infrastructure.
"""


from uuid import uuid4
import random

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

try:
    from ..models import MyAction, MyObservation
except ImportError:
    from models import MyAction, MyObservation


class MyEnvironment(Environment):

    SUPPORTS_CONCURRENT_SESSIONS = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._state.data = {}
        # Simple dataset state (counts only)
        self.missing = {}
        self.outliers = {}
        self.duplicates = 0

    # -------------------
    # RESET
    # -------------------
    def reset(self) -> MyObservation:
        self._state = State(episode_id=str(uuid4()), step_count=0)

        # Create random dataset (simple)
        columns = ["age", "salary", "experience"]

        self._state.data = {
            "missing": {col: random.randint(3, 10) for col in columns},
            "outliers": {col: random.randint(1, 5) for col in columns},
            "duplicates": random.randint(2, 6)
        }
        self._data = {
            "missing": self.missing,
            "outliers": self.outliers,
            "duplicates": self.duplicates
        }
        self._state.initial = {
            "missing": self._state.data["missing"].copy(),
            "outliers": self._state.data["outliers"].copy(),
            "duplicates": self._state.data["duplicates"]
        }
        total_missing = sum(self._state.data["missing"].values())
        total_outliers = sum(self._state.data["outliers"].values())

        return MyObservation(
            missing=self._state.data["missing"],
            outliers=self._state.data["outliers"],
            duplicates=self._state.data["duplicates"],
            total_missing=total_missing,
            total_outliers=total_outliers,
            step_count=0,
            reward=0.0,
            done=False,
            message="Environment reset. Start cleaning!"
        )       

    # -------------------
    # STEP
    # -------------------
    def step(self, action: MyAction) -> MyObservation:
        data = getattr(self._state, "data", {})

        # If data missing → auto reset
        if not data or "missing" not in data:
            obs = self.reset()
            data = self._state.data

        missing = data["missing"]
        outliers = data["outliers"]
        duplicates = data["duplicates"]
        # Ensure data exists
        if not hasattr(self, "_data"):
            return MyObservation(
                missing={},
                outliers={},
                duplicates=0,
                reward=-0.2,
                done=True
            )

        # Load state
        self.missing = self._data["missing"]
        self.outliers = self._data["outliers"]
        self.duplicates = self._data["duplicates"]
        self._state.step_count += 1

        reward = 0.0

        # -------------------
        # ACTION: fill_missing
        # -------------------
        if action.action_type == "fill_missing":
            col = action.column

            if col not in missing:
                reward = -0.15
            else:
                before = missing[col]

                if before > 0:
                    missing[col] -= 1
                    after = missing[col]

                    if after < before:
                        reward = 0.3
                    else:
                        reward = -0.1
                else:
                    reward = -0.1

        # -------------------
        # ACTION: remove_outliers
        # -------------------
        elif action.action_type == "remove_outliers":
            col = action.column

            if col in self.outliers:
                if self.outliers[col] > 0:
                    outliers[col] -= 1
                    reward = 0.3
                else:
                    reward = -0.1
            else:
                reward = -0.15

        # -------------------
        # ACTION: drop_duplicates
        # -------------------
        elif action.action_type == "drop_duplicates":
            if self.duplicates > 0:
                duplicates -= 1
                reward = 0.2
            else:
                reward = -0.1

        # -------------------
        # ACTION: do_nothing
        # -------------------
        elif action.action_type == "do_nothing":
            reward = -0.05

        else:
            reward = -0.15

        # small step penalty
        reward -= 0.01 * self._state.step_count

        # Save state back
        self._statedata = {
            "missing": missing,
            "outliers": outliers,
            "duplicates": duplicates
        }
        # -------------------
        # CORRUPTION EVENT
        # -------------------
        if self._state.step_count % 5 == 0:
            import random

            col = random.choice(list(missing.keys()))
            missing[col] += 1  # introduce new missing value

            col2 = random.choice(list(outliers.keys()))
            outliers[col2] += 1  # introduce new outlier
        # -------------------
        # DONE CONDITION
        # -------------------
        all_missing_clean = all(v == 0 for v in missing.values())
        all_outliers_clean = all(v == 0 for v in outliers.values())
        duplicates_clean = duplicates == 0

        done = all_missing_clean and all_outliers_clean and duplicates_clean
        total_missing = sum(missing.values())
        total_outliers = sum(outliers.values())
        return MyObservation(
            missing=missing,
            outliers=outliers,
            duplicates=duplicates,
            total_missing=total_missing,
            total_outliers=total_outliers,
            step_count=self._state.step_count,
            reward=reward,
            done=done,
            message ="Action executed. Corruption may occur every 5 steps."
        )

    # -------------------
    # STATE
    # -------------------
    @property
    def state(self) -> State:
        return self._state