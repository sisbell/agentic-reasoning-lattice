"""Per-claim file utilities — label index and substrate-sourced metadata.

Reads from the per-claim md + sidecar files under
`_docuverse/documents/claim/<asn>/`. The substrate-managed sidecars
(`<label>.name.md`, `<label>.description.md`) carry content that used
to live in the legacy claim YAMLs; this module surfaces them as a
single metadata dict per claim.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.backend.schema import ATTRIBUTE_SUFFIXES as _ATTR_SUFFIXES
from lib.backend.store import Store
from lib.predicates import current_contract_kind
from lib.protocols.febe.session import Session
from lib.shared.paths import LATTICE


def _is_claim_md(name):
    return (not name.startswith("_")
            and name.endswith(".md")
            and not name.endswith(_ATTR_SUFFIXES))


def build_label_index(claim_dir):
    """Return {label: filename_stem} for an ASN's claims.

    The filename stem is the label in the post-yaml architecture, so
    this is an identity map keyed by every claim md in the directory.
    """
    return {
        p.stem: p.stem
        for p in Path(claim_dir).glob("*.md")
        if _is_claim_md(p.name)
    }


def load_claim_metadata(claim_dir, label=None):
    """Load substrate-sourced metadata for one or all claims.

    Returns a dict (or {label: dict}) with keys:
    - label   : filename stem
    - name    : first line of <stem>.name.md
    - summary : full content of <stem>.description.md
    - type    : the contract.<kind> classifier on the claim's md path

    All fields are optional; absent ones simply don't appear in the dict.
    """
    claim_dir = Path(claim_dir)

    def _read_sidecar_first_line(stem, kind):
        doc = claim_dir / f"{stem}.{kind}.md"
        if not doc.exists():
            return None
        content = doc.read_text().strip()
        if not content:
            return None
        return content.split("\n", 1)[0].strip() or None

    def _read_sidecar_full(stem, kind):
        doc = claim_dir / f"{stem}.{kind}.md"
        if not doc.exists():
            return None
        content = doc.read_text().strip()
        return content or None

    lattice = Path(LATTICE).resolve()

    def _build(session, stem):
        result = {"label": stem}
        name = _read_sidecar_first_line(stem, "name")
        if name:
            result["name"] = name
        desc = _read_sidecar_full(stem, "description")
        if desc:
            result["summary"] = desc
        md_rel = str(
            (claim_dir / f"{stem}.md").resolve().relative_to(lattice)
        )
        addr = session.get_addr_for_path(md_rel)
        if addr is not None:
            kind = current_contract_kind(session, addr)
            if kind:
                result["type"] = kind
        return result

    with Store(LATTICE) as store:
        session = Session(store)
        if label is not None:
            if not (claim_dir / f"{label}.md").exists():
                return None
            return _build(session, label)
        return {
            p.stem: _build(session, p.stem)
            for p in sorted(claim_dir.glob("*.md"))
            if _is_claim_md(p.name)
        }
