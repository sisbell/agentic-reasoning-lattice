```
VERDICT: REVISE
```

## Correctness

### Issue 1: x₄ — wrong T4 clause applied
**Scenario**: Scenario 2
**Property**: T4
**Step**: "Element field's last component is Eδ=0, violating the positive-component constraint."
**Problem**: The positive-component constraint applies to non-separator field components. But in T4's framework, zeros are defined as separators; there is no T4 category of "non-separator zero." The formal count: `zeros(x₄) = #{i : x₄ᵢ = 0}` counts positions 2, 4, 6, and 8 — zeros(x₄) = 4. The primary violation is T4's **at-most-three-zeros constraint**: 4 > 3, full stop. The scenario's framing treats the 0 at position 8 as a field component (Eδ=0), which requires implicitly reading zeros(x₄) = 3 — inconsistent with the formal definition. The positive-component constraint cannot apply here because no zero can be a field component under T4 (all zeros are separators).
**Correction**: "x₄: invalid. zeros(x₄) = 4 (positions 2, 4, 6, 8 are all zero) > 3 permitted — directly violates T4's at-most-three-zero-separators constraint. All four zeros are separators under T4 (field components are strictly positive, so never zero); x₄ thus encodes four field separators, exceeding the three allowed by the four-field model."

---

## Coverage gaps

### Gap 1: T0(a) and T0(b) — unbounded address space
**Missing**: No scenario exercises unbounded component values (T0(a)) or unbounded tumbler length (T0(b)).
**Needed**: A scenario that demonstrates the allocation mechanism generates no ceiling. For T0(a): show that repeated `inc(t, 0)` increments the component at `sig(t)` without bound — exhibit an address with a component value exceeding an arbitrary M. For T0(b): show that `inc(t, 1)` (within-field child-spawning) is unlimited in depth — exhibit a tumbler of length ≥ n for arbitrary n. The distinction from T0(a) must be explicit: T0(a) bounds siblings at one level; T0(b) bounds nesting depth itself.

### Gap 2: T7 — subspace disjointness and its ordering consequence
**Missing**: No scenario demonstrates that text and link element subspaces are permanently disjoint, nor that T1 places all text addresses before all link addresses within the same document.
**Needed**: Using document [1,0,3,0,2]: take e_text=[1,0,3,0,2,0,**1**,3] and e_link=[1,0,3,0,2,0,**2**,1]. (1) T3: positions 1–8 differ at position 7 (1 vs 2) → e_text ≠ e_link. (2) T1 case (i) at position 7: 1 < 2 → e_text < e_link. State explicitly: this ordering is a *consequence* of T1 applied to the subspace identifier, not a separate assumption. (3) T7: since E₁ values differ, the tumblers are in distinct subspaces; any advance within subspace 1 preserves the value 1 at position 7, which can never equal 2.

### Gap 3: T8 — allocation permanence
**Missing**: T8 is a history property; no scenario exercises it.
**Needed**: A two-state scenario: at time t₁, allocate a₁ = [1,0,1,0,1,0,1,1]. At time t₂, allocate a₂ = inc(a₁,0) = [1,0,1,0,1,0,1,2]. Show the allocated set grows {a₁} → {a₁, a₂} with no element removed. Invoke T8: a₁ remains permanently in the allocated set regardless of subsequent allocations; it occupies its position on the tumbler line as a ghost element if no content is stored. The scenario should make the monotone-growth structure explicit: the set of allocated addresses is a non-decreasing set under set inclusion.

### Gap 4: TA3 (weak) and TA3-strict — order preservation under subtraction
**Missing**: No scenario exercises either form of subtraction's order-preservation. The TA3 proof covers five structurally distinct cases; none are illustrated.
**Needed**: Two sub-scenarios:

**Same-length (TA3-strict)**: a=[1,0,3,0,2,0,1,2], b=[1,0,3,0,2,0,1,5] (#a=#b=8), w=[0,0,0,0,0,0,0,1]. Compute: a⊖w — divergence at position 8 (2 vs 1), result [1,0,3,0,2,0,1,**1**]. b⊖w — divergence at position 8 (5 vs 1), result [1,0,3,0,2,0,1,**4**]. Compare at position 8: 1 < 4 → strict inequality. TA3-strict applies since #a = #b.

**Prefix case (TA3 weak only)**: a=[1,0,3,0,2] (proper prefix of b=[1,0,3,0,2,0,1,2]), w=[0,0,1]. Compute: a⊖w — diverge at position 3 (3 vs 1), result [0,0,**2**]. b⊖w — same divergence at position 3, result [0,0,**2**,0,2] (tail from b). Compare: [0,0,2] is proper prefix of [0,0,2,0,2] → T1 case (ii), a⊖w < b⊖w. Show explicitly that TA3-strict does *not* apply here (#a ≠ #b), only TA3 weak — this is the concrete demonstration of why the equal-length precondition on TA3-strict exists.

### Gap 5: TA6 — ordering aspect
**Missing**: TA6 has two claims: (1) no zero tumbler is a valid address; (2) every zero tumbler is less than every positive tumbler. Scenario 4 demonstrates only claim (1) — it produces [0] as a subtraction result and notes it is not a valid address. Claim (2) is never shown.
**Needed**: Add a step to Scenario 4 (or the TA6 sub-scenario): compare [0] with [1,0,3,0,2,0,1,1]. Position 1: 0 < 1 → [0] < [1,0,3,0,2,0,1,1] by T1 case (i). State the general principle: a zero tumbler has 0 at every position; a positive tumbler has tₖ > 0 at some first position k; T1 case (i) at position k gives zero tumbler < positive tumbler. This is the property that makes zero tumblers usable as lower bounds in span arithmetic.