# Review of ASN-0120

## REVISE

### Issue 1: The stated endset-record postcondition does not pin coverage — ML2 is false as written
**ASN-0120, "What the endset arguments name, and what resolution recovers" (record-packaging paragraph) and ML1/ML2**: "the operation stores some `e_j ∈ Endset` whose spans are canonical — each of the form `(s, δ(n, #s))` with `s ∈ ρ(R_j, Σ)` and `n ≥ 1` — and whose coverage traces the resolved set on the store exactly … `coverage(e_j) ⊇ ρ(R_j, Σ)` and `coverage(e_j) ∩ dom(Σ.C) = ρ(R_j, Σ)`", together with ML2: "the stored span-set's decomposition is pinned only up to coverage equivalence."

**Problem**: The formal admissibility conditions admit records that are *not* coverage-equal to the reference decomposition, because the recovery equation traces coverage on `dom(Σ.C)` rather than on `F`. Counterexample: let `ρ(R_j, Σ) = {a₁}` where `a₂ = inc(a₁, 0)` is the unallocated frontier of `A_C(origin(a₁))` — so `a₂ ∈ F` but `a₂ ∉ dom(Σ.C) ∪ dom(Σ.L)`. The record `e = {(a₁, δ(2, #a₁))}` satisfies every stated condition: it is canonical, rooted at `a₁ ∈ ρ`, and by LP-Fin Corollary `F ∩ [a₁, a₁ ⊕ δ(2, #a₁)) = {a₁, a₂}`, so `coverage(e) ∩ dom(Σ.C) = {a₁} = ρ(R_j, Σ)`. Yet `coverage(e) = {t : a₁ ≼ t} ∪ {t : a₂ ≼ t}`, strictly larger than the reference decomposition's `{t : a₁ ≼ t}`. Two consequences:

1. ML2's claim that all admissible records are coverage-equal is falsified — the unit-span record and `e` are admissible and not coverage-equal, so "pinned only up to coverage equivalence" does not follow from the stated postcondition.
2. The difference is operationally observable, contradicting ML2's indistinguishability claim. `a₂` is precisely the *next* emission of `A_C(origin(a₁))`: a later K.α allocates it, a later K.μ⁺ arranges it into some `d''`, and then by LP12 the link is discoverable from `d''` under record `e` but not under the unit-span record — discoverability from content that was never resolved at creation. LP21 gives indistinguishability only for coverage-*equal* endsets and cannot rescue this. ML9's Fact (a) holds only at the creating post-state `Σ'` and is silent about these later states, so nothing in the ASN excludes the leak.

**Required**: Strengthen the admissibility so that coverage is actually pinned. Any of the following works: (i) require the record to be *tight at Σ* in ASN-0098's sense (every F-candidate inside each span lies in the store — with the recovery equation this forces `coverage(e_j) ∩ F = ρ(R_j, Σ)`); (ii) state the recovery equation on `F` directly: `coverage(e_j) ∩ F = ρ(R_j, Σ)`; or (iii) state coverage extensionally: `coverage(e_j) = (∪ a ∈ ρ(R_j, Σ) : {t : a ≼ t})`. Each of these admits exactly the reference decomposition and the resolved-run merges the prose intends, makes ML2 true, and additionally buys stability of the content-trace at all future states (LP19a then applies to the record, guaranteeing fresh allocations never enter the coverage). Note that interior over-reach is already excluded by the present equation (a skipped `a₂ ∈ dom(Σ.C) \ ρ` violates it); the slack is exactly at the unallocated chain frontier, which is why the trace must be taken on `F`, not on the current store.

### Issue 2: ML1's claims-table formula is malformed — unbound index, missing union
**ASN-0120, Claims Introduced, ML1 row**: "each endset argument `R` is recorded as the I-addresses `ρ(R,Σ) = {Σ.M(d_j)(v) : v ∈ dom(Σ.M(d_j)) ∧ v ∈ ⟦σ_j⟧} ⊆ dom(Σ.C)`"

**Problem**: The body defines `ρ(R, Σ)` as a union over all `j` in the spec-set `R = ⟨(d₁, σ₁), …, (dₚ, σₚ)⟩`; the table formula drops the union and leaves `j` free, so as a standalone claim statement it is ill-formed. The claims table is what gets extracted for downstream consumers, so the error propagates beyond this document.

**Required**: Restore the binder in the table: `ρ(R, Σ) = (∪ j : 1 ≤ j ≤ p : {Σ.M(d_j)(v) : v ∈ dom(Σ.M(d_j)) ∧ v ∈ ⟦σ_j⟧})`.

### Issue 3: The span-merge induction uses TS3 without citing it
**ASN-0120, "What the endset arguments name…" (merge paragraph)**: "hence each unit span's reach `shift(aₖ, 1)` equals the next span's start — consecutive unit spans are *adjacent* … ASN-0053's merge (S3), applied inductively along the run, then concatenates the half-open intervals exactly: `(∪ k : 1 ≤ k ≤ n : ⟦(aₖ, δ(1, #aₖ))⟧) = ⟦(a₁, δ(n, #a₁))⟧`."

**Problem**: The per-step fact established licenses only unit-to-unit adjacency. The inductive step merges the non-unit prefix `(a₁, δ(k, #a₁))` with the next unit span, and identifying the prefix's reach `a₁ ⊕ δ(k, #a₁) = shift(a₁, k)` with the next start `aₖ₊₁ = shift(aₖ, 1)` requires shift composition — `shift(shift(a₁, k−1), 1) = shift(a₁, k)` — which is TS3 (ShiftComposition, ASN-0034) and is nowhere cited. The same lemma is needed however the induction is oriented, since the final identification of the union's right endpoint with `shift(a₁, n)` composes `n` single shifts.

**Required**: Cite TS3 at the inductive step (one clause suffices: "with `aₖ = shift(a₁, k−1)` by induction and TS3").

## OUT_OF_SCOPE

### Topic 1: Endset arguments referencing the link subspace (links to links)
**Why out of scope**: `wf` confines specs to the content subspace and the ASN defers link-targeted endsets to its Open Questions; resolving what `ρ` should recover through a link-subspace V-position is new territory (it interacts with CL-OWN/CL-UNIQ and S8★'s trivial link-subspace runs), not an error here.

### Topic 2: Direct I-address endset arguments (ghost endsets, ghost types)
**Why out of scope**: The ASN correctly derives that V-spec resolution can never produce ghost or foreign endsets, and explicitly defers the I-address argument shape that L4/L9 generality would require. That is a distinct operation signature for a future ASN.

### Topic 3: N-ary MAKELINK (arity > 3)
**Why out of scope**: The foundation Link type admits `N ≥ 3` (L3) and Nelson calls for n-sets, but this ASN fixes the standard-triple operation. An n-ary creation operation — and what uniform resolution means for slots beyond 3 — is future work, not a defect in the triple form.

### Topic 4: Semantics of an empty from/to resolution
**Why out of scope**: The operation's behavior on `ρ(R₁, Σ) = ∅` is fully determined by the stated postconditions (the endset is recorded as `∅`, which the substrate permits for non-type slots); whether that should be *rejected* is a design question the ASN properly carries as an Open Question.

VERDICT: REVISE
