# Review of ASN-0102

## REVISE

### Issue 1: (SL) closes with a use-site inventory of its downstream consumers
**ASN-0102, X14 (step-local recording fact)**: "Both the J1★ and P4★ arguments below invoke (SL) rather than re-deriving it."
**Problem**: This sentence enumerates the downstream consumers of (SL) rather than advancing the fact itself — exactly the forward-reference accretion pattern. The J1★ and P4★ arguments can cite (SL) at their own point of use; pre-announcing who will consume it is meta-prose the reader must skip past.
**Required**: Delete the closing sentence. Let the consuming arguments reference (SL) where they need it.

### Issue 2: doubled, defensive justification of the B-vs-Σ split
**ASN-0102, X14 (J1'★ discharge)**: "We split A at the opening boundary B — where P4★ legitimately holds — rather than at the mid-composite state Σ, whose Σ-local Old/New split would be unsound here: an address may be in range at Σ via a prior K.μ⁺ yet absent from Σ.R, since P4★ can fail mid-composite." … later: "with no appeal to any inclusion at the mid-composite state Σ."
**Problem**: The same soundness point — split at B, not at Σ — is stated twice, and the first instance is defensive prose justifying the proof structure against a path not taken. This is the "defensive justification / proof-structure rationale" pattern: the argument only needs to *use* P4★ at B, not to argue why the Σ-local split would fail.
**Required**: State the soundness condition once and concisely (split is taken at B because P4★ holds there); drop the second restatement and the hypothetical-unsoundness commentary.

### Issue 3: (SL) mis-cites X3 for an X7 fact
**ASN-0102, X14 (step-local recording fact)**: "the displaced and unmoved classes retain their pre-state images (X3 restricted to s_C)".
**Problem**: "Retain their pre-state images" — i.e., each displaced/unmoved position's image equals its pre-state image — is X7 (NonDestructivePlacement). X3 (SharedReference) states `ran(Σ'.M(d)) ∖ ran(Σ.M(d)) ⊆ dom(Σ.C)`, a different claim about new range additions. The argument here needs image-invariance to conclude these classes add nothing to `ran_{s_C}`, which is X7's content.
**Required**: Cite X7 (restricted to `s_C`), not X3.

## OUT_OF_SCOPE

### Topic 1: time-varying views, re-displacement discoverability, and identity under unreachable allocator
**Why out of scope**: These are correctly deferred to the Open Questions and belong to later ASNs (link projection over time, garbage/unreachability semantics), not to COPY's contract.

VERDICT: REVISE
