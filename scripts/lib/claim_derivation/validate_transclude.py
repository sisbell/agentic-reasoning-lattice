"""Validate-transclude — verify each claim md is a byte-substring of its
source note.

Runs at transclude exit. The Claim File Contract's content-preservation
invariant (#12) is transition-checkable at this boundary only:
produce_contract intentionally appends Formal Contract sections after
transclude, and validate-revise heals structural form afterward —
both legitimately diverge the body from the source.

This validator is mechanical. No LLM. If transclude is correct (it
projects via `find_in_source` which returns source-bytes), this check
always passes. Its purpose is runtime documentation of the contract:
if transclude ever drifts, the failure surfaces here rather than
silently propagating into produce_contract.

Whitespace tolerance: transclude writes `body.rstrip() + "\\n"`, so the
file on disk has trailing-newline normalization that may not match the
source's exact trailing bytes. The check rstrips the body before
testing membership in the source.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import CLAIM_DIR
from lib.shared.common import find_asn


_SIDECAR_SUFFIXES = (".label.md", ".name.md", ".description.md")


def _is_claim_body(md_path):
    """True iff `md_path` is a claim body markdown (not a sidecar or a
    structural file). Sidecar files end in `.label.md`/`.name.md`/
    `.description.md`. Structural files start with `_`."""
    name = md_path.name
    if name.startswith("_"):
        return False
    if name.endswith(_SIDECAR_SUFFIXES):
        return False
    return name.endswith(".md")


def validate_transclude_substring(asn_num):
    """Check the substring invariant at transclude exit.

    Returns (ok, findings) where:
      ok       — True iff every claim body is a byte-substring of the
                 source note (after trailing-whitespace normalization)
      findings — list of (claim_filename, reason) tuples for failures;
                 empty when ok=True
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return False, [(None, f"ASN-{asn_num:04d}: source note not found")]

    claim_dir = CLAIM_DIR / asn_label
    if not claim_dir.exists():
        return False, [(None, f"{asn_label}: claim doc directory does not exist")]

    source_text = asn_path.read_text()
    findings = []

    for md_path in sorted(claim_dir.glob("*.md")):
        if not _is_claim_body(md_path):
            continue
        body = md_path.read_text().rstrip()
        if not body:
            findings.append((md_path.name, "empty body"))
            continue
        if body not in source_text:
            findings.append((
                md_path.name,
                "body content is not a byte-substring of source note "
                "(transclude exit invariant violated)",
            ))

    return len(findings) == 0, findings


def print_validation(asn_num):
    """CLI entry — run the check and print results to stderr.

    Returns True on success (zero findings), False otherwise."""
    ok, findings = validate_transclude_substring(asn_num)

    _, asn_label = find_asn(str(asn_num))
    print(f"\n  [VALIDATE-TRANSCLUDE] {asn_label}", file=sys.stderr)

    if ok:
        print(f"  RESULT: PASS (0 findings)", file=sys.stderr)
        return True

    for fname, reason in findings:
        prefix = f"{fname} — " if fname else ""
        print(f"    ✗ {prefix}{reason}", file=sys.stderr)
    print(f"\n  RESULT: FAIL ({len(findings)} finding(s))", file=sys.stderr)
    return False


def main():
    import argparse
    import re
    parser = argparse.ArgumentParser(
        description="Verify each claim body is a byte-substring of its "
                    "source note (transclude-exit invariant).")
    parser.add_argument("asn", help="ASN number (e.g., 36)")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    ok = print_validation(asn_num)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
