# Review of ASN-0099

I read the ASN against its own definitions and the listed foundations. The core comprehension (`findlinks`), the two-phase factoring (F12), the conformance pairs (F2/F3 and variants), determinism (F8), the survivability family (F9/F9★/F9-λ), monotonicity (F19), and the worked example all check out. The realizability discharge for F4 (Strengthenings 1–3, Weakenings 1–2) is genuinely load-bearing and each witness verifies: I confirmed Strengthening 1's `α.0 ∈ {t : α ≼ t} ∖ {α}`, the all-slots-populated requirement, and the empty-slot vacuity argument; Strengthenings 2–3 correctly place the witness at slot 3 (L3) with slots 1/2 empty. F10a's Case (ii) zero-counting (M0 + T4 + Prefix + T0-discreteness) is sound, and the PrefixOrderingExtension lift to cross-document link ordering holds. The K.σ-exclusion argument (this ASN inhabits ASN-0047's extended-state vocabulary, document registration via K.δ Document-case) is consistent with the op counts.

I found one issue.

## REVISE

### Issue 1: K.α (ContentAllocation) is labeled a "non-allocating operation"
**ASN-0099, "Arrangement Independence"**: "All six atomic non-allocating operations list `L' = L` in their published frames. For four of them ({K.α, K.δ, K.μ⁺_L, K.ρ}) this is immediate."

**Problem**: K.α is `ContentAllocation` — it *is* an allocation operation (it extends `dom(C)`). Grouping it under "non-allocating operations" is a direct terminological contradiction. The shorthand "non-allocating" is used repeatedly and consistently to mean "does not modify the link store" (i.e., everything in `V ∖ {K.λ}`): the lemma names `A1 (LinkStoreInertOfNonAllocatingOperations)`, `F9-cor (NonAllocatingPreservation)`, `F9★ (NonAllocatingMultiStepPreservation)`, and the closing open question "the non-allocating fragment of its operation vocabulary" all carry this intended reading. But the term is never defined, and it clashes with K.α's own name. A reader tracking precision would reasonably expect an allocation operation to be *excluded* from "non-allocating operations," when the spec in fact includes it — the formal content (the lemma ranges over `V ∖ {K.λ}` and states "K.λ is the unique operation of V that modifies the link store") is unambiguous, but the English label misdescribes it.

**Required**: Rename the shorthand to "non-link-allocating" (or "link-store-inert," matching the A1 lemma title) wherever "non-allocating" currently appears, or introduce an explicit one-line definition at first use pinning "non-allocating" to "modifies neither nothing — specifically does not modify `Σ.L`; equivalently `V ∖ {K.λ}`." The formal claims need no change; this is a precision fix on the prose label so it stops contradicting `K.α = ContentAllocation`.

## OUT_OF_SCOPE

None. The deferred topics in "What We Have Not Specified" and "Open Questions" (partition tolerance, consistency models, access control, the inverse FOLLOWLINK direction, timing bounds, out-of-store query semantics) are correctly identified as future territory, and the operation is total over `I ⊆ T` regardless of whether `I` lands in `dom(C) ∪ dom(L)`, so no definedness gap remains.

VERDICT: REVISE
