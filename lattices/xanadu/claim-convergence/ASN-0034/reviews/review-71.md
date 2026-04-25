# Cone Review — ASN-0034/T9 (cycle 6)

*2026-04-16 06:03*

I'll read through the full document carefully, cross-checking definitions, dependency chains, and quantifier scopes.

After thorough analysis of the entire ASN as an integrated system, I find the document has been substantially reworked since the Previous Findings were written — findings #2–7, #9–12 all appear to have been addressed in the current text (Consequence 5 now has a full proof, T9 now defines its predicates and declares dependencies, TA5 now cites TA5-SIG, all T10a postconditions now carry Depends annotations, T10a-N properly scopes its necessity claim, etc.). Findings #1 and #8 remain unresolved.

Here are the genuinely new issues:

---

### T10a Consequence 5's inductive step invokes TA5(b) "for k = 0" with a scope that TA5(b) does not literally state

**Foundation**: (internal — foundation ASN)
**ASN**: T10a (AllocatorDiscipline), Consequence 5 inductive step: "the sibling stream `inc(·, 0)` modifies only position `sig(b_A) = #b_A` (TA5(b) for k = 0, TA5-SigValid, T10a.4); every other position is inherited unchanged."
**Issue**: TA5's postcondition (b) for `k = 0` states: "`(A i : 1 ≤ i ≤ #t ∧ i ≠ sig(t) : t'ᵢ = tᵢ)`." This says agreement at every position *other than* `sig(t)` — it excludes `sig(t)` from the agreement guarantee but does not assert that `sig(t)` is the *only* position that changes. The claim "modifies only position `sig(b_A)`" is the conjunction of two facts: (b) says positions `≠ sig(t)` are preserved, and (c) says `t'_{sig(t)} = t_{sig(t)} + 1 ≠ t_{sig(t)}`. The second fact — that position `sig(t)` *actually differs* — is drawn from TA5(c), not TA5(b). The citation "(TA5(b) for k = 0)" for the "modifies only" claim is incomplete; it requires TA5(c) to establish that `sig(t)` is modified (rather than merely unguaranteed by the agreement quantifier). The distinction matters because the inductive step in Case 2 (`j = #bₓ`) depends on `sig` being the position that *changes* (producing values 1, 2, 3, …), not merely the position *excluded from agreement*.
**What needs resolving**: The inductive step's citation should reference both TA5(b) (preservation of non-`sig` positions) and TA5(c) (actual modification at `sig`), since the "modifies only" claim is the conjunction of both postconditions.

---

### T10a's axiom uses `zeros(t)` in the formal contract without defining it or citing its source

**Foundation**: (internal — foundation ASN)
**ASN**: T10a (AllocatorDiscipline), formal contract axiom: "child-spawning uses exactly one `inc(·, k')` with `k' ∈ {1, 2}` satisfying the TA5a bounds (`k' = 1` when `zeros(t) ≤ 3`, `k' = 2` when `zeros(t) ≤ 2`)"
**Issue**: The formal contract introduces the predicate `zeros(t)` — the count of zero-valued components in `t` (or trailing zeros, or inter-field separators; the intended definition is ambiguous without the source). `zeros(t)` is defined in TA5a (IncrementPreservesT4), which is cited in T10a.4's Depends annotation and in the Justification paragraph. But the axiom statement itself — the top-level behavioral constraint — uses `zeros(t)` without a Depends or definition-cite at that level. Every other symbol in the axiom is either defined locally (`inc` is described inline, `k'` is constrained) or cites its source (`T4` is named). A formalizer encoding the axiom would encounter `zeros(t)` as an unresolved symbol in the axiom's own statement, needing to trace through the Justification prose to discover that TA5a is the source. Since the axiom's formal contract has no top-level Depends clause (a structural gap already noted in previous findings), this symbol is formally orphaned.
**What needs resolving**: Either a top-level Depends citing TA5a for the `zeros` predicate, or a parenthetical cite at point of use in the axiom statement (as `sig(t)` receives "(TA5-SIG)" in TA5's contract).

---

### T1's proof of irreflexivity handles Case (ii) with `m + 1 ≤ m` but the formal contract's Case (ii) requires `k = #a + 1 ≤ #b`, which under `a = b` becomes `m + 1 ≤ m` — correct but the proof text writes this as `k = m + 1 ≤ m` without noting that `k` also satisfies `k ≥ 1`

**Foundation**: (internal — foundation ASN)
**ASN**: T1 (LexicographicOrder), proof of irreflexivity: "Case (ii) requires `k = m + 1 ≤ m`, which is false."

Hmm, this is actually fine — `m + 1 ≤ m` is false for all natural numbers. The `k ≥ 1` constraint is already absorbed. Not a finding; let me remove this.

Actually wait, I wrote three findings but the third one is not valid. Let me replace it.

---

### Consequence 5 closure assumes `#x ≥ j` via T10a.3 but T10a.3 guarantees length relative to the *parent's* base, not relative to the *branching point's* child base

**Foundation**: (internal — foundation ASN)
**ASN**: T10a (AllocatorDiscipline), Consequence 5 closure: "both `#x` and `#y` weakly exceed `min(#bₓ, #bᵧ) ≥ j` (lengths grow monotonically with depth, T10a.3)"
**Issue**: The closure needs `#x ≥ j` for any `x ∈ domain(X)` where X is in Cₓ's subtree. The argument is: T10a.3 establishes that output lengths grow with nesting depth, so `#x ≥ #bₓ ≥ j`. But T10a.3 as stated gives the length formula "#output = m + k'₁ + k'₂ + … + k'\_d" relative to the *root allocator's* base length m, not relative to any intermediate allocator's base. The conclusion `#x ≥ #bₓ` requires that X is at depth ≥ Cₓ's depth *and* that Cₓ is on the path from root to X — both true by the LCA construction, but the bridge from T10a.3's global formula to the local bound `#x ≥ #bₓ` is never stated. T10a.3 doesn't have a postcondition of the form "for any ancestor A of allocator B, `#output(B) ≥ #output(A)`"; it only gives the absolute formula from the root. The monotonicity claim "lengths grow monotonically with depth" is a correct informal consequence of T10a.3's additive formula (since each k'ᵢ ≥ 1), but this consequence is cited rather than the formula itself, and the local application `#x ≥ #bₓ` is the step that actually closes the argument.
**What needs resolving**: Either T10a.3 should state the local monotonicity consequence explicitly (for any ancestor-descendant pair, descendant outputs are strictly longer), or the Consequence 5 closure should derive `#x ≥ #bₓ` from T10a.3's additive formula rather than citing the informal summary.
