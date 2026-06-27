Reading the ASN as a system, tracing cross-claim dependencies in D-CTG-depth's two-part proof.

**Contradiction setup (first postcondition).** The set `{i : 2 ≤ i ≤ m − 1 ∧ uᵢ ≠ xᵢ}` starts from 2, so j ≥ 2 is built into the definition. NAT-wellorder extracts the minimum correctly. The infinite-witness construction, S8a verification on w, D-CTG application, and S8-fin contradiction all check out.

**Reduction step (second postcondition).** The set from NAT-wellorder changes to `{i : 1 ≤ i ≤ m − 1 ∧ vᵢ ≠ uᵢ}`, starting from 1. This is where the proof needs scrutiny.

---

### D-CTG-depth reduction step: j ≥ 2 not established before invoking the contradiction chain
**Class**: REVISE
**Foundation**: subspace (VPositionSubspaceIdentifier); V-sub (SubspaceProjection)
**ASN**: D-CTG-depth body, reduction paragraph: *"Let j be that least component, 1 ≤ j ≤ m − 1; then … The hypothesis u < v therefore yields uⱼ < vⱼ. Now u and x agree across components 1 through m − 1, so xⱼ = uⱼ and hence xⱼ < vⱼ; … T1(i) … witnesses x < v. But the guard supplies v < x, and T1's trichotomy forbids x < v and v < x at once."*
**Issue**: The contradiction chain requires "uⱼ < vⱼ" at the first differing component j. For j = 1, the chain would yield "u₁ < v₁" via T1(i) from u < v — but v₁ = subspace(v) = 1 (D-CTG's `subspace(v) = 1` guard) and u₁ = 1 (u ∈ V_1(d), so subspace(u) = 1). The supposed "uⱼ < vⱼ" at j = 1 reduces to "1 < 1", which is false. The stated chain (T1 → uⱼ < vⱼ → xⱼ = uⱼ < vⱼ → x < v → contradiction with v < x) therefore does not hold for j = 1. The proof never establishes that 1 ∉ `{i : 1 ≤ i ≤ m − 1 ∧ vᵢ ≠ uᵢ}` — which follows immediately from v₁ = u₁ = 1 — so j ≥ 2 is tacit but unstated. A formal verifier working from the stated bound "1 ≤ j ≤ m − 1" must supply this exclusion independently.
**What needs resolving**: Before NAT-wellorder is applied to extract j, the proof should note: since subspace(v) = v₁ = 1 (from the D-CTG guard's subspace(v) = 1) and u₁ = 1 (from u ∈ V_1(d)), component 1 satisfies v₁ = u₁ and therefore 1 ∉ `{i : 1 ≤ i ≤ m − 1 ∧ vᵢ ≠ uᵢ}`. The set is a subset of {2, …, m − 1}, and the minimum j satisfies j ≥ 2. This makes the bound explicit and the stated contradiction chain valid at every j the proof considers.

---

### OrdShiftHom preconditions omit v ∈ T and n ∈ ℕ
**Class**: OBSERVE
**Foundation**: TumblerAdd (TumblerAdd); OrdinalShift (OrdinalShift)
**ASN**: OrdShiftHom formal contract, Preconditions: *"v is a V-position with #v = m ≥ 2; n ≥ 1."*
**Issue**: OrdinalShift (which the proof expands in the first line) carries explicit preconditions `v ∈ T` and `n ∈ ℕ`. TumblerAdd (invoked for the component-wise expansion) similarly requires `a ∈ T`. OrdShiftHom's formal contract states neither. In the ASN's context, "V-position" consistently means an element of dom(M(d)) ⊆ T (by S8a), and n ≥ 1 with ℕ context implies n ∈ ℕ, so the gap does not cause a soundness problem here — but the precondition block is not self-contained: a caller following the formal contract literally cannot confirm v ∈ T without consulting S8a separately.
**What needs resolving**: Add `v ∈ T` (or equivalently, note that "V-position" denotes an element of dom(M(d)), which S8a places in T) and `n ∈ ℕ` to OrdShiftHom's stated preconditions so the contract matches what OrdinalShift and TumblerAdd require at their call sites.

---

VERDICT: REVISE