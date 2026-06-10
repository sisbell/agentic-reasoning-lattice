# Review of ASN-0114

I worked the proofs and the worked instance. F1→F2 (via S0 convexity + the first collapse) is sound; the `|R|=1` contradiction holds because F1 forces `⟦σ⟧ = coverage(eᵢ) ∋ p,r`, and convexity drags `q` in. F5's single-step (L12) → multi-step (LP13) composition is correctly distinguished. F7's `wp(·, R = ⟨⟩)` chains the two collapses correctly. The worked instance checks out: `a₃ ⊕ δ(2,8) = a₅`, `coverage(e₁) = [a₃,a₅) ∪ [a₇,a₉)` is genuinely disconnected over `T` (witness `a₃ < a₅ < a₇`), and LP-Fin Corollary gives `∩F = {a₃,a₄,a₇,a₈}`. Two issues remain.

## REVISE

### Issue 1: F4's frame enumerates a strict subset of the state it ranges over
**ASN-0114, F4 (PureRead)**: "For the state `Σ` against which it is evaluated, the post-state equals `Σ`: the content store `Σ.C`, the link store `Σ.L`, and every arrangement `Σ.M(d)` are identical before and after."

**Problem**: The note never declares its state tuple, and it straddles two substrates with *different* tuples. The substrate section grounds on ASN-0093, whose state is `(C, L, M)` — under that reading F4's enumeration is exhaustive. But F5's derivation invokes LP13, and the worked instance invokes LP-Fin Corollary, both from ASN-0098 — and ASN-0098's `Σ →* Σ'` is the ASN-0047 *extended-state* reachability whose vocabulary includes K.δ (mutates the entity set `E`) and K.ρ (mutates the provenance relation `R`). If F5's `Σ →* Σ'` is that reachability (it must be, to license LP13), then `Σ = (C, L, E, M, R)`, and the colon-enumeration after "the post-state equals `Σ`:" presents three of five components as if they were all of `Σ`. A frame condition must account for every component of the state it ranges over; FOLLOWLINK is a pure read, so `E` and `R` are trivially fixed — but F4 must *say* so, and as written it does not. The prose claim ("post-state equals `Σ`") is correct and complete; the enumeration that purports to unpack it is not.

**Required**: Pin the state model. Either (a) restrict explicitly to the ASN-0093 `(C, L, M)` substrate and note that LP13/LP-Fin specialize to that projection, so the enumeration is exhaustive; or (b) if ranging over the ASN-0098/ASN-0047 extended reachability that F5 and the worked instance draw on, complete the enumeration with `Σ.E` and `Σ.R` (or drop the partial unpacking and rest on "post-state equals `Σ`" alone, with `Σ` defined once).

### Issue 2: F6 discussion carries evidence-weighing meta-prose (anti-bloat)
**ASN-0114, Confinement section, after F6**: "The one implementation we have evidence for nonetheless delivers it: the selector is turned into a width-one query ... never visiting the others (Q12, Q18) ... That bounded-query behavior is an artifact of this implementation; it corroborates how the implementation realizes confinement but does not strengthen F6, whose guarantee remains at coverage."

**Problem**: The load-bearing content here is two sentences — F6 confines only at coverage, and representation-level non-exposure of the other ends is *not* a contract guarantee (the genuine, non-obvious limit of F6). The remainder weighs the implementation evidence against the claim ("corroborates ... but does not strengthen F6, whose guarantee remains at coverage") rather than advancing the argument. This is the meta-prose accretion the `review-mode.anti-bloat` classifier targets: prose that exists to explain why included evidence does not change the claim. A reader chasing the F6 limit has to step past it.

**Required**: Keep the abstract limit (coverage-only; representation may leak `eⱼ`) and, if the bounded-query evidence is retained at all, reduce it to a single corroborating clause without the "does not strengthen F6" evidence-weighing tail.

## OUT_OF_SCOPE

### Topic 1: Normal form of the returned span-set (Open Question 1)
**Why out of scope**: F3 deliberately binds the contract at coverage and leaves span decomposition free; what normal form an implementation *should* emit is ASN-0053 normalization territory, correctly deferred.

### Topic 2: Resolution of the recorded end against a document's arrangement (Open Question 2; "A boundary we must respect")
**Why out of scope**: Projecting the recorded endset into a document's live arrangement and filtering absent addresses is a separable operation (the scope list excludes resolving an endset's spec-set to V-positions). The note draws this boundary correctly; the shrinkage (Q15) and document-dependence (Q11) it names are properties of that future operation, not of FOLLOWLINK.

VERDICT: REVISE
