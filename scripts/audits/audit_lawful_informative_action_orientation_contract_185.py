from __future__ import annotations

import hashlib
import json
from pathlib import Path

TARGET = Path(__file__).resolve().parents[2]
ARTIFACT = TARGET / "artifacts/json/lawful_informative_action_orientation_contract_185.v1.json"

def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def compose(p, q):
    return [p[q[index]] for index in range(len(p))]

artifact = json.loads(ARTIFACT.read_text())
prior = artifact["source_authority"]["prior_theorem"]
prior_path = Path(prior["path"])

assert prior_path.exists()
assert sha256_file(prior_path) == prior["sha256"]

checkpoint = json.loads(prior_path.read_text())
assert checkpoint["audit_pass"] is True
assert checkpoint["classification"] == (
    "bounded_archive_complete_native_mirror_axis_with_unresolved_C4_and_D5_orientation_sign"
)

objects = artifact["objects"]
positive = objects["target_positive_rotation"]
negative = objects["target_negative_rotation"]
reflection = objects["target_reflection"]
identity = list(range(5))

assert compose(reflection, reflection) == identity
assert reflection[4] == 4
assert positive[4] == 1
assert negative[4] == 2
assert reflection[1] == 2
assert reflection[2] == 1
assert compose(compose(reflection, positive), reflection) == negative

rows = artifact["conditional_target_readout"]
assert len(rows) == 2
assert rows[0] == {
    "action_orientation": "forward",
    "selected_lift": "H",
    "mirror_offset": 4,
    "successor_offset": 1,
}
assert rows[1] == {
    "action_orientation": "reverse",
    "selected_lift": "H_inverse",
    "mirror_offset": 4,
    "successor_offset": 2,
}

checks = artifact["checks"]

expected_true = [
    "artifact184_locked",
    "reflection_is_involution",
    "reflection_fixes_offset4",
    "positive_generator_sends_offset4_to_offset1",
    "negative_generator_sends_offset4_to_offset2",
    "reflection_conjugates_positive_to_negative",
    "action_reversal_exchanges_orientation_lifts",
    "action_reversal_exchanges_offsets1_and2",
    "candidate_contract_only",
]

expected_false = [
    "unoriented_action_selects_orientation",
    "absolute_internal_orientation_claimed",
    "orthogonal_pairing_constructed",
    "admission_predicate_constructed",
    "action_incidence_encoder_constructed",
    "transport_operator_constructed",
    "premultiplier_offset1_unconditionally_selected",
    "physics_claim",
]

assert all(checks[key] is True for key in expected_true)
assert all(checks[key] is False for key in expected_false)

boundary = artifact["open_boundary"]
assert boundary["orthogonality_pairing_defined"] is False
assert boundary["unique_orientation_for_every_admitted_action_proved"] is False
assert boundary["reversal_covariance_tested_on_native_actions"] is False
assert boundary["incidence_transport_operator_constructed"] is False
assert boundary["offset1_selected_without_action_input"] is False
assert boundary["physics_claim"] is False

assert artifact["status"] == "author_supplied_candidate_construction_contract"
assert artifact["source_authority"]["archive_recovery_claim"] is False

print("AUDIT_PASS: true")
print("CONTRACT_STATUS:", artifact["status"])
print("NATIVE_MIRROR_OFFSET: 4")
print("FORWARD_ACTION_SUCCESSOR_OFFSET: 1")
print("REVERSE_ACTION_SUCCESSOR_OFFSET: 2")
print("REVERSAL_COVARIANCE_SCHEMA_EXACT: true")
print("ORTHOGONALITY_PAIRING_CONSTRUCTED: false")
print("ADMISSION_PREDICATE_CONSTRUCTED: false")
print("TRANSPORT_OPERATOR_CONSTRUCTED: false")
print("UNCONDITIONAL_OFFSET1_SELECTOR_CLAIMED: false")
print("VERDICT:", artifact["classification"])
