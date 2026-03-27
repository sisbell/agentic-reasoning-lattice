#!/usr/bin/env python3
"""
Extract domain extension claims from an ASN for focused LLM verification.

Reads the deps YAML for parallels/extends entries, then extracts surrounding
prose context from the ASN for each claim. Produces structured claims that
the focused LLM judgment step can verify.

Usage:
    python scripts/lib/rebase_extensions.py 43           # extract and print
    python scripts/lib/rebase_extensions.py 43 --verify   # extract + run focused LLM
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE, load_manifest, formal_stmts, dep_graph
from lib.shared.common import find_asn, read_file

PROMPT_TEMPLATE = WORKSPACE / "scripts" / "prompts" / "formalization" / "focused-judgment.md"


@dataclass
class ExtensionClaim:
    local_label: str
    local_type: str  # "extends" or "parallels"
    foundation_label: str
    foundation_asn: int
    foundation_name: str
    context: str  # surrounding prose from ASN


def load_deps_yaml(asn_num):
    """Load deps YAML. Returns dict or None."""
    path = dep_graph(asn_num)
    if not path.exists():
        return None
    with open(path) as f:
        return yaml.safe_load(f)


def extract_prose_context(asn_text, label, max_chars=1500):
    """Extract prose around a property label from the ASN text.

    Finds the property definition (**LABEL — Name.**) and captures
    the surrounding text.
    """
    # Find the property section
    pattern = re.compile(
        r'\*\*' + re.escape(label) + r'\s*(?:—|–|-)',
        re.MULTILINE
    )
    m = pattern.search(asn_text)
    if not m:
        # Try without bold
        pattern = re.compile(r'^' + re.escape(label) + r'\s*(?:—|–|-)', re.MULTILINE)
        m = pattern.search(asn_text)
    if not m:
        return f"[property section for {label} not found in ASN]"

    start = m.start()

    # Capture forward until next property or section header
    next_prop = re.search(r'\n\*\*[A-Z]', asn_text[start + 10:])
    next_section = re.search(r'\n## ', asn_text[start + 10:])

    end = len(asn_text)
    if next_prop:
        end = min(end, start + 10 + next_prop.start())
    if next_section:
        end = min(end, start + 10 + next_section.start())

    text = asn_text[start:end].strip()
    if len(text) > max_chars:
        text = text[:max_chars] + "\n[...truncated...]"

    return text


def extract_claims(asn_num):
    """Extract all extension/parallel claims from an ASN.

    Returns list of ExtensionClaim.
    """
    deps = load_deps_yaml(asn_num)
    if deps is None:
        print(f"  [ERROR] No deps YAML for ASN-{asn_num:04d}", file=sys.stderr)
        return []

    asn_path, _ = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  [ERROR] ASN-{asn_num:04d} not found", file=sys.stderr)
        return []

    asn_text = asn_path.read_text()
    claims = []

    # Source 1: deps YAML extends/parallels entries
    for label, prop_data in deps["properties"].items():
        for rel_type in ("extends", "parallels"):
            rel = prop_data.get(rel_type)
            if not rel:
                continue

            foundation_label = rel.get("label", "")
            foundation_asn = rel.get("asn")
            foundation_name = rel.get("name", "")

            if not foundation_label or not foundation_asn:
                continue

            context = extract_prose_context(asn_text, label)

            claims.append(ExtensionClaim(
                local_label=label,
                local_type=rel_type,
                foundation_label=foundation_label,
                foundation_asn=foundation_asn,
                foundation_name=foundation_name,
                context=context,
            ))

    # Source 2: prose keyword scan for parallels/analogs not in deps YAML
    seen = {(c.local_label, c.foundation_label) for c in claims}
    manifest = load_manifest(asn_num)
    depends = manifest.get("depends", [])

    # Build label→asn map from dependency exports
    label_to_asn = {}
    for dep_id in depends:
        stmt_path = formal_stmts(dep_id)
        if not stmt_path.exists():
            continue
        text = stmt_path.read_text()
        for m in re.finditer(r'^## (\S+) — ', text, re.MULTILINE):
            label_to_asn[m.group(1)] = dep_id

    # Scan prose for parallel/analog claims
    parallel_pattern = re.compile(
        r'(?:parallels?|analog(?:ous)?\s+(?:of|to)?|mirrors?|same\s+(?:role|argument|reasoning)\s+as)\s+'
        r'(\S+)(?:\s+(?:for|in|from))?\s*(?:\((?:[^,]+,\s*)?ASN-(\d{4})\))?',
        re.IGNORECASE
    )

    for label, prop_data in deps["properties"].items():
        context = extract_prose_context(asn_text, label, max_chars=2000)

        for m in parallel_pattern.finditer(context):
            foundation_label = m.group(1).strip(".,;:()")
            foundation_asn = int(m.group(2)) if m.group(2) else label_to_asn.get(foundation_label)

            if not foundation_asn:
                continue

            if (label, foundation_label) in seen:
                continue

            seen.add((label, foundation_label))
            claims.append(ExtensionClaim(
                local_label=label,
                local_type="parallels",
                foundation_label=foundation_label,
                foundation_asn=foundation_asn,
                foundation_name="",
                context=context,
            ))

    return claims


# ---------------------------------------------------------------------------
# Focused LLM verification
# ---------------------------------------------------------------------------

def load_foundation_statement(foundation_label, foundation_asn):
    """Load a specific foundation property's statement from its export."""
    stmt_path = formal_stmts(foundation_asn)
    if not stmt_path.exists():
        return f"[export not found for ASN-{foundation_asn:04d}]"

    text = stmt_path.read_text()

    # Find the section for this label
    pattern = re.compile(
        r'^## ' + re.escape(foundation_label) + r'\s*—\s*(.+?)(?=\n## |\Z)',
        re.MULTILINE | re.DOTALL
    )
    m = pattern.search(text)
    if m:
        section = m.group(0).strip()
        if len(section) > 2000:
            section = section[:2000] + "\n[...truncated...]"
        return section

    return f"[property {foundation_label} not found in ASN-{foundation_asn:04d} export]"


