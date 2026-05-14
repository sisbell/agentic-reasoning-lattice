# Review of ASN-0043

## REVISE

### Issue 1: subspace_I extension to ghost addresses is not stated
**ASN-0043, L0 extension note and L9 proof**: L0 says "We extend `subspace_I(a) = E(a)₁` (ASN-0036's projection name) uniformly to both content and link addresses." But the L9 proof writes `subspace_I(g) = s_X` for a ghost address `g ∉ dom(Σ.C) ∪ dom(Σ.L)`.
**Problem**: The stated extension covers content+link addresses only. The L9 construction needs subspace_I on a third class (ghost addresses), and the worked example similarly invokes subspace_I(g). Reader must back-fill the extension scope from context.
**Required**: In the L0 extension note, state that `subspace_I(a) = E(a)₁` is well-defined wherever T4b's `E` projection applies — i.e., on every T4-valid tumbler with `zeros(a) = 3` and `#E(a) ≥ 1` — so ghost addresses are covered. Or rewrite L9 to invoke T7 with `E(g)₁ = s_X` directly without naming subspace_I(g).

### Issue 2: L11b proof uses operational "firing" language for a state-existence claim
**ASN-0043, L11b proof**: "Inducing a fresh `(a^(i-1), 0)` firing now extends the allocator's realized domain by one — preserving the initial-segment structure — and yields `a'` as a fresh T10a allocation event under `home(a)`'s link allocator."
**Problem**: L11b is a state-existence claim. The "firing" / "event" vocabulary belongs to operational semantics that this ASN explicitly excludes. It also leaves ambiguous whether Σ' must be operationally reachable from Σ or merely conforming as a state.
**Required**: Construct Σ' as a state directly: `Σ'.L = Σ.L ∪ {a' ↦ Σ.L(a)}`, then verify conformance. The least-i choice on the sibling stream {a, a^(1), a^(2), ...} ensures AllocatedSet's initial-segment structure is preserved without invoking firings.

### Issue 3: L9 proof's Case A chain implicitly requires structural-producibility reading of L1c
**ASN-0043, L9 proof, "Allocation of a" Case A**: Step (i) `inc(d', 2) → d'.0.1` is presented as the chain's first step, but if `d'` already has content under it then `(d', 2)` has already fired to spawn the content element-allocator. The Case A parenthetical acknowledges this and says "L1c requires structural producibility — that a is reachable from d' by a T10a-conforming chain — not that the chain corresponds to a fresh allocator initialization."
**Problem**: This load-bearing interpretation is buried in a parenthetical inside Case A, but it determines whether L1c's chain is a structural witness or an event log. Without this reading, Case A appears to violate T10a's per-(t, k') at-most-once constraint. The status of the chain (structural vs. operational) should be settled in L1c itself.
**Required**: Promote the structural-producibility reading to L1c proper: state explicitly that the chain is a structural witness establishing reachability via T10a-valid `inc` steps, distinct from any operational sequence of allocator events. Or rewrite Case A to route the chain through the existing element-allocator's frontier rather than re-traversing `(d', 2)`.

### Issue 4: PrefixSpanCoverage inclusion direction glosses the c = x case
**ASN-0043, PrefixSpanCoverage proof, Inclusion direction**: "let `c` extend `x`, so `x ≼ c`. By T1(ii), `c ≥ x`."
**Problem**: T1(ii) handles proper prefix-extension (yielding strict `<`). When `c = x` (admitted by `x ≼ c`), `c ≥ x` is by reflexivity of equality, not T1(ii). The proof as written cites T1(ii) for both cases.
**Required**: Split the case: if `c = x`, then `c ≥ x` by reflexivity; if `c` is a proper extension, then `x < c` by T1(ii). Then continue with the strict-successor argument. Both branches land `c ∈ [x, shift(x, 1))`.

### Issue 5: L-fin labeled "across transitions" in worked example
**ASN-0043, Worked Example, "L-fin across `Σ_1 → Σ_2`" and "L-fin across `Σ_2 → Σ_3`"**: L-fin is a state invariant (`|dom(Σ.L)| < ∞`), but the worked example labels its verifications across transitions, paralleling L12 and L12a (which are genuine transition invariants).
**Problem**: The labeling conflates two distinct invariant kinds. L-fin must hold at each state independently; L12 constrains state pairs related by →. Using identical "across" framing for both obscures the distinction.
**Required**: Verify L-fin separately at each state (`|dom(Σ_0.L)| = 1, |dom(Σ_1.L)| = 2, |dom(Σ_2.L)| = 3, |dom(Σ_3.L)| = 4`); verify L12, L12a only across transitions. Distinguishing them clarifies which invariants are state-local and which are transition-local.

### Issue 6: L8 (same_type) reflexivity not exercised at the basic worked-example state
**ASN-0043, Worked Example, single-link state Σ verification**: L0–L14a are checked, but L8 is omitted from the basic state. L8 is exercised only in Step 3 (arity-4 a₃ vs. arity-3 a).
**Problem**: L8's reflexivity is non-vacuous on the single-link state and would concretely illustrate the coverage-equality definition. The coverage-vs-span-set distinction (a key design choice in L8) is never illustrated with a concrete coverage computation at the basic state.
**Required**: Add an L8 verification at the basic state showing same_type(a, a) holds via `coverage(Θ) = coverage(Θ)`, with the actual coverage computed: `coverage({(g, δ(1, 8))}) = {t : g ≼ t}` by PrefixSpanCoverage.

### Issue 7: L7 (DirectionalFlexibility) not illustrated in worked example
**ASN-0043, Worked Example**: L7 is a META claim about the absence of slot-based directional semantics. The worked example uses F/G labels in `(F, G, Θ)` without observing that these labels carry no structural directional weight.
**Problem**: META claims need illustration to be load-bearing for readers; the example treats slot 1 as "from" and slot 2 as "to" by convention, but never observes that the labels are nominal.
**Required**: Add an inline note in the worked example observing that swapping F and G in `(F, G, Θ)` produces a structurally distinct link by L6, but no L-invariant determines whether F is a "source" — that interpretation lives in the type at g.

## OUT_OF_SCOPE

### Topic 1: MAKELINK, FOLLOWLINK, and other operations
**Why out of scope**: The Scope section explicitly excludes operations. Specification of how links are created, retrieved, or removed belongs to a future ASN.

### Topic 2: Three-layer link deletion (identity / index / presentation)
**Why out of scope**: The text mentions Gregory's evidence that link removal occurs at the arrangement layer while the link's own orgl persists, but defers the abstract deletion model to a future ASN. The Open Question on `Σ.M`–`Σ.L` consistency captures this.

### Topic 3: Well-formedness of compound link structures (faceted / chained / link-to-link)
**Why out of scope**: L13 establishes the structural affordance for reflexive addressing. Constraints on compound link structures (n-way faceted links, chains of meta-links) are listed in Open Questions and belong to a future ASN.

### Topic 4: Constraints on type address hierarchies beyond prefix containment
**Why out of scope**: L10 establishes that prefix containment + T5 contiguity supports type hierarchies. Additional well-formedness constraints on type registries are an Open Question.

### Topic 5: Allocation ordering of link addresses relative to content within the same document
**Why out of scope**: The Open Questions section flags this. The L-invariants and S-invariants together do not constrain allocation ordering between subspaces.

VERDICT: REVISE
