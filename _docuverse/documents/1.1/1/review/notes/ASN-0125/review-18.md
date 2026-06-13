# Review of ASN-0125

I checked the central immutability argument (EL0–EL3), the layer machinery (Df-CLS through EL-DM), both operations (assert_sup/EL6, editlink/EL7), and the consequence claims (EL8–EL16) against the foundations. The wp argument for EL0, the single-target lemma EL4, the contextual/archival discovery split EL11, the temporal-erasure commutation EL13, and the empty-current standoff EL14(c) all check out, including the boundary cases (empty store Σ₀ in EL-DM, first/last/only link in EL9(2), 2-cycle in EL14(c)). The K.λ-only-composite reachability argument is sound, and no improper cross-ASN references appear (every cited ASN is a foundation). One definitional inconsistency and one minor accretion item remain.

## REVISE

### Issue 1: The editing-layer discipline commitment contradicts editlink's own `[R]`-emission capability

**ASN-0125, Df-LAY (EditingLayer)**: "every `[K_sup]` emission through `assert_sup` or `editlink` (under `DC`), every `[R]` emission through `Nullify`."

**Problem**: The commitment pins each disciplined class to its routing operations. For `[K_sup]` it correctly lists *two* routes (assert_sup, editlink). For `[R]` it lists only Nullify — but editlink is equally an `[R]` route. EDITop's precondition `DC(ℓ')` explicitly provides for a retraction-class successor: "if `coverage(ℓ'.e₃) = coverage(R)`, then `(E t ∈ dom(Σ.L) : ℓ'.e₂ = {(t, δ(1, #t))})`", and EL7(iv) explicitly describes the case "(When `ℓ'` is itself a disciplined retraction, step 1 additionally performs exactly that retraction's declared single-target effect…)". So editlink's step-1 K.λ can grow the retraction slice `L_R`.

Read against the model this commitment imports (ASN-0086's RelationalLayer: "every `→`-step … with `L_R^Σ ⊊ L_R^{Σ'}` … is a `Nullify`"), editlink's atomic step-1 `→`-step grows `L_R` without being a Nullify. The layer therefore violates its own stated commitment — the layer as defined is internally inconsistent. The asymmetry between the `[K_sup]` line (two routes) and the `[R]` line (one route) is the defect; nothing in the ASN justifies editlink being a disciplined route for `[K_sup]` but not for `[R]` when DC's retraction clause governs both symmetrically.

This does not break the proofs — EL-DM maintains edit-discipline through EL7(vi), which relies on DC forcing unit-depth shape (Df-DISC clause i), not on the commitment's exhaustiveness. But the inconsistency matters for anything built on this ASN: a downstream consumer reading "every `[R]` emission through Nullify" would wrongly conclude every retraction tuple originates from Nullify, when editlink-under-DC produces them too.

**Required**: Widen the `[R]` line to "every `[R]` emission through `Nullify` or `editlink` (under `DC`)", parallel to the `[K_sup]` line — the proofs survive unchanged, since DC forces unit-depth shape on editlink's `[R]` successors (EL7(vi)). Alternatively, if editlink is *not* meant to emit retraction successors, remove DC's retraction clause and the EL7(iv) retraction case (contradicting EL8(d)'s "`editlink` applies to a claim, `DC` permitting"). Fix both occurrences: the Df-LAY body and the matching Df-LAY row of the Claims Introduced table, which repeats the same one-sided routing.

### Issue 2: Use-site inventory in "K.λ-only composites are valid" (anti-bloat)

**ASN-0125, preamble ("K.λ-only composites are valid")**: "so `assert_sup`'s `Σ'` and `editlink`'s `Σ₁` and `Σ₂` are reachable states at which the lifted invariants (R0a, L12, the per-state package, ASN-0086's `wp` results) apply."

**Problem**: The claim this sentence establishes is *reachability* of the operation outputs. The trailing parenthetical pre-catalogs which downstream invariants will be invoked (R0a, L12, the per-state package, the wp results) — a use-site inventory that does not advance the reachability argument and is redundant with the invocations at each actual site (R0a in EL4/EL6/EL11; L12 throughout; wp in EL6/EL7). A reader following the reachability claim must skip past the catalog. (By contrast, "Vocabulary fact V" is a genuine proof-by-cases of a repeatedly-used fact, not an inventory — it should stay.)

**Required**: End the sentence at "reachable states" (or "reachable states, so the lifted invariants apply there"); drop the parenthetical roster, letting each invariant be named where it is used.

VERDICT: REVISE
