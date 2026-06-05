# Review of ASN-0100

This ASN is mathematically thorough — every conjunct of ExtendedReachableStateInvariants is addressed, the three-region partition is correctly proven disjoint and exhaustive, INS.chain-shift is rigorously derived, and the projection-shift derivation tracks `project` through each intermediate state correctly. I found no correctness defect in the proofs. The findings below are all instances of the accumulated meta-prose and forward-reference redundancy that the `review-mode.anti-bloat` classifier flags. Because each is a "skip past prose to follow the claim" finding, the verdict is REVISE.

## REVISE

### Issue 1: The tight-endset `N_I = ∅` distinction is re-explained in four separate locations

**ASN-0100, multiple sections**: the same content (fresh `a_k` cannot land in a tight endset's coverage, can land in a non-tight one, by LP19a) appears as:
- Worked example: "*Why `N_I = ∅` here, and when it is not.*" (a full paragraph plus the `e_1'` counterexample construction)
- §Coverage and link discoverability: "*Consequence — fresh-address discoverability (the `N_{ℓ,i}` term)*"
- §INSERT vs. COPY: "*Corollary (link survivability through value coincidence).*"
- §Weakest-Precondition Analysis: "The second disjunct — fresh-address capture — collapses to `false` for any *tight* endset"

**Problem**: Four paragraphs in four sections state the same fact in different words. Three of them add no object-level content beyond the LP19a consequence already stated in §Coverage.

**Required**: State the tight/non-tight `N_I` consequence once (the §Coverage paragraph is the natural home), and have the worked example, the COPY corollary, and the wp analysis reference it rather than re-derive it. Keep the `e_1'` non-tight numeric instance only if it adds a value the canonical statement lacks.

### Issue 2: Discoverability preservation is restated four times

**ASN-0100**: "every link discoverable from any document at Σ remains discoverable at Σ'" appears in:
- §Coverage: "*Consequence — preservation of pre-state discoverability:*"
- Worked example: "*Discoverability (INS.inv.discov).*"
- §wp Analysis: the discoverability `wp` computation
- Table row INS.inv.discov

**Problem**: The general claim, the numeric instance, the backward (`wp`) form, and the table row overlap heavily. The `wp` result for tight endsets (`wp ≡ INS.pre ∧ discoverable_from(ℓ, d, Σ)`) is the same content as the forward "Consequence" paragraph viewed from the other direction.

**Required**: Keep the forward consequence and the `wp` form (they are genuinely different analyses) but cut the prose overlap; the worked-example restatement adds nothing the numeric INS.proj instance hasn't already shown.

### Issue 3: Atomicity section carries justification prose that explains *why* rather than discharging an obligation

**ASN-0100, §Atomicity and Canonical Order**: "Composite-level atomicity is *definitional* — not an extra property the substrate must separately supply." followed by "By ValidComposite★, INSERT's elementary transitions form a *contiguous* finite sequence … transitions are totally ordered (SequentialTransitionAxiom; ASN-0093), so no foreign elementary transition interleaves…"

**Problem**: This re-explains the ValidComposite★ framework and argues the *status* of atomicity rather than verifying anything. The per-state-invariant verification that follows is the real (and required) work; the "definitional" framing is meta-prose the reader must skip to reach it.

**Required**: Delete the framing sentences; open the section with the actual obligation ("each intermediate state satisfies the per-state invariants; the boundary satisfies J0, J1★, J1'★") and proceed to the verification.

### Issue 4: Worked example forward-defers to a claim stated only later

**ASN-0100, §A Worked Example**: "This corroborates INS.proj's `d' = d` text-subspace clause `project(ℓ, 1, d, Σ') = π(project(ℓ, 1, d, Σ)) ∪ N_{ℓ,1}`" and "the new term `N_{ℓ,1} = ∅` (justified below)".

**Problem**: The worked example computes the projection directly, then checks it against INS.proj, whose canonical statement and proof do not appear until the later §Coverage section. The reader meets the verification of a claim before the claim. The "(justified below)" pointer is a second deferral within the same passage.

**Required**: Either move the INS.proj canonical statement ahead of the worked example, or have the worked example present its direct computation as a standalone numeric result without forward-referencing a not-yet-stated claim.

### Issue 5: The "Empty-arrangement vs. fresh-allocator-state sub-case" paragraph re-derives ASN-0093 K.α internals

**ASN-0100, §A Worked Example**: the paragraph beginning "*Empty-arrangement vs. fresh-allocator-state sub-case.*" walks through how `a_{new0}` is selected (first-emission `[d.0.s_C.1]` vs. chain continuation `inc(max{…}, 0)`) when prior content was allocated then removed.

**Problem**: This is legitimate edge-case content (the case is not excluded by any precondition), but it reproduces the K.α emission-selection discipline that ASN-0093 already fixes, descending below the abstraction level at which INSERT is specified. The post-state predicates "hold uniformly in either sub-case" — which is the only fact INSERT needs — could be stated in one sentence.

**Required**: Reduce to the load-bearing observation (the V-position assignments are fixed by the empty-arrangement condition; the address *values* are fixed by the ASN-0093 chain state; all post-state invariants hold uniformly) and drop the re-derivation of how K.α picks `a_{new0}`.

## OUT_OF_SCOPE

(none — the Open Questions correctly defer concurrency, composition closure, derived-property maintenance, link-subspace insertion, and failure recovery to future work rather than asserting claims about them.)

VERDICT: REVISE
