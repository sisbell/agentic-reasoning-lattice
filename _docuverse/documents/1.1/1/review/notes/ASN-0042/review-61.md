# Review of ASN-0042

## REVISE

### Issue 1: "Structural forcing" claim in O10 over-generalized

**ASN-0042, *Field-opening boundary case* within O10**: "The structural forcing is delegation-intrinsic: every freshly delegated principal π_B inherits a virgin granfilade S(pfx(π_B), 2) at the moment of delegation, because O15 + O18 ensure that the only granfilade entry materialized by the delegation transition is pfx(π_B) itself..."

**Problem**: The justification (O15 + O18) only establishes that the delegation transition itself adds nothing to S(pfx(π_B), 2) — it adds pfx(π_B) alone. It does not preclude pre-delegation transitions from populating S(pfx(π_B), 2). Concretely: at any pre-delegation state Σ_t, an ancestor principal (e.g., the delegator π_A) is the most-specific covering principal of pfx(π_B) since pfx(π_B) ∉ Π yet. So π_A is O5-authorized to call Bop(pfx(π_B), 2); B6 holds because zeros(pfx(π_B)) + 1 ≤ 3 by O1a; the result enters S(pfx(π_B), 2) ∩ Σ_t.B. After delegation, π_B inherits a *non-virgin* granfilade with hwm_0 ≥ 1, and the first fork uses the sibling-advance branch, not the field-opening branch.

The trajectory-specific paragraph that precedes (showing "prior transitions on the witnessing path... perform Bop calls under different parents") is correct for this worked example, but the generalization to "delegation-intrinsic" is unsupported.

**Required**: Either (a) qualify the claim to trajectory scope ("in this trajectory, no prior Bop populated S(pfx(π_B), 2)"); (b) reframe the exhibition as "field-opening *can* arise at a freshly delegated principal, alongside the sibling-advance variant"; or (c) state explicitly that the Unilateral O10★ claim is robust to either branch — the field-opening case is one possible exhibition, not the structurally forced one. The current framing claims more than the proof supports.

### Issue 2: Minor — worked example state labeling

**ASN-0042, *Worked Example*, multiple paragraphs**: The state labels Σ₀, Σ₁, Σ₂ are used loosely. Σ_2 is referred to as "after π_A allocates a_2" but actually encompasses multiple transitions (two hwm advances, the a_2 baptism, and two namespace baptisms). The fork section then names Σ_pre := Σ_2 capturing all of these.

**Problem**: A reader expecting one-transition-per-subscript will be confused. The math is correct, but the labels conflate atomic transitions with multi-transition segments.

**Required**: Either explicitly name each transition (Σ_2a, Σ_2b, …) or state once at the top of the *Worked Example* that subscript labels denote trajectory milestones, not single transitions.

## OUT_OF_SCOPE

(None. The ASN respects its declared scope and the open questions appropriately defer adjacent topics.)

VERDICT: REVISE
