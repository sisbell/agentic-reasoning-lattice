# Cone Review — ASN-0034/T10a-N (cycle 2)

*2026-04-16 20:31*

### Prefix contract omits T0 despite using carrier-level operators
**Foundation**: N/A (internal)
**ASN**: Prefix (PrefixRelation), *Formal Contract* — "Depends: T3 (CanonicalRepresentation) — the derived postcondition `p ≺ q ⟹ #p < #q` invokes T3…".
**Issue**: The Prefix definition `p ≼ q` iff `#p ≤ #q ∧ (∀i : 1 ≤ i ≤ #p : qᵢ = pᵢ)` uses length `#p`, `#q` and component projection `pᵢ`, `qᵢ` — operators that T1 and TA5 explicitly attribute to T0 in their own Depends fields ("the definition uses length `#a` and component projection `aₖ` for `a ∈ T`, which T0 introduces"). The derived postcondition also reasons about `#p ≤ #q` and the case `#p = #q` via ℕ-ordering. T0 is nonetheless absent from Prefix's Depends, so Prefix breaks the per-step citation convention it otherwise appeals to when citing T3 forward.
**What needs resolving**: Either add T0 (CarrierSetDefinition) to Prefix's Depends with citations matched to the uses of `#·`, component projection, and ℕ-ordering, or justify a uniform exception that applies to Prefix but not T1/TA5.

### T10a-N cites T10a.6 without exposing the subclause
**Foundation**: N/A (internal)
**ASN**: T10a-N (AllocatorDisciplineNecessity), proof — "Under T10a the nesting is harmless because `t₂ = inc(t₁, 1)` would be the base address of a child allocator in a separate domain — **T10a.6 places parent and child disjointly**".
**Issue**: The argument relies on a specific subclause T10a.6 ("parent and child disjointly") to explain why the construction is harmless under T10a but pathological under the relaxation. The Depends field only names T10a as a whole ("supplies the `k = 0` sibling restriction whose relaxation this argument considers"), giving the reader no pointer to T10a.6's content and no way to check that the subclause exists or says what is claimed. The other ASNs in the document cite subclauses by label when they are load-bearing (e.g., "TA5(b)", "TA5(d)", "T1 case (i)").
**What needs resolving**: Either enumerate T10a.6 in Depends with a one-line paraphrase of its content (matching the subclause-citation style used for TA5 and T1), or restructure the proof so it does not depend on an unexposed subclause of T10a.
