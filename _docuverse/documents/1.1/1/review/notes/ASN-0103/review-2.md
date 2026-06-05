# Review of ASN-0103

## REVISE

### Issue 1: Dangling reference to undefined claim label "Q10"
**ASN-0103, Effect Three (Nothing Else Changes)**: "Entity permanence (P1, ASN-0047) is preserved, and the document population grows by *exactly one* (Q10): `|E'_doc| = |E_doc| + 1`."
**Problem**: There is no claim labeled `Q10` in this ASN (or in the cited foundations). The claims table restates this fact as `CND.E`, not `Q10`. The label appears to be a leftover from a draft or another ASN.
**Required**: Replace `(Q10)` with `(CND.E)` or delete the parenthetical.

### Issue 2: Ownership derivation invokes `ω_Σ(A)` without establishing `A ∈ Σ.B`
**ASN-0103, Ownership and Immediate Referability / CND.own**: "Let `π_A = ω_Σ(A)`; then `pfx(π_A) ≼ A ≼ d`..." preceded by "The account, a previously baptised entity, is a registry member `A ∈ Σ.B`."
**Problem**: `ω_Σ : Σ.B → Π_Σ` (ASN-0042) is only defined on registry members, so `ω_Σ(A)` presupposes `A ∈ Σ.B`. The ASN asserts `A ∈ Σ.B` inline ("a previously baptised entity is a registry member") but cites nothing that bridges the ASN-0047 entity set `E` to the ASN-0040/0042 baptismal registry `Σ.B`. PrefixBaptismCoupling (ASN-0042) only gives `pfx(π) ∈ Σ.B` for principals `π ∈ Π_Σ`; since `ω_Σ(A)` may be a node-level principal whose prefix is a *proper* prefix of `A`, nothing here forces `A` itself to be a registry member. The operation's preconditions (CND.pre) state only `A ∈ E ∧ Account(A)` and `pfx(π) ≼ A` — `A ∈ Σ.B` is neither a precondition nor a cited invariant. The derived claim CND.own therefore rests on an unsupported step, and account provisioning (which would baptise `A`) is explicitly out of scope.
**Required**: Either add `A ∈ Σ.B` to CND.pre (alongside `A ∈ E ∧ Account(A)`), or cite/state an `E`↔`Σ.B` coupling invariant that discharges it. The derivation of `ω_{Σ'}(d) = ω_Σ(A)` must name where `A ∈ Σ.B` comes from.

### Issue 3: Superseded invariant cited in the extended-state context
**ASN-0103, Effect Two (The Arrangement Is Empty)**: "referential integrity `ran(M'(d)) ⊆ dom(C')` (S3, ASN-0036) holds *vacuously* for `d`."
**Problem**: The operation is specified over the extended state `Σ = (C, L, E, M, R)`, where S3★ (ASN-0047) is the operative invariant and explicitly "supersedes S3 (ASN-0036)". The Invariants Maintained section correctly discharges S3★, so Effect Two's citation of the superseded S3 is inconsistent with the rest of the ASN.
**Required**: Cite S3★ (ASN-0047) in Effect Two for consistency.

## OUT_OF_SCOPE

### Topic 1: Entity/registry coupling invariant
A general invariant coupling membership in `E` (ASN-0047) to membership in `Σ.B` (ASN-0040/0042) — if one does not already exist in the foundations — would belong in a coupling/bridge ASN, not here. This ASN may simply cite it once it exists (see Issue 2 for the minimal local fix).

VERDICT: REVISE
