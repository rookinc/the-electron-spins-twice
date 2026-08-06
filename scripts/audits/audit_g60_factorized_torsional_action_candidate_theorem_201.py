from __future__ import annotations

import hashlib
import json
from pathlib import Path

TARGET = Path(__file__).resolve().parents[2]

SOURCE = TARGET / "artifacts/json/g60_finite_torsional_response_contract_197.v1.json"
ARTIFACT = TARGET / "artifacts/json/g60_factorized_torsional_action_candidate_theorem_201.v1.json"

EXPECTED_SOURCE_SHA = "6bb794ca200ad56c6d264e44b03a56f05a9c6f066dc80c0ba2abbe07644ab262"


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sign(value):
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def release(state):
    return state - sign(state)


def g900_outer(state):
    if abs(state) == 2:
        return state - sign(state)
    return state


def g15_inner(state):
    if abs(state) == 1:
        return 0
    return state


assert sha256_file(SOURCE) == EXPECTED_SOURCE_SHA

source = json.loads(SOURCE.read_text())
artifact = json.loads(ARTIFACT.read_text())

assert source["audit_pass"] is True
assert artifact["audit_pass"] is True
assert artifact["status"] == "author_supplied_candidate_dynamics_theorem"

states = artifact["finite_twist_register"]["states"]
assert states == [-2, -1, 0, 1, 2]

factor_failures = []

for state in states:
    composed = g900_outer(g15_inner(state))
    expected = release(state)
    if composed != expected:
        factor_failures.append([state, composed, expected])

assert factor_failures == []

cycles = artifact["response_cycles"]
assert len(cycles) == 2

forward = next(row for row in cycles if row["branch_sign"] == 1)
reverse = next(row for row in cycles if row["branch_sign"] == -1)

assert forward["path_pi_units"] == [0, 1, 2, 1, 0]
assert reverse["path_pi_units"] == [0, -1, -2, -1, 0]
assert reverse["path_pi_units"] == [
    -value for value in forward["path_pi_units"]
]

ledger_failures = []

for cycle in cycles:
    for row in cycle["ledger_rows"]:
        delta = row["after"] - row["before"]
        total = (
            row["external_drive"]
            + row["g900_restoration"]
            + row["g15_backaction"]
        )
        if delta != total or row["balance_passes"] is not True:
            ledger_failures.append(
                [cycle["branch_sign"], row["stage"], delta, total]
            )

assert ledger_failures == []

for cycle in cycles:
    rows = cycle["ledger_rows"]
    external = sum(row["external_drive"] for row in rows)
    g900 = sum(row["g900_restoration"] for row in rows)
    g15 = sum(row["g15_backaction"] for row in rows)
    assert external + g900 + g15 == 0
    assert rows[0]["before"] == 0
    assert rows[-1]["after"] == 0

emission_rows = [
    row
    for cycle in cycles
    for row in cycle["ledger_rows"]
    if row["emission_angle_degrees"] is not None
]

assert len(emission_rows) == 2
assert all(row["emission_angle_degrees"] == 180 for row in emission_rows)
assert all(row["g15_backaction"] == -row["before"] for row in emission_rows)
assert all(row["after"] == 0 for row in emission_rows)

uniqueness_failures = []

for state in [-1, 1]:
    solutions = [
        action
        for action in [-2, -1, 0, 1, 2]
        if state + action == 0
    ]
    if solutions != [-state]:
        uniqueness_failures.append([state, solutions])

assert uniqueness_failures == []

assert forward["final_receipt"] == "8_plus"
assert reverse["final_receipt"] == "8_minus"
assert forward["conditional_offset"] == 1
assert reverse["conditional_offset"] == 2

checks = artifact["checks"]

required_true = [
    "five_state_operator_exact",
    "operator_reversal_covariant",
    "operator_bounded",
    "orthogonal_passage_holds_state",
    "passage_release_control_bit_required",
    "minimum_release_factorization_exact",
    "g900_outer_jurisdiction_declared",
    "g15_inner_jurisdiction_declared",
    "perfect_180_emission_typed",
    "g15_backaction_unique_given_equilibrium_target",
    "finite_action_ledger_balanced",
    "signed_receipt_preserved_at_equilibrium",
]

required_false = [
    "native_g900_operator_bound",
    "native_g15_operator_bound",
    "native_emission_operator_bound",
    "continuous_momentum_law_derived",
    "energy_conservation_law_derived",
    "physical_emission_claim",
    "physical_electron_claim",
    "physical_gravity_claim",
    "physics_claim",
]

assert all(checks[key] is True for key in required_true)
assert all(checks[key] is False for key in required_false)

print("AUDIT_PASS: true")
print("THEOREM_STATUS:", artifact["status"])
print("TWIST_STATES:", states)
print("FACTORIZATION_FAILURE_COUNT:", len(factor_failures))
print("LEDGER_FAILURE_COUNT:", len(ledger_failures))
print("BACKACTION_UNIQUENESS_FAILURE_COUNT:", len(uniqueness_failures))
print("FORWARD_PATH:", forward["path_pi_units"])
print("REVERSE_PATH:", reverse["path_pi_units"])
print("FORWARD_RECEIPT:", forward["final_receipt"])
print("REVERSE_RECEIPT:", reverse["final_receipt"])
print("FINITE_ACTION_LEDGER_BALANCED: true")
print("PHYSICS_CLAIM: false")
print("VERDICT:", artifact["verdict"])
