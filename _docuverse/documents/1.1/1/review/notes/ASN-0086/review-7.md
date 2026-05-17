# Review of ASN-0086

## REVISE

### Issue 1: R0a's antichain proof relies on a construction that Emit_K's specification does not enforce
**ASN-0086, R0a proof, induction step**: "For class (iii), `dom(Σ'.L) = dom(Σ.L) ∪ {a}` where `a` is constructed by R0 Step 2."
**Problem**: The substrate emission primitive (page "Substrate emission primitive (for `Emit_K`)") commits to *emit-at-any-L1c-conforming-fresh-address*, and Emit_K's Definition reads only "by R0, `a ∉ dom(Σ.L)`" — no antichain postcondition. Under that specification an admissible Emit_K may deposit at `a' = a₁.1` for an existing `a₁ ∈ dom(Σ.L)`. Walking through the worked sketch values (`a₁ = 1.0.1.0.1.0.2.1`, `s_L = 2`, `d = 1.0.1.0.1`): `a' = 1.0.1.0.1.0.2.1.1` has `zeros = 3` (positions 2, 4, 6), `subspace_I = 2 = s_L`, `home = d`, `#E = 3 ≥ 2`, and the L1c chain `(d, 2) → d.0.1 → d.0.2 → (d.0.2, 1) → a₁ → (a₁, 1) → a'` is T10a-conforming with the lone fresh child-spawn pair `(a₁, 1)`, `k' = 1` (no zeros constraint). The primitive then permits the step `Σ → Σ'` with `Σ'.L(a') = (F, G, K)`. After it, `a₁ ≼ a'`, falsifying R0a. The phrase "under the Emit_K-only emission discipline" in R0a's statement is doing all the work; the disciplined construction is not derivable from the substrate primitive that R0 actually discharges.
**Required**: Either (a) tighten Emit_K's specification to require the returned address be prefix-incomparable in `≼` with every existing `a' ∈ dom(Σ.L)` and re-derive R0 with this stronger existential; (b) tighten the substrate emission primitive analogously, forbidding emissions at descendants of existing link addresses; or (c) restate R0a as conditional on a named implementation discipline (the udanax-green sibling-frontier rule the Remark cites) rather than as a substrate property. The implementation evidence below R0a is evidence the discipline is held, not that the substrate guarantees it.

### Issue 2: Nullify's single-tuple scope inherits Issue 1's fragility
**ASN-0086, Nullify "Single-tuple scope"**: "restricted to `A_rel^Σ = dom(Σ.L)`, however, R0a (FlatLinkDomain) gives that the only link address with `a` as a prefix is `a` itself."
**Problem**: If Issue 1's gap admits the adversarial emission depositing at `a₁.1`, then `{t : a₁ ≼ t} ∩ A_rel^{Σ''} ⊇ {a₁, a₁.1}`, so `Nullify(Σ'', a₁)` places both `a₁` and `a₁.1` into `nullified(Σ''')`. The "single-tuple" claim degrades into a subtree retraction whose extent depends on what other links happen to share `a` as a prefix — a different operation from the one named. The R6c restoration argument also collapses: re-emitting `(F₁, G₁)` may itself land at a descendant of `a₁`, immediately re-nullifying the replacement.
**Required**: Resolve Issue 1; or add an explicit Nullify precondition `(A a' ∈ dom(Σ.L) : a ≼ a' : a' = a)` and rederive the single-tuple-scope claim under that precondition.

### Issue 3: R0 Step 4's "Remaining L-invariants" paragraph is grouped by one-line orthogonality assertion
**ASN-0086, R0 Step 4**: "Remaining L-invariants (L2, L4–L10, L13, L14): all are properties of `Σ.L`'s value structure or its targets that are either orthogonal to extension at a fresh key (L2, L4, L5, L6, L7, L8, L10, L13) or preservation lemmas under monotone extension (L14, L9 — and L14's scoped form is preserved when the new address is link-subspace by Step 2)."
**Problem**: Nine L-invariants are dispatched by one-line orthogonality / preservation labels without per-invariant reasoning, after the prior bullets enumerate L0, L1, L1a, L1b, L1c, L3, L11a, L11b, L12, L12a, L-fin, L14a explicitly. This is exactly the "by similarly" pattern Dijkstra-style review is meant to catch — even where each individual verification is easy. L14 in particular is load-bearing for the Setup-required tag: its preservation needs (i) `a` is `s_L`-resident by Step 2, (ii) `Σ'.C = Σ.C` by Frame, (iii) `a ∉ dom(Σ.C)|_{s_C}` because `subspace_I(a) = s_L ≠ s_C` (T7), so the intersection `dom(Σ'.L) ∩ dom(Σ'.C)|_{s_C}` extends to no new element. That chain belongs in the proof, not in a grouping label.
**Required**: Replace the grouped paragraph with one explicit bullet per remaining invariant, naming the specific preservation reason.

### Issue 4: R0 Step 2 Case B cites T10a's at-most-once discipline for sibling-sweep pairs that T10a does not bind
**ASN-0086, R0 Step 2 Case B**: "each new `(parent, k)` pair along the extension is `(incʲ(b, 0), 0)` for `0 ≤ j < i`, which the original allocator producing `b` has not yet committed (precisely because `incⁱ(b, 0) ∉ dom(Σ.L)` … so T10a's at-most-once discipline is satisfied."
**Problem**: T10a's axiom binds at-most-once to *child-spawning events*: "child-spawning uses one `inc(·, k')` with `k' ∈ {1, 2}` … Each `(t, k')` pair yields at most one child-spawning event." Sibling production via `inc(·, 0)` is governed by the allocator's monotone enumeration and T10a.7 (EnumerationInjectivity), not by at-most-once on `(·, 0)` pairs. The argument's *conclusion* is sound — `incⁱ(b, 0)` is uniquely the i-th sibling, and L12 keeps prior siblings in `dom(Σ.L)`, so the least `i` with `incⁱ(b, 0) ∉ dom(Σ.L)` identifies the next available enumeration index — but the named citation is wrong; the right citation is T10a.7 + L12 + the allocator's domain definition. (Step (iii) of Case A — the `(d.0.s_L, 1)` step — is a genuine child-spawn with `k' = 1 ∈ {1, 2}` and is correctly bound by at-most-once.)
**Required**: Change Case B's justification to cite T10a.7 (EnumerationInjectivity) and L12 (LinkImmutability) for sibling-stream uniqueness; keep the at-most-once citation only at child-spawn steps (the `(d, 2)` step of Case A and any future Case-B variant that introduces a new child allocator).

### Issue 5: "Every transition in `→` is one of (i)–(iii)" is too strong relative to the underlying transition vocabulary
**ASN-0086, "State transition relation" paragraph**: "Every transition in `→` is one of (i)–(iii); the substrate exposes no removal, replacement, or in-place mutation transition (consistent with S0, L12, and T8 across the underlying ASNs)."
**Problem**: ASN-0036 admits at least one further state-changing class: arrangement extension via INSERT and similar operations, which extend `dom(Σ.M(d))` for an existing `d` without removing/replacing/mutating anything (S0/L12/T8 are not violated by addition). Such transitions affect `Σ.M`'s value but not `dom(Σ.M)` itself, and so do not match class (i). The literal statement reads as a global enumeration of `→`-transitions; it should be qualified as "every dom-extending transition of the substrate stores `(C, M, L)`" or be widened by a fourth class. Either is fine — the link-store-only claims (R0–R7) survive — but a reader interpreting `→` broadly would expect arrangement extensions in scope, and then would (correctly) note that R0's L-invariant verifications cover only one of the relevant transition classes.
**Required**: Qualify the enumeration: explicitly state that `→` here is restricted to the dom-extending substrate emissions, and that arrangement modifications (ASN-0036 / ASN-0058) live in a parallel transition vocabulary whose L-invariant preservation is handled there.

## OUT_OF_SCOPE

### Topic 1: Coverage-equivalence at the type slot vs. implementation behavior
**Why out of scope**: The TypeEquivalence Definition uses `K ~ K' ≡ coverage(K) = coverage(K')`, aligning `L_K` with L8's `same_type`. Whether the udanax-green link-typing primitives project through `coverage(·)` or compare endset values literally is a separate verification target — checkable against implementation, not derivable from the substrate model. The "coverage-equivalence" choice is well-motivated within the spec; the impl/spec alignment check belongs in a substrate-test pass.

### Topic 2: Active-subset machinery for higher-arity links
**Why out of scope**: `L_K^Σ` and `A_K^Σ` are defined only over arity-3 links by construction (Definition of TypedRelation). Higher-arity links exist in `dom(Σ.L)` per L3 but participate in no `L_K`; the note's "Nullifying a higher-arity address" remark and Open Question 2 acknowledge this. Extending active-subset machinery to `A_K^{(n),Σ}` is a separate ASN.

### Topic 3: Concurrency model for Emit / Observe
**Why out of scope**: Atomicity and consistency guarantees between concurrent Emit_K and Observe_K are correctly identified as Open Question 5. The substrate `→` is presented as sequential.

### Topic 4: Cross-arrangement-link invariants
**Why out of scope**: Whether the visibility of an endset's coverage in some arrangement should constrain `A_K` is correctly flagged as Open Question 1. `→`'s restriction to substrate-emission transitions (Issue 5) is consistent with deferring this.

### Topic 5: Cardinality / structural bounds on `nullified(Σ)`
**Why out of scope**: Whether unbounded retraction is permitted, and whether any ratio between `|nullified(Σ)|` and `|dom(Σ.L)|` must hold, is correctly Open Question 6.

VERDICT: REVISE
