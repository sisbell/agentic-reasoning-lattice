**Dependency audit:**

Reading each formal contract against the foundations in scope.

**S8-fin** — The axiom `(E n : n ∈ ℕ : (E f :: f : {j ∈ ℕ : 1 ≤ j ≤ n} → dom(Σ.M(d)) ∧ ...))` must hold at the base state where `dom(Σ₀.M(d)) = ∅` by AX-1. The only valid witness is `n = 0`: for any `n ≥ 1` the index set is non-empty and a total function from it into `∅` cannot exist. The witness `n = 0` requires `0 ∈ ℕ`. The listed foundations — NAT-carrier (ℕ as a set), NAT-closure (`1 ∈ ℕ`, identities, successor positivity), NAT-order — do not supply `0 ∈ ℕ`. NAT-closure uses `0` but draws it from NAT-zero, which it does not re-export. NAT-zero is missing from Depends. The prose ("case `n = 0`") writes the constant directly; the formal contract needs it grounded.

**V-sub** — The formal contract introduces the text-subspace specialization `V_1(d) = {v ∈ dom(Σ.M(d)) : subspace(v) = 1}`, writing `1` as a first-class natural-number constant. NAT-closure supplies `1 ∈ ℕ` (its explicit axiom clause). V-sub's Depends lists only Σ.M(d) and subspace; NAT-closure is absent. The transitive path V-sub → subspace → T0 → NAT-closure is not a substitute for direct citation when the constant appears in V-sub's own formal statement — precisely the principle S8-fin applies when it independently cites NAT-closure for the same `1` in `{j ∈ ℕ : 1 ≤ j ≤ n}`.

**S8-depth** — Formal statement uses `#u = #w` (T0) and `subspace(u) = subspace(w)` (subspace). Both cited. OrdShiftHom exclusion is sound and explained. No gap.

**Σ.M(d)** — Types the arrangement T ⇀ T, cites T0 for the carrier T. Clean.

**subspace** — Defines `subspace(v) = v₁`, cites T0 for the component projection and length operator. T0's nonemptiness grounds totality. Clean.

**D-MIN** — The Design Requirement states `min(V_1(d)) = [1, 1, ..., 1]`. The tuple `[1, 1, ..., 1]` is a specific element of T: its existence requires T0's comprehension (at `p = m`, `r ≡ 1`) and its component value requires `1 ∈ ℕ` from NAT-closure. D-MIN's Depends lists V-sub, S8-depth, T1, S8-fin — neither T0 nor NAT-closure appears directly. The transitive routes D-MIN → S8-depth → T0 and D-MIN → T1 → NAT-closure do not substitute when the symbols appear in D-MIN's own formal statement.

The independence-argument sentence "the only position strictly between its extremes [1, 5] and [1, 7] is [1, 6]" is imprecise: in T1's full order on T, depth-3 tumblers such as [1, 5, 1] satisfy [1, 5] < [1, 5, 1] < [1, 6]. The claim is true only among depth-2 positions in the text subspace, i.e., within V_1(d) under S8-depth. The argument's intent is correct but the phrase overstates.

---

