# Review of ASN-0086

## REVISE

### Issue 1: Worked Sketch Step 2 omits concrete L-invariant verification at a₂

**ASN-0086, Worked Sketch, Step 2 (concrete)**: Step 1 includes a detailed "L-invariant verification at the concrete `b₁`" — a bulleted enumeration of L0, L1, L1a, L1b, L1c, L2, L3, L4(c), L11a, L12/L12a/L12b, L14, L14a, L-fin each verified by direct inspection. Step 2, producing `a₂ = 1.0.1.0.1.0.2.3` via the same R0 Step 2 Case B mechanism, performs only the set-theoretic verification (L_K^{Σ_2}, nullified(Σ_2), A_K^{Σ_2}).

**Problem**: The asymmetry undercuts the pedagogical depth Step 1 establishes. A reader who values the explicit verification at b₁ has no counterpart at a₂. Step 1's bulleted verification is exemplary precisely because it makes R0 Step 4's abstract argument concrete; Step 2 should benefit from the same treatment, particularly because a₂ is the *restoration* emission that demonstrates R6c operationally.

**Required**: Either replay the analogous L-invariant verification at a₂ (most bullets transfer verbatim with mechanical substitution), or add an explicit note in Step 2 that "the same R0 Step 4 logic discharges every L-invariant at a₂ by the same per-bullet argument as for b₁, with the substitutions: home(a₂) = d, subspace_I(a₂) = 2, zeros(a₂) = 3, #E(a₂) = 2, with sibling-stream chain (d, 2) ⟶ inc(·, 0) sweep ⟶ inc(d.0.2, 1) ⟶ two inc(·, 0) steps in A_{a₁}."

### Issue 2: Emit_K's Definition does not specify when fresh emissions enter A_K

**ASN-0086, Definition — Emit_K**: "The returned `(Σ', a)` satisfies `a ∉ dom(Σ.L)`, `a ∈ dom(Σ'.L)`, `home(a) = d`, and `Σ'.L(a) = (F, G, K)`."

**Problem**: The postconditions guarantee L_K^{Σ'} membership (immediate from the binding plus coverage(K) = coverage(K)) but are silent on A_K^{Σ'} membership. Under the Nullify-only discipline (Nullify uses unit-depth-span to-sets, R0a's antichain gives no link-prefix-extension), a fresh address `a` is automatically not in nullified(Σ') because no L_R tuple's coverage contains it. But the substrate permits *crafted-span retractions* — the ASN itself acknowledges these in Nullify's "Crafted-span retractions" remark — whose to-spans may have coverage that retroactively contains a freshly-emitted address. Under such retractions, the fresh tuple lands in L_K but is immediately excluded from A_K. Callers reasoning about "I just emitted; therefore the tuple is active" need to know this is conditional.

**Required**: Add a clarifying note in Emit_K's Definition along these lines: "Whether `(a, F, G) ∈ A_K^{Σ'}` is determined by `a ∈ nullified(Σ')`. Under the Nullify-only retraction discipline (all L_R tuples have unit-depth to-spans targeting existing link addresses), R0a's antichain property combined with the fresh allocation of `a` ensures `a ∉ nullified(Σ')` and therefore `(a, F, G) ∈ A_K^{Σ'}`. Under crafted-span retractions whose to-set coverage may extend to not-yet-allocated addresses, a fresh `a` may land within an existing L_R tuple's coverage and so enter `nullified(Σ')` immediately upon allocation; in this case `(a, F, G) ∈ L_K^{Σ'}` but `(a, F, G) ∉ A_K^{Σ'}`."

### Issue 3: R0a's relationship to the substrate emission primitive could be more cohesively stated

**ASN-0086, R0a and surrounding material**: The chain of reasoning that establishes R0a is distributed across several sections — "Substrate emission primitive (for `Emit_K`)" (defines the broader primitive), "Breadth of the primitive vs. the discipline R0a names" remark (notes the primitive permits emissions that would falsify R0a), "Implementation discipline — sibling-frontier link emission" (names the discipline), R0a's discipline-conditional statement and proof, R0a's Remark on udanax-green evidence, and Nullify's discipline assumption. Each section is internally clear but the cumulative dependency chain — substrate primitive permits broader emissions → discipline narrows them to sibling-frontier → R0a holds under discipline → Nullify single-tuple-scope inherits the conditionality — must be reconstructed by the reader.

**Problem**: This makes the discipline-conditionality of two important substrate properties (R0a's antichain, Nullify's single-tuple-scope) harder to verify than it should be. A reader who wants to confirm "Nullify behaves as advertised iff the implementation respects sibling-frontier emission" must traverse five sections of prose.

**Required**: At the head of R0a (or in a one-paragraph summary at the close of the "Implementation discipline" section), include an explicit dependency-chain summary: "The substrate emission primitive admits L1c-conforming emissions at any fresh address, including strict prefix-extensions of existing link addresses. The sibling-frontier discipline narrows admissible emissions to those constructed by R0 Step 2. R0a's antichain property holds for traces respecting the discipline; Nullify's single-tuple-scope inherits the conditionality. The udanax-green implementation respects the discipline; alternative implementations not adopting it would break R0a and Nullify's narrow-scope guarantee. The Open Questions section enumerates two routes to elevate the discipline to a substrate-level guarantee (tightening Emit_K's spec or tightening the substrate primitive itself)."

## OUT_OF_SCOPE

### Topic 1: Higher-arity links and their typed-relation analogue
**Why out of scope**: The ASN explicitly restricts attention to standard-triple links (|Σ.L(a)| = 3), and the Open Questions list captures this restriction. The generalization to L_K^{(n)} ⊆ A_rel × ℘(A)^n is a future ASN.

### Topic 2: Concurrent Emit/Observe consistency model
**Why out of scope**: The ASN is single-state-thread; concurrency semantics are flagged in Open Questions.

### Topic 3: Behavior under L14's native scoped form (without globally s_C-resident content)
**Why out of scope**: The Setup hypothesis is stated up front, and the Open Questions section explicitly traces what changes without it. Reformulating R0/R4/R5 slice-wise is a future ASN.

### Topic 4: Formal analysis of crafted-span retractions
**Why out of scope**: Acknowledged in Nullify's "Crafted-span retractions" remark as permitted by the substrate but outside Nullify's narrow form. Higher-layer policies handle the broader case.

VERDICT: REVISE
