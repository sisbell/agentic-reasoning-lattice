#!/usr/bin/env python3
"""One-off migration: note.yaml → inquiry.md (substrate) + state.yaml (cache).

For each `lattices/<lattice>/manifests/ASN-NNNN/note.yaml`, splits the
yaml into:

    lattices/<lattice>/_store/documents/inquiries/ASN-NNNN.md
        Markdown + frontmatter. Frontmatter holds inquiry content
        (title, question, covers, out_of_scope, n_theory, n_evidence).
        Body: minimal `# {title}` heading; can be elaborated in editor.

    lattices/<lattice>/manifests/ASN-NNNN/state.yaml
        Operational + lineage state (last_*, extends, source). Only
        written if at least one such field is non-empty; otherwise
        omitted.

Substrate emissions per migrated ASN:

    `inquiry` classifier on the inquiry md (idempotent)
    `citation` from inquiry md to upstream inquiry mds for each
        declared `depends:` entry (idempotent — done after all
        inquiries are written so cross-references resolve)

The old note.yaml is deleted after successful migration. The campaign
binding (if explicitly set in manifest, rare) becomes a substrate
`campaign` link from inquiry md to campaign descriptor — but no
manifest in either lattice currently sets `campaign:`, so this path
is a no-op today.

Idempotent: re-running on a migrated lattice is a no-op.

Dropped fields (no migration target — confirmed dead):
    stage, topic, hints, already_covered

Usage:
    python3 scripts/migrate-manifest-to-inquiry.py
    python3 scripts/migrate-manifest-to-inquiry.py --apply
    LATTICE=materials python3 scripts/migrate-manifest-to-inquiry.py --apply
"""

import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from shared.common import write_frontmatter
from shared.paths import (
    INQUIRIES_DIR, MANIFESTS_DIR, WORKSPACE,
    inquiry_doc_path, state_yaml,
)
from store.cite import emit_citation
from store.emit import emit_inquiry
from store.populate import build_note_label_index
from store.store import Store


_INQUIRY_FIELDS = ("title", "covers", "out_of_scope")
_STATE_FIELDS = (
    "last_consistency_check", "last_consistency_result",
    "last_rebase_check", "last_pipeline_run",
    "extends", "source",
)
_DROP_FIELDS = ("stage", "topic", "hints", "already_covered", "depends",
                "campaign", "consultations", "inquiry")


def _build_frontmatter(manifest):
    """Extract inquiry content fields from manifest dict, flattening
    nested question and channel-count fields."""
    fm = {}
    for key in _INQUIRY_FIELDS:
        if key in manifest and manifest[key] not in (None, ""):
            fm[key] = manifest[key]

    # Question can live under `inquiry:` (older) or `consultations:` (newer).
    consultations = manifest.get("consultations") or {}
    inquiry = manifest.get("inquiry") or {}
    question = (consultations.get("question")
                or inquiry.get("question"))
    if question:
        fm["question"] = question

    # Channel counts under consultations.agents.{theory,evidence}.
    agents = consultations.get("agents") or {}
    if "theory" in agents:
        fm["n_theory"] = agents["theory"]
    if "evidence" in agents:
        fm["n_evidence"] = agents["evidence"]

    return fm


def _build_state(manifest):
    """Extract operational + lineage state fields. Returns dict or None
    if no state to record."""
    state = {}
    for key in _STATE_FIELDS:
        if key in manifest and manifest[key] not in (None, "", []):
            state[key] = manifest[key]
    return state or None


