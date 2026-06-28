Reading through the full ASN as a system, tracing precondition chains across claim boundaries and checking every operator against its grounding claim.

**Dependency audit summary.** The core chain — OrdShiftHom → S8 → partition — is well-constructed. OrdShiftHom correctly grounds depth-preservation in OrdinalShift's frame rather than S8-depth (the previously declined finding), and S8's induction handles the k = 0 convention separately from TS3's n₁ ≥ 1 precondition. Injectivity, acyclicity, and orbit uniqueness are all sound. S3's two-case exhaustion is correct and AX-2 covers exactly the complement of the inherited case. One REVISE-level dependency omission found; one OBSERVE.

---

### S8-fin Depends omits NAT-order and NAT-closure

**Class**: REVISE
**Foundation**: NAT-order (NatStrictTotalOrder); NAT-closure (NatArithmeticClosureAndIdentity)
**ASN**: S8-fin (FiniteArrangement), Formal Contract Depends — "T0 (CarrierSetDefinition, ASN-0034) — supplies the tumbler carrier T ⊇ dom(Σ.M(d)) that types the bijection's codomain, and the typed initial-segment construction {j ∈ ℕ : 1 ≤ j ≤ n} (T0's own index-domain device) used as the bijection's domain"
**Issue**: S8-fin's axiom directly writes `1 ≤ j ≤ n`, `1 ≤ i < j ≤ n`, and `1 ≤ j ≤ n` in the injectivity and surjectivity clauses — consuming `1 ∈ ℕ` (NAT-closure) and `≤`, `<` on ℕ (NAT-order) as first-class operators. The Depends list cites T0 as the source of the "typed initial-segment construction," but T0 does not export that construction as a postcondition — T0 uses `{j ∈ ℕ : 1 ≤ j ≤ p}` internally and grounds it through T0's own Depends on NAT-closure and NAT-order. A formalization tool checking S8-fin's Depends for where `1` and `≤` are grounded will not find them: T0's postconditions cover the carrier T, the length operator, component projection, comprehension, and extensionality — not the initial-segment set-builder. Compare S8a, which cites NAT-order when `≤` appears independently in T4's predicate even though T4 also uses it internally. The same obligation applies here.
**What needs resolving**: Add NAT-order (supplying `≤` and `<` in the set-comprehension bounds and injectivity clause) and NAT-closure (supplying `1 ∈ ℕ` as the lower bound in `{j ∈ ℕ : 1 ≤ j ≤ n}`) to S8-fin's Depends. Revise the T0 citation to reflect only what T0 genuinely exports: the tumbler carrier T typing the bijection's codomain — not the initial-segment construction, which is independently grounded by NAT-carrier + NAT-closure + NAT-order.

---

### S8 Formal Contract preconditions: "fixed depth m" is ambiguous

**Class**: OBSERVE
**Foundation**: S8-depth (FixedDepthVPositions)
**ASN**: S8 (CorrespondenceRunPartition), Formal Contract Preconditions — "Every v ∈ dom(M(d)) is a well-formed V-position at a fixed depth m (S8a, S8-depth)"
**Issue**: The phrase "at a fixed depth m" reads naturally as a single global m shared by all positions in dom(M(d)). S8-depth supplies only the weaker subspace-local claim — all positions in the *same subspace* share a depth — and dom(M(d)) may contain positions from multiple subspaces at different depths. The proof body correctly introduces m per-chain ("write m = #v"), and the S8-depth Depends footnote explicitly clarifies that S8-depth does not license per-step depth equality. But the precondition summary, read in isolation by a downstream consumer who does not consult the footnote, asserts something stronger than what S8-depth provides.
**What needs resolving**: Qualify the precondition to make the per-subspace scope explicit — for example: "every v ∈ dom(M(d)) is a well-formed V-position (S8a), and within each subspace all active positions share a common depth m (S8-depth)."

---

VERDICT: REVISE