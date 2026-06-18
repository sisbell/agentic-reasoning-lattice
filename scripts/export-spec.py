#!/usr/bin/env python3
"""Export the finalized spec — the active note DAG — into a standalone,
highly-navigable markdown repo (default: ./xanadu-specification).

This is a ONE-WAY, regenerable export. The lattice (_docuverse) stays the
system-of-record; this script reads it and (re)writes the spec repo. Never
hand-edit the output — re-run the export.

Membership is the live active note DAG (mirrors dag_status.py): every
non-retired note, topo-sorted, classed into three layers:
    core -> foundation/ , operations/ , protocols/
Each note contributes two files (full note + condensed statements). No
per-claim decomposition. Navigation (dependency links, cross-links,
per-layer indexes, reading order, dag.yaml) is generated, not authored.

Usage:
    python scripts/export-spec.py
    python scripts/export-spec.py --out ../xanadu-specification
"""

from __future__ import annotations

import argparse
import re
import shutil
from glob import glob
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from diagnostics.dag_status import _topo_sorted  # noqa: E402
from lib.protocols.febe.session import open_session  # noqa: E402
from lib.shared.asn_classes import class_for  # noqa: E402
from lib.shared.paths import LATTICE  # noqa: E402

# class label (from asn-classes.yaml) -> output layer directory + display name
LAYERS = {
    "core": ("foundation", "Foundation"),
    "operations": ("operations", "Operations"),
    "protocols": ("protocols", "Protocols"),
}
LAYER_ORDER = ["foundation", "operations", "protocols"]
LAYER_BLURB = {
    "foundation": (
        "The address/span/link/transition algebra the whole system rests on — "
        "tumbler arithmetic, ownership, the strand and mapping-block models, the "
        "allocation substrate, and the transition model. Every other layer builds "
        "on these."
    ),
    "operations": (
        "The FEBE command surface — the concrete operations a client invokes "
        "(retrieval, insert/delete/copy/rearrange, link creation and editing, "
        "link and document discovery). Each operation is specified against the "
        "foundation algebra."
    ),
    "protocols": (
        "A predicate system for stigmergic agentic systems, built on Xanadu. "
        "Agents coordinate by reading substrate state and emitting "
        "typed relations — there is no direct message passing. This layer specifies "
        "the typed-relation primitive and its shape and type frameworks, a predicate "
        "language whose definitions live as substrate content, predicate composition, "
        "the consistency and isolation model for concurrent agents, and quiescence "
        "as the termination condition. It is the coordination stack the "
        "[reasoning lattice](https://github.com/sisbell/agentic-reasoning-lattice) "
        "that produced this specification runs on."
    ),
}

ASN_RE = re.compile(r"ASN-(\d{4})")


def asn_num(asn: str) -> int:
    return int(ASN_RE.search(asn).group(1))


def note_path_index() -> dict[str, Path]:
    """asn -> full-note path on disk (the .md that is not .statements.md)."""
    idx: dict[str, Path] = {}
    pat = re.compile(r"/note/(ASN-\d{4})-")
    for f in glob("_docuverse/documents/**/note/ASN-*.md", recursive=True):
        if ".statements.md" in f or ".motif." in f:
            continue
        m = pat.search(f)
        if m:
            idx.setdefault(m.group(1), Path(f))
    return idx


def read_title(note_file: Path) -> str:
    try:
        first = note_file.read_text().splitlines()[0].strip()
    except (OSError, IndexError):
        return ""
    t = re.sub(r"^#+\s*", "", first)
    t = re.sub(r"^ASN-\d{4}\s*[:\-]\s*", "", t)
    return t.strip()


def slug_of(note_file: Path) -> str:
    # ASN-0034-tumbler-algebra.md -> tumbler-algebra
    stem = note_file.stem  # ASN-0034-tumbler-algebra
    return re.sub(r"^ASN-\d{4}-", "", stem)


def build_model(session):
    """Return ordered list of note records and the global asn->record map."""
    order, deps = _topo_sorted(session)
    path_idx = note_path_index()

    records: dict[str, dict] = {}
    skipped: list[str] = []
    for asn in order:
        nf = path_idx.get(asn)
        if nf is None or not nf.exists():
            skipped.append(asn)
            continue
        cls = class_for(asn_num(asn))
        layer_dir, _ = LAYERS.get(cls, ("foundation", "Foundation"))
        slug = slug_of(nf)
        records[asn] = {
            "asn": asn,
            "num": asn_num(asn),
            "title": read_title(nf) or asn,
            "class": cls,
            "layer": layer_dir,
            "slug": slug,
            "note_src": nf,
            "stmt_src": nf.with_suffix(".statements.md"),
            "filename": f"{nf.stem}.md",
            "stmt_filename": f"{nf.stem}.statements.md",
            "deps": sorted(deps.get(asn, set()), key=asn_num),
        }
    ordered = [records[a] for a in order if a in records]
    return ordered, records, skipped


