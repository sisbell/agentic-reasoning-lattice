# Review of ASN-0042

## REVISE

### Issue 1: T8 is misattributed for Σ.B monotonicity

**ASN-0042, multiple proofs and table entries** (O3, O8, PrefixBaptismCoupling, AccountLevelPermanence★ — and corresponding rows in *Properties Introduced*): "By T8 (AllocationPermanence), Σ_n.B ⊆ Σ_{n+1}.B" and similar formulations; table entries list "from T8, O12, O13, ..." as the dependency.

**Problem**: T8 in ASN-0034 (AllocationPermanence) establishes `allocated(s) ⊆ allocated(s')` — monotonicity of the *allocator-domain union*. It does not state `Σ.B ⊆ Σ'.B`, which is *baptismal-registry* monotonicity. The two sets coincide under ASN-0040's Bridge1/Bridge2, but as foundation properties they are formally distinct, and the proofs cited here actually need the registry statement, not the activation statement. The misattribution obscures the foundation chain that the proof depends on.

**Required**: Cite ASN-0040's B0 (Irrevocability) — `(A Σ, Σ' : Σ → Σ' : Σ.B ⊆ Σ'.B)` — or B0★ (MultiStepIrrevocability) for the multi-step form, in place of T8 throughout the four proofs and the corresponding *Properties Introduced* rows. T8 may remain only at sites that legitimately need allocator-domain monotonicity (none of the current ones do).

### Issue 2: Worked example invokes B1 to force ancestor baptisms it does not actually force

**ASN-0042, Worked Example, "Fork (O10)" subsection**: "the document addresses [1, 0, 2, 0, 1], [1, 0, 2, 0, 2], [1, 0, 2, 0, 3], [1, 0, 2, 0, 4], [1, 0, 2, 0, 5] are all in Σ_pre.B (B1 ContiguousPrefix forces the slots between any used document indices to be present). In particular, the document parents of the earlier element baptisms are in Σ_pre.B: [1, 0, 2, 0, 3] (the document parent of a₁) and [1, 0, 2, 0, 5] (the document parent of a₂)."

The same pattern appears in the field-opening boundary discussion: "B1 (ContiguousPrefix) of ASN-0040 forces [1, 0, 2, 0, 1], [1, 0, 2, 0, 2], [1, 0, 2, 0, 3] ∈ Σ_1.B, so hwm(Σ_1.B, [1, 0, 2], 2) ≥ 3 ≠ 0."

**Problem**: B1 establishes intra-stream contiguity — within a single stream `S(p, d)`. From `a₁ = [1, 0, 2, 0, 3, 0, 1] ∈ Σ.B` (c_1 of `S([1, 0, 2, 0, 3], 2)`) B1 does not conclude `[1, 0, 2, 0, 3] ∈ Σ.B` (c_3 of the *different* stream `S([1, 0, 2], 2)`). ASN-0040's Bop has B6 as its only precondition, requiring T4 validity of the parent prefix but not its presence in Σ.B, so an element address can in principle be baptized without its document parent being baptized. The example silently assumes a level-order baptism discipline that ASN-0040 does not enforce. The argument that the field-opening branch (hwm_0 = 0) is "incompatible" with Σ_1 collapses without that discipline.

**Required**: Either (a) replace the worked example with allocations whose hwm values follow directly from the listed baptisms without invoking a document-parent baptism — e.g., have π_N baptize [1, 0, 2, 0, 1] through [1, 0, 2, 0, 3] explicitly pre-delegation, then a₁ separately; (b) attribute the intermediate document baptisms to explicit Bop calls in π_N's pre-delegation history and π_A's post-delegation history, citing B1 only for the slots strictly between explicit baptisms; or (c) introduce (or import, if available in ASN-0040) a derived property establishing that an element baptism implies its document parent is in Σ.B, and cite that property.

## OUT_OF_SCOPE

(None — the ASN respects its declared scope boundaries. Ownership transfer, cross-domain enforcement, owner-disappearance behavior, domain density, cross-node federation, provenance-vs-effective-owner divergence, and delegation event recording are all properly deferred to Open Questions.)

VERDICT: REVISE
