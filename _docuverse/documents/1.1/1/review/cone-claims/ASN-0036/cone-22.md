I read the foundation statements and ASN-0036 content in full, tracing every dependency, precondition chain, and proof step.

**Dependency audit.** S7's Depends block lists all foundations actually consumed: T0 (comprehension for `origin(a) ∈ T`), T4 (zero-count definition and T4-valid predicate), T4a (field non-emptiness), T4b (projections N, U, D, E and ℕ⁺ postcondition), T10a.4 (T4-preservation via S7a), NAT-sub (left-telescoping for separator gap and unit gap), NAT-addassoc (re-association before telescoping fires), NAT-addcompat (strict successor and order-compatibility), NAT-order (irreflexivity, trichotomy, transitivity, ≤-definition), NAT-discrete (i < p ⟹ i+1 ≤ p for the comprehension equality at i+1), NAT-card (two-element set cardinality = 2), NAT-closure (1 ∈ ℕ, sums in ℕ), NAT-zero (0 ∈ ℕ for separators). NAT-addbound is not listed, but NAT-sub's telescoping axioms are stated unconditionally in NAT-sub's own contract with NAT-addbound internal — no gap.

**Well-definedness of origin(a).** T4-validity of `a` obtained via S7a + T10a.4 (two memberships `A_element ∈ 𝒯` and `a ∈ dom(A_element)` both supplied by S7a). `zeros(a) = 3` from S7b. T4b projections N(a), U(a), D(a), E(a) all defined. The concatenation length `p = (((#N(a)+1)+#U(a))+1)+#D(a)` is fixed left-associatively; T0 comprehension invoked at this `p ≥ 1` (from T4a's `#N(a) ≥ 1` lifted by NAT-addcompat) and the explicit component map `r` (field components in ℕ⁺ by T4b; separators `0 ∈ ℕ` by NAT-zero). Uniqueness of the resulting tumbler by T0 extensionality.

**zeros(origin(a)) = 2.** Zero-index set `{#N(a)+1, ((#N(a)+1)+#U(a))+1}` established by inspecting `r` position by position (all field positions carry ℕ⁺ values, exactly two separator positions carry 0). Strict separation `#N(a)+1 < ((#N(a)+1)+#U(a))+1` proved via NAT-addassoc re-association then NAT-addcompat strict successor and left order-compatibility chained through NAT-order's ≤-definition and transitivity. NAT-card's enumeration characterization applied: two elements in strictly increasing order enumerate the set, so `|{...}| = 2`, giving `zeros(origin(a)) = 2`.

**T4-validity of origin(a) — four conjuncts.**
1. `zeros ≤ 3`: `2 ≤ 3` trivially from NAT-addcompat. ✓
2. No adjacent zeros: Four-case walk over `{#N(a)+1, X}² ` — cases (i=j, i=j) close by irreflexivity of `<` via NAT-addcompat's strict successor; the order-reversed case closes by exactly-one trichotomy; the surviving case `i = #N(a)+1, i+1 = X` leads via NAT-addassoc re-association + NAT-sub left-telescoping (twice) + single-valuedness of subtraction to `1 = #U(a)+1`, which contradicts `#U(a)+1 ≥ 2` (T4a's `#U(a) ≥ 1` lifted by NAT-addcompat) against `1 < 2` (NAT-addcompat strict successor), with `2 ≤ 1` unfolded by NAT-order's ≤-definition dispatching `2 < 1` and `2 = 1` sub-cases both closing to `1 < 1` against irreflexivity. ✓
3. First component `≠ 0`: position 1 in node field since `#N(a) ≥ 1`; `r(1) = N(a)₁ ∈ ℕ⁺` by T4b. ✓
4. Last component `≠ 0`: position `p` in document field since `#D(a) ≥ 1`; `r(p) = D(a)_{#D(a)} ∈ ℕ⁺` by T4b. ✓

**Identification.** S7a is an axiom grounding that `origin(a)` IS the allocating document's tumbler; the proof's identification step applies S7a directly. ✓

**Uniqueness.** S7d separates documents at the level of allocation events; GlobalUniqueness lifts event-distinctness to address-distinctness; S7a bridges address-distinctness to origin-distinctness. Precondition of GlobalUniqueness (T10a-conforming system, addresses from allocation events of the correct type) met by S7d + S7a. Decidability by T3. ✓

**Permanence.** S0 gives domain persistence; tumblers are extensional objects whose components are fixed by T0's definition; `origin(a)` depends only on `a`'s components, hence is state-independent. ✓

VERDICT: CONVERGED