Reading the full proof of S7 and the supporting claims S7a, S7b, S7d, S0, and Σ.C against the foundation stack.

**S7b.** The axiom supplies only the zero-count conjunct; T4-validity is correctly deferred to S7a → T10a.4 downstream. The two-conjunct reading is well-described.

**S7d.** The injectivity of `ev` follows cleanly from T10a's at-most-once constraint: if `ev(d₁) = ev(d₂) = (P, t, k')`, both documents' nodes are the unique child T10a admits for `(t, k')` under parent `P`, collapsing to one node and hence one document by the identification posit. The at-most-once clause is consumed correctly.

**S7a.** The quantifier binding is correctly stated and the reversed-nesting warning is on point. The Depends thread (Σ.C → T10a → T10a.4, S7b) makes the projections in the axiom statement well-formed.

**S7 — Well-definedness.** The argument is complete:
- T4-validity of `a` via S7a + T10a.4. ✓
- `zeros(a) = 3 ≥ 2` from S7b, placing `a ∈ dom(U), dom(D)`. ✓
- Concatenation length `p = (((#N(a)+1)+#U(a))+1)+#D(a) ≥ 2 ≥ 1` established by climbing the left-associated sum with NAT-addcompat's left order-compatibility + NAT-closure's right identity + NAT-order's `≤`-transitivity, without invoking commutativity. ✓
- T0 comprehension applied to the explicit five-block map `r`. ✓
- `zeros(origin(a)) = 2` by NAT-card applied at `n := X` (sparing the `X ≤ p` obligation), with lower bounds via NAT-closure's successor-positivity + NAT-discrete + NAT-closure's left identity, and upper bounds from the strict separation (weakened) and reflexivity. ✓
- Separator separation `#N(a)+1 < X`: NAT-addassoc re-association to leading-summand form, then NAT-addcompat strict successor + left order-compatibility chained by NAT-order. ✓
- No-adjacent-zeros: four-case analysis is exhaustive. Cases 1–2 close by irreflexivity against `i < i+1`; case 3 closes by exactly-one trichotomy. Case 4 (surviving): the two subtraction computations of `(i+1)−i` are equated by single-valuedness, forcing `1 = #U(a)+1 ≥ 2`, i.e. `2 ≤ 1`; unfolded against `1 < 2` (NAT-addcompat's successor at `n=1`) into sub-cases `2<1` (transitivity → `1<1`) and `2=1` (substitution into `1<2` → `1<1`), both contradicted by irreflexivity at `1`. ✓
- Boundary components non-zero from T4b's `ℕ⁺` postcondition at positions 1 and `p`. ✓

**S7 — Identification.** Invokes S7a directly. ✓

**S7 — Uniqueness.** S7d supplies event-level separation (distinct documents → distinct spawning triples, by at-most-once); GlobalUniqueness lifts event-distinctness to address-distinctness; Identification bridges `origin(aᵢ) = base of dᵢ`'s node = address produced by `ev(dᵢ)`. Chain complete. ✓

**S7 — Permanence.** S0 persists `a ∈ dom(Σ'.C)`; `origin` is a pure function of `a`'s components (fixed); argument is sound. ✓

**Dependency coverage.** All twenty Depends entries of S7 are consumed; no Depends entry is cited without use; no axiom is invoked without being in the Depends list.

---

### Imprecise "truncating" gloss in S7 Definition
**Class**: OBSERVE
**Foundation**: T4 (HierarchicalParsing) — field vs. separator terminology
**ASN**: S7 (StructuralAttribution), Definition — "the document-level tumbler obtained by truncating the element field `E(a)` from `a`"
**Issue**: In T4's formal terminology a *field* (field segment) is the maximal contiguous sub-sequence of field-*component* positions, which excludes the separating zero. Literally "truncating the element field `E(a)` from `a`" removes only the `E`-component positions, leaving the third separator in place and producing [N][0][U][0][D][0] with `zeros = 3` — not `origin(a) = N(a).0.U(a).0.D(a)` with `zeros = 2`. The formal definition (`origin(a) = N(a).0.U(a).0.D(a)`) and the concatenation elaboration that immediately follows ("formed by concatenating the node field, a zero separator, the user field, a zero separator, and the document field") are unambiguous; the "truncating" phrase is the imprecise piece.
**What needs resolving**: Replace "truncating the element field `E(a)` from `a`" with "truncating the element separator and element field from `a`" (equivalently: "truncating the element-level suffix — the third zero separator together with `E(a)` — from `a`") so the gloss agrees with both the formal definition and the `zeros = 2` result established in the proof. Purely phrasing; the formal definition and proof are unaffected.

VERDICT: OBSERVE