# Review of ASN-0036

## REVISE

*(none)*

## OUT_OF_SCOPE

### Topic 1: Operation-level invariant preservation
Each operation (INSERT, DELETE, COPY, REARRANGE) must prove it preserves S0, S3, D-CTG, and D-MIN. The ASN correctly identifies this as a verification obligation ("Whether DELETE, INSERT, COPY, and REARRANGE preserve D-CTG is a verification obligation for each operation's ASN") and defers it.
**Why out of scope**: These are per-operation proofs that belong in the operation-defining ASNs, not in the state model ASN.

### Topic 2: Maximal span decomposition uniqueness
S8 proves existence of a finite decomposition (via singletons) but leaves open whether a unique maximal form (fewest runs) exists. The open questions section acknowledges this.
**Why out of scope**: The existence result is what matters for the state model; optimality of decomposition is an independent structural question.

### Topic 3: Displacement mechanism for insertion
ValidInsertionPosition defines *where* insertion is valid but not *how* existing V-positions shift to accommodate new content. The open questions ask what invariants the displacement mechanism must satisfy.
**Why out of scope**: The displacement mechanism is part of INSERT's specification, not the state model.

VERDICT: CONVERGED
