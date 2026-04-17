# Cone Review — ASN-0034/T10a-N (cycle 1)

*2026-04-16 20:23*

### T10 contract omits all dependencies
**Foundation**: N/A (internal)
**ASN**: T10 (PartitionIndependence), *Formal Contract* block — lists only Preconditions and Postconditions; no Depends field.
**Issue**: The proof invokes (a) the Prefix definition four times ("Prefix gives `aᵢ = p₁ᵢ`…", "the definition of ≼ (Prefix) requires `p₂ᵢ = p₁ᵢ`…") and (b) T3 explicitly ("by the reverse direction of T3 (tumblers that differ in any component are distinct), `a ≠ b`"). Both are load-bearing for the conclusion `a ≠ b`, yet neither appears in a Depends list. This breaks the per-step citation convention Prefix and T1 establish, where each forward/backward reference is enumerated with the point of use.
**What needs resolving**: Declare Prefix and T3 (and any T0 facts, e.g. the least-element construction used to name `k = min{j : …}`) as explicit dependencies of T10, matched to the proof steps that invoke them.

### T10a-N references an undefined discipline
**Foundation**: N/A (internal)
**ASN**: T10a-N (AllocatorDisciplineNecessity) — "Relaxing the `k = 0` restriction for siblings permits prefix nesting" and precondition note "the `k = 0` sibling restriction is relaxed for the second step".
**Issue**: The ASN nowhere states a rule that allocators must use `k = 0`, nor defines what "sibling restriction" is being relaxed. TA5 presents `k = 0` (sibling) and `k > 0` (child) as two legitimate modes of `inc`, with no normative statement that one is mandatory for any allocator context. The example then uses `inc(t₁, 1)`, which by TA5(d) is a child construction, not a "relaxed sibling" — so the demonstrated nesting `t₁ ≼ t₂` is just the defining property of child creation (every `inc(t,k)` with `k>0` produces an extension of `t`), not evidence of a violated discipline.
**What needs resolving**: Either state the allocator-discipline rule that T10a-N is claimed to justify (so "relaxing" has a referent), or re-frame T10a-N so its content matches what the proof actually establishes — that two successive `inc` calls can produce addresses one of which is a prefix of the other, disqualifying them as a non-nesting pair for T10.

### TA5 Depends omits T0 despite ℕ-level reasoning
**Foundation**: N/A (internal)
**ASN**: TA5 (HierarchicalIncrement), *Formal Contract* — "Depends: T1 (LexicographicOrder). TA5-SIG (LastSignificantPosition)".
**Issue**: TA5's construction sets components to the ℕ constants `0` and `1` (field separators, first child) and its verification of (a) for `k = 0` uses `n + 1 > n` on ℕ. Under the per-step citation convention made explicit in T1's Depends ("invokes the strict-total-order structure of `<` on ℕ that T0 enumerates, namely irreflexivity…"), these ℕ facts should be tied to T0. T0 is absent from TA5's Depends.
**What needs resolving**: Add T0 (CarrierSetDefinition) to TA5's Depends and cite the specific ℕ facts used (successor inequality for (a), designated constants `0` and `1` for the child construction), or justify why TA5 may leave these implicit while T1 cites them explicitly.
