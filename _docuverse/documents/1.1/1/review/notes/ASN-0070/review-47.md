# Review of ASN-0070

I read the full note. The core mathematics — the inverse-image definition (F0), the subspace correspondence (F-subspace), and especially the F-canonical uniqueness proof (case analysis on action point, the consecutive-tumbler characterisation, maximal-run partition, and the left/right-closure arguments) — is rigorous and complete. Both inclusions are shown where set equalities are claimed; the discreteness/well-ordering appeals to T0 are discharged explicitly; the M-int application is now correctly gated through B3. The anti-bloat audit surfaced no forward-reference accretion worth a finding: the System-reading footnotes are one-sentence ties to design intent (legitimate per the "statements of what an operation does" carve-out), and the deps are load-bearing (consistent with the prior declined dep-audit).

One genuine gap remains.

## REVISE

### Issue 1: No worked example exercises partial-block intersection (offset j > 0)

**ASN-0070, "Computation via Decomposition" / F-contig**: "If `I(β) ∩ ⟦σ⟧` is non-empty, it is a contiguous sub-progression `{a + j + k : 0 ≤ k < c}` for some offset `j` and width `c`. The corresponding V-positions are `v + j, ..., v + j + c − 1`."

**Problem**: The offset `j` is a non-trivial mechanic the note itself foregrounds (and F-contig is a catalogued LEMMA), but every one of the five worked configurations intersects a block at offset `j = 0`:
- Config 1: `β₁` fully covered, `j = 0, c = n = 2`.
- Config 2: `a₀` is index 0 of both `β₂` and `β₃`, `j = 0, c = 1`.
- Config 5: `a₀`/`ℓ₀` at index 0 of their blocks, `j = 0, c = 1`.

The case where coverage clips the *middle or tail* of a block — e.g. a block `([1,4], a₁, 3)` mapping to `{a₁, a₁+1, a₁+2}` against coverage starting at `a₁+1`, yielding `j = 1`, `c < n` — is realisable and is precisely what makes the `(j, c)` machinery and the V-run `(v + j, δ(c, m_S))` recording non-trivial. It is never concretely verified. Per the "concrete example" / "missing depth" standard, a key claim's non-trivial case should be checked against a specific scenario.

**Required**: Add (or modify) one configuration in which an endset span clips a multi-position block at an interior offset, so the result records a V-span with start `v + j` for `j > 0` and width `c < n`. Verify F-sound, F-complete, and F-contig against it.

## OUT_OF_SCOPE

### Topic 1: Concurrency semantics, cross-home transclusion resolution, transclusion-lineage relationships
**Why out of scope**: The note's own Open Questions raise these and correctly defer them; they are future-ASN territory (multi-document resolution coherence, concurrent modification) rather than defects in this query-operation spec.

VERDICT: REVISE
