# Review of ASN-0082

## REVISE

### Issue 1: Reviser drift — wp commentary imagines cases the carrier invariant already excludes
**ASN-0082, Weakest-precondition analysis (I3-VP) and (S8a-post)**:
- I3-VP wp: "but does need `n ≥ 1` (already a precondition) to advance the action point's value to a positive natural **even from `vₘ = 0`**."
- S8a-post wp: "without `p₂ ≥ 1`, even `v ≥ r` would not suffice (**a `p₂ = 0` p** with `c = v₂` would still admit `v ≥ r` with `v₂ − c = 0`)."

**Problem**: Both clauses motivate a precondition by imagining a state the contract forbids. Every `v ∈ dom(M(d))` satisfies S8a, so `vₘ ≥ 1` — `vₘ = 0` is unreachable, making "advance … even from `vₘ = 0`" a justification against an impossible input. Likewise `p ∈ V_1(d)` (a stated precondition) entails S8a on p, so `p₂ ≥ 1`; the hypothetical `p₂ = 0` p cannot arise. This is the reviser-drift pattern: prose imagining a case the precondition/carrier excludes.
**Required**: Delete the excluded-case hypotheticals. State the discharge positively (`vₘ ≥ 1` by S8a, composed with `n ≥ 1`; `v₂ ≥ p₂ + c ≥ 1 + 1` from `v ∈ R` and S8a on p) without inventing the forbidden state.

### Issue 2: Use-site inventory in the Subspace scoping axiom
**ASN-0082, Scoping axioms, Subspace axiom**: "The D-SHIFT well-definedness argument and the lemmas D-BJ, D-SEP, D-DP, D-CTG-post, D-MIN-post, D-SEQ-post, and S8-depth-post are likewise scoped to S = 1."
**Problem**: Enumerating every downstream lemma that inherits the `S = 1` scope does not advance the axiom's content — it is a forward consumer inventory that rots as lemmas are renamed or added. Each scoped lemma already states `At S = 1` in its own heading.
**Required**: Drop the inventory sentence; the axiom's "contraction is defined only on the text subspace" plus per-lemma scoping headers suffice.

### Issue 3: Prose justifying lemma ordering plus a second inventory
**ASN-0082, Invariant preservation (intro)**: "The lemmas are ordered so that each cites only earlier ones: typing invariants (S8-depth-post, S8a-post) first, then the contiguity triple (D-CTG-post, D-MIN-post, D-SEQ-post), then finiteness (S8-fin-post), then functionality (S2-post), referential integrity (S3-post), and allocation invariants (S7-post)."
**Problem**: This both justifies document ordering ("ordered so that each cites only earlier ones") and re-lists the seven post-lemmas that immediately follow under their own headings — two of the named anti-bloat patterns in one sentence. The dependency discipline is visible from the lemmas' own citations.
**Required**: Replace with a single substantive sentence (e.g., "We now verify the post-state satisfies each ASN-0036 invariant.") and let the lemmas speak for themselves.

## OUT_OF_SCOPE

### Topic 1: Depth > 1 generalization and external-reference updating
**Why out of scope**: Both are correctly deferred in Open Questions; the `#p = 2` depth axiom and the absence of an external-reference update protocol are acknowledged limitations, not errors in this ASN's stated scope.

VERDICT: REVISE
