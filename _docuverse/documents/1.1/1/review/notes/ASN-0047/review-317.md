# Review of ASN-0047

I read this as a self-verification of a five-component transition model. The proof machinery is unusually complete — the per-elementary verification matrix, the D-SEQ★ derivation (both `m=2` and `m≥3` cases with a concrete trace), the K.μ⁻ equivalence, and the worked examples all hold up under scrutiny. I could not find a correctness defect: the elementary frames compose, the coupling constraints are correctly scoped to the content subspace, FrontierEquivalence and the SubAllocatorBundle discharge link/content freshness soundly, and the boundary cases (empty subspace, full clearance, fresh-document fork, k=0 vs k=1 version chains) are each accounted for.

The findings below are about textual accretion, which the embedded `review-mode.anti-bloat` classifier explicitly asks me to surface and which the recent commit history (`unify freshness discharge…`, `k∈{1,2} freshness circularity`, `k=0/1/2 freshness discharge`) confirms is an area of repeated reviser churn.

## REVISE

### Issue 1: The k=0-vs-k∈{1,2} freshness distinction is restated in five places
**ASN-0047, K.δ (Entity creation), the k=0 worked example, S7d discharge, FrontierEquivalence**: The same conceptual point — "freshness is a live-state `e ∉ E` read in every case; the disciplines differ only in *which* state fact the guard encodes (current frontier index for k=0 vs single-spawn occurrence for k∈{1,2})" — appears at least five times:
- K.δ case (ii) preamble: *"The freshness conjunct `e ∉ E` is discharged against the present state Σ in every case; the disciplines differ only in *which* state fact the guard reads…"*
- K.δ k=0 bullet: *"No additional freshness conjunct is imposed here — the case-level `e ∉ E` *is* the k = 0 frontier check…"*
- Worked example Step 4(a): *"(both are live-state `e ∉ E` reads against Σ; they differ only in which state fact the guard encodes)"*
- S7d discharge: *"Freshness is the caller-checked guard `inc(t, 0) ∉ E`, characterized by FrontierEquivalence."*
- FrontierEquivalence itself, which formalizes the same biconditional.

**Problem**: FrontierEquivalence is the load-bearing lemma; the surrounding prose re-explains *why* the conjunct is needed and re-draws the k=0/k∈{1,2} contrast rather than advancing any new claim. A reader following the K.δ precondition must skip past the same justification at each recurrence. This is precisely the "multiple paragraphs say the same thing in different words" pattern.

**Required**: State the live-state-`e∉E` discharge and the frontier-vs-at-most-once distinction once (FrontierEquivalence is the natural home), and have the K.δ bullets, S7d, and the worked example cite it by name rather than re-derive the contrast.

### Issue 2: Multiple verification-matrix cells fan into the same downstream prose block
**ASN-0047, Class (a) verification matrix, K.μ~ column**: Four distinct invariant rows — S8a/S8-depth/S8-fin, S8★, D-CTG★/D-MIN★, and D-SEQ★ — all carry the identical cell text *"per *K.μ~ discharge for the arrangement-shape package* below."* The pointed-to block then re-separates them anyway (noting S8-fin is *not* in the package, S8★ is *not* an admissibility-(i) clause, D-SEQ★ is derived).

**Problem**: The cells defer en masse to a block that immediately qualifies that the deferral was imprecise for three of the four rows. This is the "multiple paragraphs in different sections defer to the same downstream location" accretion pattern: the matrix's navigational value is lost when four cells point to one paragraph whose first job is to undo the grouping.

**Required**: Either give each of the four rows the one-line discharge it actually uses (e.g., S8-fin: "K.μ⁻ restricts + K.μ⁺ finite-extends"; D-SEQ★: "derived from D-CTG★+D-MIN★+S8-depth+S8-fin+S8a"), or rename the downstream block to reflect that it covers a heterogeneous set rather than a single "package."

## OUT_OF_SCOPE

### Topic 1: Interior link withdrawal with renumbering
K.μ⁻'s suffix-only contraction cannot model the implementation's interior `DELETEVSPAN` (compact-and-renumber). The ASN already flags this in its open questions; it is future operation-level work, not a defect in the elementary transition.

### Topic 2: Version-derivation DAG shape
J4's operand-tracking rule forces fork content to flow linearly along the version frontier (k=0 → `prev_version`), so a document has at most one direct derivation child. Whether this faithfully captures Nelson's branching version DAG belongs to the version-lineage open question and to CREATENEWVERSION (an out-of-scope named operation).

VERDICT: REVISE
