"""Address-to-context adapters.

Bridges the trigger world (`(session, Address)`) to the work world
(`label`, `asn_num`, `claim_dir`, etc.). An agent's `run()` calls the
appropriate adapter to translate its incoming `addr` into a typed
context record, removing the boilerplate that would otherwise sit at
the top of every concrete agent.

Today: ClaimContext only. NoteContext / others can join the same
pattern when their first agent class lands.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from lib.backend.addressing import Address
from lib.lattice.labels import build_cross_asn_label_index
from lib.protocols.febe.protocol import Session
from lib.shared.claim_files import build_label_index
from lib.shared.paths import CLAIM_DIR


@dataclass(frozen=True)
class ClaimContext:
    """Per-claim domain context derived from a substrate Address.

    addr            — the substrate address
    label           — the claim's label (e.g., "T7")
    asn_label       — the ASN the claim belongs to (e.g., "ASN-0034")
    asn_num         — int form of the ASN
    claim_dir       — directory holding this ASN's per-claim files
    same_asn_deps   — labels this claim depends on within the same ASN
                      (read from citation.depends links at build time)
    """

    addr: Address
    label: str
    asn_label: str
    asn_num: int
    claim_dir: Path
    same_asn_deps: tuple[str, ...]


def claim_context_from_addr(session: Session, addr: Address) -> ClaimContext:
    """Build a ClaimContext from a substrate Address.

    Raises ValueError if the address has no label or path. Callers are
    responsible for catching when the address might not resolve cleanly
    (e.g., a stale reference).
    """
    label_index = build_cross_asn_label_index(session.store)
    rev_index = {a: lbl for lbl, a in label_index.items()}

    label = rev_index.get(addr)
    if label is None:
        raise ValueError(f"no label for address {addr}")

    path = session.get_path_for_addr(addr)
    if path is None:
        raise ValueError(f"no path for address {addr}")

    # _docuverse/documents/claim/<ASN>/<label>.md
    asn_label = path.split("/")[3]
    asn_num = int(asn_label[4:])
    claim_dir = CLAIM_DIR / asn_label

    asn_labels = set(build_label_index(claim_dir).keys())
    same_asn_deps = tuple(
        rev_index[link.to_set[0]]
        for link in session.active_links(
            "citation.depends", from_set=[addr],
        )
        if link.to_set and rev_index.get(link.to_set[0]) in asn_labels
    )

    return ClaimContext(
        addr=addr,
        label=label,
        asn_label=asn_label,
        asn_num=asn_num,
        claim_dir=claim_dir,
        same_asn_deps=same_asn_deps,
    )
