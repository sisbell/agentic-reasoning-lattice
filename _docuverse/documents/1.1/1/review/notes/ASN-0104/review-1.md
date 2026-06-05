# Review of ASN-0104

## REVISE

### Issue 1: R5 is an existential claim with no witness

**ASN-0104, "Permanence and immutability of what is delivered"**: "R5 (V-read is not time-invariant) : there exist states Σ →* Σ', a document d, and a position v with v ∈ dom(Σ.M(d)) ∩ dom(Σ'.M(d)) and retrieveV(Σ, d, v) ≠ retrieveV(Σ', d, v)."

**Problem**: This is an existence claim, and the ASN discharges it entirely by intuition ("editing rearranges the V→I mapping," "This is unavoidable and intended"). No construction is exhibited. A claim of existence is proved by producing a witness, not by appeal to plausibility — and the witness here is non-trivial because it must keep `v` in the domain across the transition while changing `M(d)(v)` to an address holding *different* content (equal content values would falsify the inequality).

**Required**: Construct a concrete witness. A reordering (K.μ~, which by K.μ~-FIX preserves `dom(M'(d)) = dom(M(d))`) with at least two distinct content values demonstrably moves some occupied position to a new I-address; exhibit the two states, the position `v`, the two addresses, and two distinct `Val` values, then show `retrieveV` differs.

### Issue 2: R4's proof applies single-step invariants to a multi-step closure without induction

**ASN-0104, R4 proof**: "By store monotonicity (S1), `dom(Σ.C) ⊆ dom(Σ'.C)`, so `a ∈ dom(Σ'.C)`... By content immutability (S0b), `Σ'.C(a) = Σ.C(a)`."

**Problem**: R4 is stated over the reflexive-transitive closure `Σ →* Σ'`, but S1 and S0(b) are both stated for a *single* transition `Σ → Σ'` (ASN-0036). The proof invokes them directly on `→*` as though they were closure properties. The step from single-transition monotonicity/immutability to the multi-step conclusion is exactly an induction over the finite atomic sequence (SequentialTransitionAxiom) — routine, but omitted. R6, which inherits from R4, carries the same gap.

**Required**: Make the induction explicit: base case (empty sequence, `Σ' = Σ`) and inductive step chaining single-step S1 and S0(b) across each atomic transition, or cite a foundation `→*` form if one exists.

### Issue 3: R8 claims retrieveV is total over all (d, v), but the definition is undefined for d ∉ dom(M)

**ASN-0104, R8**: "retrieveI and retrieveV are total... For every Σ, every a ∈ T, and every (d, v), the result is defined and lies in Val⊥."

**Problem**: `retrieveV` is defined via `dom(Σ.M(d))`. In the foundation (ASN-0047 M1, "dom(M) = E_doc"), the arrangement family `M` has domain `E_doc`, so `Σ.M(d)` is undefined when `d ∉ dom(M)` (an unallocated or non-document address). For such `d`, `dom(Σ.M(d))` has no meaning, so neither branch of the guarded command is evaluable and the totality claim fails at this boundary. The prose elsewhere ("the document d must be in a state where its arrangement is consultable") implicitly assumes `d ∈ E_doc`, contradicting R8's "every (d, v)."

**Required**: Either restrict `retrieveV`'s precondition to `d ∈ dom(M)` (and weaken R8 accordingly), or define the result for `d ∉ dom(M)` (e.g., `retrieveV(Σ, d, v) = ⊥` by treating an unallocated document as the empty arrangement) and justify it against the foundation's `dom(M) = E_doc`.

### Issue 4: No concrete worked example verifies any positive-delivery claim

**ASN-0104, throughout**: the ASN states R0–R10 but never instantiates them on a specific scenario.

**Problem**: The key claims that *deliver* content (R1, R2, R9) are never checked against a concrete state. R9 (transclusion transparency) in particular asserts equality across two arrangements resolving to a shared address but is verified only by a one-line symbolic proof; a reader cannot confirm the composition `Σ.C ∘ Σ.M(d)` behaves as claimed on an actual arrangement.

**Required**: Add at least one concrete scenario — e.g., a document `d₁` with `M(d₁)(v₁) = a`, a second `d₂` with `M(d₂)(v₂) = a`, `Σ.C(a)` a specific value, plus a position `v' ∉ dom(M(d₁))` — and verify R1 (delivery), R2 (⊥ at `v'`), and R9 (equal delivery through `d₁`, `d₂`) against it.

### Issue 5: R2's biconditional silently depends on ⊥ ∉ Val

**ASN-0104, R2**: "retrieveV(Σ, d, v) = ⊥ ⟺ v ∉ dom(Σ.M(d))".

**Problem**: The ⟹ direction (contrapositive: `v ∈ dom(M(d)) ⟹ result ≠ ⊥`) holds only because, when `v ∈ dom(M(d))`, the result is `Σ.C(Σ.M(d)(v)) ∈ Val` and `Val` is disjoint from `{⊥}`. The note writes `Val⊥ = Val ∪ {⊥}` and describes `⊥` as "no content delivered," but never states `⊥ ∉ Val`. This disjointness is load-bearing for R2 (and for the "≠ ⊥" clause of R6); if a content value could equal `⊥`, R2's forward direction collapses.

**Required**: State explicitly that `⊥ ∉ Val` when introducing `Val⊥`, and cite it where R2 and R6 rely on it.

## OUT_OF_SCOPE

### Topic 1: Cross-server resolution by identity

**Why out of scope**: The first open question (resolution across the home-location boundary) concerns inter-server replication/protocol, explicitly deferred.

### Topic 2: Authorization conferred by address possession

**Why out of scope**: The access-control/authorization layer is named as unmodeled by this content-read contract; properly a future ASN.

### Topic 3: Reader-side verification of delivered bytes

**Why out of scope**: Cryptographic/tamper-detection guarantees are correctly identified as out of the present contractual immutability model.

VERDICT: REVISE
