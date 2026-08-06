from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

TARGET = Path(__file__).resolve().parents[2]
P44 = Path.home() / "dev/cori/research/mathematics/44-c5-c3-orientation-mechanism"

TRANSPORT = P44 / "artifacts/json/project41_three_sheet_transport_native_origin_audit_002.v1.json"
ARTIFACT = TARGET / "artifacts/json/native_multiplier_reflection_axis_rotation_sign_obstruction_180.v1.json"

EXPECTED_TRANSPORT_SHA = "e2c90d608d2ab80aff64b84a1684cc8b83248bb29f72de27c7c02bdc0e1baf83"


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def compose(p, q):
    return [p[q[x]] for x in range(len(p))]


def inverse(p):
    out = [0] * len(p)
    for i, value in enumerate(p):
        out[value] = i
    return out


def order(p):
    ident = list(range(len(p)))
    power = ident
    for n in range(1, 61):
        power = compose(p, power)
        if power == ident:
            return n
    raise ValueError("order bound exceeded")


def fixed(p):
    return [x for x in range(len(p)) if p[x] == x]


def betas(rotation, reflection, target_rotation, target_reflection):
    found = []
    for candidate in itertools.permutations(range(5)):
        beta = list(candidate)
        if all(beta[rotation[x]] == target_rotation[beta[x]] for x in range(5)) and all(
            beta[reflection[x]] == target_reflection[beta[x]] for x in range(5)
        ):
            found.append(beta)
    return found


assert sha256_file(TRANSPORT) == EXPECTED_TRANSPORT_SHA
transport = json.loads(TRANSPORT.read_text())
artifact = json.loads(ARTIFACT.read_text())

edge_order = {}
for row in transport["oriented_transport_rows"]:
    edge = tuple(row["oriented_block_edge"])
    permutation = row["native_matching_permutation"]
    edge_order[edge] = order(permutation)

assert len(edge_order) == 20

perms = [list(p) for p in itertools.permutations(range(5))]
rotations = [p for p in perms if order(p) == 5]
reflections = [p for p in perms if order(p) == 2 and len(fixed(p)) == 1]

actions = []
for rotation in rotations:
    for reflection in reflections:
        if compose(compose(reflection, rotation), reflection) == inverse(rotation):
            actions.append((rotation, reflection))

grammar = []
profiles = {}
for rotation, reflection in actions:
    mark = fixed(reflection)[0]
    successor = rotation[mark]
    for base in range(5):
        if base in (mark, successor):
            continue
        first = edge_order[(base, mark)]
        second = edge_order[(base, successor)]
        if sorted([first, second]) != [2, 3]:
            continue
        profile = (1, first, 1, second, 1)
        profiles[profile] = profiles.get(profile, 0) + 1
        grammar.append((rotation, reflection, base, mark, successor))

T = [2, 3, 4, 0, 1]
T_inverse = inverse(T)
U = [3, 2, 1, 0, 4]

assert len(rotations) == 24
assert len(reflections) == 15
assert len(actions) == 120
assert len(grammar) == 72
assert profiles == {(1, 2, 1, 3, 1): 36, (1, 3, 1, 2, 1): 36}
assert fixed(U) == [4]
assert compose(compose(U, T), U) == T_inverse

positive_successors = set()
negative_successors = set()
positive_marks = set()
negative_marks = set()

for rotation, reflection, base, mark, successor in grammar:
    positive = betas(rotation, reflection, T, U)
    negative = betas(rotation, reflection, T_inverse, U)
    assert len(positive) == 1
    assert len(negative) == 1
    assert negative[0] == compose(U, positive[0])

    positive_marks.add(positive[0][mark])
    negative_marks.add(negative[0][mark])
    positive_successors.add(positive[0][successor])
    negative_successors.add(negative[0][successor])

assert positive_marks == {4}
assert negative_marks == {4}
assert positive_successors == {1}
assert negative_successors == {2}
assert artifact["checks"]["current_clean_data_select_offset1_invariantly"] is False
assert artifact["verdict"] == "intrinsic_mirror_selects_offset4_but_clean_data_leave_offsets1_and2_exchanged"

print("AUDIT_PASS: true")
print("ORIENTED_D5_ACTION_COUNT:", len(actions))
print("UNORDERED_RECEIPT_COUNT:", len(grammar))
print("PROFILE_COUNTS:", json.dumps({str(k): v for k, v in profiles.items()}, sort_keys=True))
print("POSITIVE_SUCCESSOR_OFFSETS:", sorted(positive_successors))
print("NEGATIVE_SUCCESSOR_OFFSETS:", sorted(negative_successors))
print("VERDICT:", artifact["verdict"])
