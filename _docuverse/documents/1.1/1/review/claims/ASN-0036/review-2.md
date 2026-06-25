I read the foundation statements and then ASN-0036 as a system, tracing the precondition chains across claim boundaries and checking each symbol against its definition in scope.

The substantive machinery is sound. I verified: **S8** (correspondence-run partition) — `succ` injectivity via TS2 after deriving `#u = #u'` from shift's depth-preservation, acyclicity via TS4 + T1 irreflexivity, the chain-decomposition graph fact, and the displacement-identity induction with the correct `i = 0` (convention) vs. `i ≥ 1` (TS3) case split; **D-CTG-depth** — the reductio that builds infinitely many same-depth intermediates `w` with `u < w < x` and contradicts S8-fin; **D-SEQ** — the four-step assembly to `{[1,…,1,k] : 1 ≤ k ≤ n}`; **S7** — well-definedness via the T10a.4 instantiation at the element allocator; **S5** — the two empty-transition-relation independence constructions; and the worked example (origin truncation, run-boundary at the transclusion/append seam, lockstep on the element ordinal). These hold.

The findings below concern symbol grounding, dependency annotations, and orphaned labels — not the core arguments.

### S8a grounds `zeros` (and its positivity reading) in T0, but `zeros` is a T4 symbol
**Class**: REVISE
**Foundation**: T4 (HierarchicalParsing — defines `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|` via NAT-card); NAT-zero (`n ≠ 0 ⟺ n > 0` on ℕ); T0 (supplies only ℕ-valued components)
**ASN**: S8a — `dom(Σ.M(d)) ⊆ {t ∈ T : zeros(t) = 0 ∧ #t ≥ 2}`, with prose "By T0 (ASN-0034), `zeros(t) = 0` holds exactly when every component is positive." The Properties-table row likewise cites "T0 (ASN-0034)" only.
**Issue**: `zeros` is defined in T4, not T0. The equivalence `zeros(t) = 0 ⟺ (∀i) tᵢ > 0` decomposes as: `zeros(t)=0 ⟺ {i : tᵢ=0}=∅` (T4's zero-count definition + NAT-card's `|S|=0 ⟺ S=∅`), then `tᵢ ≠ 0 ⟺ tᵢ > 0` (NAT-zero, on T0's ℕ carrier). T0 supplies only the last ingredient (ℕ-valuedness). Attributing the whole equivalence — and the `zeros` symbol itself — to T0 is incorrect, and it is inconsistent with S7b/S7d, which correctly cite T4 for `zeros`. The same omission recurs systemically: **D-CTG**'s Depends lists only S8-fin while its statement quantifies over `zeros(v)=0` (T4), `u < v < q` (T1), and `#v = #u` (T0); **D-MIN**'s Depends lists only S8-depth while its `min`/"lexicographic total order" is T1 restricted to fixed depth. A downstream consumer loading these claims' declared deps hits undefined `zeros`/order/length.
**What needs resolving**: Ground `zeros` in T4 (with the `|·|=0 ⟺ ∅` step in NAT-card and the `≠0 ⟺ >0` step in NAT-zero, T0 supplying only ℕ-valuedness), aligning S8a with S7b/S7d — or restate the membership set in the purely componentwise form `{t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ > 0) ∧ #t ≥ 2}`, which needs only T0/NAT-order/NAT-zero and no `zeros`. Correspondingly add the symbol-grounding foundation deps (`zeros`→T4, `<`/min→T1, `#`→T0) to D-CTG and D-MIN.

### ValidInsertionPosition's proof carries orphaned clause labels (b), (c), (d)
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: ValidInsertionPosition, proof: "…at `j = 0` the position is `v = min(V_1(d)) = [1, ..., 1]` by D-MIN. **This is (d).** Every component is then `≥ 1` … so `zeros(v) = 0` with componentwise positivity **(b)**, and OrdShiftHom (a) fixes `v₁ = 1` … giving exactly `N + 1` positions **(c)**."
**Issue**: The parenthetical tags `(b)`, `(c)`, `(d)` have no referent in this claim — its Definition and Postconditions are unlabeled. (`(a)` resolves, since it names "OrdShiftHom (a)".) These read as residue of a prior version whose postconditions were lettered (a) subspace / (b) positivity / (c) count / (d) shift-form; the structure was flattened but the inline pointers were left behind. The proof's prose is otherwise self-contained, so soundness is unaffected — but a reader hits three pointers that resolve to nothing.
**What needs resolving**: Either reintroduce the lettered postcondition clauses the tags point to, or drop the `(b)`/`(c)`/`(d)` parentheticals.

### S8's Depends mis-describes S8-depth's role and mislabels T1
**Class**: OBSERVE
**Foundation**: S8-depth (FixedDepthVPositions); T1 (LexicographicOrder)
**ASN**: S8 Depends: "S8-depth … used to apply TS2 at a fixed depth when proving `succ` is injective"; and "T1 (StrictTotalOrder, ASN-0034) — supplies irreflexivity."
**Issue**: In the injectivity step the common depth for TS2 is `#u = #u'`, *derived* from `shift(u,1) = shift(u',1)` plus shift's depth-preservation (`#shift(t,1) = #t`), not from S8-depth's subspace-wide fixed-depth assertion. Tracing the proof, S8-depth is never load-bearing: each `succ` link joins equal-depth positions (shift preserves depth), so chains are automatically uniform-depth even without S8-depth. The Depends use-site description therefore overstates its role. Separately, T1 is named "StrictTotalOrder" here, whereas its claim name is "LexicographicOrder" (every other ASN-0036 citation, e.g. D-SEQ's, uses "LexicographicOrder").
**What needs resolving**: Correct the S8-depth use-site description to reflect that the depth equality fed to TS2 comes from shift's depth-preservation (or note S8-depth is carried only as a well-formedness precondition, not consumed by the proof); rename the T1 citation to "LexicographicOrder."

### D-MIN over-asserts well-ordering where finiteness suffices, and leaves the order ungrounded
**Class**: OBSERVE
**Foundation**: T1 (LexicographicOrder — the tumbler order, which restricted to fixed depth `m` is exactly lexicographic order on `m`-tuples); S8-fin (FiniteArrangement)
**ASN**: D-MIN Definition: "min(S) denotes the least element of S under the lexicographic total order on integer m-tuples; since V-positions are 1-indexed …, this order well-orders the position space, so min(S) exists for every non-empty S."
**Issue**: The claim only ever applies `min` to `V_1(d)`, which is finite by S8-fin; a total order has a least element on any finite nonempty set, so the appeal to well-ordering of the whole (infinite) position space is unnecessary. The well-ordering is also asserted, not justified (it does hold — by iterated minimization over components — but that is not shown). And the order itself is introduced freshly as "lexicographic total order on integer m-tuples" rather than identified with T1 (its source in scope), which D-MIN's Depends omits.
**What needs resolving**: Ground `min` in T1 (the established tumbler order) and justify existence from S8-fin's finiteness rather than an unproved well-ordering of the full space — or, if well-ordering is genuinely wanted, supply the iterated-minimization argument.

### D-CTG-depth's "m ≥ 3" precondition is described self-referentially
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: D-CTG-depth, proof and Preconditions: "`m ≥ 3` (non-triviality bound, **per the Preconditions**)."
**Issue**: Inside the Preconditions slot, "per the Preconditions" is circular — it points at the slot it occupies. The intended content is that `m ≥ 3` is a scope restriction (at `m = 2` the index range `2 ≤ i ≤ m−1` is empty and the claim is vacuous, handled separately in D-SEQ's `m = 2` case).
**What needs resolving**: State the bound's rationale directly (e.g., "`m ≥ 3`, so the interior index range `2 ≤ i ≤ m−1` is non-empty; the `m = 2` case is vacuous") rather than deferring to "the Preconditions."

VERDICT: REVISE