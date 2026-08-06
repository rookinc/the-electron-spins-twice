from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

TARGET = Path(__file__).resolve().parents[2]
CHECKPOINT = TARGET / "artifacts/json/native_orientation_archive_terminal_checkpoint_184.v1.json"

def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def compose(p, q):
    return tuple(p[q[x]] for x in range(len(p)))

def inverse(p):
    out = [0] * len(p)
    for i, value in enumerate(p):
        out[value] = i
    return tuple(out)

def order(p):
    identity = tuple(range(len(p)))
    power = identity
    for n in range(1, 61):
        power = compose(p, power)
        if power == identity:
            return n
    raise ValueError("order bound exceeded")

def conjugate(g, p):
    return compose(compose(g, p), inverse(g))

def canonical_pair(pair, gauges):
    return min(
        conjugate(g, pair[0]) + conjugate(g, pair[1])
        for g in gauges
    )

checkpoint = json.loads(CHECKPOINT.read_text())

for source in checkpoint["sources"].values():
    path = Path(source["path"])
    assert path.exists()
    assert sha256_file(path) == source["sha256"]

obstruction = json.loads(
    Path(checkpoint["sources"]["artifact180"]["path"]).read_text()
)
g5 = json.loads(
    Path(checkpoint["sources"]["g5_oriented_lift"]["path"]).read_text()
)

assert obstruction["audit_pass"] is True
assert obstruction["verdict"] == (
    "intrinsic_mirror_selects_offset4_but_clean_data_leave_offsets1_and2_exchanged"
)

r_plus = (1, 2, 1, 3, 1)
r_minus = (1, 3, 1, 2, 1)
gram = [
    [dot(r_plus, r_plus), dot(r_plus, r_minus)],
    [dot(r_minus, r_plus), dot(r_minus, r_minus)],
]
assert gram == [[16, 15], [15, 16]]
assert gram[0][0] * gram[1][1] - gram[0][1] * gram[1][0] == 31

s3 = [tuple(p) for p in itertools.permutations(range(3))]
order2 = [p for p in s3 if order(p) == 2]
order3 = [p for p in s3 if order(p) == 3]
classes = {
    canonical_pair((a, b), s3)
    for a in order2
    for b in order3
}
assert len(classes) == 1

assert any(
    row["group"] == "C4"
    and row["split"] is False
    and row["normalized_cocycle_f_1_1"] == 1
    for row in g5["central_extension_census"]
)

assert g5["measurements"]["literal_action_order"] == 2
assert g5["measurements"]["literal_action_square_sign"] == 1
assert g5["open_boundary"]["local_g5_forces_nonsplit_c4_lift"] is False
assert g5["open_boundary"]["literal_oriented_g5_action_is_nonsplit"] is False
assert g5["open_boundary"]["construction_filtration_selects_cocycle"] is False

nonsplit = [
    row for row in g5["signed_lift_census"]
    if row["extension_class"] == "nonsplit"
    and row["lift_order"] == 4
    and row["square_sign"] == -1
]
assert len(nonsplit) == 2

pair0 = [
    nonsplit[0]["minus_to_plus"],
    nonsplit[0]["plus_to_minus"],
]
pair1 = [
    nonsplit[1]["minus_to_plus"],
    nonsplit[1]["plus_to_minus"],
]
assert pair1 == [-value for value in pair0]

checks = checkpoint["checks"]

expected_true = [
    "artifact180_locked",
    "receipt_gram_exact",
    "receipt_gram_selects_orientation_line",
    "g5_contains_nonsplit_C4_extension",
    "g5_literal_action_selects_split_square_plus_one",
    "g5_nonsplit_C4_lifts_are_inverse_pair",
    "offset4_native",
    "offset1_and_offset2_remain_exchanged",
]

expected_false = [
    "receipt_gram_selects_orientation_sign",
    "g5_forces_nonsplit_C4_lift",
    "g5_selects_one_C4_lift_sign",
    "clean_source_to_target_generator_sign_bridge_present",
    "offset1_selected_premultiplier",
    "offset2_selected_premultiplier",
    "b32k_cardinality_derived",
]

assert all(checks[key] is True for key in expected_true)
assert all(checks[key] is False for key in expected_false)
assert checkpoint["boundary"]["global_nonexistence_of_deeper_native_orientation_proved"] is False

print("AUDIT_PASS: true")
print("RECEIPT_GRAM:", json.dumps(gram, separators=(",", ":")))
print("RECEIPT_GRAM_EIGENVALUES: [31,1]")
print("BARE_S3_PAIR_CONJUGACY_CLASS_COUNT:", len(classes))
print("G5_NONSPLIT_C4_LIFT_COUNT:", len(nonsplit))
print("G5_NONSPLIT_LIFT_PAIRS:", json.dumps([pair0, pair1], separators=(",", ":")))
print("G5_NONSPLIT_LIFTS_ARE_INVERSE_PAIR: true")
print("OFFSET4_NATIVE: true")
print("OFFSET1_PREMULTIPLIER_SELECTED: false")
print("OFFSET2_PREMULTIPLIER_SELECTED: false")
print("VERDICT:", checkpoint["classification"])
