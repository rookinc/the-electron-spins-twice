from __future__ import annotations

import hashlib
import json
from collections import deque
from pathlib import Path

TARGET = Path(__file__).resolve().parents[2]

SOURCE = TARGET / "artifacts/json/g60_factorized_torsional_action_candidate_theorem_201.v1.json"
ARTIFACT = TARGET / "artifacts/json/finite_covariant_receipt_apparatus_contract_204.v1.json"

EVENTS = [
    "orthogonal_passage",
    "drive_plus",
    "drive_minus",
    "g900_step",
    "emit_180",
    "g15_step",
    "read_receipt",
]

INITIAL = (0, 0, "idle")
SINK = ("sink", 0, "error")


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def key(state):
    if state == SINK:
        return "sink"
    k, sign, mode = state
    return "%d:%+d:%s" % (k, sign, mode)


def transition(state, event):
    if state == SINK:
        return SINK

    k, sign, mode = state

    if mode == "idle":
        if event == "orthogonal_passage":
            return state
        if event == "drive_plus":
            return (1, 1, "drive")
        if event == "drive_minus":
            return (7, -1, "drive")
        return None

    if mode == "drive":
        if sign == 1 and event == "drive_plus":
            next_k = (k + 1) % 8
        elif sign == -1 and event == "drive_minus":
            next_k = (k - 1) % 8
        else:
            return None
        return (
            next_k,
            sign,
            "limit" if next_k == 4 else "drive",
        )

    if mode == "limit":
        if event == "g900_step":
            return ((k - sign) % 8, sign, "g900_return")
        return None

    if mode == "g900_return":
        if event != "g900_step":
            return None
        next_k = (k - sign) % 8
        assert next_k == (2 if sign == 1 else 6)
        return (next_k, sign, "half_turn")

    if mode == "half_turn":
        if event == "emit_180":
            return (k, sign, "emit")
        return None

    if mode == "emit":
        if event == "g15_step":
            return ((k + sign) % 8, sign, "g15_rebound")
        return None

    if mode == "g15_rebound":
        if event != "g15_step":
            return None
        next_k = (k + sign) % 8
        assert next_k == 4
        return (next_k, sign, "receipt")

    if mode == "receipt":
        if event == "read_receipt":
            return state
        return None

    raise ValueError(mode)


def reverse_state(state):
    k, sign, mode = state
    return ((-k) % 8, -sign, mode)


def reverse_event(event):
    if event == "drive_plus":
        return "drive_minus"
    if event == "drive_minus":
        return "drive_plus"
    return event


def enumerate_reachable():
    reachable = {INITIAL}
    queue = deque([INITIAL])
    rows = []

    while queue:
        state = queue.popleft()

        for event in EVENTS:
            target = transition(state, event)
            if target is None:
                continue

            rows.append(
                {
                    "source": key(state),
                    "event": event,
                    "target": key(target),
                }
            )

            if target not in reachable:
                reachable.add(target)
                queue.append(target)

    rows.sort(
        key=lambda row: (
            row["source"],
            row["event"],
            row["target"],
        )
    )

    return sorted(reachable, key=key), rows


def execute(events):
    current = INITIAL
    states = [current]

    for event in events:
        current = transition(current, event)
        assert current is not None
        states.append(current)

    return states


def minimize(reachable):
    def output_signature(state):
        if state == SINK:
            return ("error", None, None)
        k, sign, mode = state
        return (
            k % 4,
            sign if mode == "receipt" else None,
            mode == "receipt",
        )

    def total_transition(state, event):
        if state == SINK:
            return SINK
        target = transition(state, event)
        return SINK if target is None else target

    all_states = list(reachable) + [SINK]
    grouped = {}

    for state in all_states:
        grouped.setdefault(output_signature(state), set()).add(state)

    partitions = list(grouped.values())

    while True:
        index = {}

        for number, block in enumerate(partitions):
            for state in block:
                index[state] = number

        refined = []

        for block in partitions:
            split = {}

            for state in block:
                signature = (
                    output_signature(state),
                    tuple(
                        index[total_transition(state, event)]
                        for event in EVENTS
                    ),
                )
                split.setdefault(signature, set()).add(state)

            refined.extend(split.values())

        old = sorted(
            sorted(key(state) for state in block)
            for block in partitions
        )
        new = sorted(
            sorted(key(state) for state in block)
            for block in refined
        )

        partitions = refined

        if old == new:
            break

    return partitions


