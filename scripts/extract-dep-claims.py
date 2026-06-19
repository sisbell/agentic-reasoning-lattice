#!/usr/bin/env python3
"""Extract foundation claims a given note actually uses, via label-driven
inversion.

Approach:
  1. Read the target note's inquiry frontmatter to get its declared deps.
  2. For each dep ASN, parse its `note_statements.md` sidecar to
     enumerate every claim label (section headers `## <label> —`).
  3. For each label, do a word-boundary substring search in the note
     body. Labels that appear are included in the output bundle.
  4. Write a single dep-claims doc with one section per dep, listing
     hits + the extracted statements sections.

This avoids the unreliability of regexing citation patterns out of
prose. The dep's label set is finite and authoritative; matching a
label against the note body is a bounded, decidable check.

Caveats:
  - Short labels (T1, M0, S0, K.α) can occasionally match worked-example
    variable names or unrelated prose. Inspect the hit list before
    trusting the output.
  - Labels containing special characters (D-CTG★, Σ.C, S(p,d), K.μ⁺_L)
    are matched literally with non-alphanumeric flanking boundaries.

Usage:
    python scripts/extract-dep-claims.py 47
    python scripts/extract-dep-claims.py 47 --out _workspace/dep-claims/ASN-0047.md
    python scripts/extract-dep-claims.py 47 --show-misses    # also list labels NOT found
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import OrderedDict
from pathlib import Path

import yaml


SECTION_HEADER_PATTERN = re.compile(
    r'^##\s+(\S[^—–\-\n]*?)\s+[—–\-]\s*(.*)$',
    re.MULTILINE,
)

# When the left side of the dash is a generic claim-type word, the actual
# claim label lives on the right side of the dash instead. For
# `## Definition — SubspaceProjection (DEF, definition)`, the label is
# "SubspaceProjection," not "Definition." Treating "Definition" as a
# label would produce false-positive matches (the word appears in
# every note's prose).
GENERIC_TYPE_LABELS = {
    "Definition", "Theorem", "Lemma", "Axiom", "Corollary",
    "Proposition", "Sub-lemma", "Notation", "Convention",
}


def extract_label(left_side: str, right_side: str) -> str:
    """Given a parsed section header `## <left> — <right>`, return the
    label that should be used for matching.

    If the left side is a generic claim-type word (Definition, Theorem,
    Lemma, etc.), use the first identifier-like token from the right side
    instead. Otherwise the left side is the label.
    """
    left = left_side.strip()
    if left not in GENERIC_TYPE_LABELS:
        return left
    # Take the first whitespace-delimited token from the right side,
    # stripping trailing punctuation like commas or paren'd type tags.
    right = right_side.strip()
    # Strip a trailing `(...)` paren block (type/class tag)
    right = re.sub(r'\s*\(.*?\)\s*$', '', right).strip()
    # First token
    first = right.split()[0] if right else left
    return first.rstrip(',.;:')


def parse_inquiry_deps(inquiry_path: Path) -> list[int]:
    """Read the inquiry frontmatter and return the `depends:` list."""
    text = inquiry_path.read_text()
    # Frontmatter is between two `---` lines at the top
    match = re.match(r'^---\n(.*?)\n---\n', text, re.DOTALL)
    if not match:
        return []
    fm = yaml.safe_load(match.group(1)) or {}
    deps = fm.get('depends', [])
    return [int(d) for d in deps if isinstance(d, int)]


def enumerate_labels(statements_text: str) -> list[tuple[str, str]]:
    """Return list of (label, full_section_text) for every section header
    `## <label> — <name>` in the statements text.

    The label is resolved via `extract_label` so generic claim-type
    prefixes (Definition, Theorem, ...) are replaced by the right-side
    name. Section text runs from the header to the next `## ` or EOF.
    """
    results: list[tuple[str, str]] = []
    matches = list(SECTION_HEADER_PATTERN.finditer(statements_text))
    for i, m in enumerate(matches):
        label = extract_label(m.group(1), m.group(2))
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(statements_text)
        section = statements_text[start:end].rstrip() + '\n'
        results.append((label, section))
    return results


def label_appears_in(label: str, text: str) -> bool:
    """True iff `label` appears in `text` as a distinct token.

    Distinct = not preceded or followed by an alphanumeric character or
    underscore. This catches the common false-positive cases (M01 vs M0,
    T10a vs T10) while still matching labels with punctuation.
    """
    escaped = re.escape(label)
    pattern = re.compile(
        rf'(?<![A-Za-z0-9_]){escaped}(?![A-Za-z0-9_])',
    )
    return bool(pattern.search(text))


def find_note_path(asn_label: str, note_dir: Path) -> Path | None:
    for f in sorted(note_dir.glob(f'{asn_label}-*.md')):
        if '.statements.' in f.name:
            continue
        return f
    return None


def find_statements_path(
    asn_label: str, note_dir: Path, claim_root: Path,
) -> tuple[Path, str] | None:
    """Locate the authoritative statements source for `asn_label`.

    Preference order:
      1. Claim-side aggregate: `claim/<asn_label>/_statements.md`
         (claim-derived ASNs — richer content, full Formal Contracts)
      2. Note-side sidecar: `note/<asn_label>-*.statements.md`
         (note-only ASNs — abbreviated, but still usable)

    Returns `(path, kind)` where kind ∈ {'claim-aggregate', 'note-sidecar'}.
    """
    claim_agg = claim_root / asn_label / '_statements.md'
    if claim_agg.exists():
        return claim_agg, 'claim-aggregate'
    for f in sorted(note_dir.glob(f'{asn_label}-*.statements.md')):
        return f, 'note-sidecar'
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Extract foundation claims a note uses via label-driven inversion.',
    )
    parser.add_argument(
        'asn', help='Target ASN (e.g., 47 or ASN-0047)',
    )
    parser.add_argument(
        '--deps', help=(
            'Comma-separated dep ASN numbers (e.g., 34,36,43,93). '
            'Use when the target has no inquiry frontmatter.'
        ),
    )
    parser.add_argument(
        '--out', help='Write bundled output to file (default: stdout)',
    )
    parser.add_argument(
        '--show-misses', action='store_true',
        help='Append a section listing dep labels NOT found in the note',
    )
    parser.add_argument(
        '--lattice-root', default='_docuverse/documents/1.1/1',
        help='Lattice (node, user) root',
    )
    args = parser.parse_args()

    asn_num = int(re.sub(r'\D', '', args.asn))
    asn_label = f'ASN-{asn_num:04d}'

    lattice_root = Path(args.lattice_root)
    note_dir = lattice_root / 'note'
    inquiry_dir = lattice_root / 'inquiry'

    note_path = find_note_path(asn_label, note_dir)
    if note_path is None:
        print(f'No note found for {asn_label} under {note_dir}', file=sys.stderr)
        return 1

    if args.deps:
        deps = [int(re.sub(r'\D', '', d)) for d in args.deps.split(',') if d.strip()]
        deps_source = f'--deps CLI arg ({args.deps})'
    else:
        inquiry_path = inquiry_dir / f'{asn_label}.md'
        if not inquiry_path.exists():
            print(
                f'No inquiry frontmatter at {inquiry_path}. '
                f'Use --deps to specify dep ASNs explicitly '
                f'(e.g., --deps 34,36,43,93).',
                file=sys.stderr,
            )
            return 1
        deps = parse_inquiry_deps(inquiry_path)
        if not deps:
            print(f'No declared deps in {inquiry_path}', file=sys.stderr)
            return 1
        deps_source = f'inquiry frontmatter ({inquiry_path.name})'

    note_text = note_path.read_text()

    out_lines: list[str] = []
    out_lines.append(f'# Dependency Claims Bundle for {asn_label}')
    out_lines.append('')
    out_lines.append(
        f'*Label-driven inversion: each dep\'s statements.md enumerated, '
        f'each label tested for presence in {note_path.name}. '
        f'Declared deps: {", ".join(f"ASN-{d:04d}" for d in deps)} '
        f'(source: {deps_source}).*'
    )
    out_lines.append('')

    total_labels = 0
    total_hits = 0
    misses_by_dep: OrderedDict[str, list[str]] = OrderedDict()

    claim_root = lattice_root / 'claim'

    for dep_num in deps:
        dep_label = f'ASN-{dep_num:04d}'
        located = find_statements_path(dep_label, note_dir, claim_root)
        if located is None:
            out_lines.append(f'## From {dep_label}')
            out_lines.append('')
            out_lines.append(
                f'*No statements source found '
                f'(neither `claim/{dep_label}/_statements.md` nor '
                f'`note/{dep_label}-*.statements.md`). Skipped.*'
            )
            out_lines.append('')
            continue

        statements_path, statements_kind = located
        statements_text = statements_path.read_text()
        labels = enumerate_labels(statements_text)

        if not labels:
            out_lines.append(f'## From {dep_label}')
            out_lines.append('')
            out_lines.append(
                f'*No claim sections parsed from {statements_path.name} '
                f'({statements_kind}). Check section header format `## <label> —`.*'
            )
            out_lines.append('')
            continue

        hits: list[tuple[str, str]] = []
        misses: list[str] = []
        for label, section in labels:
            if label_appears_in(label, note_text):
                hits.append((label, section))
            else:
                misses.append(label)

        total_labels += len(labels)
        total_hits += len(hits)
        misses_by_dep[dep_label] = misses

        out_lines.append(f'## From {dep_label}')
        out_lines.append('')
        out_lines.append(
            f'*{len(hits)}/{len(labels)} dep labels found in {note_path.name}. '
            f'Source: `{statements_path.name}` ({statements_kind}).*'
        )
        out_lines.append('')
        out_lines.append(f'Labels in: {", ".join(label for label, _ in hits) if hits else "(none)"}')
        out_lines.append('')

        for label, section in hits:
            out_lines.append(section.rstrip())
            out_lines.append('')

    if args.show_misses:
        out_lines.append('## Labels NOT Found (Diagnostic)')
        out_lines.append('')
        out_lines.append(
            f'Labels declared in dep statements.md files but absent from the '
            f'target note body. Use this to spot dep claims the note may need '
            f'to cite but doesn\'t, or to spot labels the matcher is missing '
            f'due to short-string ambiguity.'
        )
        out_lines.append('')
        for dep_label, misses in misses_by_dep.items():
            if not misses:
                continue
            out_lines.append(f'### {dep_label} ({len(misses)} unused)')
            out_lines.append('')
            for m in misses:
                out_lines.append(f'- `{m}`')
            out_lines.append('')

    summary = (
        f'Matched {total_hits}/{total_labels} dep labels across '
        f'{len(deps)} deps for {asn_label}.'
    )

    output = '\n'.join(out_lines)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output)
        print(f'Wrote {len(output)} bytes to {out_path}', file=sys.stderr)
        print(summary, file=sys.stderr)
    else:
        sys.stdout.write(output)
        print(summary, file=sys.stderr)

    return 0


if __name__ == '__main__':
    sys.exit(main())
