# Review of ASN-0043

I checked the invariant chain (L0–L14, L-fin), the four local lemmas (CPP, FSP, FSE, PrefixSpanCoverage), the L9/L11b extension theorems, and the six-step worked example. The mathematics is sound — the coverage arithmetic in Steps 4/6, the freshness/producibility discharge through FSP+FSE, and the GlobalUniqueness single-tree argument in L11a all hold. The findings below are presentation/rigor issues, consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: CPP conflates its hypothesis with a conditional justification, hiding a caller obligation

**ASN-0043, CPP — ChainPrefixPreservation (local lemma)**: "Suppose every step modifies only positions strictly beyond `p`: each child-spawn `inc(·, k')` agrees with its input on positions `1..#tᵢ₋₁` (TA5(b)), and each sibling advance `inc(·, 0)` modifies only the `sig` position ... — so whenever `#tᵢ₋₁ > p` the advance leaves positions `1..p` fixed."

**Problem**: The "Suppose H" frame says the hypothesis is assumed, but the colon-clause reads as *establishing* H — and it only establishes it for sibling advances *conditionally* ("whenever `#tᵢ₋₁ > p`"). A sibling advance at `#tᵢ₋₁ = p` modifies the `sig` = terminal = position `p`, which is **not** strictly beyond `p`, so H fails there. The lemma is sound only because every call site (L1c with first step `k₁=2` lifting length to `#s+2` before any sibling; FSE with `p = #home(a) < #a`) happens to keep all sibling-advance inputs at length `> p`. As written, that requirement is buried inside "whenever" rather than stated as a precondition, so the reader cannot tell whether CPP proves the length condition or demands it.

**Required**: State the sibling-advance length condition as an explicit precondition (e.g., "for every sibling-advance step, `#tᵢ₋₁ > p`"), or derive it cleanly from `p ≤ #t₀` plus the fact that the first length-increasing step precedes any sibling advance. Don't smuggle it into the hypothesis-justification.

### Issue 2: L9 carries a navigational deferral sentence that advances no reasoning

**ASN-0043, L9 — TypeGhostPermission**, in the Case B construction: "The soundness of this padded construction is exactly FSP's payload hypothesis, discharged once in the application below rather than re-argued here."

**Problem**: This sentence states only *where* the work happens ("in the application below rather than re-argued here"), not any step of the argument. The subsequent "*Application to L9.*" paragraph discharges FSP's payload hypothesis on its own and stands without this pointer. Deleting the sentence loses nothing — the test for meta-prose. A precise reader must skip past it to reach the actual discharge.

**Required**: Delete the sentence; the "*Application to L9.*" paragraph already carries the discharge.

## OUT_OF_SCOPE

None to add — the Open Questions section already routes the unscoped topics (global content-subspace constant, transclusion/link-store interaction, compound-link well-formedness, decomposition-vs-coverage query equivalence) to future ASNs rather than asserting them here.

VERDICT: REVISE
