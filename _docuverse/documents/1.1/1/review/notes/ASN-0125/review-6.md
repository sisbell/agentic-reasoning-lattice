# Review of ASN-0125

## REVISE

### Issue 1: Attribution discharge invokes ASN-0042 ownership over a state that does not carry it

**ASN-0125, EL8 (ClaimStanding)(b)**: "it is attributed: `home(addr(e))` is computable from the address alone by field projection (T4b), decidably (T6), and the effective owner follows by prefix (ASN-0042) — the claim is signed by its address".

**Problem**: The first half (`home(addr(e))` computable by T4b/T6 over the working state) is solid. The second half is not discharged. The note's working state is ASN-0047's `Σ = (C, L, E, M, R)` (stated explicitly in "The substrate we build on"), which contains neither a baptismal registry `Σ.B` nor a principal set `Π_Σ`. ASN-0042's effective-owner function is typed `ω_Σ : Σ.B → Π_Σ` with precondition `a ∈ Σ.B` and a state-dependent, delegation-evolving `Π_Σ`. So "the effective owner follows by prefix (ASN-0042)" invokes machinery whose state is absent from the substrate this note works over, and the precondition is never discharged. This is not isolated: the same unbridged import recurs at EL3's address-space elimination ("allocation under a prefix is the prefix owner's monopoly — O5") and at EL13 ("ownership domain spans many documents... `odom`, ASN-0042"). RQ3 (decidable attribution) is one of the seven requirements the whole EL3 derivation rests on, so its discharge cannot lean on an out-of-scope state component.

**Required**: Either (a) add a standing assumption bridging the substrate to ASN-0042's ownership layer (identify `dom(Σ.L)`/document prefixes with `Σ.B`, supply `Π_Σ`, and discharge `ω`'s `a ∈ Σ.B` precondition), or (b) state RQ3's discharge as home-document computability (T4b/T6 over the working state), which is what is actually available and is sufficient to identify the allocating document — and confine the EL3/EL13 ownership-monopoly arguments to facts the substrate state supports.

### Issue 2: `DC(ℓ')` is a state-relative predicate applied to a bare value with the evaluation state left implicit

**ASN-0125, EDITop / EL7(vi)**: "the *discipline-conformance precondition* `DC(ℓ')`: if `coverage(ℓ'.e₃) = coverage(K_sup)` then `ℓ'` itself satisfies the claim schema of Df-DISC(ii), and if `coverage(ℓ'.e₃) = coverage(R)` then `ℓ'` satisfies the unit-depth retraction schema".

