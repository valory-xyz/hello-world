# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2021-2023 Valory AG
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

"""This module contains the transaction payloads for the Hello World skill."""

from dataclasses import dataclass

from packages.valory.skills.abstract_round_abci.base import BaseTxPayload
from packages.valory.protocols.ledger_api.custom_types import TxData


@dataclass(frozen=True)
class RegistrationPayload(BaseTxPayload):
    """Represent a transaction payload of type 'registration'."""


@dataclass(frozen=True)
class CollectRandomnessPayload(BaseTxPayload):
    """Represent a transaction payload of type 'randomness'."""

    round_id: int
    randomness: str


@dataclass(frozen=True)
class PrintMessagePayload(BaseTxPayload):
    """Represent a transaction payload of type 'randomness'."""

    message: str


@dataclass(frozen=True)
class SelectKeeperPayload(BaseTxPayload):
    """Represent a transaction payload of type 'select_keeper'."""

    keeper: str


@dataclass(frozen=True)
class ResetPayload(BaseTxPayload):
    """Represent a transaction payload of type 'reset'."""

    period_count: int


class PrintCountPayload(BaseTxPayload):
    """Payload to store the updated print count."""

    def __init__(self, sender: str, print_count: int, **kwargs):
        super().__init__(sender=sender, **kwargs)
        self.print_count = print_count

    @property
    def tx_data(self) -> TxData:
        return TxData(f"print_count:{self.print_count}")