def rel_link(from_layer: str, target: dict) -> str:
    """Relative markdown path from a note page in from_layer to target's note."""
    if target["layer"] == from_layer:
        return target["filename"]
    return f"../{target['layer']}/{target['filename']}"


def dep_links(rec: dict, records: dict) -> str:
    if not rec["deps"]:
        return "_(none — root of the DAG)_"
    parts = []
    for d in rec["deps"]:
        t = records.get(d)
        if t is None:
            parts.append(d)
        else:
            parts.append(f"[{d} · {t['title']}]({rel_link(rec['layer'], t)})")
    return ", ".join(parts)


def note_header(rec: dict, records: dict) -> str:
    layer_name = LAYERS[rec["class"]][1]
    return (
        f"> **{rec['asn']} · {rec['title']}** — {layer_name} layer  \n"
        f"> **Depends on:** {dep_links(rec, records)}  \n"
        f"> [Condensed statements →]({rec['stmt_filename']}) · "
        f"[↑ {layer_name} index](README.md) · [↑ Spec home](../README.md)\n\n"
        f"---\n\n"
    )


def stmt_header(rec: dict) -> str:
    layer_name = LAYERS[rec["class"]][1]
    return (
        f"> **{rec['asn']} · {rec['title']}** — condensed claim statements  \n"
        f"> [← Full note]({rec['filename']}) · "
        f"[↑ {layer_name} index](README.md) · [↑ Spec home](../README.md)\n\n"
        f"---\n\n"
    )


def write_notes(out: Path, ordered: list, records: dict) -> int:
    written = 0
    for rec in ordered:
        layer_path = out / rec["layer"]
        layer_path.mkdir(parents=True, exist_ok=True)
        # full note
        body = rec["note_src"].read_text()
        (layer_path / rec["filename"]).write_text(note_header(rec, records) + body)
        written += 1
        # condensed statements (every active note has one; guard anyway)
        if rec["stmt_src"].exists():
            stmt = rec["stmt_src"].read_text()
            (layer_path / rec["stmt_filename"]).write_text(stmt_header(rec) + stmt)
            written += 1
    return written


def _table(recs: list, records: dict, self_prefix: str, dep_href) -> list:
    """Render an ASN | Title | Depends-on table. self_prefix is prepended to
    a row's own note/statements links; dep_href(target_rec) yields a dep link."""
    lines = ["| ASN | Title | Depends on |", "| --- | --- | --- |"]
    for r in recs:
        deps = ", ".join(
            f"[{records[d]['num']:04d}]({dep_href(records[d])})"
            for d in r["deps"] if d in records
        ) or "—"
        lines.append(
            f"| {r['num']:04d} "
            f"| [{r['title']}]({self_prefix}{r['filename']}) "
            f"([statements]({self_prefix}{r['stmt_filename']})) | {deps} |"
        )
    return lines


def layer_readme(out: Path, layer_dir: str, ordered: list, records: dict) -> None:
    layer_name = next(n for d, n in LAYERS.values() if d == layer_dir)
    recs = [r for r in ordered if r["layer"] == layer_dir]
    lines = [
        f"# {layer_name}",
        "",
        LAYER_BLURB[layer_dir],
        "",
        f"{len(recs)} notes, in dependency (topological) order.",
        "",
    ]
    lines += _table(recs, records, "", lambda t: rel_link(layer_dir, t))
    lines += ["", "[↑ Spec home](../README.md)", ""]
    (out / layer_dir / "README.md").write_text("\n".join(lines))


XANADU_INTRO = """\
## What Xanadu is

Project Xanadu, conceived by Ted Nelson in 1960, is the original vision of
hypertext: a single, permanent, universal repository of documents — the
*docuverse* — in which every fragment of content has a stable, globally unique
address that is assigned once and never changes. From that one guarantee the
rest of Xanadu follows:

- **Permanent addressing.** Every character, link, and document has an address
  (a *tumbler*) that survives editing, copying, and reorganization. Nothing is
  ever overwritten or renumbered; new versions and edits are expressed as new
  addressed content over the same permanent space.
- **Transclusion.** Content is quoted *by reference*, not by copy. A passage
  lives in exactly one place yet can appear in any number of documents, and its
  origin is always recoverable — so quotation, reuse, and royalty all have a
  precise meaning.
- **Bidirectional links.** A link is a first-class, addressed object visible and
  traversable from *both* of its endpoints, rather than a one-way jump embedded
  in a page.
- **Versions and provenance.** Because addresses are permanent and edits are
  additive, the full history and origin of any content is always queryable.

This repository is the formal specification of that system — the address and
span algebra, the content and arrangement model, the link and relation store,
the client operations, and the cross-cutting protocols that keep the whole
consistent. It is grounded in Nelson's design intent (*Literary Machines*) and
Roger Gregory's 1988 `udanax-green` implementation.
"""

