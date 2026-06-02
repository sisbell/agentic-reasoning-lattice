# Review of ASN-0098

I checked the projection definition, the immutability/frame lemmas (LP2–LP8, LP14), the operation-effect lemmas (LP9–LP11), the discoverability machinery (LP12–LP18), and the finitude/tightness apparatus (LP-Sub, LP-Fin, LP19–LP21), plus the worked trace. The core mathematics is sound — the inclusion arguments in LP9/LP10, the bijection argument in LP11, the wp derivation in LP12a, and the case decomposition in LP-Fin all hold up. My findings are concentrated in (a) one rigor gap in LP-Fin and (b) the meta-prose / forward-reference accretion the `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: LP-Fin discharges a case by "applied symmetrically" across a differing index bound
**ASN-0098, LP-Fin (Finiteness from the bound)**: "The sub-case (ii) argument, applied symmetrically to `#d ≤ #d_0`, shows that `d` must agree with `d_0` on positions `1..#d`."
**Problem**: Sub-case (ii) was proved for `#d > #d_0` with the divergence index ranging over `j ≤ #d_0`. The symmetric application ranges `j` over `1..#d` (a different, strictly smaller bound), and the candidate's position-alignment to `s` and `s ⊕ ℓ` must be re-checked at that bound. Standard #1 forbids discharging a case by asserted symmetry when the index structure differs, even when the logic is parallel.
**Required**: State the `#d ≤ #d_0` case explicitly — name the divergence position range (`1 ≤ j ≤ #d`), exhibit prior-position agreement of `a` with `s`/`s ⊕ ℓ` on `1..j-1`, and apply T1 case (i) at `j` to derive `a < s` or `a > s ⊕ ℓ`.

### Issue 2: project-definition prose pre-states LP6, LP7, LP8 as hand-waves
**ASN-0098, "The Projection Operation"**: "Content allocation that does not modify any `Σ.M(d)` cannot affect any projection. Link allocation that does not modify `Σ.M(d)` cannot affect existing projections. Document registration (K.σ) that only updates `dom(Σ.M)` … cannot retroactively affect existing projections through existing documents."
**Problem**: These three sentences are the conclusions of LP6, LP7, and LP8 stated informally before those lemmas appear — a prose preview of downstream consumers. It duplicates content the lemmas establish rigorously and forces the reader past an unproved restatement of results-to-come.
**Required**: Keep the substantive insight ("of the two inputs, only the arrangement varies") and delete the per-operation preview; let LP6/LP7/LP8 carry their own statements.

### Issue 3: "Working reference frame" note is a use-site operation inventory
**ASN-0098, "State Components" (Working reference frame)**: "The layered frame supplies the full operation vocabulary the projection responds to — K.σ (ASN-0093) together with K.α, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.δ, K.ρ (ASN-0047)."
**Problem**: This enumerates the operation set that the LP-lemmas individually handle — a use-site inventory in a setup slot. It advances no reasoning; each operation is named again where it is actually used.
**Required**: Reduce to the frame identification (ASN-0047 over ASN-0093) and drop the operation roll-call.

### Issue 4: LP13 aftermath paragraph restates the storage/navigability split as essay and forward-references LP17
**ASN-0098, after LP13**: "The architectural separation LP13 commits to is that *storage* and *navigability* are independently regulated. LP12 characterises when a link is discoverable … LP13 says the link's stored object persists regardless … an orphaned link (LP17, …) and a discoverable link are stored identically …"
**Problem**: The storage/navigability distinction is already the formal content of LP12 vs LP13; this paragraph re-narrates it and reaches forward to LP17 (introduced two sections later). It is interpretive bloat sitting in a proof-consequence slot, deferring to a not-yet-stated claim.
**Required**: Cut to one sentence stating the consequence ("LP13 is independent of every `Σ.M` term, so persistence does not depend on discoverability"); remove the LP17 forward pointer and the re-narration.

### Issue 5: Boundary section justifies lemma scope rather than advancing it
**ASN-0098, "Boundary and Width Behaviour"**: "`F` is countably infinite. … The universal quantifier … ranges over an infinite domain. LP-Fin establishes that for a canonical span … the set `F ∩ [s, s ⊕ ℓ)` is finite, which renders the quantifier decidable. Tightness admits only canonical spans, so the canonical case is all the lemma must cover."
**Problem**: The closing sentences explain *why* LP-Fin is scoped to canonical spans rather than stating a fact the argument uses — scope-justification prose of the kind the anti-bloat note flags. The vacuity discussion of the "naive formulation" earlier in the same section is similarly a defense of the design choice, not a step in any proof.
**Required**: State the decidability fact LP-Fin needs (finite interval ⇒ decidable tightness predicate) and drop the scope-justification and naive-formulation rationale, or compress the latter to a single clause motivating `F`.

### Issue 6: Trace "branch point" carries bookkeeping prose disproportionate to its content
**ASN-0098, "A Worked Trace" (Branch point)**: "The next step does *not* follow `Σ_2`. We return to `Σ_1` … and explore a separate continuation that isolates K.μ~ behaviour. In this branch, `d₂` is never introduced … We rename the post-K.μ~ state `Σ_3` to flag that it is a sibling of `Σ_2` under `Σ_1`, not a successor of `Σ_2`."
**Problem**: Four sentences of state-naming meta-commentary to say "from `Σ_1`, apply K.μ~ instead of registering `d₂`." The renaming rationale ("to flag that it is a sibling …") is bookkeeping about the exposition, not about the system.
**Required**: Replace with one sentence: "Returning to `Σ_1`, apply K.μ~ to `d₁` (call the result `Σ_3`)."

## OUT_OF_SCOPE

### Topic 1: Reverse discovery, V-order/I-order reflection, cross-document operation comparability
**Why out of scope**: These are correctly placed in Open Questions — they require a reverse-discovery primitive, V-order invariants, and cross-document operation semantics this ASN does not define. Not errors here.

### Topic 2: Link-canonical contraction discoverability (link-subspace dual of LP12b)
**Why out of scope**: The final Open Question correctly identifies that the LP-Fin Corollary disjointness argument does not invert to the link subspace; resolving it is a future increment, not a defect in the present claims.

VERDICT: REVISE
