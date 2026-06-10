# Review of ASN-0127

I checked every numbered claim against its derivation, re-ran the worked illustration's arithmetic, and verified the K.μ~ swing witnesses are admissible transitions (domain-fixed by K.μ~-FIX, length/subspace-preserving, with non-injective witnesses justified by M13/M14 and S8★ length-1 runs). The Phase-1/Phase-2 factoring, the two-keystone separation (F-CIL store-fixed lane vs LP13 existence lane), F-LAMBDA's disjoint-union characterization, and E-CONS's exclusion direction all hold. One claim under-delivers on what it explicitly promises.

## REVISE

### Issue 1: D-CWP's "weakest precondition" is written over post-state quantities and omits the R = ∅ boundary — both present in the LP12a it claims to mirror

**ASN-0127, D-CWP**: the stability condition is stated as
> "`findlinks_disc(W, d_q, Σ') = findlinks_disc(W, d_q, Σ)` *iff* `findlinks(Δ, Σ) ⊆ findlinks(image(W, d_q, Σ'), Σ)`"

with `Δ ≡ image(W, d_q, Σ) ∖ image(W, d_q, Σ')`, and the claim
> "This is the weakest precondition for discovery-anchored stability under this single K.μ⁻ step — the discovery analog, on the contraction side, of ASN-0098's LP12a (ContractionDiscoverabilityWP)."

**Problem**: A weakest precondition is a predicate on the *pre-state*. Both `Δ` and `image(W, d_q, Σ')` reference `Σ'`. The cited analog, LP12a, deliberately does *not* do this — it expresses its wp purely over `Σ` and the retention set `R` (`project(a, i, d, Σ) ∩ R ≠ ∅`) and separately records the post/pre bridge `project(a, i, d, Σ') = project(a, i, d, Σ) ∩ R`. D-CWP leaves the corresponding bridge — `image(W, d_q, Σ') = {Σ.M(d_q)(v) : v ∈ W ∩ R}` (since `Σ'.M(d_q) = Σ.M(d_q) ↾ R`) — unstated, so as written the condition cannot be evaluated before the operation without the reader supplying that reduction. Calling a post-state-referencing biconditional "the weakest precondition" while pointing at a pre-state-form foundation lemma is the gap.

Second, the note never walks D-CWP's `R = ∅` boundary, though LP12a explicitly specialises its own (`≡ false`) and the standards make boundary cases mandatory. `R = ∅` is a valid K.μ⁻ (full clearance of a non-empty document, strict contraction satisfied), and D-CWP degenerates non-trivially there: `image(W, d_q, Σ') = ∅`, so `Δ = image(W, d_q, Σ)`, and the condition becomes `findlinks(image(W, d_q, Σ), Σ) ⊆ findlinks(∅, Σ) = ∅`, i.e. stability ⟺ `findlinks_disc(W, d_q, Σ) = ∅` — full clearance preserves the discovery set exactly when it was already empty. This differs interestingly from LP12a's `false` (single-link vs whole-set question) and is exactly the scenario the worked illustration's "Existence vs discovery zero" bullet exercises (removing all of `v_1, v_2, v_3`) without ever connecting it back to D-CWP.

(The enabledness conjunct LP12a carries, `enabled(K.μ⁻[d, R])`, is also absent — D-CWP presupposes the contraction rather than predicating on applicability. This is the lesser point; "Fix a contraction" is a defensible framing, but it makes D-CWP a stability-given-application characterization rather than the standalone wp LP12a is.)

**Required**: Reduce the condition to pre-state form — substitute `image(W, d_q, Σ') = {Σ.M(d_q)(v) : v ∈ W ∩ R}` and `Δ = image(W, d_q, Σ) ∖ {Σ.M(d_q)(v) : v ∈ W ∩ R}`, stating the bridge as LP12a does — so the predicate is evaluable on `(Σ, R)`; and add the `R = ∅` specialisation (stability ⟺ `findlinks_disc(W, d_q, Σ) = ∅`). Optionally conjoin `enabled(K.μ⁻[d_q, R])` to complete the LP12a parallel.

## OUT_OF_SCOPE

### Topic 1: the uniform weakest precondition across the whole K-vocabulary (the note's own Q3)
**Why out of scope**: Q3 correctly defers the *uniform* wp — a single characterization of `findlinks_V(W, d, Σ) = findlinks_V(W, d, Σ')` over extension, reorder, and off-document transitions, of which D-CWP is the contraction instance. Issue 1 is *not* this generalization; it concerns the form and completeness of the contraction case D-CWP already states in-scope. The reviser should not collapse Issue 1 into Q3: fixing D-CWP's pre-state form and `R = ∅` boundary is local to the lemma as written and does not require touching the deferred uniform result.

VERDICT: REVISE
