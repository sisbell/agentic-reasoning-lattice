"""Helpers translating reviewer outputs into link writes.

Each review run materializes its findings as documents under
`_store/findings/{asn}/{review_stem}/{n}.md` and emits comment links from
those documents to their target claims, plus a `review` classifier link
on the review markdown itself.

Resolution links (the reviser's accept/reject decision) are emitted by
`scripts/decide.py`, not by this module — the reviser invokes the tool
directly so its action is the protocol operation.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import FINDINGS_DIR, WORKSPACE


def emit_review(store, review_md_path):
    """Make `review` classifier link on the review markdown file."""
    return store.make_link(
        from_set=[],
        to_set=[_repo_relative(review_md_path)],
        type_set=["review"],
    )


def emit_findings(store, review_md_path, findings, asn_label, review_stem,
                  label_index, findings_dir=None):
    """Materialize each finding as a document and emit a comment link.

    `findings` is the list of (title, cls, body) tuples from
    `extract_findings()`. For each:
      - resolve target claim via the body's `**ASN**: <label>` line
        (falls back to `**Foundation**:` if ASN is absent)
      - materialize a document at <findings_dir>/<asn_label>/<review_stem>/<n>.md
      - make `comment.{revise|observe}` link from finding-doc to claim-md

    Returns list of {title, cls, comment_id, claim_path, finding_path} dicts
    in input order, omitting findings whose target couldn't be resolved
    (logged to stderr).
    """
    findings_root = Path(findings_dir) if findings_dir else Path(FINDINGS_DIR)
    out_dir = findings_root / asn_label / review_stem
    out_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for n, (title, cls, body) in enumerate(findings):
        target_label = _extract_target_label(body, label_index)
        if target_label is None:
            print(
                f"  [emit] skipping finding {n} '{title}' — "
                f"no parseable target label (no Foundation/ASN token "
                f"matches a known claim)",
                file=sys.stderr,
            )
            continue
        claim_path = label_index[target_label]

        finding_path = out_dir / f"{n}.md"
        finding_path.write_text(body)
        finding_rel = _repo_relative(finding_path)

        cls_normalized = cls.upper() if cls else "REVISE"
        if cls_normalized not in {"REVISE", "OBSERVE"}:
            cls_normalized = "REVISE"
        comment_type = f"comment.{cls_normalized.lower()}"

        comment_id = store.make_link(
            from_set=[finding_rel],
            to_set=[claim_path],
            type_set=[comment_type],
        )

        results.append({
            "title": title,
            "cls": cls_normalized,
            "comment_id": comment_id,
            "claim_path": claim_path,
            "finding_path": finding_rel,
        })

    return results


def _extract_target_label(body, label_index):
    """Find the target claim label from a finding body, validated against label_index.

    The reviewer's `**Foundation**:` field reliably starts with a claim label
    (e.g., "NAT-order *Consequence*", "T0 (CarrierSetDefinition)"). The
    `**ASN**:` field is typically descriptive prose. We try Foundation first,
    then ASN as fallback. From each field we tokenize and return the first
    token that's a known label.
    """
    for field in ("Foundation", "ASN"):
        m = re.search(rf"\*\*{field}\*\*:\s*(.+)", body)
        if m:
            tokens = re.findall(r"[A-Za-z][\w.-]*", m.group(1))
            for token in tokens:
                if token in label_index:
                    return token
    return None


def _repo_relative(path):
    return str(Path(path).resolve().relative_to(Path(WORKSPACE).resolve()))
