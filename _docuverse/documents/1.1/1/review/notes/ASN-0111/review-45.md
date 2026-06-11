# Review of ASN-0111

This note is in strong shape: the operation is honestly minimal, the wp derivation is genuine, RL4's witness pair is actually constructed rather than assumed, the three permanence families are each proved (the user-field induction over K.δ's case structure is correct — accounts arise only from `k = 2` off a node or `k = 0` off an account, both fixing `#U = 1`), and the exhaustiveness argument for the residual class checks out stage by stage (node baptism via `n₀ ≼ N(a)`, account/document frontier advances via FrontierEquivalence and ChildSpawnFreshness, element stage via ChainMembershipForOrigin). The worked read's tumbler arithmetic is correct throughout (I verified the field parses, `inc` steps, and the interval decomposition of the from-span). Two defects remain.

## REVISE

### Issue 1: The operation's state space is grounded in the wrong foundation
**ASN-0111, "Deriving the read"**: "Writing `𝒮` for the state space (ASN-0034), with the second argument restricted to reachable states per the standing precondition... `readlink : T × 𝒮 → Link ∪ {⊥}`"
**Problem**: ASN-0034's `𝒮` is the *allocator-tree* state space — AllocatedSet defines `s ∈ 𝒮` as "a configuration of the allocator tree — the set of activated allocators and, for each, the count nₛ(A)," and NoDeallocation uses the same object. A state in that space has no `.L` component, so `readlink(a, Σ) = Σ.L(a)` is not even well-typed over it. The states this ASN actually works with — carrying `Σ.L`, `Σ.C`, `Σ.M`, `Σ.E`, `Σ.R` — are ASN-0047's extended state `Σ = (C, L, E, M, R)` (equivalently ASN-0093's substrate state extended per ASN-0047), exactly as the standing precondition already says. The signature line contradicts the standing precondition's own grounding.
**Required**: Ground `𝒮` in the extended state space of ASN-0047 (or ASN-0093 as extended by ASN-0047), not ASN-0034. The citation is a one-token fix, but it sits in the type signature of the ASN's central artifact, so it must be right.

### Issue 2: RL4's witness construction claims reachability without discharging composite validity
**ASN-0111, "Faithful disclosure of nesting"**: "the post-state registers this document in dom(M) with the empty arrangement and is a state of the required form. ... branch the history by taking K.λ at `a'` with `v₁` in one branch and with `v₂` in the other. ... Writing `Σ₁, Σ₂` for the resulting states..."
**Problem**: RL4 quantifies over *reachable* `Σ₁, Σ₂`, and per ASN-0047 reachability means elementary transitions drawn from *valid composites* — clause 2 of ValidComposite★ additionally requires J0, J1★, J1'★ at each composite boundary. The construction's five steps (two K.δ steps building the document, one K.λ per branch at `a'`, the shared K.λ at `c`) each satisfy the coupling constraints vacuously (no `dom(C)` growth, no content-subspace range change, no growth of `R`), but the construction never says so. The ASN itself establishes the discharge as obligatory in its two sibling constructions — the residual-class argument states "The steps compose into valid composites: none touches dom(C), a content-subspace arrangement range, or R, so J0, J1★, and J1'★ hold vacuously at every boundary," and the worked read discharges J0/J1★/J1'★ for its K.α composites — so its omission exactly where reachability is the load-bearing hypothesis of the claim being witnessed is a completeness gap, not a stylistic one. (The worked read's three bare K.λ steps share the same unstated vacuity; a single sentence can cover both sites.)
**Required**: Add the one-line vacuity discharge for the RL4 construction's K.δ and K.λ steps (and let it cover the worked read's K.λ steps), mirroring the wording already used in the residual-class construction.

## OUT_OF_SCOPE

### Topic 1: Reader-visible identity of value-identical links
**Why out of scope**: The ASN correctly stops at "addresses, not values, carry link identity" and poses the distinguishability guarantee as an open question; specifying what the read interface must disclose about the key alongside the value is new territory for a future ASN, not an error here.

### Topic 2: Protocol encoding of the failure value
**Why out of scope**: Gregory's "distinguished failure reply" is cited only as evidence for totality; the wire-level semantics of `⊥` belongs to the inter-server protocol (BEBE), which the scope declaration excludes.

VERDICT: REVISE
