# Cone Review — ASN-0034/TA6 (cycle 2)

*2026-04-17 14:51*

### T4 Preconditions omits the inter-consequence dependency chain
**Foundation**: T4 (HierarchicalParsing), Formal Contract *Preconditions*.
**ASN**: T4 body prose establishes two dependencies among its three consequences:
- For T4b: "T3 (CanonicalRepresentation) supplies the rigidity of component values that licenses uniqueness, **and T4a supplies the segment-non-emptiness reading that the case analysis consumes**".
- For T4c: "**T4b's identification of zeros with separators supplies the equality between `zeros(t)` and the separator count**, so the number of fields present is `zeros(t) + 1`".

T4's Formal Contract *Preconditions* lists only: "T4b (UniqueParse) requires T3 (CanonicalRepresentation)".
**Issue**: The body prose declares T4b depends on T4a, and T4c depends on T4b, but the Preconditions field records neither edge. A downstream ASN reading only T4's Formal Contract cannot reconstruct the DAG among T4a/T4b/T4c that the body narrates; conversely, a reader of the body cannot confirm the dependencies are load-bearing because the contract treats T4a and T4c as preconditions-free. If the contract is canonical, either the body overclaims dependencies that the proofs don't actually need, or the contract understates what T4b and T4c consume. Either resolution changes how downstream citations to T4b and T4c must be discharged.
**What needs resolving**: Reconcile body and Preconditions. Either (a) extend T4's Preconditions to record that T4b additionally requires T4a and that T4c requires T4b (matching body prose), or (b) revise the body prose in the T4a/T4b/T4c framing paragraphs to remove appeals to T4a-as-premise-of-T4b and T4b-as-premise-of-T4c if those appeals are not genuine proof dependencies.

### T4's `fields(t)` is asserted well-defined but never defined in T4's exported content
**Foundation**: T4 (HierarchicalParsing), Formal Contract *Axiom* and *Postconditions* (T4b).
**ASN**: T4 body prose refers to "the field-parsing function `fields(t)`" and, in the T4b framing, "the partial function `fields(t)` decomposing a T4-valid tumbler into its node, user, document, and element sub-sequences". T4b's Postcondition states: "the function `fields(t)` that extracts node, user, document, and element fields is well-defined and uniquely computable from `t` alone." T4's Axiom enumerates only the positional conditions (`zeros(t) ≤ 3`, no-adjacent-zeros, boundary non-zeros), the separator biconditional, and the canonical written form — it never defines `fields(t)`.
**Issue**: `zeros(t)` is defined explicitly in body prose; `fields(t)` is not. T4b claims uniqueness of a function whose domain (all `t ∈ T` vs. only T4-valid tumblers), codomain (fixed 4-tuple vs. variable-arity tuple indexed by `zeros(t) + 1`), and action (exactly how the split is computed) are never fixed in any exported clause. "Well-defined" is meaningless without a candidate definition to verify against. A downstream ASN citing T4b for `fields(t)` finds an unspecified function at the end of its citation chain. The gap is not resolved by noting that T4b.md proves the result: the object being proved well-defined must be stated in the foundation's exported contract for downstream ASNs to cite it.
**What needs resolving**: Either (a) add a Definition clause to T4's Formal Contract that specifies `fields(t)` — its domain (T4-valid addresses), its codomain (likely a tuple whose arity depends on `zeros(t)`), and its action (split the component sequence at zero positions) — so that T4b's well-definedness claim has a defined object; or (b) relocate `fields` to T4b's own contract if T4b is where the function is first defined, and revise T4's body prose so it does not rely on `fields(t)` before T4b introduces it.
