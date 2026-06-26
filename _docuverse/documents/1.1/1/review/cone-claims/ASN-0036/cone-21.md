Reading the ASN as a system against the foundation statements.

**Structure of the ASN.** Five claims plus a defined function: Σ.C defines the content store, S0 axioms immutability, S7b axioms the zero-count for I-addresses, S7d axioms document allocation discipline, S7a axioms the document-scoped prefix relation, and S7 derives the `origin` function with a detailed proof. The dependency order is Σ.C → {S0, S7b, S7a, S7d} → S7. All cross-ASN foundations (T0, T4, T4a, T4b, T10a, T10a.4, GlobalUniqueness, NAT-*) are from ASN-0034.

**S7's proof chain.** The proof is systematic and explicit: S7a supplies `A_element ∈ 𝒯` and `a ∈ dom(A_element)`; T10a.4 fires at that pair to give T4-validity; S7b supplies `zeros(a) = 3`; T4b then gives all four projections over ℕ⁺. T0's comprehension places `origin(a) ∈ T`. The zero-count argument is sound (NAT-addassoc brings the second separator into leading-summand form before NAT-sub's left-telescoping fires; NAT-addcompat's strict successor and left order-compatibility chain to separate the two zero positions). The no-two-adjacent-zeros four-case walk closes correctly: the two equal-assignment cases by irreflexivity against `i < i+1`; the reversed-order case by exactly-one trichotomy `¬(i < i+1 ∧ i+1 < i)`; the surviving case by equating the gap two ways and reaching `1 = #U(a)+1 ≥ 2`, then closing `2 ≤ 1 ∧ 1 < 2` through the `≤`-definition case split to `1 < 1` against irreflexivity. The boundary-component arguments are clean. The Uniqueness and Permanence steps are well-grounded. The proof is sound.

One formal contract gap and three phrasing observations follow.

---

### S7 Depends section omits Σ.C
**Class**: REVISE
**Foundation**: Σ.C (ContentStore) — co-resident claim in this ASN
**ASN**: S7 (StructuralAttribution) — *Depends:* section; also the *Definition*, *Preconditions*, and *Frame* fields of S7's Formal Contract
**Issue**: S7's formal contract directly references `dom(Σ.C)` in its own definition (`origin: dom(Σ.C) → T`), its preconditions (`a ∈ dom(Σ.C)`), and its frame ("it reads no state beyond `dom(Σ.C)` membership"). Σ.C is the source of that symbol. Every other claim in this ASN that names `dom(Σ.C)` in its own statement — S7a, S7b, S7d, S0 — lists Σ.C in its Depends; S7 is the only claim that uses it directly and omits the citation. Σ.C is reachable transitively through S7a and S7b, but the direct reference in S7's own formal contract makes the direct citation necessary for the dependency specification to be self-contained.
**What needs resolving**: Add Σ.C (ContentStore) to S7's Depends section with an annotation explaining its role as the source of `dom(Σ.C)` that S7's definition, preconditions, and frame range over.

---

### S7a Depends section omits S7b
**Class**: OBSERVE
**Foundation**: T4b (UniqueParse) — `dom(D) = {t ∈ dom(N) : zeros(t) ≥ 2}`; S7b (ElementLevelIAddresses) — `zeros(a) = 3` for all `a ∈ dom(Σ.C)`
**ASN**: S7a (DocumentScopedAllocation) — *Depends:* section; body uses `D(a)` from T4b
**Issue**: S7a's body uses the projection `D(a)`, whose T4b domain condition is `zeros(a) ≥ 2`. T10a (cited in S7a) establishes T4-validity, which bounds `zeros ≤ 3` but gives no lower bound. As an axiom, S7a implicitly posits the element-level structure (including D(a) being defined), so there is no soundness defect — but the Depends section provides no annotation pointing to S7b as the source of the zero-count grounding. A reader cross-checking S7a's projection usage against T4b's domain conditions finds no pointer to where `zeros ≥ 2` is established.
**What needs resolving**: Add S7b (ElementLevelIAddresses) to S7a's Depends with a note that S7a's use of D(a) presupposes `zeros(a) ≥ 2`, which S7b provides as `zeros(a) = 3`.

---

### "Subtraction being single-valued" names the wrong warrant
**Class**: OBSERVE
**Foundation**: NAT-sub (NatPartialSubtraction) — left-telescoping `(n + m) − n = m`; NAT-order (NatStrictTotalOrder) — transitivity of `=`
**ASN**: S7 (StructuralAttribution) — Well-definedness, no-two-zeros-adjacent, surviving Case 4: "Both expressions denote the one value `(i + 1) − i`; subtraction being single-valued, its two computed outputs coincide, so `1 = #U(a) + 1`."
**Issue**: The conclusion `1 = #U(a) + 1` follows from: (1) NAT-sub left-telescoping at `n := i, m := 1` gives `(i+1)−i = 1`; (2) under Case 4's substitution `i = #N(a)+1`, `i+1 = (#N(a)+1)+(#U(a)+1)`, the same expression `(i+1)−i` equals `((#N(a)+1)+(#U(a)+1))−(#N(a)+1) = #U(a)+1` by NAT-sub again; (3) transitivity of `=` yields `1 = #U(a)+1`. The warrant doing the work is transitivity of `=` (both conclusions equate the same expression `(i+1)−i` to different values). "Single-valuedness" is a property that applies when the same function is called with identical arguments twice; here the two telescoping instances use different `(n, m)` pairs.
**What needs resolving**: N/A — reasoning is correct; the label on the warrant is imprecise but does not affect soundness.

---

### "One position past" understates the positional bound
**Class**: OBSERVE
**Foundation**: NAT-addcompat (NatAdditionOrderAndSuccessor) — left order-compatibility; T4a (SyntacticEquivalence) — `#D(a) ≥ 1`
**ASN**: S7 (StructuralAttribution) — Well-definedness, Last-component-nonzero: "T4a's non-emptiness of the D field gives `#D(a) ≥ 1`, so `p = (((#N(a) + 1) + #U(a)) + 1) + #D(a) ≥ (((#N(a) + 1) + #U(a)) + 1) + 1`, one position past the second separator"
**Issue**: The bound established is `p ≥ P₂ + 1` (position p is at least one past the second separator), not exactly one past. `#D(a) ≥ 1` gives `p ≥ P₂ + 1`, placing p somewhere in the D-block `[P₂+1, p]`. "One position past" could be read as `p = P₂ + 1` (i.e., `#D(a) = 1` exactly). The mathematical content is correct — `p ≥ P₂ + 1` suffices to conclude `r(p) = D(a)_{#D(a)}` lies in the D block and is strictly positive — but the phrasing is ambiguous.
**What needs resolving**: N/A — pure phrasing observation; the bound `p ≥ P₂ + 1` is correctly derived and sufficient for the argument.

---

VERDICT: REVISE