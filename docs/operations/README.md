# Xanadu Operations

This directory inventories, compares, and analyzes the operations that make up Xanadu's user-facing surface — the FEBE protocol commands by which the system is actually *used*. The work here defines what each operation is and explores how three independent statements of that definition agree or diverge.

## The three sources

1. **LM** — Nelson, *Literary Machines* 87.1, pages 4/61-4/70. The original specification. 17 operations.
2. **udanax-green** — Gregory's implementation under `channels/gregory/resources/udanax-test-harness/backend/`. The historical attempt at making the spec real, with the renumberings, dropped operations, additions, and stubs that emerged from contact with implementation reality.
3. **Project ASN notes** — our derivations and formalizations of each operation, under `_docuverse/documents/.../note/`. The math behind what each operation must guarantee.

Each source captures something the others don't: LM gives intent, Green gives implementation reality, ASNs give formal semantics. The directory holds the work of comparing them and reconciling the gaps.

## Questions this directory answers

- What did Nelson specify, and at what granularity?
- What did Green ship of that spec, and what did it drop or add?
- Where do the three sources diverge in opcode numbering, naming, or return shape?
- Which operations get ASN-level formalization in this project, and at what granularity (one note per opcode, or one per capability)?
- What does the LM-to-Green delta reveal about how protocol design survives implementation?

## Contents

- [`catalog.md`](catalog.md) — Master inventory. Side-by-side table of LM operations against Green's `requests.h` opcodes, `fns.c` entry points, and our extracted FEBE protocol reference. Includes discrepancies, evolution observations, and a three-layer split (information / operational / administrative) that frames how the operation surface grew under implementation pressure.

## What may grow here

- Per-operation deep-dives — semantic divergence, edge cases, the math an ASN note formalizes
- BEBE catalog — back-end/back-end protocol (LM 4/70-4/79; undefined in 87.1, undergoing definition)
- Mappings between ASN notes and the LM/Green operations they cover
- Wire-protocol details: opcode numbering on the wire, request/response encoding, dispatch behavior
- Findings from the udanax-test-harness against the three-source comparison
