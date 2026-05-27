# Review of ASN-0099

## REVISE

### Issue 1: Conformance contract for `findlinks_V` is implicit, not explicit

**ASN-0099, "Completeness" section**: F2, F3, F2-filt, F3-filt, F2-sco, F3-sco state conformance for the I-side operations (`findlinks`, `findlinks_filtered`, `findlinks_scoped`). No conformance pair is stated for `findlinks_V`.

**Problem**: The ASN's opening sentence frames the reader's question in V-coordinates: "*what connects here from elsewhere?*" The reader-facing operation is `findlinks_V`. But the formal conformance contracts bind implementations only on the I-side. An implementation exposing `findlinks_V` directly (the natural user-facing API) has no explicit conformance obligation in this ASN.

**Required**: Add a conformance pair (e.g., F2-V ∧ F3-V) for `findlinks_V`, either as a stand-alone constraint on a `result_V : 𝒫(T) × dom(M) × 𝒮 → 𝒫(T)` function, or as a labeled derived claim establishing that `result_V` conformance follows from `result` conformance plus correct `image` computation. The derivation through F12 is one line, but the conformance scope should not be left implicit.

### Issue 2: F10's general "version chains nested" claim is verified only for one case

**ASN-0099, F10 discussion**: "with version chains nested under their parents by the version-extension ordering just derived"

**Problem**: The version-nesting claim is established for one specific instance (`d_c = inc(d_a, 1)`, `d_b = inc(d_a, 0)`, showing `ℓ < ℓ_v < ℓ'`). The general statement — that for any document `d`, any version `v` of `d`, and any sibling `d'` of `d` with `d < d'`, all of `v`'s links sort between `d`'s and `d'`'s — is suggested by the structural argument but not separately stated. A reader following F10 sees only the specific case but the prose claims the general structure.

**Required**: Either state the version-nesting structure as a separate derived lemma with the full structural argument, or soften the F10 discussion prose to indicate the specific case is illustrative and the general structure follows by the same reasoning.

### Issue 3: F4's realizability discharge implicitly assumes reachability from Σ₀

**ASN-0099, F4 realizability discussion**: "The construction extends any base state Σ with `dom(Σ.M) ≠ ∅` as follows."

**Problem**: At Σ₀ (ASN-0047 initial state), `dom(M₀) = ∅`. The realizability discharge requires that "any base state Σ with `dom(Σ.M) ≠ ∅`" is reachable, but the ASN doesn't cite the construction. The standard K.δ chain (node initialization → account → document via successive K.δ steps) makes this true, but the implicit assumption weakens F4's "operationally observable" claim when read in isolation.

**Required**: Add one sentence citing the K.δ-chain reachability of a base state with `dom(Σ.M) ≠ ∅` from Σ₀, or note that the existence of such a base state follows from the standard initialization sequence.

### Issue 4: A1's transitional status

**ASN-0099, A1 (LinkStoreInertOfNonAllocatingOperations) Status section**: A1 is introduced as an applications-level axiom because ASN-0047's published frames for K.μ⁺, K.μ⁻, and K.ρ do not include `L' = L`. A1 is grounded in design intent and implementation evidence, and the ASN issues a "Substrate-promotion request" for ASN-0047 to add the missing clauses.

**Problem**: F9, F11, F17, F18, F19, F9-cor, F9★, F9★-cor, F19-filt, F19-sco all depend on A1 at the K.μ⁺/K.μ⁻/K.ρ sub-cases. The ASN handles this transparently — gap identified, grounding provided, promotion requested — but A1's status as an applications-level patch to substrate-level frame clauses leaves the load-bearing claims in transitional state. A reader cannot tell from this ASN alone whether A1 is permanent applications-level content or a temporary holding pattern.

**Required**: Clarify A1's intended permanence. If A1 is a temporary patch, mark this ASN as not finally converged pending ASN-0047 revision. If A1 is permanently applications-level (e.g., because the ASN-0047 authors decline the request), justify why this axiom doesn't belong in the substrate despite its scope being substrate-wide.

## OUT_OF_SCOPE

### Topic 1: I→V resolution (FOLLOWLINK / RETRIEVEENDSETS)
**Why out of scope**: Inverse-direction operation; the ASN correctly identifies it as a separate future ASN with its own subtleties around unmapped I-addresses.

### Topic 2: Phantom-address query semantics
**Why out of scope**: Operational interpretation of queries against addresses outside `dom(Σ.C) ∪ dom(Σ.L)`. The match predicate is mechanically well-defined for any `I ⊆ T`; only the operational meaning is unsettled.

### Topic 3: Access control composition
**Why out of scope**: Orthogonal concern that composes with scoping; correctly noted as belonging to a different specification layer.

### Topic 4: Multi-instance / partition handling / replication
**Why out of scope**: Replication and BEBE are listed in scope exclusions; this is their natural location.

### Topic 5: Time-bound between K.λ commit and discoverability
**Why out of scope**: Performance is correctly noted as an implementation property, not a correctness property.

### Topic 6: Combined `findlinks_filtered_scoped(C, S, Σ)`
**Why out of scope**: The composition adds no new structural content; the ASN correctly defers this to downstream ASNs that need the composed form.

### Topic 7: Substrate commitment minimum for non-allocating-fragment invariance
**Why out of scope**: Substrate-level structural-commitment question; belongs in substrate revision work, not in this operation specification.

VERDICT: REVISE
