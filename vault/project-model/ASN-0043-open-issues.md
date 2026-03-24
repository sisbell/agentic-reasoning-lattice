No open issues. All audit and review issues resolved through revisions 28–29.

### In the "Endset Structure" section, the motivating text for hierarchical type classification cites T6 for the claim that 
**Source**: consistency check (ASN-0043)

In the "Endset Structure" section, the motivating text for hierarchical type classification cites T6 for the claim that "tumbler containment is decidable":

> "Because tumbler containment is decidable (T6, ASN-0034), type addresses support hierarchical relationships: a type at address `p` and a subtype at an address extending `p` are related by prefix ordering."

T6 (DecidableContainment) establishes decidability for four specific questions: whether two tumblers share the same node field (a), node+user fields (b), node+user+document-lineage fields (c), and whether the *document field* of one is a prefix of the *document field* of the other (d). T6 does not cover element-field prefix containment — the relevant relationship for type hierarchies, where type addresses are element-level tumblers. For `p = 1.0.2.6` and `c = 1.0.2.6.2`, the question "is `p` a prefix of `c`?" involves the full tumbler, not the document field; T6(d) covers document-field prefix containment specifically and does not extend to this case. The correct foundation citation for this claim is T2 (IntrinsicComparison) — comparison is computable from the tumblers alone — combined with the PrefixRelation definition. The formal proof of L10 itself is unaffected (it relies on T5 and PrefixSpanCoverage, not T6), but the motivating citation misapplies T6's stated scope.

### 2e. Scope Narrowing in Citations

(none)

### 3. Structural Drift

T4 field notation (`N.0.U.0.D.0.E`), `zeros(t)`, `fields(t)`, and the `origin` formula all match current foundation definitions. The subspace designation via `E₁` in L0 is consistent with ASN-0036's `subspace(v) = v₁`. No outdated content.

(none)

### 4. Missing Dependencies

All cited properties trace to ASN-0034 or ASN-0036, both in the declared depends list. No undeclared dependency.

(none)

### 5. Exhaustiveness Gaps

L14 (DualPrimitive) claims only two categories of stored entity. The state is defined as `Σ = (Σ.C, Σ.M, Σ.L)` with arrangements `Σ.M(d)` explicitly not storing entities. The claim "no third category" is grounded in the state definition. S3 restricts arrangements to content addresses; L0 excludes link addresses from content; the exhaustiveness follows definitionally.

(none)

### 6. Registry Mismatches

All properties in the table verified against body text: `introduced` entries contain new content; none listed as `cited` (so the converse does not apply). L4 (LEMMA) follows from L3 by definitional unpacking — the body explains this explicitly. L7 (META) is a meta-statement with no formal proof; the type META is non-standard but internally consistent. PrefixSpanCoverage (LEMMA) has a complete formal proof. No mismatch between registry status and body treatment.

(none)

### `home(a)` applies the `origin` formula outside `origin`'s stated domain
**Source**: consistency check (ASN-0043)

`home(a)` applies the `origin` formula outside `origin`'s stated domain.

The foundation (ASN-0036, Definition — Origin) defines:

> `origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)` for every `a ∈ dom(Σ.C)`.

ASN-0043 introduces `home(a)` using the identical formula for `a ∈ dom(Σ.L)`:

> "This is the same formula as `origin` (ASN-0036), applied here to link addresses rather than content addresses."

This applies the `origin` formula to a domain (`dom(Σ.L)`) outside `origin`'s stated domain (`dom(Σ.C)`). The registry correctly says `introduced`, and the ASN provides justification (T4, L1, L1a). Per Category 2a this is a finding regardless.
