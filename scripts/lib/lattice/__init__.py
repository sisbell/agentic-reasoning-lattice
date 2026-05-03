"""Lattice — project-level conventions for organizing lattices.

This project's conventions for how lattices are structured: ASN
organization, label sidecar paths, notation document format, etc.
Domain-neutral (applies to xanadu, materials, and any future
lattice).

Distinguishes from:
- `lib/backend/` — the substrate (addresses, links, persistence,
  type catalog). Xanadu in Nelson's sense.
- `lib/febe/` — FEBE wire-protocol binding to the substrate.
- `lib/<protocol>/` — protocol-specific composition (claim_convergence,
  note_convergence, etc.).

Code lives here when it composes substrate primitives but encodes
*how this project organizes lattices* — recognized formats, naming
conventions, sidecar layouts. Not part of the substrate; not specific
to one protocol; reusable across the project's lattices.
"""
