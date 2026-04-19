# Cone Review — ASN-0034/TA3-strict (cycle 3)

*2026-04-18 17:21*

### TA3-strict omits the `(d_a, d_b)` NAT-order trichotomy site, though the proof's case analysis on three ordered-ness outcomes in ℕ is exhaustive only by trichotomy at that pair

**Foundation**: N/A — internal consistency. The relevant anchor is NAT-order's Formal Contract ("exactly one of `m < n`, `m = n`, `n < m`"), and the convention stated verbatim in TA3-strict's NAT-order entry by which each distinct ℕ-pair earns a separate site (the entry enumerates four roles — length pairs `(#a, #b)`, `(#a, #w)`, `(#b, #w)`, and the component pair `(x_d, w_d)` — under the per-instance convention declared in T1's Depends).

**ASN**: TA3-strict, Setup and case headings:
> "**Case 1: `d_a = d_b = d`.** … **Case 2: `d_a < d_b`.** … **Case 3: `d_a > d_b`.**"

and the Setup step ruling out a fourth possibility ("We verify that `d_b = zpd(b, w)` also exists …").

**Issue**: The three cases partition all pairs `(d_a, d_b)` in ℕ × ℕ into exactly the three trichotomy outcomes, and the claim of exhaustiveness rests on NAT-order's trichotomy at the ℕ-pair `(d_a, d_b)` — exactly the "exactly one of `m < n`, `m = n`, `n < m`" clause. TA3-strict's NAT-order Depends entry enumerates four pairs/roles, none of which is `(d_a, d_b)`: the length pairs `(#a, #b)`, `(#a, #w)`, `(#b, #w)` and the component pair `(x_d, w_d)` discharge the length-naming and `>` → `≥` conversions, not the divergence-index case split. Under the per-instance convention stated by TA3-strict itself, a trichotomy invocation at a fresh pair is a fresh site and must be enumerated.

**What needs resolving**: Either extend TA3-strict's NAT-order Depends entry with a fifth role — trichotomy at the index pair `(d_a, d_b)` discharging the exhaustive case split into `d_a = d_b`, `d_a < d_b`, `d_a > d_b` — matching the per-instance convention already applied to the four enumerated sites; or restructure the proof so the three-way case split is routed through a cited consumer (e.g., invoke ZPD or another axiom whose postcondition already packages the comparison).

### TA3-strict's Setup derives `a > w` from `a ≥ w ∧ not-ZPE(a, w)` without citing T3, though the convention elsewhere in the ASN requires it

**Foundation**: N/A — internal consistency. The relevant anchor is TumblerSub's T3 Depends entry (site (i)): "the proof concludes `a ≠ w` from the premise that `a` and `w` are not zero-padded-equal … the contrapositive of T3's forward direction supplies this inference — if `a = w` as tumblers, then by T3 they share both length and every component, so their zero-padded extensions … coincide at every position, contradicting the 'not zero-padded-equal' fact. Without T3 there is no basis for transporting the tumbler-level equality `a = w` to componentwise identity of the padded sequences". TA2's site (i) performs the same citation for the same inference.

**ASN**: TA3-strict, *Setup for remaining cases*:
> "Since `a ≥ w` and `a` is not zero-padded-equal to `w`, we have `a > w`, and at the first padded disagreement `a_{d_a} > w_{d_a}`."

TA3-strict's Depends lists T0 (via previous finding), T1, TumblerSub, ZPD, TA2, NAT-sub, NAT-zero (via previous finding), and NAT-order — no T3.

**Issue**: To pass from `a ≥ w` to `a > w` the argument must eliminate the `a = w` disjunct of `a ≥ w ⟺ a > w ∨ a = w`. The elimination uses "not-ZPE ⟹ `a ≠ w`", whose contrapositive `a = w ⟹ ZPE` is the T3-licensed step that TumblerSub and TA2 explicitly cite T3 to discharge. TA3-strict performs the identical step (visible as "`a` is not zero-padded-equal to `w`, we have `a > w`") but does not cite T3. Under the ASN's convention that "each proof cites only the ℕ [and T3/T0] facts it actually uses", this step is unsourced. The same omission arguably carries into the Setup's rebuttal step ("if `b` were zero-padded-equal to `w` …"), though that chain can be reached through ZPD alone.

**What needs resolving**: Either add T3 to TA3-strict's Depends with a citation covering the Setup's `not-ZPE(a, w) ⟹ a ≠ w` and (if the rebuttal is read the same way) `not-ZPE(b, w) ⟹ b ≠ w` steps — matching the per-site T3 citation TumblerSub and TA2 already apply to the structurally identical derivations — or restructure the Setup to consume TumblerSub's precondition-consequence directly (which already exports `a_k > w_k` at `k = zpd(a, w)` with the T3 appeal discharged internally), eliminating the intermediate `a > w` step from TA3-strict's own argument.
