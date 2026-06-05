# Review of ASN-0100

The mathematical core is sound. I checked the three-region partition, the K.α/K.μ⁻/K.μ⁺/K.ρ decomposition, functionality (S2), the D-CTG★/D-MIN★/D-SEQ★ closed-interval reduction (including the off-prefix `m ≥ 3` case, which is correctly handled rather than hand-waved), the projection-shift derivation through each intermediate, and the empty/append/interior boundary cases. The worked-example arithmetic checks out (`a_5 = shift(a_2,3)`, projection `{[1,2],[1,5],[1,6]}`, tight vs. non-tight `N_I`). INS.chain-shift's inc/shift equivalence is correctly grounded in T4-validity rather than asserted definitionally.

The findings below are the meta-prose/deferral patterns the `review-mode.anti-bloat` classifier asks for.

## REVISE

### Issue 1: Duplicated prose stating the same fact in two sections
**ASN-0100, §A Worked Example (Non-tight alternative)**: "Non-tight endsets are designed to capture later-allocated content within their declared range, and INSERT's freshly placed I-addresses are exactly such content."
**ASN-0100, §Coverage and link discoverability (Consequence — fresh-address discoverability)**: "For non-tight endsets, a fresh `a_k` may indeed land in coverage, and this is by intent: non-tight endsets are designed to capture later-allocated content within their declared range."
**Problem**: The same claim about non-tight endset intent appears near-verbatim in two sections — the "two paragraphs say the same thing in different words" pattern. A precise reader hits it twice and must confirm they are not different claims.
**Required**: State it once (it belongs with the INS.proj derivation in §Coverage); the worked example can simply exhibit `N_I = {[1,3],[1,4]}` without re-asserting the design rationale.

### Issue 2: Subsection that exists mainly to defer its own derivation
**ASN-0100, §Verifying the Invariants → Cross-document independence (Q3)**: "Cross-document independence extends to link projection... The stepwise derivation — chaining LP4 ... across each elementary step's cross-document frame — is given once, in the `d' ≠ d` case of INS.proj (§Coverage and link discoverability)."
**Problem**: This adds a sentence whose only content is "the derivation is elsewhere." The frame `M'(d') = M(d')` is already stated; the deferral narration ("is given once") is meta-prose around a forward reference.
**Required**: Drop the "is given once, in..." sentence and let the INS.proj statement carry the projection consequence, or fold the one-line projection consequence here without the navigational prose.

### Issue 3: Forward-reference deferral in the Substrate Decomposition
**ASN-0100, §The Operation's Inputs / Substrate Decomposition**: "Which invariants hold at each intermediate versus only at the boundary — the Class (a) per-state / Class (b) composite-boundary split — is stated and proved in §Atomicity and Canonical Order."
**Problem**: Pointer-prose announcing where a split is proved, not advancing the decomposition. Combined with Issue 2, two structural slots defer downstream rather than carrying their own weight.
**Required**: Remove the forward pointer; the §Atomicity section already labels the split where it is proved, so the announcement is redundant.

## OUT_OF_SCOPE

### Topic 1: Partial-failure recovery to canonical order
**Why out of scope**: Already correctly listed under Open Questions — recovery semantics after a partial composite failure is implementation-realization territory, not a state/operation/invariant of this ASN.

VERDICT: REVISE
