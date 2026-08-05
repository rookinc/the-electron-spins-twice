from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

PACKET_NAME = "electron_spins_twice_registered_multiplier_decorated_recentered_seam_theorem_090"
HOME = Path.home()
TARGET = HOME / "dev/cori/research/physics/quantum_mechanics/01-the-electron-spins-twice"
PROJECT41 = HOME / "dev/cori/research/mathematics/41-order-4-dodecahedral-residue"
CANDIDATE = HOME / "storage/downloads/inspect_pentagram_multiplier_anchor_geometry_028m16.py"
REPORT = HOME / "tmp/electron_spins_twice_registered_multiplier_decorated_recentered_seam_theorem_090_out.txt"

EXPECTED_CANDIDATE_HASH = (
    "d38e4069e1bc721cab1f79d4d3ec3802dc3191e5e599f50fd1fc4a0ed55d45c3"
)

SOURCE_SPECS = {
    "audit019": (
        "a5_v4_k22_four_slot_alignment_audit_019.json",
        "e8bbfe48053bdc1a80407ce7a26bf02b12f83bfcf695fed0073a9a8581ae896a",
    ),
    "audit028c": (
        "nested_dodecahedral_registration_audit_028c.json",
        "83cae85f200ff774ab45875cfddd265be1be59c9bde8a4bc7c5737c5a3855f6f",
    ),
    "audit028d": (
        "registration_antipode_d5_orientation_audit_028d.json",
        "869bb29956426d8c8e2aaaf6f9b49e7b934d4a340ee043629fccf5a044f59c39",
    ),
    "audit028e": (
        "canonical_seam_carrier_offset_audit_028e.json",
        "19a5818b817f241bcb285b6ddfefedd7d9dde818a4538b44d93543f81f47b49b",
    ),
}

lines: list[str] = []


def emit(key: str, value: Any = "") -> None:
    if isinstance(value, (dict, list, tuple, bool)) or value is None:
        rendered = json.dumps(value, sort_keys=True, separators=(",", ":"))
    else:
        rendered = str(value)
    lines.append(f"{key}: {rendered}")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"Expected JSON object: {path}")
    return value


def require_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be a dict")
    return value


def require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise TypeError(f"{label} must be a list")
    return value


def int_tuple(value: Any, label: str) -> tuple[int, ...]:
    return tuple(int(v) for v in require_list(value, label))


