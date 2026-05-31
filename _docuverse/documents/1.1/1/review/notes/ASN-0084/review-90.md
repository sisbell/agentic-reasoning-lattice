# Review of ASN-0084

The mathematics is sound: the well-definedness lemmas (R-PIV, R-SWP), the bijection proofs (R-PPERM, R-SPERM), R-COMM, and the R-BLK run-transformation all check out, region partitioning is exhaustive and disjoint in both forms, and the six worked examples each exercise a genuinely distinct sub-case (forward/fixed/backward μ, empty exterior, non-S pass-through) — that coverage is warranted, not padding. The findings below are confined to the accreted meta-prose the `review-mode.anti-bloat` classifier flags.

## REVISE

### Issue 1: Citation-hygiene meta-prose in R-BLK Phase 1
**ASN-0084, R-BLK, "Non-S runs are carried verbatim"**: "The later phases cite this carry by name rather than re-derive it."
**Problem**: This sentence advances no reasoning — it narrates the document's own citation practice. It is exactly the kind of prose a reader must skip past to follow the claim.
**Required**: Delete the sentence. The carry result stands on its own; later phases will cite it whether or not the text announces that they will.

### Issue 2: Phase 2 restates Phase 1's empty-right-exterior conclusion
**ASN-0084, R-BLK, Phase 2 (Classify)**: "When c_{n−1} > max(V_S(d)), the exterior-right region is empty and no run is classified there; the non-S region is empty when dom(M(d)) ⊆ V_S(d), and either condition may hold independently."
**Problem**: The empty-right-exterior fact is already established in EXT-VAC (Consequences of R-PRE) and applied in Phase 1's "Outside ⋃_k V(b_k)" sub-case. Phase 2 re-asserts the same conclusion, and the trailing clause "either condition may hold independently" is defensive boundary-bookkeeping that the partition statement already accommodates. The story of c_{n−1} = N+1 is now told in EXT-VAC, Phase 1, Phase 2, and the boundary worked example.
**Required**: Drop the Phase 2 emptiness enumeration; classification of whatever runs exist into their regions is all Phase 2 needs to assert. Let EXT-VAC and Phase 1 own the empty-exterior argument.

### Issue 3: Anticipatory / "we record … here" framing
**ASN-0084, R-NS section opening**: "We record the pointwise consequence of this structural fact here." And **Correspondence-Run preamble**: "Extended Associativity and its underlying TS3 … hold for any tumbler in T irrespective of depth, so below we apply them freely to I-addresses."
**Problem**: Both are stage-direction prose announcing that a result will be stated or applied downstream, rather than stating it. R-NS's content is the one-line lemma; the preamble's content is "shift acts on I-addresses identically." The "we record here" / "apply them freely below" wrappers are noise.
**Required**: State the lemma and the I-address shift fact directly, without the framing clauses.

### Issue 4: Merge's correctness proof is unconsumed in this ASN
**ASN-0084, "Merge"**: full S8-cons derivation for the merged run.
**Problem**: Split is load-bearing (R-BLK Phase 1 invokes it). Merge is not: no lemma here consumes the merged-run S8-cons result. Merge appears only in worked-example "merge checks" and in the canonical-recovery question deferred to Open Questions. The *definition* of Merge is needed to state CanonicalRunDecomposition; the *proof* is machinery for work this ASN explicitly does not do.
**Required**: Either consume the Merge correctness result in a lemma (e.g., the recovery of the canonical partition from B′), or reduce Merge to its definition and move the S8-cons proof to the ASN that resolves canonical recovery.

## OUT_OF_SCOPE

### Topic 1: Weakest precondition and R-PRE(iv) redundancy
The Open Questions already ask "what does R-PRE(iv) guarantee beyond what D-SEQ already supplies." Since D-SEQ fixes V₁(d) = {[1,k] : 1≤k≤N} contiguously, R-PRE(iv)'s residual content is effectively the bound on the cuts (c_{n−1} ≤ N+1, derived in EXT-VAC). Resolving whether R-PRE(iv) is necessary or derivable is genuine future analysis, not an error here.
**Why out of scope**: A precondition-minimality result is its own investigation; the ASN correctly flags it rather than half-answering it.

### Topic 2: k-cut generalization (k > 4)
**Why out of scope**: The class of cut-point permutations for k > 4 is new territory; CS1's restriction to n ∈ {3,4} is a deliberate scope boundary, not a gap.

VERDICT: REVISE
