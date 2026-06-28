"""Synthetic-workspace fixture for foundation / sync_deps tests.

`foundation_dep_addrs` and `plan_reconciliation` resolve an ASN's
declared dependencies against the workspace globals (WORKSPACE,
NOTE_DIR, INQUIRY_DIR) and the live substrate. Tests that pinned those
functions to a real ASN (e.g. ASN-0097) were brittle: when that ASN's
deps changed — or it was retired — the golden values went stale.

This fixture builds a throwaway workspace on disk, monkeypatches the
path globals (in every module that captured them) to point at it, and
hands back a small builder for declaring ASN notes/inquiries with
known dependency sets. Tests then assert against what they declared,
never against the evolving live substrate.
"""

from __future__ import annotations

import json
import tempfile
from dataclasses import dataclass
from pathlib import Path

import pytest

from lib.backend.emit import emit, emit_inquiry, emit_note
from lib.backend.store import Store
from lib.protocols.febe.session import Session


@dataclass
class SynthWorkspace:
    """Builder over a temp workspace with the real docuverse layout."""

    root: Path
    store: Store
    session: Session
    note_dir: Path
    inquiry_dir: Path

    def _rel(self, p: Path) -> str:
        return str(p.relative_to(self.root))

    def add_note(self, asn_id: int, slug: str = "synthetic"):
        """Register a note doc `ASN-NNNN-<slug>.md` and classify it."""
        path = self.note_dir / f"ASN-{asn_id:04d}-{slug}.md"
        path.write_text(f"# ASN-{asn_id:04d}\n")
        addr = self.session.register_path(self._rel(path))
        emit_note(self.store, addr)
        return addr

    def add_inquiry(self, asn_id: int, depends):
        """Register an inquiry doc `ASN-NNNN.md` whose frontmatter
        declares `depends: [...]`, and classify it."""
        path = self.inquiry_dir / f"ASN-{asn_id:04d}.md"
        dep_list = ", ".join(str(d) for d in depends)
        path.write_text(f"---\ndepends: [{dep_list}]\n---\n\n# inquiry\n")
        addr = self.session.register_path(self._rel(path))
        emit_inquiry(self.store, addr)
        return addr

    def emit_dep(self, from_addr, to_addr):
        """Emit a single one-per-target `citation.depends` link."""
        return emit(
            self.store, "citation.depends",
            from_set=[from_addr], to_set=[to_addr],
        )[0]


@pytest.fixture
def synth_workspace(monkeypatch):
    """Yield a SynthWorkspace with the workspace path globals redirected.

    The globals are captured at import time by several modules, so each
    copy must be patched: `paths` (function-local importers in
    foundation), `common` (find_asn), and `sync_deps` (module-level).
    """
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp).resolve()
        docuverse = root / "_docuverse"
        author = docuverse / "documents" / "1.1" / "1"
        note_dir = author / "note"
        inquiry_dir = author / "inquiry"
        note_dir.mkdir(parents=True)
        inquiry_dir.mkdir(parents=True)
        docuverse.joinpath("paths.json").write_text(json.dumps({
            "_meta": {
                "registry_doc": "1.1.0.1.0.1",
                "lattice_doc": "1.1.0.1.0.1.1",
                "lattice_name": "test",
            },
            "paths": {},
        }, indent=2))
        docuverse.joinpath("links.jsonl").write_text("")

        import lib.shared.common as common_mod
        import lib.shared.paths as paths_mod
        import lib.shared.sync_deps as sync_deps_mod
        for mod, attr in (
            (paths_mod, "WORKSPACE"), (paths_mod, "NOTE_DIR"),
            (paths_mod, "INQUIRY_DIR"), (common_mod, "NOTE_DIR"),
            (sync_deps_mod, "WORKSPACE"), (sync_deps_mod, "NOTE_DIR"),
        ):
            target = root if attr == "WORKSPACE" else (
                note_dir if attr == "NOTE_DIR" else inquiry_dir
            )
            monkeypatch.setattr(mod, attr, target)

        store = Store(root)
        session = Session(store)
        yield SynthWorkspace(
            root=root, store=store, session=session,
            note_dir=note_dir, inquiry_dir=inquiry_dir,
        )
