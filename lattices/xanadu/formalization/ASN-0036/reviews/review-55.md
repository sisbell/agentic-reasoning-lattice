# Cone Review — ASN-0036/D-SEQ (cycle 1)

*2026-04-13 18:25*

I'll read the ASN content carefully, examining the cross-cutting connections between properties.

### D-SEQ Assembly step miscites T0(a) for component positivity
**Foundation**: T0(a) (UnboundedComponentValues) — "Every component value of a tumbler is unbounded — no maximum value exists"
**ASN**: D-SEQ, Assembly step — "The k-values are positive integers — tumbler components are positive naturals (T0(a), ASN-0034)"
**Issue**: T0(a) establishes that component values have no upper bound. It does not establish that they are positive — T4 explicitly uses 0 as a field separator, so "any natural number" in T0(a) cannot exclude 0. The positivity of V-position components is the province of S8a (V-position well-formedness), which is available to D-SEQ transitively through D-MIN's preconditions. The citation T0(a) does not support the claim it is attached to. (Note: the positivity assertion is also redundant in context — Step 2 already establishes minimum k = 1, so 0 cannot appear in the contiguous range regardless.)
**What needs resolving**: The Assembly step should cite S8a (via D-MIN) for positivity, or drop the positivity clause entirely since Step 2's minimum suffices. T0(a) should be cited only where unboundedness is needed (as in D-CTG-depth's infinity argument).

---

### S8-vdepth is a phantom dependency — referenced but never formally stated
**Foundation**: S8-depth formal contract — axiom states fixed depth, postconditions 1–4 address correspondence runs; no sub-property establishes m ≥ 2
**ASN**: S8-depth postcondition 1 ("S8-vdepth guarantees #v ≥ 2"), D-MIN preconditions ("S8-vdepth gives m ≥ 2"), D-SEQ preconditions ("common V-position depth m ≥ 2 (S8-depth)"), ValidInsertionPosition ("S8-vdepth gives m ≥ 2" and "S8-vdepth demands #v ≥ 2")
**Issue**: At least four properties cite S8-vdepth as a precondition or enabling fact, but S8-vdepth has no formal contract — no axiom, no definition, no postcondition of any stated property. S8-depth's axiom guarantees a *common* depth within a subspace; it does not bound that depth from below. The ValidInsertionPosition empty case says m ≥ 2 is "required for compatibility with S7c" and then separately says "S8-vdepth demands #v ≥ 2" — but S7c constrains I-address element-field depth, not V-position depth, and S8-vdepth is the very property being invoked without a source. D-SEQ attributes m ≥ 2 to "S8-depth" parenthetically, but S8-depth's formal contract does not deliver this bound. The result is that every property depending on m ≥ 2 has an ungrounded precondition.
**What needs resolving**: S8-vdepth needs a formal contract — either as a standalone axiom (design requirement that all V-positions have depth ≥ 2) or as a derived postcondition of some stated property with a proof chain. If it is an axiom, it should appear alongside S8-depth's axiom. If derived, the chain from S7c (I-address constraint) to V-position depth needs to be made explicit, since V-position depth and I-address element-field depth are structurally independent quantities.

---

### D-MIN postcondition claims D-SEQ's conclusion via dependencies not in its own preconditions
**Foundation**: D-MIN formal contract — preconditions list S8-depth, S8-vdepth, S8a; postcondition says "Combined with D-CTG, S8-fin, and S8-vdepth"
**ASN**: D-MIN postcondition — "V_S(d) = {[S, 1, …, 1, k] : 1 ≤ k ≤ n} for some finite n ≥ 1"; D-SEQ postcondition — "(E n : n ≥ 1 : V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n})"
**Issue**: D-MIN's postcondition and D-SEQ's postcondition state the same result. D-MIN achieves this by invoking "Combined with D-CTG, S8-fin" — but D-CTG and S8-fin are not in D-MIN's precondition list. A formal contract's postconditions should follow from its axiom and preconditions; introducing additional dependencies in the postcondition clause bypasses the contract structure. D-SEQ has the correct preconditions (D-CTG, D-MIN, S8-fin, S8-depth) for this conclusion. D-MIN's body also contains a full case-analysis proof (m = 2 and m ≥ 3) that duplicates D-SEQ's proof, creating two canonical sources for the same result. Any downstream ASN citing "V_S(d) = {[S, 1, …, 1, k] : 1 ≤ k ≤ n}" cannot tell whether to cite D-MIN or D-SEQ.
**What needs resolving**: D-MIN's postcondition should state only what follows from D-MIN's axiom and its own preconditions — namely, that the minimum of V_S(d) is [S, 1, ..., 1]. The sequential-positions characterization should be D-SEQ's exclusive postcondition. The inline case-analysis proof in D-MIN's body that derives V_S(d) = {[S, 1, …, 1, k] : 1 ≤ k ≤ n} should either be removed or reframed as motivation that D-SEQ formalizes.
