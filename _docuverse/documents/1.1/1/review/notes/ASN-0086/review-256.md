# Review of ASN-0086

## REVISE

### Issue 1: "Entirety of stored-entity addresses" mis-cited to SD

**ASN-0086, Definition — AddressUniverse**: "By SD (StoreDisjointness, ASN-0093), `A^Σ` is the entirety of stored-entity addresses at Σ; no third category exists."

**Problem**: SD establishes only `dom(Σ.C) ∩ dom(Σ.L) = ∅` — that content and link addresses do not overlap. It does **not** establish that no *other* address category bears stored entities. The "entirety / no third category" claim is exactly L14 (DualPrimitive, ASN-0043): "The set of addresses at which entity values reside is `dom(Σ.C) ∪ dom(Σ.L)`. No state component maps an address outside this union to an entity value." The partition `A^Σ = A_doc^Σ ⊔ A_rel^Σ` rests on *both* facts: disjointness (SD) and exhaustiveness (L14). As written, the exhaustiveness half is asserted from a premise that cannot supply it — document tumblers in `dom(Σ.M)` are excluded from `A^Σ` only because L14 says arrangements are not entity-bearing addresses, never because of SD.

**Required**: Cite L14 (DualPrimitive) for the "entirety / no third category" claim, retaining SD for disjointness only.

### Issue 2: Type-mismatched set-difference in the ActiveSubset decidability note

**ASN-0086, Definition — ActiveSubset**: "`A_K^Σ = L_K^Σ \ nullified(Σ)`."

**Problem**: `L_K^Σ` is a set of triples `(a, F, G)`; `nullified(Σ)` is a set of addresses. Their set difference is ill-typed — no triple equals any address, so literally `L_K^Σ \ nullified(Σ) = L_K^Σ`, which contradicts the intended meaning. The correct form is used in the worked sketch ("`L_K^{Σ_1} \ {(a, F, G) : a ∈ nullified(Σ_1)}`") and in the formal Definition just above, so this is a local lapse, but in a note that computes `A_K` membership repeatedly it should not stand as written.

**Required**: Write `A_K^Σ = L_K^Σ \ {(a, F, G) ∈ L_K^Σ : a ∈ nullified(Σ)}` (or simply reference the formal definition for the difference).

### Issue 3: Anti-bloat — WP Case 2 Result defensive parenthetical

**ASN-0086, Weakest-Precondition Analysis, Case 2 *Result***: "Over the layer-reachable states (Definition — layer-reachable) — required because the derivation below invokes the unit-depth retraction discipline ... which mere `→*`-reachability does not supply (in contrast to Case 1, whose derivation runs over the weaker `→*`-reachable domain, needing only R0a's antichain) — the weakest precondition is..."

**Problem**: The domain restriction is justified, and contrasted against Case 1, *before the formula is even stated* — and the same justification ("disciplinedness rules out a pre-existing retraction covering the fresh `a`") is then given again, properly, in the *Derivation* paragraph below. The pre-statement contrast is defensive meta-prose explaining why the domain is needed rather than advancing the wp claim; it forces the reader to detour through a rationale that the derivation supplies in place. This is the reviser-drift pattern the anti-bloat classifier targets.

**Required**: State the Result with its domain qualifier plainly ("over layer-reachable Σ"); let the *Derivation* carry the single explanation of why disciplinedness is needed. Drop the inline contrast with Case 1.

## OUT_OF_SCOPE

### Topic 1: Higher-arity typed relations `L_K^{(n)}`

**Why out of scope**: The note restricts `L_K` to standard triples (`|Σ.L(a)| = 3`) and explicitly leaves higher-arity links inhabiting `dom(Σ.L)` without indexing any tuple. The relational algebra over `n`-ary links is genuinely new territory (and is already listed in Open Questions), not a defect in the binary-relation development here.

### Topic 2: Atomicity/consistency of Emit vs. concurrent Observe

**Why out of scope**: Concurrency semantics for `A_K` transitions under concurrent reads are not part of this note's sequential-transition substrate (SequentialAtomicTransitions, ASN-0093) and are correctly deferred to a future ASN.

VERDICT: REVISE
