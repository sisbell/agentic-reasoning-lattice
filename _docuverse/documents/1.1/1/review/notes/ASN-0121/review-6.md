# Review of ASN-0121

## REVISE

### Issue 1: The "answer is forced" derivation does not actually force exclusion of retracted-but-satisfying links

**ASN-0121, "The answer is forced"**: "Demand of any candidate answer `R` two things. *Soundness*: `(A a : a ∈ R : sat(a, q, Σ))` … *Completeness*: `(A a : a ∈ addressable(Σ) ∧ sat(a, q, Σ) : a ∈ R)` … The two demands meet with no slack between them, leaving no design freedom."

**Problem**: As stated, soundness only requires `sat(a, q, Σ)` of returned links — it does *not* require `a ∈ addressable(Σ)`. Completeness only forces *addressable* satisfying links into `R`. Therefore both demands are equally satisfied by `R = {a ∈ addressable : sat}` **and** by `R' = {a ∈ dom(Σ.L) : sat}` (which additionally returns nullified links that still satisfy `sat`): every `a ∈ R'` satisfies `sat` (soundness ✓), and every addressable satisfying link is in `R'` (completeness ✓). The set `nullified(Σ) ∩ {a : sat}` is left entirely undetermined by the two demands, so FL-DEF is not the unique solution and "leaving no design freedom" is false. Concretely, Trace 4 (a₁ ∈ nullified yet endsets still satisfy `(∗,X,Y,∗)`) is exactly the witness that the two demands as written would permit returning a₁.

**Required**: Strengthen soundness to forbid phantoms — `(A a ∈ R : a ∈ addressable(Σ) ∧ sat(a, q, Σ))` — or add a third "currency" demand `R ⊆ addressable(Σ)`. Only then do soundness and completeness jointly force `findlinks(q, Σ) = {a ∈ addressable(Σ) : sat(a, q, Σ)}` uniquely.

### Issue 2: Empty *link-side* endsets (e₁ = ∅ or e₂ = ∅) are a permitted boundary the ASN never addresses

**ASN-0121, "What is being matched" / FL-EMP**: L3 constrains only `e₃ ≠ ∅`; `e₁, e₂ ∈ Endset` may be empty. The ASN treats the empty *request* component (FL-EMP, `lift(e, ∅) = false`) but never the case where a stored link's own from- or to-endset is empty.

**Problem**: A link with `e₁ = ∅` gives `touch(∅, F) = coverage(∅) ∩ coverage(F) = ∅ ≠ ∅ = false` for any constrained from-request `F`, so it never matches a constrained from-slot, yet under a from-wildcard it is admitted. FL-CMP quantifies over "every addressable link" and FL-WILD over "every arity," but neither verifies this boundary, and the worked instance contains no empty-endset link. Since "boundary cases mandatory — empty, zero, first, last" and empty endsets are an explicit hazard, the interaction between an empty *link* endset and a constrained vs. wildcard slot should be stated.

**Required**: Add a sentence (and ideally a worked-trace line) establishing that a link with `e₁ = ∅` (resp. `e₂ = ∅`) is correctly excluded from any constrained from- (resp. to-) slot and admitted only under the corresponding wildcard — confirming this is the intended "from nothing is not a from-match" semantics and noting the `touch` symmetry with FL-EMP (empty on either side yields `false`).

## OUT_OF_SCOPE

### Topic 1: Version-/time-qualified inquiry surfacing a currently-retracted link
Already correctly deferred by the ASN's own Open Questions; FL-RET is properly scoped to current addressability per Nelson's "not currently addressable" (4/9).

### Topic 2: The invariant connecting an I-address request to its V-spec phrasing
The arrangement-mediated naming front-end is explicitly held separable and listed as an Open Question; not a defect in this ASN.

VERDICT: REVISE
