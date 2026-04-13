"""
Dependency cone detection and cone-scoped review.

Detects when a single property (the apex) keeps getting revised while
its dependencies are stable — a "dependency cone." Runs a focused
review/revise loop on just the cone to accelerate convergence.
"""

import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE, FORMALIZATION_DIR, next_review_number
from lib.shared.common import (
    find_asn, build_label_index, load_property_metadata,
    step_commit_asn,
)
from lib.formalization.cross_review.review import run_review, extract_findings
from lib.formalization.cross_review.revise import revise


def detect_dependency_cone(asn_num, window=5, threshold=3):
    """Detect a dependency cone from git history.

    Scans the last `window` cross-review commits for this ASN.
    If one property has >= `threshold` touches while its YAML
    dependencies have <= 1 touch, returns (apex_label, dep_labels).
    Otherwise returns None.
    """
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        return None

    prop_dir = FORMALIZATION_DIR / asn_label
    rel_dir = prop_dir.relative_to(WORKSPACE)

    # Get last N cross-review commits touching this ASN
    try:
        result = subprocess.run(
            ["git", "log", f"--grep=cross-review", f"-{window}",
             "--format=%H", "--", str(rel_dir)],
            capture_output=True, text=True, cwd=str(WORKSPACE),
        )
    except Exception:
        return None

    commits = result.stdout.strip().split("\n")
    commits = [c for c in commits if c]

    if len(commits) < threshold:
        return None

    # Count property file touches per commit
    touch_counts = {}  # label → count
    label_index = build_label_index(prop_dir)
    stem_to_label = {stem: lbl for lbl, stem in label_index.items()}

    for commit_hash in commits:
        try:
            result = subprocess.run(
                ["git", "diff-tree", "--no-commit-id", "--name-only", "-r",
                 commit_hash],
                capture_output=True, text=True, cwd=str(WORKSPACE),
            )
        except Exception:
            continue

        for line in result.stdout.strip().split("\n"):
            if not line.startswith(str(rel_dir)):
                continue
            fname = Path(line).name
            # Skip reviews, structural files, non-property files
            if "reviews/" in line or fname.startswith("_") or fname.startswith("."):
                continue
            stem = fname.replace(".md", "").replace(".yaml", "")
            label = stem_to_label.get(stem, stem)
            touch_counts[label] = touch_counts.get(label, 0) + 1

    if not touch_counts:
        return None

    # Find candidate apex: most-touched property above threshold
    apex = max(touch_counts, key=touch_counts.get)
    if touch_counts[apex] < threshold:
        return None

    # Load apex dependencies (same-ASN only)
    asn_labels = set(label_index.keys())
    meta = load_property_metadata(prop_dir, label=apex)
    if not meta:
        return None

    dep_labels = [d for d in meta.get("depends", []) if d in asn_labels]

    # Check if dependencies are stable relative to apex
    # Apex should have at least 2x the touches of any single dep
    apex_count = touch_counts[apex]
    max_dep_touches = max(
        (touch_counts.get(d, 0) for d in dep_labels), default=0
    )
    if max_dep_touches > apex_count // 2:
        return None  # Dependencies are also thrashing — not a cone

    print(f"  [CONE] Detected: {apex} ({touch_counts[apex]} touches, "
          f"{len(dep_labels)} stable deps)", file=sys.stderr)
    return (apex, dep_labels)


def assemble_cone(asn_label, apex_label, dep_labels):
    """Assemble just the cone properties for focused review.

    Returns concatenated text of apex + same-ASN dependency properties.
    """
    prop_dir = FORMALIZATION_DIR / asn_label
    label_index = build_label_index(prop_dir)
    parts = []

    # Include dependencies first (context), then apex
    for label in dep_labels + [apex_label]:
        stem = label_index.get(label)
        if stem is None:
            continue
        md_path = prop_dir / f"{stem}.md"
        if md_path.exists():
            parts.append(md_path.read_text().strip())

    return "\n\n---\n\n".join(parts)


