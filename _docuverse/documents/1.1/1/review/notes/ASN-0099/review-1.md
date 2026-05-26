# Review of ASN-0099

## REVISE

### Issue 1: No concrete worked example
**ASN-0099, throughout**: No section shows FINDLINKS evaluated against a specific state.
**Problem**: The reader cannot verify the operation's key claims against an instance — e.g., a state with two transcluded documents, a link with type endset on slot 3, and a query showing F6 (transclusion transparency) or F13 (set-additivity) hold concretely.
**Required**: Add a worked example: specify a small Σ (a few links with explicit endsets, two documents with overlapping ranges), pose a V-region query, walk through Phase 1 (image computation) and Phase 2 (match against each link), and verify F2/F6/F13 against the result.

### Issue 2: F2 and F3 stated as obligations but not derived
**ASN-0099, "Completeness"**: "The operation's defining obligation is *completeness*..."
**Problem**: F2 and F3 are immediate from the set-comprehension definition `findlinks(I, Σ) = {a ∈ dom(Σ.L) : matches(a, I, Σ)}` — completeness because the comprehension includes every matching `a ∈ dom(Σ.L)`; soundness because the predicate selects only matching members of `dom(Σ.L)`. The ASN frames them as obligations without showing they follow from the abstract definition.
**Required**: After stating F2 and F3, add a one-paragraph derivation noting both are tautologies of the definition, and that they become non-trivial only as implementation obligations (which is what the "What Completeness Demands of Implementations" section addresses).

### Issue 3: Preconditions on `image` left implicit
**ASN-0099, "A Two-Phase Factoring"**: `image(R, d, Σ) = {Σ.M(d)(v) : v ∈ R}`
**Problem**: `Σ.M(d)(v)` is undefined when `d ∉ dom(Σ.M)` or `v ∉ dom(Σ.M(d))`. The definition is well-formed only under `d ∈ dom(Σ.M) ∧ R ⊆ dom(Σ.M(d))`. Neither precondition is stated.
**Required**: State the preconditions explicitly. Address what happens when `R` contains positions outside `dom(Σ.M(d))` (silent skip? error? definition undefined?).

### Issue 4: `*` notation conflicts with the filter framework
**ASN-0099, "Endset Filtering"**: "The unfiltered form is recovered by taking `C = {(*, I)}` where `*` denotes 'existentially quantified over slots'"
**Problem**: The filtered form is defined as a universal over `(i, J) ∈ C` — a conjunction. The unfiltered form is an existential over slots — a disjunction. These are structurally distinct; no single conjunctive constraint set recovers the disjunction. The `*` notation is informal and the equivalence claim is incorrect as stated.
**Required**: Either (a) drop the claim that filtered recovers unfiltered and present them as two distinct operations, or (b) formalize the filter framework to admit per-slot disjunctions (e.g., a constraint of the form "exists slot in S with coverage overlapping J").

### Issue 5: F10 OrderedResult requires finiteness, not derived
**ASN-0099, "Result Ordering"**: "The result is presentable as a sequence ⟨a₁, a₂, ..., aₙ⟩"
**Problem**: Presentability as a finite sequence requires the result set to be finite. The ASN does not derive this. The derivation is one line: `result(I, Σ) ⊆ dom(Σ.L)`, finite by L-fin (ASN-0093), so the result is finite.
**Required**: State and discharge the finiteness step explicitly, citing L-fin (ASN-0093) and the well-orderedness of T1 (ASN-0034) on the finite subset.

### Issue 6: Empty-query boundary case not addressed
**ASN-0099, throughout**: No discussion of `findlinks(∅, Σ)` or `findlinks_V(∅, d, Σ)`.
**Problem**: For `I = ∅`, every `coverage(eᵢ) ∩ ∅ = ∅`, so no slot matches; the result is `∅`. Similarly `image(∅, d, Σ) = ∅`. This is a meaningful boundary — a reader querying an empty selection — and the ASN's claims (F2, F3, F8, F13) all must specialize correctly.
**Required**: Add a short paragraph addressing the empty-query case explicitly. Verify F13 specializes correctly (`findlinks(∅ ∪ I₂, Σ) = ∅ ∪ findlinks(I₂, Σ)`).

