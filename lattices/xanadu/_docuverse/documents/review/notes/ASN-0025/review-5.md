# Review of ASN-0025

## REVISE

### Issue 1: P6 derivation assumes an unstated equivalence between Σ.D and orgl
**ASN-0025, The Permanence Invariant**: "Since d's membership in Σ.D is witnessed by orgl(d) ∈ Σ.A, removing d would require removing orgl(d) from Σ.A — which P0 forbids."
**Problem**: The argument assumes that removing d from Σ.D *requires* removing orgl(d) from Σ.A. But Σ.D is introduced as an independent state component (one of three). Nothing prevents an operation from removing d from Σ.D while leaving orgl(d) in Σ.A — P0 constrains Σ.A, not Σ.D. The word "witnessed by" does not establish the necessary biconditional. Additionally, orgl appears in the state model informally ("Each document d ∈ Σ.D has a distinguished I-address orgl(d) ∈ Σ.A") but is not listed among the three components of Σ, despite being load-bearing for this derivation.
**Required**: Either (a) define Σ.D = {d : orgl(d) ∈ Σ.A}, making P6 a direct corollary of P0; or (b) state an explicit invariant (d ∈ Σ.D iff orgl(d) ∈ Σ.A) and verify it is preserved by each operation; or (c) derive P6 by direct case analysis — all seven operations already state Σ'.D ⊇ Σ.D, so the proof is one sentence with no orgl argument needed. Whichever route, include orgl as a formal state component or define it as derived from Σ.ι.

### Issue 2: INSERT has no formal postcondition for new V-entries
**ASN-0025, INSERT — V-space effect on d**: "The new content maps at positions starting at p."
**Problem**: The two formal postconditions specify the value mapping for shifted entries (q ≥ p) and unchanged entries (q < p). No formal postcondition specifies what Σ'.v(d) maps at the n new positions. The J0 preservation argument then asserts "The new V-entries map positions to addresses in B ⊆ Σ'.A" — but this claim has no formal antecedent to cite. The domain of Σ'.v(d) is also left implicit: the postconditions describe values at certain positions but do not collectively establish dom(Σ'.v(d)).
**Required**: Add a third postcondition: `(A i : 0 ≤ i < n : Σ'.v(d)(p ⊕ [i]) = b_{i+1})`. Optionally state dom(Σ'.v(d)) explicitly as the union of unchanged, new, and shifted position sets.

### Issue 3: COPY V-space postconditions given by reference to INSERT
**ASN-0025, COPY — V-space effect on d**: "their I-address mappings are unchanged — the shift is structurally parallel to INSERT"
**Problem**: The COPY section gives one formal postcondition (P5, visibility) but no formal shift postconditions. The shift is described as "structurally parallel to INSERT" — this is proof by similarity. The cases differ: INSERT adds fresh I-addresses from B; COPY adds existing I-addresses from S. The shift mechanics may be identical, but each operation's postconditions should be self-contained.
**Required**: State the shift postconditions explicitly for COPY: positions below p unchanged (with values), positions at or beyond p shifted forward by |S| (with values), new entries mapping to source I-addresses (with values). These may be textually identical to INSERT's postconditions — that is fine; the point is that they must be *stated*, not referenced.

### Issue 4: CREATE VERSION V-space postcondition is informal
**ASN-0025, CREATE VERSION — V-space effect**: "A new document d' appears with initial V-space mapping to the same I-addresses as Σ.v(d)."
**Problem**: This is the only formal postcondition for d's V-space relationship to d'. It is ambiguous between two readings: (a) Σ'.v(d') = Σ.v(d) as functions (position-for-position copy), or (b) rng(Σ'.v(d')) = rng(Σ.v(d)) (same content, possibly at different positions). The Structural Consequences section (Correspondence) later relies on "rng(Σ'.v(d')) = rng(Σ.v(d)) at creation" — which is reading (b). The Gregory evidence describes a position-for-position copy via `insertpm` — which is reading (a). These are different properties; the stronger one (a) implies the weaker (b) but not conversely.
**Required**: State a formal postcondition. If position-for-position: `(A q : q ∈ dom(Σ.v(d)) : Σ'.v(d')(q) = Σ.v(d)(q))` and `dom(Σ'.v(d')) = dom(Σ.v(d))`. If range-only: `rng(Σ'.v(d')) = rng(Σ.v(d))`. Choose one and state it.

### Issue 5: DELETE precondition does not declare its parameters
**ASN-0025, DELETE — Preconditions**: "d ∈ Σ.D; the target span exists in dom(Σ.v(d))."
**Problem**: The parameters p (start position) and n (width) appear only in the V-space effect, not in the preconditions. A precondition block should declare the operation's inputs and the conditions they must satisfy. "The target span exists" is informal — it does not state what must hold about p and n.
**Required**: State: d ∈ Σ.D; p ∈ dom(Σ.v(d)); n ≥ 1; {q : p ≤ q < p ⊕ [n]} ⊆ dom(Σ.v(d)). This mirrors INSERT's precondition structure.

## OUT_OF_SCOPE

### Topic 1: Link endset formalization
**Why out of scope**: The ASN correctly conditions link survivability on the premise that endsets reference I-space addresses and explicitly defers formalization to a link ASN. The conditional treatment is appropriate — the permanence guarantee applies to whatever I-addresses exist, regardless of how links use them.

### Topic 2: Version DAG structure
**Why out of scope**: CREATE VERSION establishes d' from d but does not formalize the parent-child relationship or the DAG structure of versions. This belongs in a version/branching ASN. The permanence ASN only needs the I-space and V-space effects of version creation, which it provides.

### Topic 3: Historical backtrack and storage reclamation
**Why out of scope**: Both are listed in Open Questions. P0 establishes that content *exists* in I-space permanently; whether a conforming implementation must provide retrieval mechanisms for invisible content, or may garbage-collect unreachable content, are implementation-boundary questions that do not affect the abstract permanence invariant.

VERDICT: REVISE