### S8-fin missing NAT-zero for base-state witness
**Class**: REVISE
**Foundation**: NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ`
**ASN**: S8-fin (FiniteArrangement), Formal Contract axiom and prose: *"The empty arrangement is the case `n = 0`, where the index domain `{j ∈ ℕ : 1 ≤ j ≤ 0}` is empty"*
**Issue**: At the base state, `dom(Σ₀.M(d)) = ∅` by AX-1. The axiom's existential `(E n : n ∈ ℕ : (E f :: f : {j ∈ ℕ : 1 ≤ j ≤ n} → dom(Σ.M(d)) ∧ ...))` must be satisfied there. For any `n ≥ 1`, the index set `{j ∈ ℕ : 1 ≤ j ≤ n}` is non-empty, and a total function from it into `∅` does not exist. The unique valid witness is `n = 0`, which requires `0 ∈ ℕ`. That membership is NAT-zero's contribution. NAT-zero is not in S8-fin's Depends. The listed foundations do not supply it: NAT-carrier declares ℕ as a set; NAT-closure uses `0` (in `0 + n = n`, `n + 0 = n`, `0 < n + 1`) but obtains it from NAT-zero, which NAT-closure does not re-export to its consumers; NAT-order gives the order but not the distinguished element `0`. The prose writes `n = 0` as a first-class constant; the formal contract needs it grounded.
**What needs resolving**: Add NAT-zero (NatZeroMinimum) to S8-fin's Depends, citing it for `0 ∈ ℕ` — the value the unique base-state witness `n = 0` inhabits and the constant the prose writes directly in the empty-arrangement case.

---

### V-sub missing NAT-closure for text-subspace constant
**Class**: REVISE
**Foundation**: NAT-closure (NatArithmeticClosureAndIdentity, ASN-0034) — supplies `1 ∈ ℕ`
**ASN**: V-sub (SubspaceProjection), Formal Contract: *"The text-subspace specialization is `V_1(d) = {v ∈ dom(Σ.M(d)) : subspace(v) = 1}`"*
**Issue**: V-sub's formal contract writes the constant `1` as a specific natural-number value — the text-subspace identifier `S = 1`. The constant `1 ∈ ℕ` is supplied by NAT-closure's axiom clause. V-sub's Depends lists only Σ.M(d) and subspace; NAT-closure is absent. The same principle applied consistently in this ASN — S8-fin cites NAT-closure for the `1` in `{j ∈ ℕ : 1 ≤ j ≤ n}`, T0 cites NAT-closure for the `1` in `1 ≤ #a` — applies here. The transitive route V-sub → subspace → T0 → NAT-closure does not substitute for direct citation when the constant appears in V-sub's own formal statement.
**What needs resolving**: Add NAT-closure (NatArithmeticClosureAndIdentity, ASN-0034) to V-sub's Depends, citing it for `1 ∈ ℕ` — the constant written directly as the text-subspace identifier `S = 1` in the formal contract.

---

### D-MIN missing T0 and NAT-closure for the all-ones tuple
**Class**: REVISE
**Foundation**: T0 (CarrierSetDefinition, ASN-0034); NAT-closure (NatArithmeticClosureAndIdentity, ASN-0034)
**ASN**: D-MIN (VMinimumPosition), Design Requirement: *"min(V_1(d)) = [1, 1, ..., 1] — the length-m tuple ... with every component 1"*
**Issue**: The tuple `[1, 1, ..., 1]` is a specific element of T. Its existence as a tumbler requires T0's comprehension axiom (take `p = m`, `r(i) = 1` for all `i`); its component value requires `1 ∈ ℕ` from NAT-closure. Neither T0 nor NAT-closure appears in D-MIN's Depends. The transitive routes D-MIN → S8-depth → T0 and D-MIN → T1 → NAT-closure are not substitutes for direct citation when symbols appear in D-MIN's own formal statement — the same principle that leads S8-fin to independently cite T0 (for the carrier `T ⊇ dom(Σ.M(d))`) and NAT-closure (for `1` in the index-domain bounds).
**What needs resolving**: Add T0 (CarrierSetDefinition, ASN-0034) and NAT-closure (NatArithmeticClosureAndIdentity, ASN-0034) to D-MIN's Depends. T0 grounds the carrier T that `[1,...,1]` inhabits (via comprehension at `p = m`, `r ≡ 1`); NAT-closure grounds the constant `1 ∈ ℕ` that is the common component value.

---

### D-MIN independence argument overstates "only position between"
**Class**: OBSERVE
**Foundation**: T1 (LexicographicOrder, ASN-0034) — strict total order on all of T, not depth-restricted
**ASN**: D-MIN (VMinimumPosition), non-derivability body: *"the only position strictly between its extremes [1, 5] and [1, 7] is [1, 6], which is present"*
**Issue**: In T1's strict total order on all of T, the claim is false: depth-3 tumblers such as [1, 5, 1] satisfy [1, 5] < [1, 5, 1] < [1, 6], and so lie strictly between [1, 5] and [1, 7]. The sentence is correct only among depth-2 positions with subspace 1 — i.e., within V_1(d) as constrained by S8-depth. The argument's logical intent is sound (D-CTG quantifies within V_1(d), so the witness satisfies it), but the phrase "only position" should be qualified to "only element of V_1(d)" or "only depth-m position in the text subspace."
**What needs resolving**: Qualify the phrase to restrict "position strictly between" to positions within V_1(d) (or equivalently, depth-m positions in the text subspace), matching how D-CTG's quantifier is scoped.

VERDICT: REVISE