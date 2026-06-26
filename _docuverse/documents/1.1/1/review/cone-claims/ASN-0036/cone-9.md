Reading the foundation statements first, then tracing the proof steps of each ASN claim against them.

**S7b** is a clean axiom: it supplies only `zeros(a) = 3` and correctly defers T4-validity to downstream (S7 via S7a → T10a.4). The two-conjunct reading of T4b is accurate.

**S7a** is an axiomatic design invariant positing `A_element ∈ 𝒯` and `a ∈ dom(A_element)` for every `a ∈ dom(Σ.C)`. T4-validity of `a` follows from these memberships via T10a.4 (a postcondition of T10a, which S7a depends on). The depend chain is sound.

**S7d** is an axiom grounding documents in T10a allocation events and asserting event-distinctness for distinct documents. It does not depend on GlobalUniqueness, so there is no circularity: S7d works at the event level, GlobalUniqueness at the address-output level.

**S7 Well-definedness**: The chain `a ∈ dom(Σ.C)` → S7a → `A_element ∈ 𝒯`, `a ∈ dom(A_element)` → T10a.4 → T4-validity of `a` is correctly assembled. T4b then gives all four projections defined with ℕ⁺ components. The construction of `origin(a)` via T0's comprehension at length `p = #N(a)+1+#U(a)+1+#D(a) ≥ 5` is correct. The zero-count computation: r is defined piecewise over three field ranges and two separator positions, which partition `{1,…,p}` with total count `#N(a)+1+#U(a)+1+#D(a) = p` — arithmetically sound. The two separator positions at `#N(a)+1` and `#N(a)+#U(a)+2` differ by `#U(a)+1 ≥ 2 > 0` (from T4b's nonempty U field). NAT-card at `n = p` gives cardinality 2. `zeros(origin(a)) = 2` is correctly established.

**S7 Identification**: S7a posits that `N(a).0.U(a).0.D(a)` identifies the allocating document; S7 reads this as `origin(a)` being that document's tumbler. In this system documents are addressed by their tumblers (S7d), so the reading is correct.

**S7 Uniqueness**: S7d gives distinct documents → distinct T10a allocation events, each producing a document-level tumbler. GlobalUniqueness gives distinct T10a events → distinct address outputs. Chain is valid. GlobalUniqueness's precondition ("within a system conforming to T10a, events of type root-initialization or inc(t,k)") is met: S7d says document tumblers arise from T10a-disciplined events, all of which are root-initialization or inc calls.

**S7 Permanence**: S0 gives address persistence; `origin(a)` is a pure function of `a`'s components, which are fixed once `a` is a tumbler. Sound.

Two observations follow.

---

### S7 postcondition invokes T4 hierarchy for origin(a) without establishing T4-validity
**Class**: OBSERVE
**Foundation**: T4 (HierarchicalParsing) — T4's four-level hierarchy is defined for T4-valid tumblers: `zeros(t) ≤ 3` plus no adjacent zeros plus nonzero first and last components.
**ASN**: S7, Postconditions — "zeros(origin(a)) = 2 obtained by applying T4's zero-count definition… placing origin(a) at the document level in T4's hierarchy"
**Issue**: The proof explicitly establishes `origin(a) ∈ T` and `zeros(origin(a)) = 2`. The phrase "at the document level in T4's hierarchy" imports T4's four-level structure, which applies formally only to T4-valid tumblers. The remaining T4-validity conditions — no adjacent zeros and nonzero endpoints — are satisfied by the construction (separator positions differ by `#U(a)+1 ≥ 2`, endpoints carry ℕ⁺ components from T4b) but are never assembled into an explicit T4-validity assertion. The proof stops at zeros = 2 without naming the result T4-valid. A mechanical verifier following the postcondition would need this discharge made explicit.
**What needs resolving**: After establishing `zeros(origin(a)) = 2`, the proof or postcondition should collect the three remaining T4-validity conditions — (i) no adjacent zeros (separator positions differ by `#U(a)+1 ≥ 2 > 1`), (ii) first component nonzero (position 1 carries a component of N(a) ∈ ℕ⁺), (iii) last component nonzero (position p carries a component of D(a) ∈ ℕ⁺) — and state explicitly that `origin(a)` is T4-valid, which is what "at the document level in T4's hierarchy" formally requires.

---

### T3 citation in S7 Uniqueness is logically redundant
**Class**: OBSERVE
**Foundation**: T3 (CanonicalRepresentation) — biconditional `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`; GlobalUniqueness — invariant `a ≠ b` for addresses from distinct T10a allocation events.
**ASN**: S7, Uniqueness step — "By T3 (CanonicalRepresentation, ASN-0034), this distinctness is decidable by component-wise comparison."
**Issue**: GlobalUniqueness's invariant directly yields `origin(a₁) ≠ origin(a₂)` once event-distinctness (S7d) and the identification of origins with document tumblers (Identification step) are in hand. T3 would contribute if the argument needed to exhibit a *witness position* where `origin(a₁)` and `origin(a₂)` disagree — but S7's Uniqueness step asserts only the bare inequality, not a witness. T3's biconditional adds no logical step to the conclusion as written. The citation suggests T3 is doing work it is not, and a reader checking the proof may spend time tracing a dependency that contributes nothing.
**What needs resolving**: Remove the T3 citation from the Uniqueness step, or — if the intent is to ground the characterization of how the distinct tumblers are distinguished — state explicitly what T3 contributes beyond what GlobalUniqueness already supplies (e.g., that component-wise comparison is the decision procedure, with T3 licensing that move). As written, the citation misleads the reader about the structure of the argument.

---

VERDICT: OBSERVE