**Problem**: Df-DISC(ii)'s "claim schema" is a whole-slice predicate `(A (b,F,G) ∈ S^Σ : (E x, y ∈ dom(Σ.L) : ...))`, and the unit-depth retraction schema requires `t ∈ A_rel^Σ = dom(Σ.L)` — both are state-relative through `dom(·.L)`. "`ℓ'` itself satisfies the claim schema" reduces these to a value predicate without saying at which state the witnesses `x, y` (or target `t`) must lie in `dom(·.L)`. This is load-bearing: EL7(vi)'s proof that `Σ₁` is edit-disciplined depends on `DC(ℓ')` placing the new claim's witnesses in `dom(Σ.L) ⊆ dom(Σ₁.L)` so that the claim at `a'` conforms at `Σ₁`. If the witnesses were only required to lie in `dom(Σ₁.L)`, they could include the fresh `a'`, and the transfer argument changes. The proof silently uses the `dom(Σ.L)` reading without stating it.

**Required**: State `DC(ℓ')` as an explicit value-level predicate evaluated at the editlink pre-state `Σ` — e.g., for the `K_sup` case, `(E x, y ∈ dom(Σ.L) : x ≠ y ∧ ℓ'.e₁ = {(x, δ(1,#x))} ∧ ℓ'.e₂ = {(y, δ(1,#y))})` — and have EL7(vi) cite `dom(Σ.L) ⊆ dom(Σ₁.L)` explicitly as the conformance-transfer step.

### Issue 3: The successor is born unlisted — a consequence of EL7 not drawn out

**ASN-0125, EL7 (EditContract)(i)**: "No content address, no entity, no provenance entry, no arrangement change: `Σ₂.C = Σ.C`, `Σ₂.M = Σ.M`, `Σ₂.E = Σ.E`, `Σ₂.R = Σ.R`."

**Problem**: `editlink` is `K.λ + assert_sup`; neither step performs `K.μ⁺_L`, so the successor `a'` enters `dom(Σ₂.L)` but never enters `ran(Σ₂.M(d))` for any `d` — the successor is born **unlisted**. The note states `Σ₂.M = Σ.M` but never names this consequence, and it is a surprising one for an operation called "edit": by EL11(a) the successor projects into no document (`listed(a', d, Σ₂)` is false everywhere, so its arrangement-gated discovery is empty), so the freshly edited link is contextually invisible in every current view until a separate `K.μ⁺_L` lists it. The note carefully explores the *original's* three axes (EL9) and two-regime discovery (EL11) but leaves the *successor's* discoverability status unexamined. This is a postcondition established (the frame) whose consequence is not explored.

**Required**: In EL7 (or EL9/EL11), state that the successor is born unlisted and trace the consequence: it is archivally discoverable via `out(a', Σ₂)` (and as `new(e_b)` of the claim) but contextually undiscoverable from any document until a separate `K.μ⁺_L` registers it. This is distinct from Open Question 7 (which asks for a *coupling invariant*); here the request is only to surface the behavior of the operation as defined.

### Issue 4: Miscited foundation operator

**ASN-0125, "The substrate we build on," Scope paragraph**: "citing existing foundation operators (`Observe_K`, ASN-0098) where a reader capability must be named."

**Problem**: `Observe_K` is defined in ASN-0086 (ObserveK), not ASN-0098. The note's own "Above the substrate" paragraph correctly attributes `Observe_K` to ASN-0086, and EL11(b) uses `Observe_{K_sup}` as an ASN-0086 operation, so this is an internal inconsistency. ASN-0098 is the source of `project`/`discoverable_from`, which is a different operator. A reader chasing the citation lands in the wrong ASN.

**Required**: Attribute `Observe_K` to ASN-0086 (and, if `project` was intended, name it with ASN-0098 separately).

### Issue 5: `Df-LISTED` reinvents ASN-0047's `Contains`

**ASN-0125, Df-LISTED**: "`listed(t, d, Σ) ≡ (E v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) = t)` — `t` appears in `d`'s current arrangement."

**Problem**: `listed(t, d, Σ) ⟺ t ∈ ran(Σ.M(d))`, which for `d ∈ dom(M) = E_doc` is exactly `(t, d) ∈ Contains(Σ)` (ASN-0047, CurrentContainment). The note introduces a fresh predicate for a relation a foundation already defines, rather than using or relating to it.

**Required**: Define `listed` as an abbreviation for `(t,d) ∈ Contains(Σ)` (ASN-0047), or use `Contains` membership directly; keep the genuinely new structural observation ("only its home can list it," via CL-OWN) as the value `Df-LISTED` adds.

## OUT_OF_SCOPE

### Topic 1: Span-level endset correspondence under reshaping edits (Open Question 6)
**Why out of scope**: `editlink` here is whole-link supersession ("`a'` replaces `a`"). Recording which spans of the new endset correspond to which spans of the old is a finer operation; the note correctly defers it.

### Topic 2: Meta-claims — supersession claims targeting supersession claims (Open Question 3)
**Why out of scope**: Df-DISC permits `x, y` to be claim addresses, and `current`/`reach_o` remain well-defined and finite over such edges, so no claim of this note breaks; the well-foundedness/stratification of meta-claim currency is genuinely new territory.

### Topic 3: Cross-asserter retraction authority (Open Question 1) and the edit↔listing coupling invariant (Open Question 7)
**Why out of scope**: The note establishes that assertion cannot be substrate-enforced (Remark, "no enforceable coupling") and that activity is monotone-downward (EL9(3)); what authority *should* govern another's claim, and what coupling *should* bind an edit to listing, are future design questions, not errors in the present operation.

VERDICT: REVISE
