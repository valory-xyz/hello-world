# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2021 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This module contains the models for common app ABCI application."""


from typing import Any

from packages.valory.skills.abstract_round_abci.models import BaseParams


class Params(BaseParams):  # pylint: disable=too-many-instance-attributes
    """Parameters."""

    observation_interval: float

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the parameters object."""
        self.max_healthcheck = self._ensure("max_healthcheck", kwargs)
        self.round_timeout_seconds = self._ensure("round_timeout_seconds", kwargs)
        self.sleep_time = self._ensure("sleep_time", kwargs)
        self.retry_timeout = self._ensure("retry_timeout", kwargs)
        self.retry_attempts = self._ensure("retry_attempts", kwargs)
        self.observation_interval = self._ensure("observation_interval", kwargs)
        self.oracle_params = self._ensure("oracle", kwargs)
        self.drand_public_key = self._ensure("drand_public_key", kwargs)
        self.tendermint_com_url = self._ensure("tendermint_com_url", kwargs)
        self.reset_tendermint_after = self._ensure("reset_tendermint_after", kwargs)
        super().__init__(*args, **kwargs)