### Issue 7: F8 Determinism proof too brief
**ASN-0099, "Determinism"**: "Determinism is structurally guaranteed by the form of `matches`."
**Problem**: The one-paragraph proof skips steps. From `Σ.L = Σ'.L`, derive: `dom(Σ.L) = dom(Σ'.L)`, then `(A a ∈ dom(Σ.L) :: Σ.L(a) = Σ'.L(a))`, then per-slot `Σ.L(a).eᵢ = Σ'.L(a).eᵢ`, then `coverage(Σ.L(a).eᵢ) = coverage(Σ'.L(a).eᵢ)`, then `matches(a, I, Σ) ⟺ matches(a, I, Σ')`, then equality of result sets by extensionality.
**Required**: Make the chain explicit. The ASN holds itself to "no proof by similarly"; F8 currently leans on it.

### Issue 8: F7 Endset symmetry not stated or derived in prose
**ASN-0099, claims table**: "F7 | Endset symmetry: slots are equally searchable; filters conjoin"
**Problem**: F7 appears in the claims table but no body section labels it as F7, states it, or derives it. "Slots equally searchable" follows from the existential in `matches` treating all slots uniformly; "filters conjoin" follows from the universal in `findlinks_filtered`. Neither is made explicit.
**Required**: State F7 in the prose (likely in the "Match Predicate" or "Endset Filtering" section) and derive both halves from the corresponding quantifiers.

### Issue 9: Link-subspace V-positions in `image` not addressed
**ASN-0099, "The Image Set"**: Discussion treats V-region as text-subspace content.
**Problem**: A reader may query V-positions with `subspace(v) = s_L`, in which case `Σ.M(d)(v) ∈ dom(Σ.L)` by S3★. The image set then contains link addresses, and Phase 2 matches links against link addresses — well-defined by L4 (ASN-0043) which permits endsets to reference the link subspace. The case is not discussed.
**Required**: Address explicitly. Note that the operation works uniformly across both subspaces because the match predicate is address-set agnostic. This is a real use case (finding links-to-links, e.g., when a comment annotates a link).

### Issue 10: Creation-order recovery claim not derived
**ASN-0099, "Result Ordering"**: "within a single home document, link addresses are produced by repeated `inc(·, 0)` from a base, so T1 on those addresses agrees with the order in which links were allocated"
**Problem**: This requires citing the relevant chain machinery: SubAllocatorAxiom.ChainDiscipline (ASN-0093) gives the `inc(·, 0)` recurrence; ChainEnumerationInjectivity (ASN-0093) makes the enumeration strictly T1-increasing. The ASN gestures at the conclusion without naming the discharging premises.
**Required**: Cite the foundation lemmas that establish the T1-monotone enumeration of a sub-allocator chain.

## OUT_OF_SCOPE

### Topic 1: Query I-sets containing addresses outside `dom(Σ.C) ∪ dom(Σ.L)`
**Why out of scope**: The ASN explicitly flags this as an open question. The match predicate is mechanically well-defined for any `I ⊆ T`, but the operational semantics of phantom-address queries is a new design question, not a defect of this specification.

### Topic 2: Multi-instance / cross-server consistency
**Why out of scope**: Inter-server protocol (BEBE) is excluded by scope directive. The ASN's single-state framing is appropriate.

### Topic 3: Access control composition with completeness
**Why out of scope**: Access control is a separate concern that composes with discovery; the ASN correctly identifies it as orthogonal.

### Topic 4: FOLLOWLINK / inverse I→V resolution
**Why out of scope**: A separate operation with its own specification; correctly noted as future work.

### Topic 5: Time bounds on K.λ-to-query propagation
**Why out of scope**: Performance/timing is an implementation property, not an abstract guarantee. The ASN's atomicity discussion suffices at the abstract layer.

VERDICT: REVISE
