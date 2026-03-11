# FSM Audit Report

**Scope:** `packages/valory/skills/hello_world_abci/`
**Dev/Third-Party Classification:** Based on `packages/packages.json`
**Date:** 2026-03-11

---

## CLI Tool Output

The hello-world repository does not have a `pyproject.toml`-based Poetry setup, so the `autonomy` CLI tools (`fsm-specs`, `handlers`, `dialogues`, `docstrings`) could not be executed via `poetry run`. Analysis was performed using static code review and Python introspection instead.

---

## Critical Findings

No findings.

### C1: Shared Mutable References — PASS
No instances of `([],) * n` or `({},) * n` found anywhere in the skill.

### C2: Operator Precedence in Boolean Guards — PASS
No multi-line conditionals with mixed `and`/`or` operators found.

### C3: Transition Function Completeness — PASS
All events returned by `end_block()` implementations have corresponding transition function entries:
- `RegistrationRound.end_block()` → `Event.DONE` → `CollectRandomnessRound` ✓
- `CollectRandomnessRound` (CollectSameUntilThresholdRound): `DONE`, `NONE`, `NO_MAJORITY`, `ROUND_TIMEOUT` all wired ✓
- `SelectKeeperRound` (CollectSameUntilThresholdRound): `DONE`, `NONE`, `NO_MAJORITY`, `ROUND_TIMEOUT` all wired ✓
- `PrintMessageRound.end_block()` → `DONE` and `ROUND_TIMEOUT` wired ✓
- `ResetAndPauseRound.end_block()` → `DONE`, `NO_MAJORITY`, `RESET_TIMEOUT` all wired ✓

### C4: Dead Timeouts — PASS
Both entries in `event_to_timeout` are live:
- `Event.ROUND_TIMEOUT: 30.0` — appears as a key in CollectRandomnessRound, SelectKeeperRound, PrintMessageRound transitions ✓
- `Event.RESET_TIMEOUT: 30.0` — appears as a key in ResetAndPauseRound transition ✓

### C5: Invalid Event String Defaults in Behaviours — PASS
Behaviours do not use hardcoded string event defaults. They use `self.set_done()` for signalling round completion. No `event = "..."` patterns found.

---

## High Findings

No findings.

### H1: Background App Configuration — PASS
No `BackgroundAppConfig` or `background_apps` used in this skill.

### H2: Composition Chain Completeness — PASS
No `chain()` composition used. The skill is a standalone FSM.

### H3: Resource Lifecycle — PASS
- HTTP requests handled via `_do_request()` helper with proper async delegation ✓
- `CollectRandomnessBehaviour.clean_up()` properly resets retry counters ✓
- No unclosed file handles, no `requests.get/post` without timeout, no zombie processes ✓

---

## Medium Findings

No findings.

### M1: Payload Class Mismatch — PASS

| Round | payload_class | Fields used in end_block() | Status |
|---|---|---|---|
| RegistrationRound | RegistrationPayload | (none) | ✓ |
| CollectRandomnessRound | CollectRandomnessPayload | `round_id`, `randomness` | ✓ |
| SelectKeeperRound | SelectKeeperPayload | `keeper` | ✓ |
| PrintMessageRound | PrintMessagePayload | `message` | ✓ |
| ResetAndPauseRound | ResetPayload | `period_count` | ✓ |

### M2: Event Enum Completeness — PASS
All five Event members are used in the transition function:
- `DONE`, `NONE`, `NO_MAJORITY` — referenced in multiple round transitions
- `ROUND_TIMEOUT` — in `event_to_timeout` and in transition entries
- `RESET_TIMEOUT` — in `event_to_timeout` and in `ResetAndPauseRound` transition

No unused enum members.

### M3: DB Pre/Post Conditions Consistency — PASS
`SynchronizedData` uses `get_strict()` for all key accesses, raising on missing keys rather than silently returning `None`. Pre/post conditions are consistent with the metaclass expectations.

### M4: Thread Join Without Timeout — PASS
No `thread.join()` calls found. All concurrency uses `yield from` async delegation.

### M5: collection_key/selection_key vs SynchronizedData Mismatch — PASS
- `CollectRandomnessRound`: `collection_key = get_name(SynchronizedData.participant_to_randomness)`, `selection_key = get_name(SynchronizedData.most_voted_randomness)` — both match the SynchronizedData properties ✓
- `SelectKeeperRound`: `collection_key = get_name(SynchronizedData.participant_to_selection)`, `selection_key = get_name(SynchronizedData.most_voted_keeper_address)` — both match ✓

Using `get_name()` on the SynchronizedData properties ensures keys stay in sync automatically.

---

## Low Findings

No findings.

### L1: Dead Code — PASS
All defined classes are referenced:
- All behaviour classes registered in `HelloWorldRoundBehaviour.behaviours` ✓
- All round classes appear in `transition_function` ✓
- All payload classes referenced in rounds ✓

### L2: Stale Imports — PASS
No unused imports identified in `rounds.py`, `behaviours.py`, `payloads.py`, or `models.py`.

### L3: Docstring / Transition Function Drift — PASS
The `HelloWorldAbciApp` docstring FSM description matches the actual `transition_function` definition exactly. The `fsm_specification.yaml` is consistent with the implementation.

---

## Test Coverage

### T1: @classmethod @pytest.fixture Anti-Pattern — PASS
No `@classmethod` combined with `@pytest.fixture` found in test files.

### T2: Wrong Base Test Class for Round Type — PASS
`BaseRoundTestClass` (the project-local wrapper) sets `_synchronized_data_class = SynchronizedData` and `_event_class = Event`, then all round test classes inherit from it. Correct.

### T3: Missing Required Test Class Attributes — PASS
- `BaseRoundTestClass`: has `_synchronized_data_class` and `_event_class` ✓
- `HelloWorldAbciFSMBehaviourBaseCase`: has `path_to_skill = PACKAGE_DIR` ✓

### T4: Missing mock_a2a_transaction() — PASS
All behaviour tests that send a payload call `self.mock_a2a_transaction()` after `self.behaviour.act_wrapper()`.

### T5: Incomplete Round Event Testing — PASS
- `TestRegistrationRound`: tests DONE ✓
- `TestCollectRandomnessRound`: tests DONE and NO_MAJORITY via `_test_no_majority_event()` ✓
- `TestSelectKeeperRound`: tests DONE and NO_MAJORITY ✓
- `TestPrintMessageRound`: tests DONE ✓
- `TestResetAndPauseRound`: tests DONE and NO_MAJORITY ✓

### T6: _MetaPayload.registry Not Saved/Restored — PASS
No overrides of `setup_class` / `teardown_class` that skip `super()`.

---

## Third-Party Impact Assessment

No third-party impact findings. The two third-party skills used (`abstract_abci`, `abstract_round_abci`) provide base classes and are not audited here — any issues in them would need to be reported upstream to `valory-xyz/open-autonomy`.

---

## Summary

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 |
| **Total** | **0** |

The `hello_world_abci` skill is clean across all audit categories. No action items required.

## Notes

- CLI tools (`autonomy analyse fsm-specs` etc.) could not be run because the repository uses `Pipfile`/`Pipfile.lock` rather than `pyproject.toml`/`poetry.lock`. To run the CLI tools, activate the virtualenv created by `pipenv` and run `autonomy analyse ...` directly.
- `ROUND_TIMEOUT` appearing in the Event enum is standard convention for library-style skills and is not flagged as M2.
- The `_allow_rejoin_payloads = True` attribute on `ResetAndPauseRound` is inherited from the framework's reset round and is correct by design.