artifact = json.loads(ARTIFACT.read_text())
source = json.loads(SOURCE.read_text())

assert artifact["audit_pass"] is True
assert artifact["status"] == "author_supplied_general_apparatus_contract"
assert source["audit_pass"] is True
assert sha256_file(SOURCE) == artifact["source_lock"]["sha256"]

homomorphism_failures = []

for a in range(8):
    for b in range(8):
        if ((a + b) % 8) % 4 != ((a % 4) + (b % 4)) % 4:
            homomorphism_failures.append([a, b])

assert homomorphism_failures == []
assert [value for value in range(8) if value % 4 == 0] == [0, 4]
assert (4 + 4) % 8 == 0

reachable, rows = enumerate_reachable()
assert len(reachable) == 19
assert len(rows) == 21
assert rows == artifact["reachable_transducer"]["transitions"]

covariance_failures = []

for state in reachable:
    reversed_state = reverse_state(state)
    assert reversed_state in reachable

    for event in EVENTS:
        target = transition(state, event)
        reversed_target = transition(
            reversed_state,
            reverse_event(event),
        )

        if target is None:
            if reversed_target is not None:
                covariance_failures.append([key(state), event])
        elif reversed_target != reverse_state(target):
            covariance_failures.append([key(state), event])

assert covariance_failures == []

plus_events = artifact["response_cycles"]["plus"]["events"]
minus_events = artifact["response_cycles"]["minus"]["events"]

plus_states = execute(plus_events)
minus_states = execute(minus_events)

assert plus_states[-1] == (4, 1, "receipt")
assert minus_states[-1] == (4, -1, "receipt")
assert plus_states[-1][0] % 4 == INITIAL[0] % 4
assert minus_states[-1][0] % 4 == INITIAL[0] % 4
assert plus_states[-1] != INITIAL
assert minus_states[-1] != INITIAL

partitions = minimize(reachable)
non_sink = [block for block in partitions if SINK not in block]

assert len(non_sink) == 19

supersession = artifact["artifact201_supersession"]

assert supersession["status"] == "partially_superseded_by_apparatus_contract_204"
assert supersession["historical_artifact_mutated"] is False
assert supersession["historical_audit_invalidated"] is False

checks = artifact["checks"]

required_true = [
    "exact_c2_c8_c4_extension",
    "quarter_turn_generator_order8",
    "visible_orientation_order4",
    "full_turn_kernel_nontrivial",
    "signed_action_latch_required",
    "typed_control_modes_required",
    "reachable_state_count_19",
    "defined_transition_count_21",
    "reachable_transducer_minimal",
    "reversal_covariance_exact",
    "response_360_180_360_exact",
    "visible_return_exact",
    "lifted_receipt_nontrivial",
    "plus_minus_receipts_distinct",
    "artifact201_partial_supersession_recorded",
]

required_false = [
    "native_physical_realization_derived",
    "electron_claim",
    "gravity_claim",
    "radiation_claim",
    "physics_claim",
]

assert all(checks[key] is True for key in required_true)
assert all(checks[key] is False for key in required_false)

print("AUDIT_PASS: true")
print("APPARATUS_STATUS:", artifact["status"])
print("C8_C4_EXTENSION_EXACT: true")
print("REACHABLE_STATE_COUNT:", len(reachable))
print("DEFINED_TRANSITION_COUNT:", len(rows))
print("MINIMIZED_REACHABLE_CLASS_COUNT:", len(non_sink))
print("REVERSAL_COVARIANCE_FAILURE_COUNT:", len(covariance_failures))
print("PLUS_FINAL_STATE:", key(plus_states[-1]))
print("MINUS_FINAL_STATE:", key(minus_states[-1]))
print("VISIBLE_RETURN_EXACT: true")
print("SIGNED_RECEIPTS_DISTINCT: true")
print("ARTIFACT201_PARTIALLY_SUPERSEDED: true")
print("PHYSICS_CLAIM: false")
print("VERDICT:", artifact["verdict"])
