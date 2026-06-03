# Review of ASN-0069

## REVISE

### Issue 1: V9a lists "direct allocation" as an indistinguishable acquisition path, contradicting V9b
**ASN-0069, §"Provenance Recording", V9a and V9b**: V9a — "For every `(a, d_new) ∈ R'` recorded by a fork, the relation does not distinguish whether `d_new` acquired `a` via fork from `d_src`, via transclusion from a third document also containing `a`, or **via direct allocation**." V9b — "For every `(a, d_new) ∈ R'` recorded by a fork, `origin(a) ≠ d_new`."

**Problem**: Both properties scope to the *same* subject — pairs `(a, d_new) ∈ R'` recorded by a fork. V9b proves every such `a` has `origin(a) ≠ d_new`, i.e., `d_new` did **not** directly allocate `a`. Yet V9a enumerates "via direct allocation" (which would force `origin(a) = d_new`) as one of the acquisition paths R supposedly cannot distinguish. For a fork-recorded pair, direct allocation is not an indistinguishable alternative — it is a *proven-impossible* one. The two adjacent properties make incompatible claims about the same set.

**Required**: Reconcile V9a with V9b. Either drop "via direct allocation" from V9a's enumeration (since V9b excludes it for fork-recorded pairs), or re-scope V9a away from "recorded by a fork" to all of R if the intent is that R-as-a-relation encodes no mechanism in general — and state the relationship to V9b's stronger fork-specific result.

### Issue 2: T4-validity of `d_new` is established twice by independent routes
**ASN-0069, §"Identity by Sub-Allocation" and §"The Fork Composite"**: Identity section — "every emission `cₙ ∈ S(d_src, 1)` satisfies T4 by B6(a)'s sufficiency clause." Composite verification — "Outer-precondition `T4-valid(d_new)` is discharged by T10a.4 (T4PreservationUnderDiscipline) applied to `A_v(d_src)`."

**Problem**: `d_new` satisfying T4 is the same fact, derived first via B6(a) (ASN-0040) in the Identity section and again, independently, via T10a.4 (ASN-0034) in the composite verification. The composite verification already cites V1 for `Document(d_new)` and `parent(d_new)` rather than re-deriving them; the T4-validity discharge is the one identity fact it re-establishes from scratch instead of citing the prior result. Under the anti-bloat mandate this is a redundant second derivation of an already-established fact.

**Required**: In the composite verification, cite the T4-validity of `d_new` already established in §"Identity by Sub-Allocation" (via B6(a)) rather than re-deriving it through T10a.4.

## OUT_OF_SCOPE

### Topic 1: V6a(ii)/(iii) link-discoverability machinery
**ASN-0069, §"Subspace Selectivity", V6a and the worked-example "Link discoverability" paragraph**: introduces `coverage(e)`, `project(a, i, d, Σ)`, and `discoverable_from(a, d, Σ)`, then proves projection-preservation (ii) and projection-inheritance (iii) with full set-inclusion arguments.

**Why out of scope**: "link semantics" is named out of scope for this ASN. The fork-relevant claim is V6 (the fork's link subspace is empty) and V6a(i) (`L' = L`, a frame fact). Parts (ii)/(iii) formalize *how links project onto V-positions via endset coverage and resolve to discoverability* — that is link-resolution semantics, which belongs in a links-focused ASN. The fork operation only needs the bare observation that inherited I-addresses are shared, which V4 already supplies. The discoverability apparatus (and its worked-example walkthrough with a hypothetical `a₁ ∈ coverage(...)`) should be relocated to the link-semantics ASN.

VERDICT: REVISE
