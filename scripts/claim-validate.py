"""claim-validate — structural invariants on claim-convergence-stage claim files.

Runs mechanical checks from the Claim Document Contract
(docs/design-notes/claim-document-contract.md) against
lattices/<lattice>/claim-convergence/ASN-NNNN/.

The filename stem is the claim's label. Substrate links (claim,
contract.<kind>, citation, label, name, description) carry the rest of
the claim's structural metadata. The bold markdown declaration
(invariant #3) must use the filename stem in the label-position.

Implemented invariants:

  1. File pair completeness (every yaml has md and vice versa)
  2. Declaration matches label (includes type-keyword subtype)
  3. Depends agreement (substrate citations ↔ md Formal Contract Depends section)
  4. References resolve (every md Depends entry names an existing claim label)
  5. Declared symbols resolve (substrate: notation doc + per-claim signatures)
  6. Acyclic dependency graph (no cycles in the citation DAG)
  7. Body uniqueness (primary: cross-file bold declaration;
                      secondary: >1 Formal Contract block per file)
  8. Substrate attribute shape, doc format, coverage (label/name/description)

Usage:
    python scripts/claim-validate.py <ASN>
    python scripts/claim-validate.py 34
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from shared.common import find_asn
from shared.paths import CLAIM_DIR, LATTICE
from store.store import Store
from store.populate import build_cross_asn_label_index
from store.queries import current_contract_kind, active_links
from store.schema import VALID_SUBTYPES
from store.attributes import VALID_KINDS
from store.notation import read_notation

VALID_TYPES = VALID_SUBTYPES["contract"]


DECLARATION_RE = re.compile(
    r"\*\*([A-Za-z0-9()-]+(?:\.[0-9]+)?)"
    r"\s+\(([A-Za-z][A-Za-z0-9-]*)\)"
    r"\.\s*\*\*"
)
FORMAL_CONTRACT_RE = re.compile(r"^\*Formal Contract:\*\s*$", re.MULTILINE)
DEPENDS_MARKER_RE = re.compile(r"^-\s*\*Depends:\*")
DEP_ENTRY_RE = re.compile(r"^\s+-\s+([A-Za-z0-9()-]+(?:\.[0-9]+)?)(?:\s|$|,)")
TYPE_KEYWORDS = {
    "Axiom", "Definition", "Design-requirement", "Lemma", "Theorem", "Corollary", "Consequence",
}
# Substrate-owned document attribute kinds; their sibling docs are
# `<stem>.<kind>.md` and aren't claim files in their own right.
ATTRIBUTE_KINDS = tuple(sorted(VALID_KINDS))
# Kinds whose presence on every claim is enforced. description and
# signature are omitted intentionally — both are optional content, not
# structural requirements.
COVERED_ATTRIBUTE_KINDS = ("label", "name")

SINGLE_CHAR_SYMBOLS = re.compile(r"[<≤≥>≠=∈∉⊆⊇⇒⇔∀∃∧∨¬+−⊕⊖⊗⨀]")
MULTICHAR_SYMBOLS = [
    ("#·", re.compile(r"#·")),
    ("|·|", re.compile(r"\|·\|")),
]
STRUCTURAL_FIELDS = ("Axiom", "Definition", "Preconditions", "Postconditions",
                     "Invariant", "Frame", "Consequence")
FIELD_BULLET_RE = re.compile(r"^-\s+\*(\w[\w-]*)[:*]", re.MULTILINE)


def _extract_structural_fc_text(md_text):
    """Return Formal Contract content restricted to structural fields.

    Structural fields are the ones whose content is the claim's own
    load-bearing assertion: Axiom, Definition, Preconditions,
    Postconditions, Invariant, Frame. Depends descriptions (which
    mention other claims' symbols as documentation) are excluded.
    Trailing prose after the bulleted field list is also excluded —
    that prose is commentary, not structural content.

    Only the first Formal Contract block is considered — subsequent FC
    blocks belong to inlined bodies (a body-uniqueness violation) and
    should not attribute their symbols to this file.
    """
    fc_match = FORMAL_CONTRACT_RE.search(md_text)
    if not fc_match:
        return ""

    collected = []
    in_structural_field = False
    for line in md_text[fc_match.end():].split("\n"):
        # End of FC block: next bold claim-declaration
        if re.match(r"^\*\*[A-Za-z]", line):
            break
        # Top-level field bullet
        m = re.match(r"^-\s+\*(\w[\w-]*)[:*]", line)
        if m:
            field = m.group(1)
            in_structural_field = field in STRUCTURAL_FIELDS
            if in_structural_field:
                collected.append(line)
            continue
        # Continuation lines are kept only if indented (part of the
        # current structural bullet). An unindented non-empty line is
        # trailing prose — ends the structured list.
        if in_structural_field:
            if line == "" or line.startswith((" ", "\t")):
                collected.append(line)
            else:
                in_structural_field = False

    return "\n".join(collected)


_BULLET_RE = re.compile(r"^- `([^`]+)`")


def _build_symbol_owners(store):
    """Walk the substrate's `signature` links to build a symbol-owner map.

    Returns dict[symbol -> set[owner_label]]. Multiple owners per symbol
    are allowed (matched at check-time: owner-in-closure passes if ANY
    owner is in closure). Empty if no signatures exist.
    """
    owners = {}
    root = Path(LATTICE).resolve() if isinstance(LATTICE, str) else LATTICE.resolve()
    for link in active_links(store, "signature"):
        for sidecar_rel in link["to_set"]:
            sidecar_abs = root / sidecar_rel
            if not sidecar_abs.exists():
                continue
            owner_label = sidecar_abs.name[:-len(".signature.md")]
            for line in sidecar_abs.read_text().splitlines():
                m = _BULLET_RE.match(line)
                if m:
                    owners.setdefault(m.group(1), set()).add(owner_label)
    return owners


def claim_convergence_dir(asn_label):
    return CLAIM_DIR / asn_label


def line_of_offset(text, offset):
    return text.count("\n", 0, offset) + 1


_ATTR_SUFFIXES = tuple(f".{k}.md" for k in ATTRIBUTE_KINDS)


def _is_attr_doc(name):
    """Filename for a substrate-owned attribute doc (`.<kind>.md`). These
    are siblings of claim md files, not claims themselves; load_pairs
    skips them so they don't appear as orphan md files lacking yaml
    siblings."""
    return name.endswith(_ATTR_SUFFIXES)


def load_pairs(claim_dir):
    """Return {stem: {md: md_text}} across every claim .md in the dir.

    Substrate attribute docs (`<stem>.<kind>.md` for any attribute kind)
    are skipped — they are siblings of claim md files, not claims
    themselves.
    """
    pairs = {}
    for md_path in claim_dir.glob("*.md"):
        if md_path.name.startswith("_") or _is_attr_doc(md_path.name):
            continue
        pairs[md_path.stem] = {"md": md_path.read_text()}
    return pairs


def check_contract_classifier_present(pairs, store, label_index):
    """Every claim must have a contract.<kind> classifier link in the store
    with a valid subtype. This replaces the old yaml type-validity check.
    """
    findings = []
    for stem in sorted(pairs):
        md_path = label_index.get(stem)
        kind = current_contract_kind(store, md_path) if md_path else None
        if kind is None:
            findings.append({
                "rule": "missing-contract-classifier",
                "file": f"{stem}.md",
                "line": None,
                "detail": "no contract.<kind> classifier link in the store",
            })
            continue
        if kind not in VALID_TYPES:
            findings.append({
                "rule": "invalid-contract-classifier",
                "file": f"{stem}.md",
                "line": None,
                "detail": f"contract kind '{kind}' not in {sorted(VALID_TYPES)}",
            })
    return findings


def parse_md_depends(md_text):
    """Extract the set of labels listed under `- *Depends:*` in a claim's md."""
    labels = set()
    in_depends = False
    for line in md_text.split("\n"):
        if not in_depends:
            if DEPENDS_MARKER_RE.match(line):
                in_depends = True
            continue
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        if indent == 0 and stripped:
            break
        m = DEP_ENTRY_RE.match(line)
        if m:
            labels.add(m.group(1))
    return labels


def _build_citation_graph(pairs, store, label_index):
    """Build {label: [dep_labels]} from the substrate's citation links.

    For each claim with a known label and md path, follow citation links
    out of its md path. Map each citation's to_set[0] back to a label via
    the cross-ASN index. Citations to documents outside the index appear
    as labels that aren't in `pairs.values()` and will be flagged by
    check_references_resolve, matching the pre-migration behavior on
    yaml depends entries.
    """
    rev_index = {p: l for l, p in label_index.items()}
    graph = {}
    for stem in pairs:
        from_path = label_index.get(stem)
        if not from_path:
            graph[stem] = []
            continue
        deps = []
        for link in active_links(store, "citation", from_set=[from_path]):
            if not link["to_set"]:
                continue
            dep_label = rev_index.get(link["to_set"][0])
            if dep_label:
                deps.append(dep_label)
        graph[stem] = deps
    return graph


def check_depends_agreement(pairs, citation_graph):
    findings = []
    for stem, entry in sorted(pairs.items()):
        text = entry["md"]
        if text is None:
            continue
        store_deps = set(citation_graph.get(stem, []))
        md_deps = parse_md_depends(text)
        only_in_store = store_deps - md_deps
        only_in_md = md_deps - store_deps
        if only_in_store:
            findings.append({
                "rule": "depends-agreement",
                "file": f"{stem}.md",
                "line": None,
                "detail": f"in store citations but not in md Depends: {sorted(only_in_store)}",
            })
        if only_in_md:
            findings.append({
                "rule": "depends-agreement",
                "file": f"{stem}.md",
                "line": None,
                "detail": f"in md Depends but not in store citations: {sorted(only_in_md)}",
            })
    return findings


def check_references_resolve(pairs, citation_graph):
    """Every store citation and md Depends entry must name a claim that
    exists in the lattice (i.e., has a file pair). Inline prose citations
    are not checked."""
    findings = []
    labels = set(pairs.keys())

    for stem, entry in sorted(pairs.items()):
        text = entry["md"]

        for dep in citation_graph.get(stem, []):
            if dep not in labels:
                findings.append({
                    "rule": "references-resolve",
                    "file": f"{stem}.md",
                    "line": None,
                    "detail": f"citation to '{dep}' — no claim has that label",
                })

        if text:
            for dep in sorted(parse_md_depends(text)):
                if dep not in labels:
                    findings.append({
                        "rule": "references-resolve",
                        "file": f"{stem}.md",
                        "line": None,
                        "detail": f"md Depends references '{dep}' — no claim has that label",
                    })

    return findings


def check_declared_symbols_resolve(pairs, citation_graph, store):
    """Every tracked symbol used in a claim's Formal Contract block must
    resolve via the claim's transitive citation closure to an owning
    claim (or be a primitive). Implements invariant #7.

    Scope is the Formal Contract block only — not preamble or proof
    prose. A symbol in the Formal Contract is structurally required by
    the claim; a symbol in preamble or proof prose is often descriptive
    (e.g., "T4a uses NAT-sub's `−`") and not a structural dependence.

    Tracked symbols come from the substrate: notation (always-in-scope
    primitives) plus the union of all per-claim signatures. Symbols
    outside both are ignored — v1 accepts false negatives; false
    positives are the hard constraint.
    """
    primitives = read_notation(store)
    owners = _build_symbol_owners(store)

    graph = citation_graph

    def closure(label):
        seen = set()
        stack = [label]
        while stack:
            l = stack.pop()
            if l in seen:
                continue
            seen.add(l)
            stack.extend(graph.get(l, []))
        return seen

    findings = []
    for stem, entry in sorted(pairs.items()):
        text = entry["md"]
        if text is None:
            continue

        # Restrict to the structural fields of the first Formal Contract
        # block (Axiom, Definition, Preconditions, Postconditions,
        # Invariant, Frame). Preamble, proof prose, and Depends
        # descriptions are excluded — they commonly mention other
        # claims' symbols as documentation without structurally using
        # them, which would false-flag.
        fc_region = _extract_structural_fc_text(text)
        if not fc_region:
            continue

        symbols_used = set(SINGLE_CHAR_SYMBOLS.findall(fc_region))
        for tok, pat in MULTICHAR_SYMBOLS:
            if pat.search(fc_region):
                symbols_used.add(tok)

        deps = closure(stem)

        for sym in sorted(symbols_used):
            if sym in primitives:
                continue
            sym_owners = owners.get(sym)
            if not sym_owners:
                continue
            if stem in sym_owners:
                continue
            if sym_owners & deps:
                continue
            owner = sorted(sym_owners)[0] if len(sym_owners) == 1 else sorted(sym_owners)
            findings.append({
                "rule": "declared-symbols-resolve",
                "file": f"{stem}.md",
                "line": None,
                "detail": f"uses '{sym}' but does not depend on its owner '{owner}'",
            })

    return findings


def check_acyclic_dependency_graph(pairs, citation_graph):
    """Detect cycles in the citation subgraph. Dangling refs are ignored here
    — they're reported by references-resolve."""
    graph = {label: list(deps) for label, deps in citation_graph.items()}

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {label: WHITE for label in graph}
    findings = []
    seen = set()

    def visit(node, path):
        color[node] = GRAY
        for dep in graph.get(node, []):
            if dep not in color:
                continue
            if color[dep] == GRAY:
                cycle = path[path.index(dep):] + [dep]
                min_idx = cycle.index(min(cycle))
                canonical = tuple(cycle[min_idx:-1] + cycle[:min_idx] + [cycle[min_idx]])
                if canonical not in seen:
                    seen.add(canonical)
                    findings.append({
                        "rule": "acyclic-depends",
                        "file": None,
                        "line": None,
                        "detail": "cycle: " + " → ".join(canonical),
                    })
            elif color[dep] == WHITE:
                visit(dep, path + [dep])
        color[node] = BLACK

    for label in sorted(graph):
        if color[label] == WHITE:
            visit(label, [label])

    return findings


def check_declaration_and_body_uniqueness(pairs):
    """Checks invariants #3 (declaration matches label) and #9 (body uniqueness).

    Both scan the same bold-declaration matches; a single pass classifies each
    non-own-label declaration.
    """
    findings = []
    labels = set(pairs.keys())

    for stem, entry in sorted(pairs.items()):
        text = entry["md"]
        if text is None:
            continue
        own_label = stem

        own_decl_count = 0
        for m in DECLARATION_RE.finditer(text):
            decl_label = m.group(1)
            line_no = line_of_offset(text, m.start())
            if decl_label == own_label:
                own_decl_count += 1
                continue
            if decl_label in TYPE_KEYWORDS:
                findings.append({
                    "rule": "declaration-label-mismatch",
                    "file": f"{stem}.md",
                    "line": line_no,
                    "detail": f"type keyword '{decl_label}' in label-position "
                              f"(expected '{own_label}')",
                })
                continue
            if decl_label in labels:
                findings.append({
                    "rule": "body-uniqueness",
                    "file": f"{stem}.md",
                    "line": line_no,
                    "detail": f"declaration of {decl_label} "
                              f"(canonical home: {decl_label}.md)",
                })
                continue
            findings.append({
                "rule": "declaration-label-mismatch",
                "file": f"{stem}.md",
                "line": line_no,
                "detail": f"declaration of '{decl_label}' matches neither "
                          f"own label '{own_label}' nor any existing file's label",
            })

        if own_decl_count == 0:
            findings.append({
                "rule": "declaration-label-mismatch",
                "file": f"{stem}.md",
                "line": None,
                "detail": f"no bold declaration matches own label '{own_label}'",
            })

        contract_count = len(FORMAL_CONTRACT_RE.findall(text))
        if contract_count > 1:
            findings.append({
                "rule": "body-uniqueness",
                "file": f"{stem}.md",
                "line": None,
                "detail": f"{contract_count} Formal Contract blocks (expected 1)",
            })

    return findings


def check_attribute_link_shape(pairs, store, label_index, kind):
    """For each claim with a `<kind>` substrate attribute link, verify its
    shape: from_set is the claim md path, to_set is `<stem>.<kind>.md`,
    type_set is exactly `[<kind>]`. Coverage (whether the link exists) is
    a separate concern — this check operates only on links that exist.
    """
    findings = []
    for stem in sorted(pairs):
        md_path = label_index.get(stem)
        if not md_path:
            continue
        from pathlib import PurePosixPath
        expected_to = str(
            PurePosixPath(md_path).with_suffix(f".{kind}.md")
        )

        for link in active_links(store, kind, from_set=[md_path]):
            if link["type_set"] != [kind]:
                findings.append({
                    "rule": f"{kind}-link-shape",
                    "file": f"{stem}.md",
                    "line": None,
                    "detail": (f"link {link['id']}: type_set "
                               f"{link['type_set']} != [{kind!r}]"),
                })
                continue
            if link["from_set"] != [md_path]:
                findings.append({
                    "rule": f"{kind}-link-shape",
                    "file": f"{stem}.md",
                    "line": None,
                    "detail": (f"link {link['id']}: from_set "
                               f"{link['from_set']} != [{md_path!r}]"),
                })
                continue
            if link["to_set"] != [expected_to]:
                findings.append({
                    "rule": f"{kind}-link-shape",
                    "file": f"{stem}.md",
                    "line": None,
                    "detail": (f"link {link['id']}: to_set "
                               f"{link['to_set']} != [{expected_to!r}]"),
                })
    return findings


def check_attribute_coverage(pairs, store, label_index, kind):
    """For each claim in `pairs`, verify it has exactly one active
    substrate `<kind>` link (I1: label, I2: name).

    Coverage is not enforced for `description` — see COVERED_ATTRIBUTE_KINDS.
    """
    findings = []
    for stem in sorted(pairs):
        md_path = label_index.get(stem)
        if not md_path:
            continue
        links = active_links(store, kind, from_set=[md_path])
        if not links:
            findings.append({
                "rule": f"{kind}-coverage",
                "file": f"{stem}.md",
                "line": None,
                "detail": f"no active {kind} link from claim md",
            })
        elif len(links) > 1:
            findings.append({
                "rule": f"{kind}-coverage",
                "file": f"{stem}.md",
                "line": None,
                "detail": (f"{len(links)} active {kind} links "
                           f"(expected 1)"),
            })
    return findings


def check_attribute_doc_format(claim_dir, kind):
    """For each `<stem>.<kind>.md` doc in claim_dir, verify content format.
    Common rule: doc must be non-empty.
    Label-specific (stage-1 bridge): the first line must equal the
    filename stem.
    """
    findings = []
    suffix = f".{kind}.md"
    for doc in sorted(claim_dir.glob(f"*{suffix}")):
        if doc.name.startswith("_"):
            continue
        content = doc.read_text()
        if not content.strip():
            findings.append({
                "rule": f"{kind}-doc-format",
                "file": doc.name,
                "line": None,
                "detail": f"{kind} doc is empty",
            })
            continue
        if kind == "label":
            first_line = content.split("\n", 1)[0].rstrip()
            stem = doc.name[:-len(suffix)]
            if first_line != stem:
                findings.append({
                    "rule": "label-doc-format",
                    "file": doc.name,
                    "line": 1,
                    "detail": (f"first line {first_line!r} must equal "
                               f"filename stem {stem!r}"),
                })
    return findings


def run_all_checks(pairs, store=None, label_index=None, claim_dir=None):
    """Run every implemented invariant check in one pass. Returns a list of
    findings. Used by this script's main(), the gate, and validate-revise
    to avoid triplicating the check list.

    Citation invariants now query the substrate. If `store` is not provided,
    a Store is opened with default paths and closed at function exit.
    `claim_dir` is required for substrate-attribute doc-format checks; if
    omitted those checks are skipped.
    """
    own_store = store is None
    if own_store:
        store = Store()
        label_index = build_cross_asn_label_index(store=store)
    elif label_index is None:
        label_index = build_cross_asn_label_index(store=store)

    try:
        citation_graph = _build_citation_graph(pairs, store, label_index)

        findings = []
        findings.extend(check_contract_classifier_present(pairs, store, label_index))
        findings.extend(check_depends_agreement(pairs, citation_graph))
        findings.extend(check_references_resolve(pairs, citation_graph))
        findings.extend(check_declared_symbols_resolve(pairs, citation_graph, store))
        findings.extend(check_acyclic_dependency_graph(pairs, citation_graph))
        findings.extend(check_declaration_and_body_uniqueness(pairs))
        for kind in ATTRIBUTE_KINDS:
            findings.extend(check_attribute_link_shape(pairs, store, label_index, kind))
            if claim_dir is not None:
                findings.extend(check_attribute_doc_format(claim_dir, kind))
            if kind in COVERED_ATTRIBUTE_KINDS:
                findings.extend(check_attribute_coverage(pairs, store, label_index, kind))
        return findings
    finally:
        if own_store:
            store.close()


def main():
    parser = argparse.ArgumentParser(
        description="Validate claim-convergence-stage claim files against "
                    "the Claim Document Contract.")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        print(f"ASN-{asn_num:04d} not found", file=sys.stderr)
        return 2

    claim_dir = claim_convergence_dir(asn_label)
    if not claim_dir.exists():
        print(f"No claim-convergence directory: {claim_dir}", file=sys.stderr)
        return 2

    pairs = load_pairs(claim_dir)
    findings = run_all_checks(pairs, claim_dir=claim_dir)

    print(f"[FORMALIZATION-VALIDATE] {asn_label} ({claim_dir})")
    if not findings:
        print("  all checks: clean")
        return 0

    by_rule = {}
    for f in findings:
        by_rule.setdefault(f["rule"], []).append(f)

    for rule, fs in sorted(by_rule.items()):
        print(f"  {rule}: {len(fs)} finding(s)")
        for f in fs:
            if f["file"] and f["line"]:
                loc = f"{f['file']}:{f['line']}"
            elif f["file"]:
                loc = f["file"]
            else:
                loc = None
            prefix = f"{loc} — " if loc else ""
            print(f"    {prefix}{f['detail']}")

    return 1


if __name__ == "__main__":
    sys.exit(main())
