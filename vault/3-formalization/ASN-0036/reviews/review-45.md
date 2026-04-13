# Cross-cutting Review — ASN-0036 (cycle 1)

*2026-04-12 17:51*

I've read the full ASN-0036 and its foundation statements carefully, tracing every definition, precondition chain, and citation across properties.

---

### D-MIN justification mis-attributes component positivity; formal preconditions omit S8a

**Foundation**: T0(a) (UnboundedComponentValues) — "Every component value of a tumbler is unbounded — no maximum value exists." S8a (V-position well-formedness) — `zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0`.

**ASN**: D-MIN (VMinimumPosition), justification text: "Tumbler components are positive natural numbers (T0(a)), so 1 is the smallest value any component can take."

**Issue**: T0(a) says component values are *unbounded* — it establishes no maximum exists. It does not say components are positive; T0 defines T as sequences over ℕ, which includes 0. The claim that "1 is the smallest value any component can take" is true only for V-positions, where S8a (via T4's positive-component constraint on element fields) guarantees every component is strictly positive. The citation "(T0(a))" is wrong; the supporting property is S8a. Moreover, D-MIN's formal contract lists only S8-depth as a precondition, omitting S8a entirely — yet the argument that `[S, 1, …, 1]` is the least element of V_S(d) under T1 requires that every V-position component is ≥ 1 (otherwise `[S, 0, …]` would be smaller). This gap propagates to D-SEQ Step 2, which says "D-MIN gives the minimum k = 1" — a step that depends on the minimum element having all-1 components, which depends on S8a constraining the domain.

**What needs resolving**: D-MIN's justification must cite S8a (not T0(a)) for the positivity of V-position components. D-MIN's formal preconditions must include S8a, since the claim that `[S, 1, …, 1]` is the least element of V_S(d) under T1 fails without it.

---

### D-SEQ attributes m ≥ 2 lower bound to S8-depth, which provides only uniformity

**Foundation**: S8-depth (Fixed-depth V-positions) — `(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`. S8-vdepth (MinimalVPositionDepth) — `(A d, v : v ∈ dom(Σ.M(d)) : #v ≥ 2)`.

**ASN**: D-SEQ (SequentialPositions), formal contract: "Preconditions: V_S(d) non-empty; common V-position depth m ≥ 2 (S8-depth)."

**Issue**: The parenthetical "(S8-depth)" is cited as the source of "m ≥ 2", but S8-depth establishes only that all V-positions in a subspace share a *common* depth — it says nothing about what that depth is. The lower bound m ≥ 2 requires S8-vdepth, which is a separate axiom not cited anywhere in D-SEQ's formal contract or proof. D-SEQ's own text acknowledges the precondition is necessary ("at m = 1 the tuple `[S, 1, …, 1, k]` collapses to a single component") and attributes it to ValidInsertionPosition's empty-subspace case — but ValidInsertionPosition is a definition (of valid positions), not an axiom. The axiomatic guarantee is S8-vdepth. The same misattribution appears in ValidInsertionPosition itself: "m ≥ 2 (inherited from the empty-case establishment and S8-depth)." Since D-SEQ is the cornerstone result characterizing V_S(d)'s structure, and its postcondition is used by D-MIN's derivation and ValidInsertionPosition's postconditions, the missing citation creates an ungrounded precondition in a load-bearing chain.

**What needs resolving**: D-SEQ's formal preconditions must cite S8-vdepth for the m ≥ 2 lower bound, distinguishing it from S8-depth's uniformity guarantee. ValidInsertionPosition's non-empty case should similarly ground m ≥ 2 in S8-vdepth rather than in its own empty-case design.

---

### V_S(d) used in six properties without formal definition

**Foundation**: T0 (CarrierSetDefinition), Σ.M(d) (Arrangement), S8a (V-position well-formedness).

**ASN**: D-CTG axiom quantifies over V_S(d); D-CTG-depth derives properties of V_S(d); D-MIN axiom specifies min(V_S(d)); D-SEQ characterizes V_S(d) completely; ValidInsertionPosition partitions cases on V_S(d) = ∅ vs non-empty; S8-depth constrains V_S(d) implicitly. Additionally, `subspace(v) = v₁` is used as a function in D-CTG-depth proofs, OrdAddHom postcondition (b), and S8a's proof, but has no formal definition block alongside `ord(v)` and `vpos(S, o)`.

**Issue**: The set V_S(d) — intended as {v ∈ dom(Σ.M(d)) : v₁ = S} — appears in axioms, theorems, and definitions throughout the ASN but has no Formal Contract establishing its definition, domain, or relationship to dom(Σ.M(d)). D-CTG's axiom universally quantifies over elements of V_S(d) and forces membership in V_S(d); D-MIN specifies its minimum; D-SEQ characterizes its exact form. Without an explicit definition, there is no single point where a formalizer can verify that all uses agree — for instance, whether V_S(d) includes only V-positions satisfying S8a (as the derivations assume) or all tumblers in dom(M(d)) with first component S (which is the same thing given S8a, but only provably so). The function `subspace(v)` is in the same position: used as a formal construct without a definition block.

**What needs resolving**: V_S(d) needs a formal definition establishing it as {v ∈ dom(Σ.M(d)) : v₁ = S}, with its relationship to S8a made explicit. `subspace(v) = v₁` needs a Formal Contract parallel to `ord(v)` and `vpos(S, o)`.
