# Review of ASN-0109

## REVISE

### Issue 1: No concrete worked example
**ASN-0109, whole document**: The ASN introduces eleven claims (E0–E10) plus the `res`/`resolved` projection but never verifies any of them against a specific scenario.
**Problem**: The review standard is explicit — "no concrete example" is a REVISE item. A read operation has verifiable instances: e.g., a standard-triple link `Σ.L(a) = (F, G, Θ)` with `F = {(s₁,ℓ₁),(s₂,ℓ₂)}` discontiguous across two documents, `G = ∅` (one-sided), and `Θ` referencing a ghost type address. Walk the read through E1 (slot-for-slot return), E3 (both `F` spans returned), E4 (empty `G` slot returned, not invented), E5 (ghost `Θ` returned undereferenced), E7 (`participants(a)` names both `F` documents), and E9 (resolution of `F` when one span's content has been deleted from every arrangement).
**Required**: Add a worked instance that checks the load-bearing claims (E1, E3, E4, E5, E7, E9) against concrete endset values.

### Issue 2: E6 invokes single-step immutability for the transitive closure without induction
**ASN-0109, E6**: "Let `Σ →* Σ'` be any reachable evolution with `a ∈ dom(Σ.L)`. By link immutability, `Σ'.L(a) = Σ.L(a)`."
**Problem**: Link immutability (L12) is stated for a single transition `Σ → Σ'`. E6 quantifies over the reflexive-transitive closure `Σ →* Σ'`. The step from single-transition fixity to multi-transition fixity requires induction over the chain, and persistence of membership (`a ∈ dom(Σ'.L)`) across the chain requires store monotonicity (L12a), neither of which is cited. "By link immutability" is exactly the kind of one-sentence derivation the standards forbid for a multi-step argument.
**Required**: Give the induction: base case identity, step case applying L12 (value fixity) and L12a (membership persistence) at each link, concluding `Σ'.L(a) = Σ.L(a)` for the whole `→*` evolution.

### Issue 3: `home` is broadened beyond its foundation definition
**ASN-0109, §"Throughout we lean...":** "the field-projection `home(a) = N(a).0.U(a).0.D(a)` that recovers a document-level prefix from any address carrying a document field"; **E7**: `participants(a) = { home(s) : (s, ℓ) ∈ Σ.L(a).eᵢ, …, s carries a document field }`.
**Problem**: The foundation defines `home(a)` only for T4-valid element-level tumblers (`zeros(a) = 3`), where the T4b projections `N, U, D` are defined. E7 applies `home(s)` to *span start addresses*, and by L4 (EndsetGenerality) endset spans may reference arbitrary addresses — including non-element-level addresses, link addresses, and ghost addresses that need not be T4-valid. For such `s`, the T4b projections (and hence `home`) are undefined, so `home(s)` may not exist even when `s` superficially "carries a document field." The guard "s carries a document field" is itself imprecise (it is not the foundation's `zeros = 3` / T4-validity condition).
**Required**: Either restrict `participants(a)` to span starts that are T4-valid with `zeros(s) ≥ 2`, making the T4b projection well-defined, or define precisely the broadened `home` and prove it total on the guarded set. Do not silently extend a foundation definition.

### Issue 4: Weakest-precondition analysis is only the trivial case
**ASN-0109, §"What is returned…":** `wp(READENDSETS(·, a), result = R) ≡ a ∈ dom(Σ.L) ∧ Σ.L(a) = R`.
**Problem**: This is the trivially-true wp (the postcondition is the operation's defining equation). The standard requires a non-trivial wp case. The natural non-trivial target is the resolution layer: `wp(READENDSETS then res, "resolved(Σ, eᵢ) = ∅")` — under what condition on `Σ.M` does a non-empty stored endset resolve to nothing (the "ghost link")? This is the analytically interesting precondition and it is precisely the discriminating case the reader cannot distinguish (last Open Question).
**Required**: Compute one non-trivial wp — e.g., the condition for empty resolution of a non-empty endset — and show its derivation.

### Issue 5: Operation name inconsistent with title and Nelson's term
**ASN-0109, title and §"The operation"**: Title is "The RETRIEVEENDSETS Operation"; the prose states "Nelson calls the operation RETRIEVEENDSETS"; the specification then defines `READENDSETS : Σ × T ⇀ Link` with no explanation of the rename.
**Problem**: The claims table, the operation contract, and every E-claim reference `READENDSETS`, while the title and motivating text name `RETRIEVEENDSETS`. A reader cannot tell whether these are the same operation or whether a rename is intentional.
**Required**: Use one name throughout, or state explicitly that `READENDSETS` is this ASN's name for Nelson's RETRIEVEENDSETS and justify the choice.

### Issue 6: E8 asserts properties of traversal, which is undefined and out of scope
**ASN-0109, E8**: "From `READENDSETS(Σ, a)` the reader learns, and from arriving at any single endpoint the reader does *not* learn: (i) the *discontiguity*… Traversal collapses this structure to the single span it happens to reach."
**Problem**: The negative half of E8 is a claim about what link traversal (FOLLOWLINK) reveals. Traversal is out of scope and is nowhere defined in this ASN, so the comparison "traversal collapses… the read preserves it" cannot be established here — it rests on an unspecified operation. The positive content (the read returns the full N-ary structure) is already given by E2/E3/E5; the contrastive claim adds an unverifiable assertion.
**Required**: Either drop the comparative negative claims and retain only what the read establishes (E2, E3, E5 as a unit), or relocate the traversal contrast to motivational prose clearly marked as non-normative rather than a stated claim E8.

## OUT_OF_SCOPE

### Topic 1: Cross-arrangement resolution agreement
The fourth and fifth Open Questions (relating resolutions of one endset across two arrangements sharing Istream origin, and distinguishability of empty resolution) point to genuine invariants of the resolution layer that belong in an arrangement/version-correspondence ASN, not here. Correctly left open.

### Topic 2: Access control on identity disclosure
The first Open Question (confidentiality gating of participant disclosure) is a policy layer above the read operation. Correctly deferred.

META: not applicable — the ASN stays within abstract system territory (a state-pure read operation and its invariants), not implementation mechanics.

VERDICT: REVISE
