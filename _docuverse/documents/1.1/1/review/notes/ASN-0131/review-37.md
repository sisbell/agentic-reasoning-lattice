# Review of ASN-0131

I checked the operation against its definition, verified the worked instance by hand (the field-agreement argument for `coverage(e₃) ∩ dom(Σ.C) = ∅`, the touch tests, the `RE = {(1, e₁)}` result), and traced the four derived results — RE-UDIST, RE-SEL, RE-CWP, RE-RET. The mathematics is sound: the wp derivation in RE-CWP correctly reduces "unchanged" to "no available pair dropped" (`coverage(e) ∩ Δ ≠ ∅ ⟹ coverage(e) ∩ I_R ≠ ∅`), the `R = ∅` collapse is right, the RE-RET forward/backward halves are correctly conditioned (forward on the `coverage(Θ)` hypothesis, backward on R-Scope/R0a), and the ASN-0086→ASN-0047 bridge is load-bearing, not filler. Edge cases (empty image, no addressable links, empty slot, `R = ∅`, sole-bearer) are all covered. The note specifies an operation, its answer-invariants, and its stability under the transition vocabulary — it has not drifted into implementation mechanics.

One finding remains: accreted consistency meta-prose around a forward reference, which is exactly the accumulation this review cycle targets.

## REVISE

### Issue 1: Consistency cross-commentary appended to a self-complete argument
**ASN-0131, "Stability: the answer as the document is edited" (link-subspace-confined paragraph) and the RE-EDIT row of the Claims table**:
- prose: "...so `I_R = image(W, d, Σ)` and `Δ = ∅`, whence the weakest precondition holds vacuously — **the prose and RE-CWP agree**."
- table: "The contraction member is precisely RE-CWP's `Δ = ∅` instance (no content position dropped), **consistent with it**."

**Problem**: The link-subspace-confined stability is already established, in full, by the direct argument earlier in the same paragraph: under `W ⊆ s_C` the link-only edit leaves `W ∩ dom(Σ.M(d)) = W ∩ V_{s_C}(d)` and hence the content image unchanged, and frames `Σ.L` so `Avail` is fixed — giving `RE(W, d, Σ') = RE(W, d, Σ)` outright. The trailing clause then forward-references RE-CWP (defined in a later subsection), re-derives the vacuous-wp conclusion, and asserts internal consistency. The assertion "the prose and RE-CWP agree" — echoed by the table's "consistent with it" — is meta-commentary about the document's own coherence, not a fact about the system. If the link-only contraction *is* RE-CWP's `Δ = ∅` instance, consistency follows automatically; stating it adds nothing a precise reader needs, and it is stated twice (prose + table). This is consistency-meta-prose of exactly the kind that compounds across cycles.

**Required**: Drop "— the prose and RE-CWP agree" and the table's "consistent with it." The `Δ = ∅` *connection* itself may stay as a bare one-clause cross-link if it earns its place, but the agreement/consistency assertions should go. (The narrative forward-pointers elsewhere — "as we shall see" in the per-endset property and in the soundness paragraph — are milder instances of the same habit; tightening them in the same pass would be welcome, but they are not individually blocking.)

## OUT_OF_SCOPE

No out-of-scope violations. The ASN cites only the provided foundations, names sibling operations (FINDLINKSFROMTOTHREE, the FEBE realiser) by name for contrast rather than as dependencies, and confines new territory — rendering into V-order (OQ3), intersection-distributivity (OQ4), non-co-resident link stores (OQ5), type-slot/content matches (OQ6), link-subspace regions (OQ7) — to open questions rather than claims. The provisional status of RE-WHOLE (deferred to OQ1) is handled correctly.

VERDICT: REVISE
