#!/usr/bin/env python3
"""
Extract structural conventions from finalized ASNs and update vocabulary.

Reads one or more ASNs, extracts state components, naming conventions,
and organizational patterns. Updates vault/vocabulary.md with structural
conventions (not property claims — those must be derived by each ASN).

Usage:
    python scripts/extract-vocab.py vault/asns/ASN-0004-*.md
    python scripts/extract-vocab.py vault/asns/*.md
    python scripts/extract-vocab.py --dry-run vault/asns/ASN-0004-*.md
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
VOCAB_PATH = WORKSPACE / "vault" / "vocabulary.md"

PROMPT = """You are updating a shared vocabulary file for a specification project.

## Current Vocabulary

{current_vocab}

## Finalized ASN(s)

{asn_content}

## Task

Extract STRUCTURAL conventions from the ASN(s) and propose an updated vocabulary.
The vocabulary must contain:

1. **Types** — what things ARE (not what they guarantee). Keep existing type
   definitions. Add any new types the ASN introduces.

2. **Canonical State Components** — NEW SECTION. Extract the state component
   names and signatures that the ASN uses. These become the standard names
   for all future ASNs. Example:
   - `Σ.content : IAddr ⇀ Byte` — the content store
   - `d.map : VAddr ⇀ IAddr` — document arrangement (text subspace)

3. **Naming Conventions** — NEW SECTION. Extract the property labeling pattern.
   What prefix scheme does the ASN use? What pattern for preconditions,
   postconditions, frame conditions, derived properties, invariants?

4. **Organizational Pattern** — NEW SECTION. What sections does the ASN use
   and in what order? This becomes the recommended structure.

5. **Key Distinctions** — keep existing, add any new ones from the ASN.

## Rules

- State components: give the NAME and TYPE SIGNATURE only. Do NOT include
  what the component guarantees (e.g., "append-only" or "immutable").
  The guarantee is a property to be derived, not a vocabulary entry.
- Naming conventions: describe the PATTERN, not the specific properties.
  "R0-R7 for postconditions" is a pattern. "R5 means I-space frame" is
  a specific property — don't include it.
- If multiple ASNs use different conventions, note the conflict and pick
  the clearest one.
- Keep the vocabulary CONCISE. This is a reference card, not a textbook.

## Output

Output the complete updated vocabulary.md content. Nothing else — no
commentary, no explanation, just the markdown file content.
"""


def main():
    parser = argparse.ArgumentParser(description="Extract vocabulary from ASNs")
    parser.add_argument("asns", nargs="+", help="ASN files to extract from")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show proposed vocab, don't write")
    parser.add_argument("--model", "-m", default="sonnet",
                        help="Model (default: sonnet)")
    args = parser.parse_args()

    # Read current vocabulary
    current_vocab = ""
    if VOCAB_PATH.exists():
        current_vocab = VOCAB_PATH.read_text()

    # Read ASN(s)
    asn_parts = []
    for path_str in args.asns:
        path = Path(path_str)
        if not path.exists():
            # Try relative to workspace
            path = WORKSPACE / path_str
        if path.exists():
            asn_parts.append(f"### {path.name}\n\n{path.read_text()}")
        else:
            print(f"  [WARN] Not found: {path_str}", file=sys.stderr)

    if not asn_parts:
        print("No ASN files found", file=sys.stderr)
        sys.exit(1)

    asn_content = "\n\n".join(asn_parts)

    # Build prompt
    prompt = PROMPT.format(
        current_vocab=current_vocab or "(empty)",
        asn_content=asn_content,
    )

    print(f"  Extracting from {len(asn_parts)} ASN(s)...", file=sys.stderr)
    print(f"  Prompt: {len(prompt) // 1024}KB (~{len(prompt) // 4} tokens)",
          file=sys.stderr)

    # Invoke claude
    model_flag = {
        "opus": "claude-opus-4-6",
        "sonnet": "claude-sonnet-4-6",
    }.get(args.model, args.model)

    cmd = ["claude", "--print", "--model", model_flag, "--tools", "",
           "--output-format", "json"]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)

    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        timeout=None,
    )

    if result.returncode != 0:
        print(f"  FAILED (exit {result.returncode})", file=sys.stderr)
        if result.stderr:
            print(result.stderr[:500], file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(result.stdout)
        new_vocab = data.get("result", "")
        usage = data.get("usage", {})
        cost = data.get("total_cost_usd", 0)
        print(f"  ${cost:.4f}", file=sys.stderr)
    except (json.JSONDecodeError, KeyError):
        new_vocab = result.stdout

    # Strip markdown fences if the model wrapped output
    if new_vocab.startswith("```"):
        lines = new_vocab.split("\n")
        # Remove first and last fence lines
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        new_vocab = "\n".join(lines)

    new_vocab = new_vocab.strip() + "\n"

    if args.dry_run:
        print("\n--- PROPOSED VOCABULARY ---\n")
        print(new_vocab)
        print("--- END ---")
        print(f"\n  [DRY RUN] Would write to {VOCAB_PATH.relative_to(WORKSPACE)}",
              file=sys.stderr)
    else:
        VOCAB_PATH.write_text(new_vocab)
        print(f"  Written to {VOCAB_PATH.relative_to(WORKSPACE)} "
              f"({len(new_vocab)} bytes)", file=sys.stderr)


if __name__ == "__main__":
    main()
