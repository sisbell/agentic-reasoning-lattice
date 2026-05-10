# Review of ASN-0034

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Zero-padded divergence vs Divergence definition
The Divergence definition (two cases: component divergence and prefix divergence) and TumblerSub's zero-padded divergence are conceptually distinct — the zero-padded scan can find a later divergence point when the shorter operand's extension has matching zeros. The TA3 proof correctly qualifies with "under zero-padding" and is sound throughout, but a future ASN that builds on both concepts may benefit from a named distinction.
**Why out of scope**: The TA3 proof is correct as written; the terminological overlap is a readability concern for downstream consumers, not an error in this ASN.

### Topic 2: Left cancellation for the order
The open question asks whether `a ⊕ x ≤ a ⊕ y ⟹ x ≤ y`. This would strengthen TA1-strict from a strict-order statement to an order-embedding characterization. The answer is likely yes for same-action-point displacements (follows from the constructive definition) and requires care for different action points.
**Why out of scope**: Stated as an open question; belongs in a future ASN on order-algebraic consequences.

### Topic 3: Projection algebra of TumblerAdd
The open question about TA-MTO's projection interpretation (idempotence, composition at different action points) is interesting — TumblerAdd at action point k discards information below k, and nested projections interact in a well-defined way (the TA-assoc proof already shows this for three cases). Formalizing this as an abstract projection would give a cleaner account of the tail-replacement semantics.
**Why out of scope**: The observation is correct but extends the algebra beyond what the current ASN requires.

VERDICT: CONVERGED