def _extract_apex_history(asn_label, apex_label, max_reviews=5):
    """Extract recent review findings that mention the apex label."""
    review_dir = FORMALIZATION_DIR / asn_label / "reviews"
    if not review_dir.exists():
        return ""

    review_files = sorted(review_dir.glob("review-*.md"),
                          key=lambda f: int(re.search(r'\d+', f.stem).group()),
                          reverse=True)

    relevant = []
    for rf in review_files[:max_reviews]:
        text = rf.read_text()
        if apex_label in text:
            relevant.append(text.strip())

    if not relevant:
        return "(no recent findings)"

    return "\n\n---\n\n".join(reversed(relevant))


def run_cone_review(asn_num, apex_label, dep_labels, max_cycles=3,
                    dry_run=False, model="opus"):
    """Run a focused review/revise loop on the dependency cone.

    Same structure as cross-review but with narrower context:
    only the apex and its same-ASN dependencies.

    Returns "converged" or "not_converged".
    """
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        return "failed"

    prop_dir = FORMALIZATION_DIR / asn_label
    review_dir = prop_dir / "reviews"

    print(f"\n  [CONE-REVIEW] {apex_label} + {len(dep_labels)} deps",
          file=sys.stderr)

    # Load review history for the apex
    history = _extract_apex_history(asn_label, apex_label)

    start_time = time.time()
    previous_findings = history
    had_findings = False

    for cycle in range(1, max_cycles + 1):
        print(f"\n  [CONE CYCLE {cycle}/{max_cycles}]", file=sys.stderr)

        # Assemble just the cone
        cone_content = assemble_cone(asn_label, apex_label, dep_labels)

        # Run review with cone content instead of full ASN
        findings_text, elapsed = run_review(
            asn_num, cone_content, asn_label, previous_findings, model=model)

        if findings_text is None:
            print(f"\n  [CONE] Converged after {cycle} cycle{'s' if cycle > 1 else ''}.",
                  file=sys.stderr)
            break

        had_findings = True

        # Save review
        review_dir.mkdir(parents=True, exist_ok=True)
        review_num = next_review_number(asn_label, reviews_dir=review_dir)
        review_path = review_dir / f"review-{review_num}.md"
        with open(review_path, "w") as rf:
            rf.write(f"# Cone Review — {asn_label}/{apex_label} (cycle {cycle})\n\n")
            rf.write(f"*{time.strftime('%Y-%m-%d %H:%M')}*\n\n")
            rf.write(findings_text + "\n")

        findings = extract_findings(findings_text)
        for title, _ in findings:
            print(f"\n  ### {title}", file=sys.stderr)

        if dry_run:
            print(f"\n  [DRY RUN] {len(findings)} findings, no fixes.",
                  file=sys.stderr)
            break

        # Revise each finding
        any_changed = False
        for title, finding_text in findings:
            ok = revise(asn_num, title, finding_text, prop_dir=prop_dir)
            if ok:
                any_changed = True

        if not any_changed:
            print(f"  No changes made — stopping.", file=sys.stderr)
            break

        step_commit_asn(asn_num,
                        f"cone-review(asn): {asn_label}/{apex_label} — cycle {cycle}")

        previous_findings = (previous_findings + "\n\n" + findings_text).strip()

    elapsed = time.time() - start_time
    converged = not had_findings or (findings_text is None)

    if had_findings:
        with open(review_path, "a") as rf:
            rf.write(f"\n## Result\n\n")
            if converged:
                rf.write(f"Cone converged after {cycle} cycles.\n")
            else:
                rf.write(f"Cone not converged after {cycle} cycles.\n")
            rf.write(f"\n*Elapsed: {elapsed:.0f}s*\n")

    print(f"  [CONE] Elapsed: {elapsed:.0f}s", file=sys.stderr)
    return "converged" if converged else "not_converged"
