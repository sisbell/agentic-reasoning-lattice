# Review of ASN-0120

The ASN is in strong shape: the V→I conversion thesis is carried through with genuine proofs, the recovery equation's `F`-trace is well-motivated by the frontier counterexample, the confinement argument (T5 through the shared prefix), the covering-surplus argument, the K.μ⁺_L precondition discharge, and the ML9 wp derivation are all sound on checking, and the worked example exercises the home-document boundary case (`d' = d`). Two issues remain — one notational gap at a proof's base case, one anti-bloat duplication.

## REVISE

### Issue 1: `shift(·, 0)` is used without being defined, and the merge induction's base case invokes TS3 outside its precondition

**ASN-0120, "What the endset arguments name" (merge-identity paragraph and extensional-form paragraph)**: "the accumulated prefix `(a₁, δ(k, #a₁))` reaches … `aₖ₊₁ = shift(aₖ, 1) = shift(shift(a₁, k−1), 1) = shift(a₁, k)`, with `aₖ = shift(a₁, k−1)` by induction and the composition of shifts by TS3" and "the `F`-trace `{shift(s, k) : 0 ≤ k < n}`".

**Problem**: ASN-0034's OrdinalShift is defined only for `n ≥ 1`. At the induction's base case `k = 1`, the chain reads `shift(shift(a₁, 0), 1)` — `shift(a₁, 0)` is an undefined term — and TS3 (ShiftComposition) requires `n₁ ≥ 1, n₂ ≥ 1`, so it does not license the composition at that step. The `F`-trace expression `{shift(s, k) : 0 ≤ k < n}` likewise consults `shift(s, 0)`. The foundations that need this case adopt it as an explicit local convention (ASN-0036 S8: "Under the convention `shift(t, 0) := t`"; ASN-0058 OrdinalShiftBase), each scoped "throughout this ASN" — neither convention is in force here, and ASN-0120 states none.

**Required**: Adopt the convention `shift(t, 0) := t` once, where the merge identity is first developed (matching ASN-0036/ASN-0058's practice), and handle the induction's `k = 1` step explicitly (it is the trivial case `a₂ = shift(a₁, 1)`, no TS3 needed; TS3 carries the steps `k ≥ 2`). Alternatively restructure both expressions to avoid the zero index.

### Issue 2: the store-trace consequence of the recovery equation is established in ML1 and then re-derived or restated twice in ML9

**ASN-0120, ML9 Fact (a) and the closing paragraph of the ML9 discussion**: Fact (a): "The content half follows from ML1's recovery equation by set algebra, since `dom(Σ'.C) = dom(Σ.C) ⊆ F` (ML10; LP-Sub): `coverage(eᵢ) ∩ dom(Σ'.C) = (coverage(eᵢ) ∩ F) ∩ dom(Σ.C) = ρ(R_i, Σ) ∩ dom(Σ.C) = ρ(R_i, Σ)`"; closing paragraph: "Nor can the guarantee silently widen at later states: each `eᵢ` is tight at `Σ` (ML1), so by LP19a (ASN-0098) no address freshly allocated … ever enters `coverage(eᵢ)`."

**Problem**: ML1's own paragraph already establishes both halves: store-trace exactness at the creating state ("`coverage(e_j) ∩ dom(Σ.C) = ρ(R_j, Σ)`, by set algebra from the recovery equation and `dom(Σ.C) ⊆ F`") and stability at every later state ("`coverage(e_j) ∩ dom(Σ''.C) = ρ(R_j, Σ)` at every `Σ''` with `Σ →* Σ''`"). Fact (a)'s content half repeats the identical set-algebra derivation with a prime decoration instead of citing the established result plus ML10's `dom(Σ'.C) = dom(Σ.C)`; the ML9 closing paragraph restates ML1's LP19a stability sentence a third time. This is the accretion pattern this note is flagged for: the same consequence derived in one place and re-derived or re-narrated in two others.

**Required**: Establish once in ML1 and cite thereafter. Fact (a)'s content half should read as an application: by ML10, `dom(Σ'.C) = dom(Σ.C)`, and by ML1's store-trace exactness, `coverage(eᵢ) ∩ dom(Σ'.C) = ρ(R_i, Σ)`. The closing paragraph should either be cut or compressed to its one new clause (that discoverability from a new document can arise only through arrangement of *originally resolved* content), citing ML1's stability rather than re-invoking tightness and LP19a.

## OUT_OF_SCOPE

### Topic 1: Endset arguments supplied as direct I-addresses (ghost types, foreign endsets, links targeting links)
**Why out of scope**: The ASN correctly restricts MAKELINK-via-V-specs to content-backed endsets and identifies the direct-I-address argument shape as a distinct operation surface; together with the semantics of an empty from/to resolution, these are properly carried as the ASN's own Open Questions rather than gaps in this operation's contract — the postcondition is already determinate on those inputs (`ρ = ∅` forces `e_j = ∅`, and the recovery equation holds vacuously).

VERDICT: REVISE
