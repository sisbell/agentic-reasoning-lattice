# Review of ASN-0071

## REVISE

### Issue 1: The depth-wise/breadth-wise contrast is articulated three times

**ASN-0071, "The query"**: The discrimination between permitted cross-depth subtree-capture (`#u < m`) and forbidden interior-action-point sibling-sweep is stated abstractly twice and then again concretely.

- First in the relaxation paragraph: "an action point *interior* to the span ... would let the displacement act on an interior prefix component, so `⟦σ⟧` would range across prefix structure and resolution would collect content positions the user never named."
- Again in the dedicated asymmetry paragraph: "What separates the two cases is precisely *which* component the displacement perturbs ... captures the *descendants* ... sweeps *sideways* ... Descending into a subtree realizes ... sweeping siblings ... collects content the user never named."
- A third time, concretely, in the worked scenario's "Interior action point, rejected against an arrangement."

**Problem**: The two abstract statements say the same thing in different words — the `review-mode.anti-bloat` "two paragraphs say the same thing" pattern. The concrete worked-scenario instance is legitimate (it is a concrete example against a live arrangement); the two abstract paragraphs preceding it are redundant with each other and with the example.
**Required**: Collapse the two abstract paragraphs into one statement of the rule (`actionPoint = #u` permits depth-wise descent, forbids breadth-wise sweep), and let the worked scenario carry the demonstration.

### Issue 2: Defensive justification framing the cross-depth case

**ASN-0071, "The query"**: "It is the intent, and the asymmetry with the action-point case is principled rather than an oversight" — followed by four LM citations (4/25, 4/23, 4/63) and the rhetorical "the question is whether collecting them is a defect or the intent."

**Problem**: "principled rather than an oversight" and "the question is whether collecting them is a defect or the intent" are defensive prose anticipating a reviewer's objection, not advancing the argument. This is the flagged "defensive justifications" pattern.
**Required**: State the operative claim plainly — coarse anchor names its whole subtree (cite Nelson once) — and drop the anticipatory hedging.

### Issue 3: The depth-1 counterexample is stated in two sections

**ASN-0071, "The query" and "Resolution"**: The counterexample `u = [s_C] = [1]`, `ℓ = [2]` is fully exhibited in "The query" ("Take `u = [s_C] = [1]` with `ℓ = [2]` ... Such a span straddles the content and link subspaces"), then re-explained in "Resolution" ("the counter-example `u = [s_C]`, `ℓ = [2]` exhibited above ... would silently include a link-subspace V-position").

**Problem**: The Resolution restatement re-derives the consequence already established. One full exhibition suffices.
**Required**: In "Resolution," reference the precondition discharge in one clause without re-explaining the counterexample.

### Issue 4: "Only content sharing can satisfy the predicate" states its conclusion twice

**ASN-0071, "The operation"**: The paragraph first derives `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ⊆ (dom(Σ.C) ∪ dom(Σ.L)) ∩ dom(Σ.C) = dom(Σ.C)` via set algebra, then immediately re-derives it elementwise: "More precisely, any `a` in the intersection lies in `iaddrs(Q)(Σ) ⊆ dom(Σ.C)`, so it cannot be a link image..."

**Problem**: Two derivations of the identical conclusion in adjacent sentences. The second adds no rigor the first lacks.
**Required**: Keep one derivation.

### Issue 5: PC totality sub-argument forward-references its own later step

**ASN-0071, "The query"**: The proof that `#t ≥ #u` reads: "either `t` agrees with `u` on its whole length ... or `t` first disagrees with `u` at some position `p ≤ #t < #u`, which the case-(i) argument below contradicts."

**Problem**: The totality argument leans on "the case-(i) argument below," which is presented afterward. The dependency is in fact non-circular (the case-(i) step at `p ≤ #t` needs only `t_p`, which exists), but the reader must reconstruct that to trust the order. A proof should not require the reader to verify its own forward references are acyclic.
**Required**: Either establish the case-(i) componentwise contradiction first and invoke it for both totality and the prefix claim, or inline the `p ≤ #t` instance where totality uses it.

### Issue 6: Repetitive composite-boundary narration in the worked scenario

**ASN-0071, "A worked scenario," Composite structure**: Composites 2, 4, and 5 each repeat near-identical text — "No fresh allocation ... so J0 is vacuous; ... range-new to `M(d_X)`'s content subspace, so J1★ forces ... and J1'★ matches/holds symmetrically."

**Problem**: Three boundaries discharge the coupling by the identical argument, restated verbatim. Stating the pattern once and noting the remaining boundaries discharge it identically would lose nothing.
**Required**: Give the J0-vacuous / J1★-forces argument in full once, then for the remaining transcluding composites state only the new I-addresses and that the same discharge applies.

## OUT_OF_SCOPE

### Topic 1: Relationship between `find`'s current result and the provenance relation `R`
**Why out of scope**: The ASN correctly defers the history-vs-currency reconciliation to a separate mechanism and lists it as an open question; specifying the `R`-based historical query is new territory.

### Topic 2: Visibility/access-control filtering and replica-divergent completeness
**Why out of scope**: The note explicitly leaves order, replica freshness, and access-control as policy layers overlaid on the unfiltered operation; these belong in separate specifications.

VERDICT: REVISE
