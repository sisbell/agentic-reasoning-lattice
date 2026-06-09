# Review of ASN-0116

## REVISE

### Issue 1: IP4's "incomparable" claim is false

**ASN-0116, IP4 (LinkSurvival)**: "When at least one suffix witness is present the two sets are **incomparable**: a shifted witness `v ≥ p` is relabelled to the new V-position `shift(v, n)`, vacating `v` (so `project(e, d, Σ) ⊄ project(e, d, Σ')`), while the largest shifted witness lands at a slot that carried no coverage witness before (so `project(e, d, Σ') ⊄ project(e, d, Σ)`)."

**Problem**: The "vacating `v`" step is unsound. A suffix-witness position `v ≥ p` is vacated of its *old* content, but `M'(d)` re-populates `v` — with block content `shift(a, k)` if `v` is a block slot, or a shifted-suffix address otherwise. If that *new* content also lies in `coverage(e)`, then `v` stays a witness and is *not* dropped from `project(e, d, Σ')`. L4/L9 permit exactly this: a pre-existing endset may reference both `A_new` (as ghosts) and the shifted-suffix addresses.

Counterexample: `n = 1`, `J = N` (insert one unit immediately before the last text position), `coverage(e) = {shift(a, 0), M(d)(q_N)}` — a ghost reference to the to-be-allocated address plus the address at `q_N`. Pre-insert `project(e, d, Σ) = {q_N}`, and `q_N` is a suffix witness (`q_N ≥ p = q_N`). Post-insert the block fills `q_N` with `shift(a, 0) ∈ coverage(e)` (so `q_N` is *still* a witness) and the shift carries `M(d)(q_N)` to `q_{N+1} ∈ coverage(e)`. Hence `project(e, d, Σ') = {q_N, q_{N+1}} ⊋ {q_N} = project(e, d, Σ)` — a **proper containment**, with a suffix witness present. The universal "incomparable" claim is contradicted.

(The other direction, `project(e, d, Σ') ⊄ project(e, d, Σ)`, *does* hold whenever a suffix witness is present — the largest shifted witness lands on a previously-non-witness slot, as argued. The error is one-directional.)

**Required**: Drop the universal "incomparable" assertion and its "vacating `v`" proof. Keep what is actually true and already correctly proved in IP4: the bijection onto (left ∪ shifted-suffix ∪ cross-subspace), the non-decreasing witness **count**, and the monotone resolved **content** — none of which depends on the flawed step. State the residual set relationship correctly: when a suffix witness is present, `project(e, d, Σ') ⊄ project(e, d, Σ)` always holds, while `project(e, d, Σ) ⊆ project(e, d, Σ')` is possible, so the V-position sets are not comparable in a fixed direction (incomparable in some configurations, `project ⊊ project'` in others). The worked example's "confirming IP4's incomparable case" is a true *instance* of incomparability but does not establish the universal; reword it as "an instance where the sets are incomparable."

### Issue 2: PROV mischaracterizes provenance timing as "atomic with allocation"

**ASN-0116, PROV (InsertionProvenance)** (and the Claims-Introduced table): "provenance is established atomically-with-allocation as part of the operation, not deferred — every freshly minted content address `shift(a, k)` enters `R` coupled to its inserting document `d` in the same composite that allocates and places it."

**Problem**: The claim is internally inconsistent. The valid-composite section sequences `K.α₁…K.αₙ → K.μ⁻ → K.μ⁺ → K.ρ₁…K.ρₙ`: every provenance step (`K.ρ`) is sequenced *after* every allocation step (`K.α`) and after both arrangement steps. So provenance is recorded in the *same composite* as allocation (the sentence's second half, correct) but **not** in the same atomic step ("atomically-with-allocation", first half, false). PROV's stated novel content is "the timing observation," so the imprecision sits in the claim's substance, not merely its prose.

**Required**: Replace "atomically-with-allocation" with "within the same composite as allocation" (or "as a non-deferred part of the same composite operation") in both PROV's prose and the table entry. The "not deferred" intent is correct and should be kept; only the false "atomic with allocation" goes.

### Issue 3: Methodology meta-prose around the citation style

**ASN-0116, Effect section** ("We name them but derive them by citation, not from scratch:") and **valid-composite section** ("in the precise sense of ASN-0047's ValidComposite★ (which we cite rather than restate)").

**Problem**: These are defensive justifications of citation methodology — they tell the reader *how* the clauses are obtained (cited, not reproved) rather than advancing any claim. Under the note's anti-bloat discipline this is exactly the meta-prose that accretes around forward references; it duplicates information the per-clause status tags already carry.

**Required**: Delete the methodology asides; the clause-level "cited (K.α, ASN-0093)" / "introduced" status annotations already record derivation provenance.

## OUT_OF_SCOPE

(none — the Scope section and Open Questions correctly defer transclusion-at-insertion, concurrent-insertion freshness, transclusion provenance, and post-edit fragmentation; none is wrongly pulled into this ASN.)

VERDICT: REVISE
