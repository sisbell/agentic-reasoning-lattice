# Review of ASN-0025

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Link deletion and modification operations
The seven operations include CREATE LINK but no DELETE LINK or MODIFY LINK. Since DELETE restricts its precondition to text-subspace V-positions, link positions are irremovable under the current operation set — the link ordinal range within each document can only grow. A future link-operations ASN would need to define link removal (with J2-preserving backward shifts) and verify P0/P1/J0 for it.
**Why out of scope**: New operations, not an error in the permanence argument for the seven operations defined here.

### Topic 2: REARRANGE zone-level postconditions
The ASN deliberately specifies REARRANGE at the constraint level (P4 + domain preservation + exterior frame + link frame) rather than giving zone-by-zone position mappings for 3-cut rotation and 4-cut swap. The constraint level suffices for invariant preservation but does not uniquely determine the permutation. The ASN explicitly defers this to an operation-semantics ASN.
**Why out of scope**: Operation semantics, not permanence.

### Topic 3: Link internal structure and endset formalization
Link survivability is derived conditionally: "if link endsets reference I-space addresses." The CREATE LINK precondition requires endpoint addresses in Σ.A, and the link value v_l is stored immutably (P1), but v_l is an opaque Value — no formal structure is given for extracting endsets from it. The derivation chain (creation → encoding → immutability → permanent resolution) requires the link ASN to formalize that encoding.
**Why out of scope**: Link structure is a new specification topic, and the ASN correctly identifies the conditional nature of its derivation.

### Topic 4: Concurrency
All invariant preservation proofs assume sequential state transitions. Concurrent operations on different documents satisfy UF-V independently, but concurrent operations on the same document are not addressed. This is standard for a sequential specification; a concurrency model is separate work.
**Why out of scope**: New territory requiring a different formal framework.

---

The ASN is thorough. Every claim I checked held up.

**State model**: VPos = {text, link} × ℕ⁺ is a clean abstraction of TA7a's ordinal-only formulation. The tag/ordinal decomposition correctly restricts comparison and arithmetic to within a single subspace. DocId = IAddr gives orgl injectivity for free.

**Invariant verification**: P0, P1, J0, J1, J2, and P6 are verified for all seven operations. The J1/J2 set-algebra arguments are explicit — each partitions the post-state ordinals into disjoint sets (new, shifted, unchanged) and shows their union is {1, ..., k ± n}. I checked boundary cases (INSERT into empty document, DELETE of entire text, INSERT at end/beginning, self-COPY with overlapping source and destination) and all resolve correctly under the stated preconditions and postconditions.

**Domain completeness**: For each operation, the explicit domain formula and value postconditions together fully determine Σ'.v(d) — every position in the post-state domain is covered by exactly one postcondition clause, and the clauses are pairwise disjoint. I verified this for INSERT (five domain components with non-overlapping ordinal ranges), DELETE (three components), and COPY (five components, same structure as INSERT).

**Derivations**: P2 follows from P0 ∧ P1 by induction — the step is shown explicitly. P7 follows from T9 + T10 + GlobalUniqueness + P3 — the chain from distinct creation events to distinct address sets is explicit. The four structural consequences (link survivability, attribution, correspondence, transclusion integrity) each name their premises and show the chain.

**Self-COPY (d = d_s)**: The P5 case split is correct. When the source span overlaps the insertion point, shifted entries retain their I-addresses (third V-space postcondition), so source content remains visible at shifted positions. Source is evaluated in the pre-state, so the semantics is unambiguous.

VERDICT: CONVERGED
