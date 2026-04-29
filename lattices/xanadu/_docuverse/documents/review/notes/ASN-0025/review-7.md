# Review of ASN-0025

## REVISE

### Issue 1: REARRANGE link-subspace frame relies on unestablished cross-subspace ordering
**ASN-0025, REARRANGE**: "Since all cut positions are text-subspace and link positions sort after all text positions under T1, the exterior frame subsumes link positions per TA7b."
**Problem**: The exterior frame quantifier `(A q : q ∈ dom(Σ.v(d)) ∧ (q < c₁ ∨ q ≥ cₖ) : Σ'.v(d)(q) = Σ.v(d)(q))` requires evaluating `q < c₁` or `q ≥ cₖ` when `q` is a link-subspace position and `c₁, cₖ` are text-subspace positions. Under TA7a's ordinal-only formulation, V-positions within a subspace are single-component ordinals with the subspace identifier held as structural context. Cross-subspace comparison is not defined in this formulation. A link at ordinal [3] compared against text cuts c₁ = [2] and cₖ = [5] would satisfy neither [3] < [2] nor [3] ≥ [5], placing it *inside* the cut range — incorrectly subjecting it to rearrangement. INSERT and DELETE both include explicit link-subspace frame postconditions `(A q : q is a link position : Σ'.v(d)(q) = Σ.v(d)(q))`; REARRANGE relies instead on an ordering argument that the formalism does not support.
**Required**: Add an explicit link-subspace frame postcondition to REARRANGE, matching INSERT and DELETE. Alternatively, formalize V-position ordering as operating on the full `[S, x]` form (subspace identifier, ordinal) so that T1 gives `[2, y] > [1, x]` for all x, y. Either approach resolves the gap, but the explicit postcondition is more consistent with the other operations.

### Issue 2: REARRANGE interior postconditions under-determined
**ASN-0025, REARRANGE**: "The displacement arithmetic for each zone follows from the cut geometry; we specify REARRANGE at the constraint level."
**Problem**: The formal postconditions — P4 (multiset invariance), domain preservation, exterior frame — do not uniquely determine REARRANGE. Multiple distinct permutations satisfy all three constraints. The prose describes the intended permutation (3-cut rotation, 4-cut swap with middle shift), but these are not formalized. The other six operations have fully determined V-space postconditions; REARRANGE is the exception. For the permanence argument (P0/P1/J0 preservation), the constraint level suffices. But the ASN presents itself as defining operations ("We now examine each operation's effect on Σ.ι and Σ.v"), and an under-determined operation definition is a gap relative to that framing.
**Required**: Either add zone-level postconditions specifying which V-positions map where within [c₁, cₖ) for the 3-cut and 4-cut cases, or explicitly state that the constraint-level specification is deliberate for this ASN and that zone-level semantics are deferred.

### Issue 3: V-space contiguity invariant unstated
**ASN-0025, State Model**: "next(d, Σ) = max({q ∈ dom(Σ.v(d)) : q is a text position}) ⊕ [1]"
**Problem**: The definitions of `next(d, Σ)` and `next_link(d, Σ)`, and the INSERT/DELETE preconditions, implicitly require V-positions within each subspace to form contiguous ordinal ranges {[1], [2], ..., [k]}. This invariant is maintained by all seven operations — INSERT and COPY shift to create room, DELETE shifts to close gaps, REARRANGE preserves the domain, CREATE VERSION copies position-for-position, CREATE DOCUMENT starts empty — but it is never stated. Without it, `next(d, Σ) = max + 1` does not guarantee the result is the first *unused* position (there could be gaps), and the INSERT precondition `p ∈ dom(Σ.v(d)) ∪ {next(d, Σ)}` does not guarantee gap-free insertion.
**Required**: State contiguity as a formal invariant — e.g., `(A d ∈ Σ.D : {q ordinal : q ∈ dom(Σ.v(d)) ∧ q is a text position} = {1, ..., |text positions in d|})` — and verify it is preserved by each operation. The same applies to link-subspace positions and `next_link`.

### Issue 4: P6 status ambiguous between constraint and theorem
**ASN-0025, The Permanence Invariant**: "P6 (Document Set Growth). No operation removes a document from Σ.D. ... This follows by case analysis over the seven operations."
**Problem**: P0 and P1 are stated as universal constraints on "any state transition Σ → Σ' caused by any operation." P6 is labeled "derived (case analysis)" in the properties table — a theorem about these seven operations, not a universal constraint. But the phrasing "No operation removes a document" reads as universal. The distinction matters: a future operation (e.g., ARCHIVE DOCUMENT) could satisfy P0 ∧ P1 while removing a document from Σ.D, breaking P6. Furthermore, P6 implicitly stabilizes UF-V's quantification domain — if Σ.D can shrink, the set of documents covered by UF-V changes between states.
**Required**: Decide whether P6 is a constraint (all conforming operations must preserve it) or a theorem (derived for these operations only). If a constraint, introduce it alongside P0/P1 as an axiom and remove "derived." If a theorem, scope the "No operation" language to the seven defined operations.

## OUT_OF_SCOPE

### Topic 1: Full REARRANGE zone-level semantics
**Why out of scope**: The detailed displacement arithmetic for 3-cut rotation and 4-cut swap — specifying exactly which V-positions map where within the cut range — is a complete operation semantics question, not an address permanence question. The constraint-level specification is sufficient for P0/P1/J0 preservation. Zone-level postconditions belong in an operation semantics ASN.

### Topic 2: Link endset formalization
**Why out of scope**: The ASN correctly conditions link survivability on "if link endsets reference I-space addresses." Formalizing endset representation, the link state model, and link-specific invariants is a distinct specification topic.

### Topic 3: Orgl properties (injectivity, immutability)
**Why out of scope**: The orgl function maps documents to their structural I-addresses. Injectivity follows from GlobalUniqueness, and immutability follows from P1. These properties are not needed for the permanence argument and belong in a document model ASN.

### Topic 4: Historical backtrack and storage reclamation
**Why out of scope**: The open questions about whether invisible content must be re-accessible, whether I-space can be garbage-collected, and what durability granularity is required are policy questions that constrain implementations beyond the abstract permanence guarantee. These are separate specification concerns.

VERDICT: REVISE
