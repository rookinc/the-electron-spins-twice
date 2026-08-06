from __future__ import annotations

import hashlib
import json
from pathlib import Path

TARGET = Path(__file__).resolve().parents[2]

SOURCE = TARGET / "artifacts/json/action_aware_emergence_candidate_theorem_195.v1.json"
ARTIFACT = TARGET / "artifacts/json/g60_finite_torsional_response_contract_197.v1.json"

EXPECTED_SOURCE_SHA = "957c8342f5d2206c22b961c23f5e9f323342f790526ae16ccc5884017759bd7d"


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


assert sha256_file(SOURCE) == EXPECTED_SOURCE_SHA

source = json.loads(SOURCE.read_text())
artifact = json.loads(ARTIFACT.read_text())

assert source["audit_pass"] is True
assert artifact["audit_pass"] is True
assert artifact["status"] == "author_supplied_candidate_dynamics_contract"
assert artifact["scope"]["archive_search_continued"] is False
assert artifact["scope"]["new_forward_theory"] is True

rows = artifact["twist_register"]["rows"]
assert len(rows) == 5

by_twist = {
    row["twist_units_pi"]: row
    for row in rows
}

assert sorted(by_twist) == [-2, -1, 0, 1, 2]

reversal_failures = []
restoration_failures = []

for twist, row in sorted(by_twist.items()):
    reverse = by_twist[-twist]

    if row["bare_orientation_class_mod_2"] != reverse["bare_orientation_class_mod_2"]:
        reversal_failures.append([twist, "bare_class"])

    if row["candidate_gravity_observable"] != reverse["candidate_gravity_observable"]:
        reversal_failures.append([twist, "gravity_threshold"])

    if row["first_limit_reached"] != reverse["first_limit_reached"]:
        reversal_failures.append([twist, "first_limit"])

    if row["candidate_g60_action_is_maximum"] != reverse["candidate_g60_action_is_maximum"]:
        reversal_failures.append([twist, "maximum_action"])

    next_twist = row["restoration_next_twist_units_pi"]

    if twist == 0:
        if next_twist != 0:
            restoration_failures.append([twist, next_twist])
    elif abs(next_twist) != abs(twist) - 1:
        restoration_failures.append([twist, next_twist])

assert by_twist[0]["selected_lift"] is None
assert by_twist[0]["conditional_offset"] is None

for twist in [1, 2]:
    assert by_twist[twist]["selected_lift"] == "H"
    assert by_twist[twist]["conditional_offset"] == 1

for twist in [-1, -2]:
    assert by_twist[twist]["selected_lift"] == "H_inverse"
    assert by_twist[twist]["conditional_offset"] == 2

assert by_twist[1]["candidate_gravity_observable"] is True
assert by_twist[-1]["candidate_gravity_observable"] is True
assert by_twist[0]["candidate_gravity_observable"] is False

assert by_twist[2]["first_limit_reached"] is True
assert by_twist[-2]["first_limit_reached"] is True
assert by_twist[2]["candidate_g60_action_is_maximum"] is True
assert by_twist[-2]["candidate_g60_action_is_maximum"] is True

assert by_twist[2]["bare_orientation_class_mod_2"] == 0
assert by_twist[-2]["bare_orientation_class_mod_2"] == 0
assert by_twist[0]["bare_orientation_class_mod_2"] == 0

assert reversal_failures == []
assert restoration_failures == []

checks = artifact["checks"]

required_true = [
    "finite_twist_register_defined",
    "perfectly_orthogonal_passage_defined",
    "nonorthogonal_signed_drive_defined",
    "action_reversal_covariance_defined",
    "half_twist_candidate_threshold_defined",
    "full_turn_candidate_limit_defined",
    "g15_restoration_role_declared",
    "g900_restoration_role_declared",
]

required_false = [
    "native_action_magnitude_encoder_bound",
    "native_torque_operator_bound",
    "native_electron_potential_derived",
    "native_gravity_observable_derived",
    "native_maximum_action_law_derived",
    "native_restoration_dynamics_derived",
    "physical_electron_claim",
    "physical_gravity_claim",
]

assert all(checks[key] is True for key in required_true)
assert all(checks[key] is False for key in required_false)

print("AUDIT_PASS: true")
print("CONTRACT_STATUS:", artifact["status"])
print("TWIST_STATE_COUNT:", len(rows))
print("TWIST_STATES_PI_UNITS:", sorted(by_twist))
print("REVERSAL_FAILURE_COUNT:", len(reversal_failures))
print("RESTORATION_FAILURE_COUNT:", len(restoration_failures))
print("BARE_ZERO_ORIENTATION_CLASS_STATES:", [-2, 0, 2])
print("HALF_TURN_CANDIDATE_GRAVITY_STATES:", [-1, 1])
print("FIRST_LIMIT_MAXIMUM_ACTION_STATES:", [-2, 2])
print("ORTHOGONAL_PASSAGE_DEFINED: true")
print("NATIVE_ELECTRON_POTENTIAL_DERIVED: false")
print("NATIVE_GRAVITY_OBSERVABLE_DERIVED: false")
print("PHYSICAL_GRAVITY_CLAIM: false")
print("VERDICT:", artifact["verdict"])
