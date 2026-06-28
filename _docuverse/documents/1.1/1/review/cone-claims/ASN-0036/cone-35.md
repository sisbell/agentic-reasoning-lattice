Reading the full ASN, tracing the dependency chain, and checking between-claim consistency.

The dependency graph is sound: S0 (axiom) → S1 (one-step derivation); {AX-1, AX-2, S0, S1} → S3 (induction); {S0–S3, T3} → S5 (consistency witnesses). No circular dependencies. T3 from ASN-0034 is correctly cited.

S1's proof is clean: applies S0 pointwise to conclude subset inclusion. S3's induction is well-structured — the case split (inherited / new-or-redirected) is exhaustive (A∧B versus ¬(A∧B) = ¬A∨¬B), the inherited case is discharged by S1, and the new-or-redirected case exactly matches AX-2's antecedent. S5's explicit constructions are correct: T3 is applied only to show distinctness from distinct last components, S2 is verified per construction, and S3 holds directly (a ∈ dom(C) in both witnesses).

Three observations follow.

---

### S5 informal text asserts finite sharing multiplicity per state without grounding
**Class**: OBSERVE
**Foundation**: None directly; concerns the informal text of S5 before its formal proof
**ASN**: S5 (UnrestrictedSharing) — "In any particular state, the sharing multiplicity of each address is a definite finite number — possibly zero for orphaned content — but no invariant imposes a uniform bound that holds across all states."
**Issue**: "Definite finite number" is a mathematical claim requiring that the set `{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}` is finite in every state Σ satisfying S0–S3. S0–S3 place no finiteness constraint on domain sizes; an infinite-domain model is not excluded. The formal postcondition of S5 (no uniform bound across models) is established, but the per-state finiteness claim is not derived from S0–S3. A downstream reader may use this sentence as grounds for finiteness reasoning that S0–S3 do not support.
**What needs resolving**: Either ground the finite-multiplicity-per-state assertion in an explicit finiteness axiom on state domains, or soften the phrasing to "a specific (possibly infinite) count" to match what S0–S3 actually entail. If finite-domain states are all that the protocol intends, name that assumption.

---

### S5 consistency result is scoped to S0–S3 alone; AX-1 is not satisfied by the witnesses
**Class**: OBSERVE
**Foundation**: AX-1 (InitialEmpty) — `(A d :: dom(Σ₀.M(d)) = ∅)` on the designated initial state
**ASN**: S5 (UnrestrictedSharing), proof — "we take it as the initial state of the trivial transition system whose transition relation is empty"; both cross-document and within-document witnesses have `M(d_i) = {v ↦ a}` or `M(d) = {v_k ↦ a}`, with non-empty arrangement domains
**Issue**: AX-1 is not a transition-level invariant; it constrains the designated initial state. The S5 witnesses have non-empty M domains in their initial states, so they do not model AX-1. The formal postcondition accurately scopes the result to "initial state of a model of S0–S3" (not of {AX-1, AX-2, S0–S3}), so the formal claim is correct as stated. However, the Nelson and Gregory citations in S5's framing suggest the intended claim is full-protocol applicability — that the system under all axioms permits unbounded sharing. This stronger claim (reachable from Σ₀ via finitely many transitions satisfying AX-2) is not proved; S5 sidesteps AX-1 rather than threading through it.
**What needs resolving**: If the intended claim is full-protocol consistency with unbounded sharing, either provide AX-1-satisfying witnesses (e.g., states reachable from Σ₀ by N+1 transitions adding one mapping each), or add a brief note explaining that AX-1 and AX-2 impose no additional multiplicity bound beyond what S0–S3 already permit, so the S0–S3 consistency result extends to the full axiom set.

---

### Axiom formal contracts explain why the axiom is needed rather than what it says
**Class**: OBSERVE
**Foundation**: S0 (ContentImmutability), AX-1 (InitialEmpty)
**ASN**: S0 formal contract — "it is accepted within this ASN without proof, it supplies the precondition S1 invokes, and it grounds the dependence of S3 and S5. It holds by the design of the content stream, not by derivation from other claims." AX-1 formal contract — "The point of naming it is methodological: an invariant on M proved by induction on transitions needs an explicit, citable anchor for its base case, and the empty base state is that anchor."
**Issue**: The review instructions name this pattern: new prose around an axiom that explains why the axiom is needed rather than what it says is reviser drift, and it compounds across cycles. Both passages are accurate descriptions of the axiom's role in downstream proofs, but role-description belongs in commentary prose, not in the formal-contract slot, which should state the axiom's content and scope. Readers scanning formal contracts for the assertion itself must work past the explanatory meta-prose to find it.
**What needs resolving**: Move the "why it is needed" sentences (role in proof chain, methodological rationale) out of the formal contract body and into the claim's prefatory prose or a trailing remark. The formal contract slot should contain: the assertion, its scope (every transition / designated start state), and its status (axiom / posit). Nothing about which other claims invoke it.

---

VERDICT: OBSERVE