HOW_GENERATED = """\
## How this specification was generated

This spec was not written by hand. It was *derived* by an [agentic reasoning
lattice](https://github.com/sisbell/agentic-reasoning-lattice). For each
question about the system, two independent agent channels —
one reasoning from established theory, one from the raw source evidence — explore
the hypothesis space separated by a vocabulary firewall, and a synthesis step
integrates them into a reasoning document with explicit, dependency-tracked
claims. Each note (an **ASN**) then matures through review / revise cycles until
it reaches *quiescence*.

The result is the dependency DAG below: every note builds only on notes beneath
it, and every claim is traceable back to its foundations and to the design
intent it came from.
"""


def top_readme(out: Path, ordered: list, records: dict) -> None:
    counts = {d: sum(1 for r in ordered if r["layer"] == d) for d in LAYER_ORDER}
    lines = [
        "# Xanadu Specification",
        "",
        "A formal specification of the Xanadu hypertext system — "
        f"**{len(ordered)} notes** organized into three layers and connected as a "
        "dependency DAG.",
        "",
        XANADU_INTRO,
        HOW_GENERATED,
        "## The three layers",
        "",
    ]
    for d in LAYER_ORDER:
        name = next(n for dd, n in LAYERS.values() if dd == d)
        lines.append(f"- **[{name}](#{name.lower()}-{counts[d]}-notes)** "
                     f"({counts[d]}) — {LAYER_BLURB[d]}")
    lines += [
        "",
        "Within each layer the notes are listed in dependency (topological) "
        "order — every note appears after all of its dependencies.",
        "",
    ]
    for d in LAYER_ORDER:
        name = next(n for dd, n in LAYERS.values() if dd == d)
        recs = [r for r in ordered if r["layer"] == d]
        lines += [
            f"## {name} ({counts[d]} notes)",
            "",
            LAYER_BLURB[d],
            "",
        ]
        lines += _table(recs, records, f"{d}/",
                         lambda t: f"{t['layer']}/{t['filename']}")
        lines += ["", f"Full index: [{name} layer]({d}/README.md)", ""]
    lines += [
        "## Machine-readable graph",
        "",
        "See [`dag.yaml`](dag.yaml) for the structured dependency graph "
        "(id, title, class, depends-on).",
        "",
    ]
    (out / "README.md").write_text("\n".join(lines))


def write_dag_yaml(out: Path, ordered: list) -> None:
    lines = [
        "# Xanadu specification dependency graph (generated by scripts/export-spec.py).",
        "# Topologically ordered. class mirrors the lattice's asn-classes.yaml",
        "# ('core' = foundation layer).",
        "notes:",
    ]
    for r in ordered:
        deps = "[" + ", ".join(str(asn_num(d)) for d in r["deps"]) + "]"
        title = r["title"].replace('"', '\\"')
        lines += [
            f"  - asn: {r['num']}",
            f"    title: \"{title}\"",
            f"    class: {r['class']}",
            f"    layer: {r['layer']}",
            f"    depends_on: {deps}",
        ]
    (out / "dag.yaml").write_text("\n".join(lines) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="xanadu-specification",
                    help="output spec repo directory (default: xanadu-specification)")
    args = ap.parse_args()

    out = Path(args.out)
    # Clean only the generated content dirs + index files; leave .git, LICENSE etc.
    for d in LAYER_ORDER:
        if (out / d).exists():
            shutil.rmtree(out / d)
    out.mkdir(parents=True, exist_ok=True)

    with open_session(LATTICE) as session:
        ordered, records, skipped = build_model(session)

    n = write_notes(out, ordered, records)
    for d in LAYER_ORDER:
        layer_readme(out, d, ordered, records)
    top_readme(out, ordered, records)
    write_dag_yaml(out, ordered)

    counts = {d: sum(1 for r in ordered if r["layer"] == d) for d in LAYER_ORDER}
    print(f"Exported {len(ordered)} notes ({n} files) to {out}/")
    for d in LAYER_ORDER:
        print(f"  {d:<12} {counts[d]}")
    if skipped:
        print(f"  skipped (no note file): {', '.join(skipped)}")
    print(f"  + README.md, dag.yaml, {len(LAYER_ORDER)} layer indexes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
