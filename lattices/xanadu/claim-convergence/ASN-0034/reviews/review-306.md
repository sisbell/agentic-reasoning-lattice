# Cone Review — ASN-0034/TA3 (cycle 7)

*2026-04-18 16:31*

### Case B's B2/B3/B4 sub-case split uses NAT-order trichotomy at a divergence-position pair not enumerated among the four NAT-order roles

**Foundation**: N/A — cross-cutting citation discipline established in TA3's own NAT-order Depends, which enumerates exactly four roles (length-pair trichotomy at `(#a, #w)`, length-pair trichotomy at `(#b, #w)`, result-length trichotomy at `(L_{a,w}, L_{b,w})`, and defining-clause conversion at component pairs).

**ASN**: TA3 Case B's three-way split at the zero-padded divergence positions: "*Sub-case B2: `dₐ = d_b = d`.*", "*Sub-case B3: `dₐ < d_b`.*", "*Sub-case B4: `dₐ > d_b`.*". The introduction names `dₐ = zpd(a, w)` and `d_b = zpd(b, w)` as ℕ-valued divergence indices, then partitions Case B exhaustively into the three orderings `=`, `<`, `>` of the pair `(dₐ, d_b)`.

**Issue**: The B2/B3/B4 partition is an invocation of NAT-order's trichotomy exactly-one clause applied at the ℕ-pair `(dₐ, d_b)` — the same axiom-clause already enumerated at the length-pair and result-length pairs but here at a distinct divergence-position pair. Under this ASN's per-instance convention (declared in T1's Depends, reinforced by TumblerSub's enumeration of five NAT-order sites, and matching TA3's own decision to separately list the `(#a, #w)`, `(#b, #w)`, and `(L_{a,w}, L_{b,w})` trichotomy sites), this use earns a separate site. TA3 collapses the partition into prose without adding it to the Depends enumeration, leaving the exhaustiveness of B2/B3/B4 discharged without axiomatic source.

**What needs resolving**: TA3's NAT-order Depends must either enumerate the `(dₐ, d_b)` trichotomy dispatch as an additional role (matching the per-pair accounting already applied for `(#a, #w)`, `(#b, #w)`, `(L_{a,w}, L_{b,w})`), or restructure Case B so the B2/B3/B4 partition reduces to a trichotomy invocation already listed.

---

### NAT-closure missing at TA3's T1 case (ii) witness constructions that produce `+ 1` successors

**Foundation**: N/A — cross-cutting citation discipline established in ZPD's Depends, which explicitly cites NAT-closure for the `+ 1` successor operator at length-pair sub-case boundaries (`#a + 1`, `#w + 1`), and propagated through Divergence's Depends for the same pattern.

**ASN**: TA3 Sub-case A1: "the successor bound `#(a ⊖ w) + 1 = #a + 1 ≤ #b = #(b ⊖ w)`". Sub-case A2 no-disagreement branch: "the successor bound `L_{a,w} + 1 ≤ L_{b,w}`". Sub-case A3: "the successor bound `#(a ⊖ w) + 1 = #a + 1 ≤ #b = #(b ⊖ w)`". TA3's Depends lists TA2, TumblerSub, ZPD, T1, T3, TA6, NAT-sub, NAT-order, NAT-zero — no NAT-closure.

**Issue**: Each T1 case (ii) witness construction writes the successor `k = x + 1` at an ℕ-valued length (resp. `L_{a,w}`, `#a`). The ℕ-membership of `x + 1` is the closure fact supplied by NAT-closure's successor-closure clause `(A n ∈ ℕ :: n + 1 ∈ ℕ)`; neither NAT-discrete (which supplies the comparison `m + 1 ≤ n` but presupposes `+ 1 ∈ ℕ`) nor NAT-order (which quantifies over ℕ presupposing its extension) furnishes the closure step. ZPD's Depends cites NAT-closure precisely for this pattern at `#a + 1` and `#w + 1`, and the Relationship-to-Divergence postcondition propagates that citation when reproducing the same sub-case values. TA3 performs the same `+ 1` construction at three distinct sites but omits NAT-closure, leaving the `+ 1` operator as an unsourced ℕ-valued expression.

**What needs resolving**: TA3 must either add NAT-closure to its Depends with per-site accounting of the three `+ 1` successor constructions at A1, A2's no-disagreement branch, and A3, or reformulate each witness so the `+ 1` form is supplied by a postcondition already cited.
