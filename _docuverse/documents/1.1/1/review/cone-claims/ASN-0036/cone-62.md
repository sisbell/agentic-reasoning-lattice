Reading the foundation statements carefully against each ASN claim in turn.

**AX-1, AX-2, S0** — Each is a declared axiom or protocol posit. The accompanying prose correctly explains scope (AX-2's domain guard keeps `Σ.M(d)(v)` inside `dom(Σ.M(d))` before use; S0 is the root posit supplying S1). No derivation is attempted; none is needed. ✓

**S1** — One-step proof from S0: `a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)` (S0's first conjunct), taken universally. ✓

**S2** — Holds by unpacking "partial function": at most one image per domain element. ✓

**S3** — Induction on the transition sequence. Base case: AX-1 makes the quantifier range empty. Inductive step splits on whether the mapping at `(d, v)` is inherited unchanged or new/redirected. The two sub-cases are complementary and exhaustive (their union is the full complement of "inherited unchanged"), matching exactly AX-2's range for the second sub-case. S1 discharges the inherited case; AX-2 discharges the new/redirected case. The formal contract's framing (S1 handles one half, AX-2 the other, AX-1 pins the base) is correctly stated and matches the body proof. ✓

**subspace** — Definitional extension; precondition `#v ≥ 1` ensures `v₁` is in the component-projection domain (T0). ✓

**S8a, S8-depth, S8-fin** — Each is a declared design posit. S8a's prose correctly derives the chain `zeros(t) = 0 ⟺ |{i : tᵢ = 0}| = 0` (NAT-card empty-set characterization) `⟺ (∀ i : tᵢ ≠ 0)` `⟺ (∀ i : tᵢ > 0)` (NAT-zero on ℕ-valued components). S8-fin correctly avoids `|·|` on tumblers (outside NAT-card's scope), using a bijection from an initial segment of ℕ instead; the empty arrangement is the `n = 0` case. ✓

**OrdShiftHom** — Proof walks component-wise from TumblerAdd's three-region rule. Preconditions for TumblerAdd/TA0 are satisfied: `Pos(δ(n,m))` and `actionPoint(δ(n,m)) = m ≤ #v = m`. Part (a): position 1 is in the copy region (m ≥ 2 means 1 < m), so `r₁ = v₁`; subspace definition then reads `subspace(r) = r₁ = v₁`. Part (b): copy region gives `rᵢ = vᵢ ≥ 1` for `i < m` (from S8a hypothesis); action-point component `rₘ = vₘ + n ≥ 1` comes from OrdinalShift's exported bound, not re-derived. `zeros(r) = 0` and `#r = m ≥ 2` follow. The proof correctly consumes OrdinalShift's postcondition `shift(v,n)_{#v} = v_{#v} + n ≥ 1` rather than re-establishing the arithmetic from scratch. ✓

**S8** — The central argument. Lockstep successor `succ` is a well-defined partial function on `dom(M(d))`: injectivity from TS2 (common depth from shift's frame, not S8-depth's domain-restricted quantifier — matching the formal contract's explicit disclaimer); acyclicity from TS4 (`shift(v,1) > v`) composed with T1 irreflexivity. Forward and backward walks terminate (S8-fin + acyclicity), giving finite maximal chains. The displacement identity induction is correctly case-split: at i = 0, the `shift(t,0) := t` convention (declared axiom in S8) handles both the base and the i = 0 sub-case of the inductive step without invoking TS3 (which requires n₁ ≥ 1); for i ≥ 1, TS3 applies with n₁ = i ≥ 1, n₂ = 1 ≥ 1. Both the V-position chain and the I-address chain are collapsed by the same argument (a ∈ T via dom(Σ.C) ⊆ T). Conjunct (b) — `shift(a,k) ∈ dom(Σ.C)` — follows at each step from S3, since `shift(v,k) ∈ dom(M(d))` is established inductively. Partition properties: coverage uses the trivial run (v, M(d)(v), 1) for any v; disjointness from uniqueness of orbits; finiteness from S8-fin. The proof handles the empty case explicitly. ✓

The declined findings are correctly described by the reviser's rationale and are not re-surfaced.

VERDICT: CONVERGED