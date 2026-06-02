# Review of ASN-0047

I read the full transition model. The core mutability-hierarchy result (P3), the K.δ entity taxonomy, the elementary/composite framework, the J-couplings, and the eight worked examples are internally consistent and the proofs are largely sound. The findings below are specific and local — none is a size/split complaint.

## REVISE

### Issue 1: SubAllocatorBundle is miscategorized as inherited
**ASN-0047, "Properties Introduced → Inherited from foundation (restated for narrative continuity)"**: the table's intro reads "These properties are foundation invariants of ASN-0093 (or earlier foundation ASNs)," yet the SubAllocatorBundle row's statement is "Bundling lemma (introduced here): ... the one obligation discharged beyond them is the cross-subspace disjointness delta `dom(A_C(d)) ∩ dom(A_L(d')) = ∅`" with source column "derived (...)".
**Problem**: A lemma that is "introduced here," is "derived," and discharges a *new* obligation is not a foundation invariant. Filing it under "Inherited from foundation" contradicts both the table's stated scope and the row's own labels. A precise reader scanning the inherited table for what is taken on faith will misread an obligation this ASN actually proves.
**Required**: Move SubAllocatorBundle to the "New properties introduced by this ASN" table (or give it its own clearly-labeled "bundling lemma" row), keeping the explicit split between the inherited chain facts and the cross-subspace delta proved here.

### Issue 2: P7a is stated without a derivation at its definition site
**ASN-0047, "Cross-layer invariants"**: P6 and P7 each carry an explicit "*Derivation.*" block immediately after their statements; P7a is stated bare — "Every I-address in the content store has at least one provenance record" — with no derivation and no pointer.
**Problem**: At the definition site the guarantee is unsubstantiated. Its actual derivation lives far away in the Class (b) proof (where it leans on J0 + S3★ + L14 + S3★-aux + J1★), and a reader at the definition has no signal that it is discharged or where. By the standard that derived guarantees must carry their derivation, the asymmetry with P6/P7 is a gap.
**Required**: Add either a one-line forward pointer ("derived at Class (b) below") or a brief inline derivation matching the P6/P7 treatment.

### Issue 3: The "New properties introduced" table reproduces full operation definitions verbatim
**ASN-0047, "Properties Introduced → New properties"**: the K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.λ, K.ρ, and K.μ⁺_L rows restate complete preconditions/effects/frames already given in *Elementary transitions* and *Link allocation* (e.g., the K.λ row reproduces the entire precondition conjunction including the sub-allocator emission cases).
**Problem**: This is the same content stated twice in the same document. A summary index should name the operation and its one-line role; reproducing the full contract means two sites can drift, and the reader must reconcile them. This is distinct from the (declined) size/split findings — it is a per-row duplication, the exact accretion the anti-bloat classifier targets.
**Required**: Reduce each operation row to a one-line characterization (name + what it changes), and let the elementary-transition box remain the single normative statement of preconditions/effects/frames.

## OUT_OF_SCOPE

### Topic 1: Interior link/content withdrawal with renumbering
The Open Questions already park interior `DELETEVSPAN`-style compaction (K.μ⁻ models suffix removal only). This is correctly future territory, not an error in this ASN — noting it only to confirm no REVISE is warranted there.

META: not applicable — the ASN defines state, abstract operations on it, and their invariants without drifting into implementation mechanics.

VERDICT: REVISE