def _build_body(fm):
    title = fm.get("title", "")
    if title:
        return f"# Inquiry: {title}\n"
    return "# Inquiry\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    grp = ap.add_mutually_exclusive_group()
    grp.add_argument("--apply", action="store_true",
                     help="perform the migration (default is dry-run)")
    grp.add_argument("--dry-run", action="store_true", default=True)
    args = ap.parse_args()
    apply_mode = args.apply

    label = "APPLY" if apply_mode else "DRY-RUN"
    print(f"[migrate-manifest-to-inquiry] {label}")
    print(f"  MANIFESTS_DIR  = {MANIFESTS_DIR.relative_to(WORKSPACE)}")
    print(f"  INQUIRIES_DIR  = {INQUIRIES_DIR.relative_to(WORKSPACE)}")
    print()

    if not MANIFESTS_DIR.exists():
        print(f"  no MANIFESTS_DIR at {MANIFESTS_DIR}", file=sys.stderr)
        return 1

    manifests = sorted(MANIFESTS_DIR.glob("ASN-*/note.yaml"))
    print(f"  Found {len(manifests)} legacy note.yaml file(s)")
    print()

    plan = []
    for path in manifests:
        asn_label = path.parent.name  # ASN-NNNN
        asn_num = int(asn_label.split("-")[1])
        try:
            with open(path) as f:
                manifest = yaml.safe_load(f) or {}
        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"  ! {asn_label} unreadable: {e}", file=sys.stderr)
            continue
        fm = _build_frontmatter(manifest)
        state = _build_state(manifest)
        depends = list(manifest.get("depends") or [])
        plan.append((asn_num, asn_label, path, fm, state, depends))

    if not apply_mode:
        for asn_num, asn_label, src, fm, state, depends in plan[:5]:
            print(f"    {asn_label}: fm keys={sorted(fm.keys())}, "
                  f"state={'yes' if state else 'no'}, "
                  f"depends={depends}")
        if len(plan) > 5:
            print(f"    ... and {len(plan) - 5} more")
        print()
        print(f"  (dry-run; no changes made. Use --apply to migrate.)")
        return 0

    INQUIRIES_DIR.mkdir(parents=True, exist_ok=True)

    store = Store()
    inquiry_paths = {}  # asn_label → inquiry md path
    written_inquiry = 0
    written_state = 0
    classifier_count = 0
    deleted_count = 0

    try:
        # Phase A: write inquiry mds + state.yaml + emit classifiers.
        for asn_num, asn_label, src, fm, state, depends in plan:
            inq_path = inquiry_doc_path(asn_num)
            if not inq_path.exists():
                inq_path.write_text(write_frontmatter(fm, _build_body(fm)))
                written_inquiry += 1
            inquiry_paths[asn_label] = inq_path

            if state:
                st_path = state_yaml(asn_num)
                if not st_path.exists():
                    st_path.write_text(yaml.safe_dump(
                        state, default_flow_style=False, sort_keys=True,
                    ))
                    written_state += 1

            _, created = emit_inquiry(store, inq_path)
            if created:
                classifier_count += 1

        # Phase B: emit citation links between inquiries (deps).
        # Each citation goes from this inquiry to the upstream inquiry md.
        # The upstream inquiry exists because Phase A wrote all of them.
        cite_count = 0
        for asn_num, asn_label, src, fm, state, depends in plan:
            inq_path = inquiry_paths[asn_label]
            for dep_id in depends:
                dep_label = f"ASN-{int(dep_id):04d}"
                dep_path = inquiry_paths.get(dep_label)
                if dep_path is None:
                    print(f"  ! {asn_label} depends on {dep_label} but no "
                          f"inquiry md exists for it — skipping",
                          file=sys.stderr)
                    continue
                # emit_citation expects a label_index dict {label: path}
                # We synthesize a single-entry index per call.
                from_rel = str(inq_path.resolve().relative_to(WORKSPACE.resolve()))
                dep_rel = str(dep_path.resolve().relative_to(WORKSPACE.resolve()))
                try:
                    _, created = emit_citation(
                        store, from_rel, dep_label, {dep_label: dep_rel},
                    )
                    if created:
                        cite_count += 1
                except KeyError as e:
                    print(f"  ! {asn_label} → {dep_label} failed: {e}",
                          file=sys.stderr)

        # Phase C: delete old note.yaml files.
        for asn_num, asn_label, src, fm, state, depends in plan:
            if src.exists():
                src.unlink()
                deleted_count += 1
    finally:
        store.close()

    print(f"  inquiries written:  {written_inquiry}")
    print(f"  state files:        {written_state}")
    print(f"  inquiry classifiers (new): {classifier_count}")
    print(f"  inquiry→inquiry citations (new): {cite_count}")
    print(f"  legacy note.yaml deleted:  {deleted_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