def git_snapshot(root: Path) -> dict[str, Any]:
    def run(*args: str) -> tuple[int, str]:
        proc = subprocess.run(
            ["git", *args],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        return proc.returncode, proc.stdout.rstrip()

    head_rc, head = run("rev-parse", "HEAD")
    status_rc, status = run("status", "--short", "--branch")
    diff_rc, diff = run("diff", "--no-ext-diff")
    cached_rc, cached = run("diff", "--cached", "--no-ext-diff")
    return {
        "head": head if head_rc == 0 else "",
        "status": status,
        "status_rc": status_rc,
        "diff_rc": diff_rc,
        "cached_diff_rc": cached_rc,
        "diff_sha256": hashlib.sha256(diff.encode()).hexdigest(),
        "cached_diff_sha256": hashlib.sha256(cached.encode()).hexdigest(),
    }


TARGET_BEFORE = git_snapshot(TARGET)
PROJECT41_BEFORE = git_snapshot(PROJECT41)
candidate_hash_before = sha256_file(CANDIDATE) if CANDIDATE.is_file() else ""

payloads: dict[str, dict[str, Any]] = {}
source_records = []

for label, (filename, expected_hash) in SOURCE_SPECS.items():
    matches = sorted(path for path in PROJECT41.rglob(filename) if path.is_file())
    record = {
        "label": label,
        "filename": filename,
        "match_count": len(matches),
        "path": str(matches[0]) if len(matches) == 1 else "",
        "sha256": "",
        "hash_match": False,
        "audit_pass": False,
        "verdict": "",
    }
    if len(matches) == 1:
        payload = load_json(matches[0])
        actual_hash = sha256_file(matches[0])
        payloads[label] = payload
        record.update({
            "sha256": actual_hash,
            "hash_match": actual_hash == expected_hash,
            "audit_pass": payload.get("audit_pass") is True,
            "verdict": payload.get("verdict", ""),
        })
    source_records.append(record)

sources_ready = (
    len(payloads) == 4
    and all(row["match_count"] == 1 for row in source_records)
    and all(row["hash_match"] for row in source_records)
    and all(row["audit_pass"] for row in source_records)
)

m19 = require_dict(payloads["audit019"]["measurements"], "Audit019 measurements")
m28c = require_dict(payloads["audit028c"]["measurements"], "Audit028C measurements")
m28d = require_dict(payloads["audit028d"]["measurements"], "Audit028D measurements")
m28e = require_dict(payloads["audit028e"]["measurements"], "Audit028E measurements")

# Reconstruct the Audit019 state table.

state_records: dict[int, dict[str, Any]] = {}
state_record_failures = []
alignment_rows = require_list(m19["alignment_rows"], "Audit019 alignment_rows")

for alignment_index, raw_alignment in enumerate(alignment_rows):
    alignment = require_dict(raw_alignment, "Audit019 alignment")
    native_g15_state = int(alignment["native_g15_state"])
    source_edge = int_tuple(
        alignment["source_petersen_edge"],
        "Audit019 source edge",
    )
    multipliers = int_tuple(
        alignment["pentagram_twist_multipliers"],
        "Audit019 multipliers",
    )
    coordinate_rows = require_list(
        alignment["state_coordinates"],
        "Audit019 state coordinates",
    )
    coordinate_states = set()

    for raw_coordinate in coordinate_rows:
        coordinate_row = require_dict(raw_coordinate, "Audit019 coordinate row")
        state = int(coordinate_row["g60_state"])
        coordinate = int_tuple(
            coordinate_row["coordinate"],
            "Audit019 coordinate",
        )
        coordinate_states.add(state)
        record = {
            "state": state,
            "native_g15_state": native_g15_state,
            "source_petersen_edge": source_edge,
            "coordinate": coordinate,
            "multipliers": multipliers,
            "alignment_index": alignment_index,
        }
        if state in state_records:
            state_record_failures.append({
                "state": state,
                "failure": "duplicate state",
            })
        state_records[state] = record

    fiber = set(int_tuple(
        alignment["native_v4_g60_fiber"],
        "Audit019 native fiber",
    ))
    if coordinate_states != fiber:
        state_record_failures.append({
            "alignment_index": alignment_index,
            "failure": "coordinate states differ from native fiber",
        })

state_table_exact = (
    len(alignment_rows) == 15
    and set(state_records) == set(range(60))
    and not state_record_failures
)
# Parse both Audit028C registrations.

anchors: dict[tuple[int, int], dict[str, Any]] = {}
arrival_occurrences: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
departure_occurrences: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
registration_failures = []

registration_rows = require_list(
    m28c["registration_rows"],
    "Audit028C registration_rows",
)

for raw_registration in registration_rows:
    registration = require_dict(raw_registration, "Audit028C registration")
    registration_index = int(registration["registration_index"])
    anchor_rows = require_list(registration["anchors"], "Audit028C anchors")

    for raw_anchor in anchor_rows:
        anchor = require_dict(raw_anchor, "Audit028C anchor")
        anchor_index = int(anchor["anchor_positive_index"])
        seam_rows = require_list(anchor["seam_rows"], "Audit028C seam rows")
        inward_states = []
        outward_states = []

        for position, raw_seam in enumerate(seam_rows):
            seam = require_dict(raw_seam, "Audit028C seam")
            inward_state = int(seam["inward_state"])
            outward_state = int(seam["outward_state"])
            inward_states.append(inward_state)
            outward_states.append(outward_state)
            arrival_occurrences[(registration_index, inward_state)].append(
                (anchor_index, position)
            )
            departure_occurrences[(registration_index, outward_state)].append(
                (anchor_index, position)
            )
            if inward_state not in state_records or outward_state not in state_records:
                registration_failures.append({
                    "registration": registration_index,
                    "anchor": anchor_index,
                    "position": position,
                    "failure": "seam state absent from Audit019",
                })

        anchors[(registration_index, anchor_index)] = {
            "registration_index": registration_index,
            "anchor_index": anchor_index,
            "inward_states": tuple(inward_states),
            "outward_states": tuple(outward_states),
            "neighbor_cycle": int_tuple(
                anchor["neighbor_cycle"],
                "Audit028C neighbor cycle",
            ),
        }

typed_register_coverage_exact = (
    set(registration["registration_index"] for registration in registration_rows)
    == {0, 1}
    and set(anchors) == {
        (registration_index, anchor_index)
        for registration_index in (0, 1)
        for anchor_index in range(12)
    }
    and not registration_failures
    and all(
        len(arrival_occurrences[(registration_index, state)]) == 1
        and len(departure_occurrences[(registration_index, state)]) == 1
        for registration_index in (0, 1)
        for state in range(60)
    )
)

# Independently select each local reflected offset by exact preservation
# of the permanent Audit019 carrier-multiplier tuple.

offset_census = []
selected_offsets: dict[tuple[int, int], int] = {}
offset_selection_failures = []

for key in sorted(anchors):
    anchor = anchors[key]
    inward_states = anchor["inward_states"]
    outward_states = anchor["outward_states"]
    candidate_rows = []

    for offset in range(5):
        comparisons = []
        for outward_position, outward_state in enumerate(outward_states):
            inward_position = (-outward_position + offset) % 5
            inward_state = inward_states[inward_position]
            outward_word = state_records[outward_state]["multipliers"]
            inward_word = state_records[inward_state]["multipliers"]
            comparisons.append(outward_word == inward_word)

        candidate_rows.append({
            "offset": offset,
            "equal_count": sum(comparisons),
            "all5_equal": all(comparisons),
        })

    exact_offsets = tuple(
        row["offset"] for row in candidate_rows if row["all5_equal"]
    )
    if len(exact_offsets) == 1:
        selected_offsets[key] = exact_offsets[0]
    else:
        offset_selection_failures.append({
            "registration": key[0],
            "anchor": key[1],
            "exact_offsets": exact_offsets,
        })

    offset_census.append({
        "registration": key[0],
        "anchor": key[1],
        "exact_offsets": exact_offsets,
        "candidate_equal_counts": {
            str(row["offset"]): row["equal_count"]
            for row in candidate_rows
        },
    })

all24_local_offsets_unique = (
    len(selected_offsets) == 24
    and not offset_selection_failures
)

# Resolve each state into one register row per registration.

register_rows = []
register_lookup: dict[tuple[int, int], dict[str, Any]] = {}
register_failures = []

for registration_index in (0, 1):
    for state in range(60):
        inward_hits = arrival_occurrences[(registration_index, state)]
        outward_hits = departure_occurrences[(registration_index, state)]

        if len(inward_hits) != 1 or len(outward_hits) != 1:
            register_failures.append({
                "registration": registration_index,
                "state": state,
                "failure": "nonunique inward or outward occurrence",
            })
            continue

        arrival_anchor, occupied_inward_position = inward_hits[0]
        departure_anchor, occupied_outward_position = outward_hits[0]
        key = (registration_index, arrival_anchor)

        if key not in selected_offsets:
            register_failures.append({
                "registration": registration_index,
                "state": state,
                "failure": "arrival anchor lacks selected offset",
            })
            continue

        offset = selected_offsets[key]
        anchor = anchors[key]
        predecessor_outward_position = (
            offset - occupied_inward_position
        ) % 5
        predecessor_state = anchor["outward_states"][
            predecessor_outward_position
        ]

        row = {
            "registration_index": registration_index,
            "state": state,
            "arrival_anchor": arrival_anchor,
            "departure_anchor": departure_anchor,
            "occupied_inward_position": occupied_inward_position,
            "occupied_outward_position": occupied_outward_position,
            "selected_offset": offset,
            "predecessor_outward_position": predecessor_outward_position,
            "predecessor_state": predecessor_state,
        }
        register_rows.append(row)
        register_lookup[(registration_index, state)] = row

two_full60_registers_reconstructed = (
    len(register_rows) == 120
    and len(register_lookup) == 120
    and not register_failures
)

# Derive the typed anchor map from the two state registers.

anchor_map_evidence: dict[int, set[int]] = defaultdict(set)
for state in range(60):
    if (0, state) in register_lookup and (1, state) in register_lookup:
        anchor_map_evidence[
            register_lookup[(0, state)]["arrival_anchor"]
        ].add(
            register_lookup[(1, state)]["arrival_anchor"]
        )

derived_anchor_map = {
    anchor: next(iter(targets))
    for anchor, targets in anchor_map_evidence.items()
    if len(targets) == 1
}
relative_positive_map = int_tuple(
    m28d["relative_positive_map"],
    "Audit028D relative_positive_map",
)
anchor_map_matches_audit028d = (
    set(derived_anchor_map) == set(range(12))
    and tuple(derived_anchor_map[index] for index in range(12))
    == relative_positive_map
)

# Reconstruct the cross-registration position map and recenter it at
# each inherited state. Search all five affine multipliers independently.

cross_rows = []
action_rows = []
cross_failures = []

for state in range(60):
    if (0, state) not in register_lookup or (1, state) not in register_lookup:
        cross_failures.append({
            "state": state,
            "failure": "missing typed register row",
        })
        continue

    left = register_lookup[(0, state)]
    right = register_lookup[(1, state)]
    left_anchor = anchors[(0, left["arrival_anchor"])]
    right_anchor = anchors[(1, right["arrival_anchor"])]
    left_inward = left_anchor["inward_states"]
    right_inward = right_anchor["inward_states"]

    if set(left_inward) != set(right_inward):
        cross_failures.append({
            "state": state,
            "failure": "registered inward-state sets differ",
        })
        continue

    right_position_by_state = {
        inward_state: position
        for position, inward_state in enumerate(right_inward)
    }
    position_map = tuple(
        right_position_by_state[inward_state]
        for inward_state in left_inward
    )
    left_zero = left["occupied_inward_position"]
    right_zero = right["occupied_inward_position"]

    exact_multipliers = tuple(
        multiplier
        for multiplier in range(5)
        if all(
            position_map[(left_zero + residue) % 5]
            == (right_zero + multiplier * residue) % 5
            for residue in range(5)
        )
    )
    multiplier = (
        exact_multipliers[0]
        if len(exact_multipliers) == 1
        else None
    )

    if multiplier is None:
        cross_failures.append({
            "state": state,
            "failure": "recentered affine multiplier not unique",
            "exact_multipliers": exact_multipliers,
            "position_map": position_map,
        })
        continue

    cross_row = {
        "state": state,
        "left_anchor": left["arrival_anchor"],
        "right_anchor": right["arrival_anchor"],
        "left_zero": left_zero,
        "right_zero": right_zero,
        "left_offset": left["selected_offset"],
        "right_offset": right["selected_offset"],
        "position_map": position_map,
        "exact_multipliers": exact_multipliers,
        "multiplier": multiplier,
    }
    cross_rows.append(cross_row)

    for residue in range(5):
        left_position = (left_zero + residue) % 5
        actual_right_position = position_map[left_position]
        predicted_right_position = (
            right_zero + multiplier * residue
        ) % 5
        action_rows.append({
            "state": state,
            "residue": residue,
            "multiplier": multiplier,
            "left_position": left_position,
            "actual_right_position": actual_right_position,
            "predicted_right_position": predicted_right_position,
            "prediction_match": (
                actual_right_position == predicted_right_position
            ),
        })
full60_multiplier_assignment_reconstructed = (
    len(cross_rows) == 60
    and not cross_failures
    and all(len(row["exact_multipliers"]) == 1 for row in cross_rows)
)
full300_coordinate_action_reconstructed = (
    len(action_rows) == 300
    and all(row["prediction_match"] for row in action_rows)
)

multiplier_by_state = {
    row["state"]: row["multiplier"]
    for row in cross_rows
}
multiplier_profile = Counter(multiplier_by_state.values())
all_multipliers_are_2_or_3 = (
    set(multiplier_by_state.values()) <= {2, 3}
    and len(multiplier_by_state) == 60
)
both_branches_order4 = all(
    pow(multiplier, 4, 5) == 1
    and pow(multiplier, 2, 5) == 4
    for multiplier in multiplier_by_state.values()
)

anchor_multiplier_sets: dict[int, dict[int, set[int]]] = {
    0: defaultdict(set),
    1: defaultdict(set),
}
for state, multiplier in multiplier_by_state.items():
    for registration_index in (0, 1):
        anchor_multiplier_sets[registration_index][
            register_lookup[(registration_index, state)]["arrival_anchor"]
        ].add(multiplier)

anchor_purity_failures = []
anchor_multiplier_maps = {0: {}, 1: {}}
for registration_index in (0, 1):
    for anchor_index in range(12):
        values = anchor_multiplier_sets[registration_index][anchor_index]
        if len(values) == 1:
            anchor_multiplier_maps[registration_index][anchor_index] = next(
                iter(values)
            )
        else:
            anchor_purity_failures.append({
                "registration": registration_index,
                "anchor": anchor_index,
                "multipliers": sorted(values),
            })

typed_anchor_multiplier_failures = []
for left_anchor, right_anchor in sorted(derived_anchor_map.items()):
    left_multiplier = anchor_multiplier_maps[0].get(left_anchor)
    right_multiplier = anchor_multiplier_maps[1].get(right_anchor)
    if left_multiplier != right_multiplier:
        typed_anchor_multiplier_failures.append({
            "left_anchor": left_anchor,
            "right_anchor": right_anchor,
            "left_multiplier": left_multiplier,
            "right_multiplier": right_multiplier,
        })

canonical_registration = int(m28e["canonical_registration_index"])
canonical_anchor = int(m28e["canonical_anchor_positive_index"])
canonical_offset = int(
    m28e.get(
        "selected_native_offset",
        payloads["audit028e"].get("boundary", {}).get("selected_offset"),
    )
)
canonical_offset_matches_audit028e = (
    selected_offsets.get((canonical_registration, canonical_anchor))
    == canonical_offset
)

state_examples = {
    str(state): next(
        (row for row in cross_rows if row["state"] == state),
        None,
    )
    for state in (0, 39)
}

assignment_rows = [
    {
        "state": state,
        "multiplier": multiplier_by_state[state],
        "left_anchor": register_lookup[(0, state)]["arrival_anchor"],
        "right_anchor": register_lookup[(1, state)]["arrival_anchor"],
        "left_zero": register_lookup[(0, state)]["occupied_inward_position"],
        "right_zero": register_lookup[(1, state)]["occupied_inward_position"],
    }
    for state in sorted(multiplier_by_state)
]

registered_multiplier_decorated_seam_theorem_pass = all((
    sources_ready,
    candidate_hash_before == EXPECTED_CANDIDATE_HASH,
    state_table_exact,
    typed_register_coverage_exact,
    all24_local_offsets_unique,
    two_full60_registers_reconstructed,
    anchor_map_matches_audit028d,
    canonical_offset_matches_audit028e,
    full60_multiplier_assignment_reconstructed,
    full300_coordinate_action_reconstructed,
    all_multipliers_are_2_or_3,
    both_branches_order4,
    not anchor_purity_failures,
    not typed_anchor_multiplier_failures,
))

failure_flags = []
for name, passed in (
    ("sources_ready", sources_ready),
    ("candidate_hash_match", candidate_hash_before == EXPECTED_CANDIDATE_HASH),
    ("state_table_exact", state_table_exact),
    ("typed_register_coverage_exact", typed_register_coverage_exact),
    ("all24_local_offsets_unique", all24_local_offsets_unique),
    ("two_full60_registers_reconstructed", two_full60_registers_reconstructed),
    ("anchor_map_matches_audit028d", anchor_map_matches_audit028d),
    ("canonical_offset_matches_audit028e", canonical_offset_matches_audit028e),
    ("full60_multiplier_assignment_reconstructed", full60_multiplier_assignment_reconstructed),
    ("full300_coordinate_action_reconstructed", full300_coordinate_action_reconstructed),
    ("all_multipliers_are_2_or_3", all_multipliers_are_2_or_3),
    ("both_branches_order4", both_branches_order4),
    ("anchor_purity", not anchor_purity_failures),
    ("typed_anchor_multiplier_preservation", not typed_anchor_multiplier_failures),
):
    if not passed:
        failure_flags.append(name)

TARGET_AFTER = git_snapshot(TARGET)
PROJECT41_AFTER = git_snapshot(PROJECT41)
candidate_hash_after = sha256_file(CANDIDATE) if CANDIDATE.is_file() else ""

emit("OUT ==")
emit("PACKET", PACKET_NAME)
emit("MODE", "read-only bespoke permanent-source full60 seam reconstruction")
emit("TARGET", TARGET)
emit("PROJECT41", PROJECT41)
emit("CANDIDATE_M16", CANDIDATE)
emit("CANDIDATE_SOURCE_READ", False)
emit("CANDIDATE_M15_EXECUTED", False)
emit("CANDIDATE_M16_EXECUTED", False)
emit("REPOSITORY_MUTATION", "none")
emit("PERMANENT_ARTIFACT_WRITTEN", False)
emit("COMMIT_PERFORMED", False)
emit("PUSH_PERFORMED", False)
emit("TARGET_GIT_BEFORE", TARGET_BEFORE)
emit("PROJECT41_GIT_BEFORE", PROJECT41_BEFORE)
emit("candidate_m16_sha256_before", candidate_hash_before)
emit("candidate_m16_hash_match", candidate_hash_before == EXPECTED_CANDIDATE_HASH)
emit("permanent_source_records", source_records)
emit("permanent_sources_ready", sources_ready)

emit("audit019_state_record_count", len(state_records))
emit("audit019_state_record_failure_count", len(state_record_failures))
emit("state_table_exact", state_table_exact)
emit("audit028c_anchor_count", len(anchors))
emit("registration_failure_count", len(registration_failures))
emit("typed_register_coverage_exact", typed_register_coverage_exact)

emit("local_offset_census", offset_census)
emit("offset_selection_failure_count", len(offset_selection_failures))
emit("offset_selection_failures", offset_selection_failures)
emit("all24_local_offsets_unique", all24_local_offsets_unique)
emit("selected_offset_profile", dict(sorted(Counter(selected_offsets.values()).items())))
emit("canonical_offset_matches_audit028e", canonical_offset_matches_audit028e)

emit("register_row_count", len(register_rows))
emit("register_failure_count", len(register_failures))
emit("register_failures", register_failures)
emit("two_full60_registers_reconstructed", two_full60_registers_reconstructed)
emit("derived_anchor_map", derived_anchor_map)
emit("audit028d_relative_positive_map", relative_positive_map)
emit("anchor_map_matches_audit028d", anchor_map_matches_audit028d)

emit("cross_row_count", len(cross_rows))
emit("cross_failure_count", len(cross_failures))
emit("cross_failures", cross_failures)
emit("action_row_count", len(action_rows))
emit("full60_multiplier_assignment_reconstructed", full60_multiplier_assignment_reconstructed)
emit("full300_coordinate_action_reconstructed", full300_coordinate_action_reconstructed)
emit("multiplier_profile", dict(sorted(multiplier_profile.items())))
emit("all_multipliers_are_2_or_3", all_multipliers_are_2_or_3)
emit("both_branches_order4", both_branches_order4)
emit("state_examples", state_examples)
emit("assignment_rows", assignment_rows)
emit("full60_assignment_sha256", canonical_sha256(assignment_rows))
emit("full300_action_sha256", canonical_sha256(action_rows))

emit("left_anchor_multiplier_map", anchor_multiplier_maps[0])
emit("right_anchor_multiplier_map", anchor_multiplier_maps[1])
emit("anchor_purity_failure_count", len(anchor_purity_failures))
emit("anchor_purity_failures", anchor_purity_failures)
emit("typed_anchor_multiplier_failure_count", len(typed_anchor_multiplier_failures))
emit("typed_anchor_multiplier_failures", typed_anchor_multiplier_failures)
emit(
    "multiplier_preserved_by_typed_registration_exchange",
    not typed_anchor_multiplier_failures,
)

emit(
    "registered_multiplier_decorated_seam_theorem_pass",
    registered_multiplier_decorated_seam_theorem_pass,
)
emit("failure_flag_count", len(failure_flags))
emit("failure_flags", failure_flags)

emit("TARGET_GIT_AFTER", TARGET_AFTER)
emit("PROJECT41_GIT_AFTER", PROJECT41_AFTER)
emit("target_repository_unchanged", TARGET_BEFORE == TARGET_AFTER)
emit("project41_repository_unchanged", PROJECT41_BEFORE == PROJECT41_AFTER)
emit(
    "project41_preexisting_status_preserved_exactly",
    PROJECT41_BEFORE["status"] == PROJECT41_AFTER["status"],
)
emit("candidate_m16_sha256_after", candidate_hash_after)
emit("original_candidate_m16_hash_unchanged", candidate_hash_before == candidate_hash_after)
emit("fake_repository_script_absent_after", not (TARGET / CANDIDATE.name).exists())

emit("REQUIRED_BOUNDARY_BEGIN")
emit("candidate_source_read", False)
emit("candidate_m15_executed", False)
emit("candidate_m16_executed", False)
emit("permanent_sources_all_green", sources_ready)
emit("two_full60_typed_registers_reconstructed", two_full60_registers_reconstructed)
emit("all24_multiplier_preserving_offsets_unique", all24_local_offsets_unique)
emit("anchor_registration_equals_audit028d", anchor_map_matches_audit028d)
emit("canonical_offset_equals_audit028e", canonical_offset_matches_audit028e)
emit("full60_multiplier_assignment_reconstructed", full60_multiplier_assignment_reconstructed)
emit("full300_coordinate_action_reconstructed", full300_coordinate_action_reconstructed)
emit("statewise_multiplier_is_always_2_or_3", all_multipliers_are_2_or_3)
emit("both_handed_branches_have_order4", both_branches_order4)
emit(
    "registered_multiplier_decorated_seam_theorem_promotable",
    registered_multiplier_decorated_seam_theorem_pass,
)
emit(
    "permanent_authority_statewise_handed_assignment_reconstructed",
    full60_multiplier_assignment_reconstructed,
)
emit("independent_premultiplier_handed_selector_found", False)
emit("native_handed_multiplier_selected_without_multiplier_input", False)
emit("source_ab_winder_identified_with_order4_map", False)
emit("drawing09_returned_W_operation_constructed", False)
emit("returned_W_bound_as_ab_square", False)
emit("receipt_I_constructed", False)
emit("finite_spinor_constructed", False)
emit("electron_constructed", False)
emit("physics_claim", False)
emit("MUTATION_PERFORMED", False)
emit("REQUIRED_BOUNDARY_END")

if registered_multiplier_decorated_seam_theorem_pass:
    emit(
        "FINAL_CLASSIFICATION",
        "full60 handed recentered seam action reconstructed directly from permanent multiplier-decorated authority",
    )
    emit(
        "NEXT_GATE",
        "Promote only the registered multiplier-decorated seam theorem, while retaining the unresolved pre-multiplier handed-selector boundary.",
    )
else:
    emit(
        "FINAL_CLASSIFICATION",
        "direct permanent-source full60 reconstruction failed",
    )
    emit(
        "NEXT_GATE",
        "Inspect only the reported reconstruction failures before any theorem promotion.",
    )

emit(
    "KEEPER",
    "Permanent authority reconstructs the turn state by state; it does not yet explain why that hand was chosen.",
)
emit("REPOSITORY_MUTATION", "none")
emit("PERMANENT_ARTIFACT_WRITTEN", False)
emit("COMMIT_PERFORMED", False)
emit("PUSH_PERFORMED", False)

REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(REPORT)
