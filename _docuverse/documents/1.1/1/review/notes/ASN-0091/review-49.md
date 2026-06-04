# Review of ASN-0091

## REVISE

### Issue 1: Re-proof of a foundation identification already supplied by ASN-0047

**ASN-0091, "Unified-State Identification E_doc = dom(M)"**: the subsection proves by induction (base case `dom(M₀) = (E₀)_doc = ∅`, step via K.σ and K.δ joint extension, monotonicity via M1/P1) that `E_doc = dom(M)` at every reachable state.

**Problem**: ASN-0047's M1 (ArrangementMonotonicity) already states this identification verbatim — "Constrains the *document set* `dom(M) = E_doc` (the allocated documents...)." The entire inductive re-derivation reconstructs a foundation fact. It is also not specific to REARRANGE: any operation bridging the 0047 and 0093 vocabularies would need the same identification, so it is infrastructure accreted into an operation note.

**Required**: Delete the inductive argument; discharge RA-reg from K.μ~'s `d ∈ E_doc` precondition by a one-line citation of ASN-0047 M1's `dom(M) = E_doc`.

### Issue 2: The content↔link crossing exclusion is argued twice

**ASN-0091, RA-adm definition paragraph**: "for example, a π carrying a content-subspace V-position to a link-subspace V-position would yield a Σ' violating S3★ + L14 (a content-subspace V-position would map to an address in `dom(Σ'.C)`... disjoint from `dom(Σ'.L)`... so S3★'s link-subspace clause would fail...)."

**Problem**: This is the identical argument later formalized as a derived claim in RE-subpres Stage 2 (content-to-link direction). The definitional paragraph pre-empts its own later derivation with the same S3★ + L14 reasoning — "two paragraphs say the same thing in different words."

**Required**: State RA-adm abstractly in the definition (Σ' satisfies the per-state invariants); let the crossing exclusion appear once, as RE-subpres.

### Issue 3: "What Rearrangement Is Not" is summary meta-prose

**ASN-0091, "What Rearrangement Is Not"**: "What rearrangement does is exactly one thing... Everything else is invariant — the content store, link store... — each catalogued with its RE-* label and provenance in the Claims Introduced table. Everything else follows..."

**Problem**: The section advances no reasoning. It restates the Claims Introduced table in prose and explicitly points back to it. This is the essay-content-in-a-structural-slot pattern the anti-bloat classifier targets.

**Required**: Remove the section; the Claims Introduced table already carries this content.

### Issue 4: P4a is discharged twice

**ASN-0091, "P4a Handling"** vs. the **"Remaining per-state invariants"** layer: the latter states ExtendedReachableStateInvariants (a valid composite) establishes "the composite-boundary properties P4★ and P7a" and P4a; the former then gives a bespoke trace-append argument for P4a as "the one foundation invariant excluded from the frame-inheritance class."

**Problem**: For the non-trivial (K.μ~) case, ExtendedReachableStateInvariants already delivers P4a at the boundary, so the bespoke subsection duplicates that discharge. (The collapse case is `Σ' = Σ`, where P4a is trivial.)

**Required**: Drop the standalone "P4a Handling" subsection, or fold it into one sentence noting that the collapse case is the identity; do not re-derive what the composite-boundary discharge already covers.

### Issue 5: The collapse case is re-explained in four locations

**ASN-0091**: the collapse case (`π ≠ id` but `M'(d) = M(d)`, realiser is the identity) is set up in the opening "REARRANGE as Vstream-Only Operation," restated in the "REARRANGE_K Realises" intro ("the collapse case needs no clause discharge"), again in the admissibility-discharge layer ("The collapse case is the identity transition `Σ' = Σ`..."), and again as clause (ii)'s table row.

**Problem**: The underlying case split is genuine and needed once, but it is narrated in four places. Multiple sections deferring to / restating the same case is the accretion pattern.

**Required**: Establish the K.μ~-vs-identity case split once (the opening), and let downstream sections reference it without re-explaining.

### Issue 6: Use-site inventory in the shape-package layer

**ASN-0091, shape-package layer**: "This layer depends only on RA-dom, and supplies exactly the shape invariants (S8a, S8-depth, D-CTG★, D-MIN★) that K.μ~'s admissibility clause (i) consumes."

**Problem**: The trailing clause enumerates a downstream consumer rather than advancing the layer's content; the clause-(i) discharge is already tabulated in the admissibility table.

**Required**: End the sentence at "depends only on RA-dom."

## OUT_OF_SCOPE

### Topic 1: Link-subspace REARRANGE semantics
The note's Open Questions ask what a link-subspace rearrangement would preserve. RE-sub fixes the link subspace pointwise when the cut subspace is content; defining a link-subspace REARRANGE is new territory for a future ASN, not a gap here.

VERDICT: REVISE
