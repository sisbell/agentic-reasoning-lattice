# Review of ASN-0119

This is a careful, deep note. The central thesis — that every obligation follows from REARRANGE rewriting only the arrangement and never an I-address — is correct, and the author largely earns it: the S3★ inheritance argument (via π mapping each subspace onto itself), the contiguity-by-unchanged-keys observation, the P7c footprint analysis with three correctly-computed fragmentation counterexamples, and both worked transpositions all check out arithmetically. I verified the pivot (`A B C D E ↦ A C D E B`), the swap (`A B C D E F ↦ A E F C D B`), the middle displacement `w_β − w_α`, and the two-move atomicity decomposition; they are all sound. The issues below are one real gap in a cited dependency, plus accreted forward-reference prose.

## REVISE

### Issue 1: LP11 is invoked by mischaracterizing its hypothesis; REARRANGE is never established as a K.μ~ transition

**ASN-0119, "Links" (P7a derivation)**: "LP11's only hypotheses — a domain-preserving reordering whose bijection satisfies `M'(d)(π(v)) = M(d)(v)` — are exactly what P2 (R-PPERM/R-SPERM) supplies, so it applies directly."

**Problem**: ASN-0098's LP11 is stated "For every **K.μ~ transition** `Σ → Σ'` operating on `d` via the witnessing bijection π." Its hypothesis is that the transition *is a K.μ~ transition* (ASN-0047), which carries the full admissibility package (i)–(v): shape-invariant preservation, non-triviality, length-preservation, subspace-preservation, and link-subspace fixing. The note paraphrases this hypothesis as merely "a domain-preserving reordering whose bijection satisfies `M'(d)(π(v)) = M(d)(v)`" — that is the content of LP11's *proof* (which leans only on K.μ~-FIX + the bijection equation), not its *stated* precondition. REARRANGE_K (ASN-0084) is specified directly by PivotPostcondition/SwapPostcondition, not as a K.μ~ composite, and the note nowhere establishes that REARRANGE_K's `Σ → Σ'` is a K.μ~ transition. So P7a — and through it P7b, P7c, and the link-survival guarantees that are the whole point of the note — rests on a foundation lemma whose gating precondition is asserted-as-weaker rather than discharged. This is exactly the "X follows from Y" move the standards forbid: the lemma is cited, but its hypothesis is not shown to hold.

**Required**: Either
- (a) establish that REARRANGE_K's transition is a K.μ~ transition by discharging K.μ~'s admissibility (i)–(v), then cite LP11 as stated. The note already holds (i),(iii),(iv),(v) — they fall out of the same "`V_{s_C}(d)` unchanged as a set" observation and the "π maps each subspace onto itself" fact used in the S3★ proof. Condition (ii) (non-triviality, `M'(d) ≠ M(d)`) must be addressed separately, since a REARRANGE on symmetric content yields `M'(d) = M(d)` and is *not* a K.μ~ transition; or
- (b) drop the LP11 citation and derive the transport inline from P2 (the bijection equation) plus LP2/LP3 (slot/coverage invariance) — this is the same three lines as LP11's proof and sidesteps the non-triviality wrinkle entirely.

### Issue 2: Forward-reference accretion and essay content in structural slots

The `review-mode.anti-bloat` patterns are present at several sites:

- **Forward-reference deferrals.** "The two streams": *"The grounds for confining the operation to the text subspace are stated where we fix the scope."* And "Cuts and regions": *"We return to its consequences in the section on atomicity."* Both are bare pointers announcing that an argument lives downstream; neither advances the local reasoning. The scope can be confined and justified where it is fixed without the pre-announcement, and the atomicity consequence can simply be stated in the atomicity section.
- **Meta-prose justifying inclusion of imported material.** "The transposition as a permutation": *"For the reader's convenience we recall the destination equations — they are ASN-0084's, cited, not introduced here."* Recalling the equations is fine; the sentence explaining *why* they are being recalled and re-asserting their provenance is noise around the citation.
- **Claims-table entries that duplicate the body's analysis.** The P7a and P7c rows of the Claims Introduced table carry paragraph-length statements ("...so fragmentation of a contiguous run occurs only when it straddles a cut — straddling alone does not force it, and conversely a straddle that mixes the fixed exterior with a relocated region can fragment even when every block it covers is complete"). This is the body's nuanced P7c discussion transcribed into a structural slot meant for a concise claim statement. The table should name the claim; the geometry already lives — correctly and at length — in the body.

**Required**: Remove the two deferral pointers and the provenance meta-line; compress the P7a/P7c table cells to one-line statements, leaving the analysis in the body where it belongs.

### Issue 3 (minor): the "first position" boundary is handled only implicitly

**ASN-0119, "A worked transposition"**: The pivot example exercises a region touching the document's *right* end (β = {C,D,E} with `c₂ = ord 6` past the last active position, so the right exterior is empty), but no worked example places `c₀` at the document minimum `[s_C, 1]`, leaving the left exterior (the R-EXT `v < c₀` branch) empty.

**Problem**: "First/last" are mandatory boundaries. The right-end case is shown; the symmetric left-end case (no exterior before the affected interval, and the case where the affected interval covers the entire active run) is only handled implicitly by the equations.

**Required**: This is genuinely minor — R-EXT degenerates to the empty quantifier and π remains a bijection — so the equations *do* cover it. Either add one line confirming the `c₀ = min(V_{s_C}(d))` case (empty left exterior) against P2/P3, or fold it into the well-definedness discussion alongside the degenerate-document cases.

## OUT_OF_SCOPE

The note's Open Questions correctly defer the genuinely future territory — transclusion-shared cuts as boundaries, serializer-free concurrent rearrangement, content-index invariants under footprint fragmentation, recoverability of a prior arrangement from the Istream, and the displacement-vs-subspace-boundary relationship. None of these are errors in this ASN, and the note does not smuggle claims about them into the body. Nothing to add.

VERDICT: REVISE
