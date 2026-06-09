# ASN-0120 Claim Statements

*Source: ASN-0120-makelink-operation.md (revised 2026-06-08) — Extracted: 2026-06-09*

## Definition — EndsetResolutionFunction

For a spec-set `R = ⟨(d₁, σ₁), …, (dₚ, σₚ)⟩` at state `Σ`:

> `ρ(R, Σ) = (∪ j : 1 ≤ j ≤ p : { Σ.M(d_j)(v) : v ∈ dom(Σ.M(d_j)) ∧ v ∈ ⟦σ_j⟧ })`

Each `σ_j = (u_j, ℓ_j)` is a V-span with `subspace(u_j) = s_C`, depth `m = #u_j ≥ 2`, and displacement `ℓ_j = δ(n_j, m)` for some `n_j ≥ 1`. Filters to currently-active V-positions; resolves partial spans.

## Definition — DiscoverableFrom

`discoverable_from(a, d', Σ') ⟺ (E i : 1 ≤ i ≤ 3 : coverage(Σ'.L(a).eᵢ) ∩ ran(Σ'.M(d')) ≠ ∅)`

## Definition — EnabledMakelink

`enabled(makelink(d, R₁, R₂, R₃)) ≡ d ∈ dom(Σ.M) ∧ ρ(R₃, Σ) ≠ ∅`

---

## ML0 — IdentityAllocation (introduced)

IdentityAllocation: the link's identity is a fresh (`a ∉ dom(Σ.L)`), permanent (never removed, never reused — GlobalUniqueness, T8), value-fixed (L12) link-subspace address allocated by `A_L(d)` under home `d`, with `home(a) = d`

## ML1 — EndsetResolution (introduced)

EndsetResolution: each endset argument `R` is recorded as `ρ(R,Σ) = {Σ.M(d_j)(v) : v ∈ dom(Σ.M(d_j)) ∧ v ∈ ⟦σ_j⟧}` ⊆ dom(Σ.C) (ASN-0058 `resolve` generalized to partial spans) — I-addresses read through source arrangements at creation; canonical unit-depth spans give `coverage(e_j) ⊇ ρ(R_j,Σ)` with `coverage(e_j) ∩ dom(Σ.C) = ρ(R_j,Σ)` (covering, not exact — ASN-0053 S7)

## ML2 — FaithfulRecovery (introduced)

FaithfulRecovery: `coverage(e_j) ∩ dom(Σ.C) = ρ(R_j,Σ)` regardless of I-space fragmentation — every referenced content address recovered, none spurious; recorded span-set cardinality is a representation matter (no span-positional accessor, L5; projection by coverage only, LP21), not an abstract observable

## ML3 — UniformResolution (introduced)

UniformResolution: from, to, and type arguments are resolved by one procedure with no slot privileged at the V→I conversion step

## ML4 — ResidenceApplicationOrthogonality (introduced)

ResidenceApplicationOrthogonality: home document and endset content are independent; the precondition relates `d` to no `ρ(R_j,Σ)`; a link may home anywhere and point anywhere, connecting two documents without residing in either

## ML5 — OrderedEndsets (introduced)

OrderedEndsets: the recorded triple is ordered, `(F,G,Θ) ≠ (G,F,Θ)` for `F ≠ G` (L6); the order fixes from/to roles semantically without restricting reachability (discovery is endset-symmetric)

## ML6 — TypedRelation (introduced)

TypedRelation: operation precondition `ρ(R₃,Σ) ≠ ∅` (the operation is undefined on a type spec that resolves empty, since K.λ requires `e₃ ≠ ∅`, L3); the third endset, recorded like from/to but matched by address (L8), distinguishes a typed relation from a bare connection; MAKELINK's type always resolves to stored content (`ρ(R₃,Σ) ⊆ dom(Σ.C)`), so it does *not* exercise L9's ghost-type permission — the only unstored tumblers in `coverage(e₃)` are surplus descendants

## ML7 — Permanence (introduced)

Permanence: `(A Σ' → Σ'' : a ∈ dom(Σ'.L) : a ∈ dom(Σ''.L) ∧ Σ''.L(a) = Σ'.L(a))` — the made link is not broken by any editing of the content it connects

## ML8 — EndsetImmutability (introduced)

EndsetImmutability: the recorded value `Σ'.L(a)` is frozen at creation (L12), with `coverage(e_i) ∩ dom(Σ.C) = ρ(R_i,Σ)`; editing source documents changes `Σ.M` but never the recorded I-addresses, so by S0 the endset survives as long as any referenced content persists

## ML9 — DiscoverabilityDecoupledFromResidence (introduced)

DiscoverabilityDecoupledFromResidence: `wp(makelink, discoverable_from(a, d', ·)) ≡ enabled(makelink) ∧ d' ∈ dom(Σ.M) ∧ (E i : ρ(R_i,Σ) ∩ ran(Σ.M(d')) ≠ ∅)`, with `enabled(makelink) ≡ d ∈ dom(Σ.M) ∧ ρ(R₃,Σ) ≠ ∅`; beyond enabledness the home `d` does not appear in the discoverability test — the link is discoverable from every region its endsets reference, residence-independently and endset-symmetrically

## ML10 — Frame (introduced)

Frame: `Σ'.C = Σ.C`; `(A d' ≠ d : Σ'.M(d') = Σ.M(d'))`; existing `Σ.L` entries unchanged; the linked-into sources are unmodified by being linked into
