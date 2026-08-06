from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

TARGET = Path(__file__).resolve().parents[2]

CONTRACT = TARGET / "artifacts/json/lawful_informative_action_orientation_contract_185.v1.json"
HISTORY = TARGET / "artifacts/json/g5_history_filtration_crucible_002.json"
ARTIFACT = TARGET / "artifacts/json/action_aware_emergence_candidate_theorem_195.v1.json"

EXPECTED_CONTRACT_SHA = "a940c408b4728c8e82da17e2e9098229ba6fe830618142c89ce187e9da9ef70a"
EXPECTED_HISTORY_SHA = "0fe630a0b871c09dd808d498c3c73843e0556f905b1018b04b983002d545a76c"


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


assert sha256_file(CONTRACT) == EXPECTED_CONTRACT_SHA
assert sha256_file(HISTORY) == EXPECTED_HISTORY_SHA

history = json.loads(HISTORY.read_text())
artifact = json.loads(ARTIFACT.read_text())

edges = {
    row[0]: (row[1], row[2])
    for row in history["history_model"]["edges"]
}

assert edges["plus_out"] == ("G4_plus", "G5")
assert edges["minus_out"] == ("G4_minus", "G5")

boundary = history["model_boundary"]
assert boundary["plus_history_is_source_ordered_branch"] is True
assert boundary["minus_history_is_derived_mirror_branch"] is True

edge_mirror = {
    "plus_out": "minus_out",
    "minus_out": "plus_out",
}

sign_maps = []
for values in itertools.permutations([-1, 1]):
    sign_map = dict(zip(["minus_out", "plus_out"], values))
    equivariant = all(
        sign_map[edge_mirror[edge]] == -sign_map[edge]
        for edge in edge_mirror
    )
    if equivariant:
        sign_maps.append(sign_map)

anchored = [
    sign_map
    for sign_map in sign_maps
    if sign_map["plus_out"] == 1
]

assert len(sign_maps) == 2
assert len(anchored) == 1
assert anchored[0] == {"minus_out": -1, "plus_out": 1}

plus = artifact["new_post_g5_construction"]["plus"]
minus = artifact["new_post_g5_construction"]["minus"]

assert plus["native_incidence_state"] == ["plus_out", "G5"]
assert minus["native_incidence_state"] == ["minus_out", "G5"]
assert plus["selected_lift"] == "H"
assert minus["selected_lift"] == "H_inverse"
assert plus["conditional_successor_offset"] == 1
assert minus["conditional_successor_offset"] == 2

assert plus["signed_return_state"] == "1_after_6_plus"
assert minus["signed_return_state"] == "1_after_6_minus"
assert plus["signed_stage7"] == "plus_7"
assert minus["signed_stage7"] == "minus_7"
assert plus["signed_stage8_receipt"] == "8_plus"
assert minus["signed_stage8_receipt"] == "8_minus"

checks = artifact["checks"]
assert checks["native_g5_branch_core_bound"] is True
assert checks["native_arriving_incidence_sign_carrier_bound"] is True
assert checks["source_order_anchor_selects_unique_sign_character"] is True
assert checks["post_g5_signed_continuation_constructed"] is True
assert checks["full_signed_continuations_mirror_equivariant"] is True
assert checks["drawing_quotient_recovered"] is True
assert checks["forward_action_conditionally_selects_offset1"] is True
assert checks["reverse_action_conditionally_selects_offset2"] is True
assert checks["unconditional_offset1_selected"] is False
assert checks["post_g5_extension_recovered_from_old_source"] is False
assert checks["complete_native_g900_transport_operator_bound"] is False
assert checks["physics_claim"] is False

assert artifact["new_post_g5_construction"]["bare_quotient_tail"] == [
    "6",
    "1",
    "7",
    "8",
]

assert artifact["audit_pass"] is True
assert artifact["status"] == "author_supplied_candidate_construction_theorem"

print("AUDIT_PASS: true")
print("MIRROR_EQUIVARIANT_SIGN_CHARACTER_COUNT:", len(sign_maps))
print("SOURCE_ORDER_ANCHORED_SIGN_CHARACTER_COUNT:", len(anchored))
print(
    "ANCHORED_SIGN_CHARACTER:",
    json.dumps(anchored[0], sort_keys=True, separators=(",", ":")),
)
print(
    "NATIVE_ARRIVING_INCIDENCE_STATES:",
    json.dumps(
        artifact["native_old_source_theorem"]["arriving_incidence_states"],
        separators=(",", ":"),
    ),
)
print(
    "FORWARD_SIGNED_CONTINUATION:",
    json.dumps(
        [
            plus["native_incidence_state"],
            plus["signed_return_state"],
            plus["signed_stage7"],
            plus["signed_stage8_receipt"],
        ],
        separators=(",", ":"),
    ),
)
print(
    "REVERSE_SIGNED_CONTINUATION:",
    json.dumps(
        [
            minus["native_incidence_state"],
            minus["signed_return_state"],
            minus["signed_stage7"],
            minus["signed_stage8_receipt"],
        ],
        separators=(",", ":"),
    ),
)
print("FORWARD_CONDITIONAL_OFFSET:", plus["conditional_successor_offset"])
print("REVERSE_CONDITIONAL_OFFSET:", minus["conditional_successor_offset"])
print("UNCONDITIONAL_OFFSET1_SELECTED:", str(checks["unconditional_offset1_selected"]).lower())
print("PHYSICS_CLAIM:", str(checks["physics_claim"]).lower())
print("VERDICT:", artifact["verdict"])