def verify_claims(claims, model="sonnet", effort="high", batch_size=3):
    """Run focused LLM verification on extension claims.

    Returns list of (claim, verdict, explanation) tuples.
    """
    template = read_file(PROMPT_TEMPLATE)
    if not template:
        print(f"  [ERROR] Prompt template not found: {PROMPT_TEMPLATE}",
              file=sys.stderr)
        return []

    results = []

    # Process in batches
    for i in range(0, len(claims), batch_size):
        batch = claims[i:i + batch_size]

        # Build prompt for this batch
        sections = []
        for j, claim in enumerate(batch, 1):
            foundation_stmt = load_foundation_statement(
                claim.foundation_label, claim.foundation_asn)

            sections.append(f"""### Claim {j}
**Local property**: {claim.local_label} ({claim.local_type} {claim.foundation_label} from ASN-{claim.foundation_asn:04d})
**Foundation property**:
{foundation_stmt}

**Local context**:
{claim.context}
""")

        claims_text = "\n---\n".join(sections)
        prompt = template.replace("{{claims}}", claims_text)
        prompt = prompt.replace("{{count}}", str(len(batch)))

        # Call LLM
        model_flag = {"opus": "claude-opus-4-6", "sonnet": "claude-sonnet-4-6"}.get(model, model)
        cmd = ["claude", "--print", "--model", model_flag,
               "--output-format", "json", "--tools", ""]

        env = os.environ.copy()
        env.pop("CLAUDECODE", None)
        env["DISABLE_AUTOUPDATER"] = "1"
        if effort:
            env["CLAUDE_CODE_EFFORT_LEVEL"] = effort

        start = time.time()
        result = subprocess.run(
            cmd, input=prompt, capture_output=True, text=True, env=env,
            timeout=None,
        )
        elapsed = time.time() - start

        if result.returncode != 0:
            print(f"  [VERIFY] Batch {i // batch_size + 1} FAILED ({elapsed:.0f}s)",
                  file=sys.stderr)
            for claim in batch:
                results.append((claim, "ERROR", "LLM call failed"))
            continue

        # Parse response
        try:
            data = json.loads(result.stdout)
            response_text = data.get("result", result.stdout)
        except (json.JSONDecodeError, KeyError):
            response_text = result.stdout

        # Extract verdicts: look for VERIFIED or GAP patterns
        for j, claim in enumerate(batch, 1):
            verdict_pattern = re.compile(
                rf'(?:Claim\s*{j}|{re.escape(claim.local_label)})\s*[:\-]\s*(VERIFIED|GAP)\s*[:\-]?\s*(.*?)(?=(?:Claim\s*\d|$))',
                re.DOTALL | re.IGNORECASE
            )
            vm = verdict_pattern.search(response_text)
            if vm:
                verdict = vm.group(1).upper()
                explanation = vm.group(2).strip()[:200]
                results.append((claim, verdict, explanation))
            else:
                results.append((claim, "UNCLEAR", "Could not parse verdict"))

        print(f"  [VERIFY] Batch {i // batch_size + 1}: "
              f"{sum(1 for _, v, _ in results[-len(batch):] if v == 'VERIFIED')} verified, "
              f"{sum(1 for _, v, _ in results[-len(batch):] if v == 'GAP')} gaps "
              f"({elapsed:.0f}s)", file=sys.stderr)

    return results


def format_findings(results):
    """Format GAP results as findings for open-issues.md."""
    lines = []
    for claim, verdict, explanation in results:
        if verdict == "GAP":
            lines.append(f"### Finding: [{claim.local_type}] {claim.local_label} "
                         f"→ {claim.foundation_label} (ASN-{claim.foundation_asn:04d})")
            lines.append(f"**Type**: domain extension gap")
            lines.append(f"**Detail**: {explanation}")
            lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Extract and verify domain extension claims")
    parser.add_argument("asn", help="ASN number (e.g., 43)")
    parser.add_argument("--verify", action="store_true",
                        help="Run focused LLM verification on claims")
    parser.add_argument("--model", "-m", default="sonnet",
                        choices=["opus", "sonnet"])
    parser.add_argument("--effort", default="high")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    claims = extract_claims(asn_num)

    if not claims:
        print(f"  [EXTENSIONS] No extension claims found for ASN-{asn_num:04d}",
              file=sys.stderr)
        return

    print(f"  [EXTENSIONS] {len(claims)} claims found:", file=sys.stderr)
    for c in claims:
        print(f"    {c.local_label} {c.local_type} {c.foundation_label} "
              f"(ASN-{c.foundation_asn:04d})", file=sys.stderr)

    if args.verify:
        results = verify_claims(claims, model=args.model, effort=args.effort)
        findings = format_findings(results)
        if findings:
            print(findings)
        else:
            print(f"  [EXTENSIONS] All claims verified", file=sys.stderr)


if __name__ == "__main__":
    main()
