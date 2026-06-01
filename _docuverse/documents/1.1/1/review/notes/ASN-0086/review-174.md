# Review of ASN-0086

The mathematical content is strong: R0–R7a are layered without circularity (the previously-flagged Σ_D circularity is gone), the boundary cases a precise reader worries about — first vs. subsequent emission, empty homed-set, self-nullification, retraction-of-retractor, nullify-of-nonexistent-address — are all exercised in the worked sketch, and the wp Case 2 two-failure-mode analysis (each domain restriction independently load-bearing) is exactly the depth the standards ask for. The findings below are anti-bloat (the note carries `review-mode.anti-bloat`), not correctness.

## REVISE

### Issue 1: "Load-bearing thesis" duplicates the relational-layer corollary
**ASN-0086, R7a "Load-bearing thesis" and "Definition — relational layer" Corollary proof**: The thesis paragraph closes with "the relational layer is only the degenerate `m = 1` instance," and the Corollary proof independently closes with "The relational layer is thus the `m = 1` instance of a guarantee R7a establishes for arbitrary `m`."

**Problem**: The same point — R7a's value is its generality to arbitrary future substrate-conforming layers, with the relational layer as the trivial `m = 1` case — is made twice, in two sections, in near-identical prose. The "Load-bearing thesis" paragraph as a whole is essay content about *why* R7a matters; it restates R7a's quantifier scope rather than advancing the lemma. This is the "essay content in structural slots" / "two paragraphs say the same thing in different words" pattern.

**Required**: Keep the generality observation in exactly one place. The Corollary proof is the natural home (it already needs to explain why R7a is invoked for a trivial reduction); delete or fold the standalone "Load-bearing thesis" paragraph into it.

### Issue 2: Forward-reference accretion in "The Two Foundational Sets"
**ASN-0086, "The Two Foundational Sets" / "State transition relation"**: e.g. "the disjointness is `dom(Σ.C) ∩ dom(Σ.L) = ∅`, i.e. SD ... **recorded as R4 below**"; "The closure of substrate-conformance ... **is recorded in Lemma — K-Step Conformance Preservation below**"; "**formalized as the Nullify operation below**"; "that ... never a sub-tree of `A_rel`, **is the lemma R-Scope**."

**Problem**: A cluster of forward pointers whose only function is to announce that a later section will restate the current claim. Per the anti-bloat guidance these are "multiple paragraphs deferring to the same downstream location" and prose that points at document order rather than advancing reasoning. The substantive content (the disjointness fact, the closure fact) is already stated where it appears; the "recorded as X below" tail adds nothing the reader needs at that point.

**Required**: Drop the bare "recorded as / formalized as X below" tails. State the fact; let the downstream lemma cite back if a forward link is genuinely needed.

## OUT_OF_SCOPE

### Topic 1: Higher-arity typed relations and elevating the unit-depth discipline to the substrate
**Why out of scope**: The note explicitly restricts to standard-triple (`|Σ.L(a)| = 3`) links and confines the unit-depth retraction discipline to a *layer* convention (with the design tradeoff flagged in Open Questions). Generalizing `L_K` to `L_K^{(n)} ⊆ A_rel × ℘(A)^n`, and deciding whether a designated retraction K-operation should carry a substrate-level unit-depth shape constraint, are genuinely new territory — correctly deferred, not defects here.

VERDICT: REVISE
