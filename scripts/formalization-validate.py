"""formalization-validate — structural invariants on formalization-stage claim files.

Runs mechanical checks from the Claim File Contract
(docs/design-notes/claim-file-contract.md) against
lattices/<lattice>/formalization/ASN-NNNN/.

yaml `label` is the authoritative identity for each claim. Filename (invariant
#2) and markdown bold declaration (invariant #3) must conform to it. These
checks compare both surfaces against the yaml.

Implemented invariants:

  1. File pair completeness (every yaml has md and vice versa)
  2. Filename matches label
  3. Declaration matches label (includes type-keyword subtype)
  4. YAML well-formed (parses; required fields present; type is a valid keyword)
  5. Depends agreement (yaml depends list ↔ md Formal Contract Depends section)
  6. References resolve (every yaml/md Depends entry names an existing claim label)
  7. Declared symbols resolve (v1: curated symbol-owners table per lattice,
                               in place of per-claim yaml vocabulary fields)
  8. Acyclic dependency graph (no cycles in the yaml depends DAG)
  9. Body uniqueness (primary: cross-file bold declaration;
                      secondary: >1 Formal Contract block per file)

Usage:
    python scripts/formalization-validate.py <ASN>
    python scripts/formalization-validate.py 34
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from shared.common import find_asn
from store.store import Store
from store.populate import build_cross_asn_label_index


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
VALID_TYPES = {
    "axiom", "definition", "design-requirement", "lemma", "theorem", "corollary", "consequence",
}
REQUIRED_YAML_FIELDS = ("label", "name", "type", "summary")

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


def _repo_root():
    return Path(__file__).resolve().parent.parent


def _load_symbol_config():
    """Return the symbol-owners config for the xanadu lattice.

    Returns a dict with 'primitives' (list) and 'owners' (dict).
    Missing config file is treated as empty (check becomes a no-op).
    """
    path = _repo_root() / "lattices" / "xanadu" / "symbol-owners.yaml"
    if not path.exists():
        return {"primitives": [], "owners": {}}
    data = yaml.safe_load(path.read_text()) or {}
    return {
        "primitives": data.get("primitives") or [],
        "owners": data.get("owners") or {},
    }


def formalization_dir(asn_label):
    repo_root = Path(__file__).resolve().parent.parent
    return repo_root / "lattices" / "xanadu" / "formalization" / asn_label


def line_of_offset(text, offset):
    return text.count("\n", 0, offset) + 1


def load_pairs(claim_dir):
    """Return {stem: {yaml, md, yaml_error}} across every .yaml/.md in the dir."""
    pairs = {}
    for yaml_path in claim_dir.glob("*.yaml"):
        if yaml_path.name.startswith("_"):
            continue
        stem = yaml_path.stem
        entry = pairs.setdefault(stem, {"yaml": None, "md": None, "yaml_error": None})
        try:
            entry["yaml"] = yaml.safe_load(yaml_path.read_text())
        except yaml.YAMLError as e:
            entry["yaml_error"] = str(e)
    for md_path in claim_dir.glob("*.md"):
        if md_path.name.startswith("_"):
            continue
        stem = md_path.stem
        entry = pairs.setdefault(stem, {"yaml": None, "md": None, "yaml_error": None})
        entry["md"] = md_path.read_text()
    return pairs


def check_file_pair_completeness(pairs):
    findings = []
    for stem, entry in sorted(pairs.items()):
        has_yaml = entry["yaml"] is not None or entry["yaml_error"] is not None
        if not has_yaml and entry["md"] is not None:
            findings.append({
                "rule": "missing-yaml",
                "file": f"{stem}.md",
                "line": None,
                "detail": f"body exists but no {stem}.yaml",
            })
        if has_yaml and entry["md"] is None:
            findings.append({
                "rule": "missing-md",
                "file": f"{stem}.yaml",
                "line": None,
                "detail": f"yaml exists but no {stem}.md",
            })
    return findings


def check_yaml_well_formed(pairs):
    findings = []
    for stem, entry in sorted(pairs.items()):
        if entry["yaml_error"]:
            findings.append({
                "rule": "yaml-error",
                "file": f"{stem}.yaml",
                "line": None,
                "detail": f"YAML parse error: {entry['yaml_error']}",
            })
            continue
        data = entry["yaml"]
        if data is None:
            if entry["md"] is not None:
                findings.append({
                    "rule": "yaml-error",
                    "file": f"{stem}.yaml",
                    "line": None,
                    "detail": "empty YAML document",
                })
            continue
        if not isinstance(data, dict):
            findings.append({
                "rule": "yaml-error",
                "file": f"{stem}.yaml",
                "line": None,
                "detail": f"top level is not a mapping "
                          f"(got {type(data).__name__})",
            })
            continue
        for field in REQUIRED_YAML_FIELDS:
            if field not in data:
                findings.append({
                    "rule": "missing-field",
                    "file": f"{stem}.yaml",
                    "line": None,
                    "detail": f"missing required field '{field}'",
                })
                continue
            value = data[field]
            if not value:
                findings.append({
                    "rule": "missing-field",
                    "file": f"{stem}.yaml",
                    "line": None,
                    "detail": f"required field '{field}' is empty",
                })
        prop_type = data.get("type")
        if prop_type and prop_type not in VALID_TYPES:
            findings.append({
                "rule": "invalid-type",
                "file": f"{stem}.yaml",
                "line": None,
                "detail": f"type='{prop_type}' not in {sorted(VALID_TYPES)}",
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
    for entry in pairs.values():
        data = entry["yaml"]
        if not isinstance(data, dict):
            continue
        label = data.get("label")
        if not label:
            continue
        from_path = label_index.get(label)
        if not from_path:
            graph[label] = []
            continue
        deps = []
        for link in store.find_links(from_set=[from_path], type_set=["citation"]):
            if not link["to_set"]:
                continue
            dep_label = rev_index.get(link["to_set"][0])
            if dep_label:
                deps.append(dep_label)
        graph[label] = deps
    return graph


def check_depends_agreement(pairs, citation_graph):
    findings = []
    for stem, entry in sorted(pairs.items()):
        data = entry["yaml"]
        text = entry["md"]
        if not isinstance(data, dict) or text is None:
            continue
        label = data.get("label")
        if not label:
            continue
        store_deps = set(citation_graph.get(label, []))
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
    """Every store citation and md Depends entry must name a claim whose
    yaml.label exists in the lattice. Inline prose citations are not checked."""
    findings = []
    labels = set()
    for entry in pairs.values():
        data = entry["yaml"]
        if isinstance(data, dict) and data.get("label"):
            labels.add(data["label"])

    for stem, entry in sorted(pairs.items()):
        data = entry["yaml"]
        text = entry["md"]

        if isinstance(data, dict):
            this_label = data.get("label")
            for dep in citation_graph.get(this_label, []):
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


def check_declared_symbols_resolve(pairs, citation_graph, config=None):
    """Every tracked symbol used in a claim's Formal Contract block must
    resolve via the claim's transitive citation closure to an owning
    claim (or be a primitive). Implements invariant #7.

    Scope is the Formal Contract block only — not preamble or proof
    prose. A symbol in the Formal Contract is structurally required by
    the claim; a symbol in preamble or proof prose is often descriptive
    (e.g., "T4a uses NAT-sub's `−`") and not a structural dependence.

    The config (primitives + owners) is curated at
    lattices/xanadu/symbol-owners.yaml. Untracked symbols (not in either
    list) are ignored — v1 accepts false negatives; false positives are
    the hard constraint.
    """
    if config is None:
        config = _load_symbol_config()
    primitives = set(config.get("primitives") or [])
    owners = config.get("owners") or {}

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
        data = entry["yaml"]
        text = entry["md"]
        if not isinstance(data, dict) or text is None:
            continue
        label = data.get("label")
        if not label:
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

        deps = closure(label)

        for sym in sorted(symbols_used):
            if sym in primitives:
                continue
            owner = owners.get(sym)
            if owner is None:
                continue
            if owner == label:
                continue
            if owner in deps:
                continue
            findings.append({
                "rule": "declared-symbols-resolve",
                "file": f"{stem}.yaml",
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


def check_filename_matches_label(pairs):
    findings = []
    for stem, entry in sorted(pairs.items()):
        data = entry["yaml"]
        if not isinstance(data, dict):
            continue
        label = data.get("label")
        if label and label != stem:
            findings.append({
                "rule": "filename-label-mismatch",
                "file": f"{stem}.yaml",
                "line": None,
                "detail": f"yaml label '{label}' but file stem '{stem}' "
                          f"(rename file to '{label}.{{yaml,md}}')",
            })
    return findings


def check_declaration_and_body_uniqueness(pairs):
    """Checks invariants #3 (declaration matches label) and #9 (body uniqueness).

    Both scan the same bold-declaration matches; a single pass classifies each
    non-own-label declaration.
    """
    findings = []
    labels_to_stem = {}
    for stem, entry in pairs.items():
        data = entry["yaml"]
        if isinstance(data, dict) and data.get("label"):
            labels_to_stem[data["label"]] = stem

    for stem, entry in sorted(pairs.items()):
        text = entry["md"]
        data = entry["yaml"]
        if text is None or not isinstance(data, dict):
            continue
        own_label = data.get("label")
        if not own_label:
            continue

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
            if decl_label in labels_to_stem:
                findings.append({
                    "rule": "body-uniqueness",
                    "file": f"{stem}.md",
                    "line": line_no,
                    "detail": f"declaration of {decl_label} "
                              f"(canonical home: {labels_to_stem[decl_label]}.md)",
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
                "detail": f"no bold declaration matches own yaml.label '{own_label}'",
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


def run_all_checks(pairs, store=None, label_index=None):
    """Run every implemented invariant check in one pass. Returns a list of
    findings. Used by this script's main(), the gate, and validate-revise
    to avoid triplicating the check list.

    Citation invariants now query the substrate. If `store` is not provided,
    a Store is opened with default paths and closed at function exit.
    """
    own_store = store is None
    if own_store:
        store = Store()
        label_index = build_cross_asn_label_index()
    elif label_index is None:
        label_index = build_cross_asn_label_index()

    try:
        citation_graph = _build_citation_graph(pairs, store, label_index)

        findings = []
        findings.extend(check_file_pair_completeness(pairs))
        findings.extend(check_yaml_well_formed(pairs))
        findings.extend(check_filename_matches_label(pairs))
        findings.extend(check_depends_agreement(pairs, citation_graph))
        findings.extend(check_references_resolve(pairs, citation_graph))
        findings.extend(check_declared_symbols_resolve(pairs, citation_graph))
        findings.extend(check_acyclic_dependency_graph(pairs, citation_graph))
        findings.extend(check_declaration_and_body_uniqueness(pairs))
        return findings
    finally:
        if own_store:
            store.close()


def main():
    parser = argparse.ArgumentParser(
        description="Validate formalization-stage claim files against "
                    "the Claim File Contract.")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        print(f"ASN-{asn_num:04d} not found", file=sys.stderr)
        return 2

    claim_dir = formalization_dir(asn_label)
    if not claim_dir.exists():
        print(f"No formalization directory: {claim_dir}", file=sys.stderr)
        return 2

    pairs = load_pairs(claim_dir)
    findings = run_all_checks(pairs)

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
