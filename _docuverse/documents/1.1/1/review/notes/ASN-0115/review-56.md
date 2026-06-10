# Review of ASN-0115

## REVISE

### Issue 1: The repeatability/citation rationale claims editing never mutates an existing arrangement — contradicting the substrate and this ASN's own R11

**ASN-0115, R7 (Repeatability)**: "Editing produces a *new* version (a new document tumbler with its own arrangement) rather than mutating an existing one, so 'the same spec-set against the same version' is always a well-defined, reproducible request — the foundation of permanent citation."

**Problem**: This is false against the substrate ASN-0115 builds on, and against ASN-0115 itself.

- ASN-0047 provides K.μ⁻ (ArrangementContraction), K.μ⁺ (ArrangementExtension), and K.μ~ (ArrangementReordering), each operating on an **existing** `d ∈ E_doc` and changing `Σ.M(d)`. P3 (ArrangementMutabilityOnly) states outright that M is the component that "can lose information." So a fixed document tumbler `d` does **not** carry a fixed arrangement; in-place editing is permitted.
- The ASN's own **R11 worked instance** does exactly this: "Now contract `d`'s arrangement by K.μ⁻ (ASN-0047), removing the binding of `v_d`: the post-state `Σ'` has `v_d ∉ dom(Σ'.M(d))`." R11 even labels K.μ⁻ "deletion" — a form of editing — and shows it mutating `d` in place. So R7 says editing never mutates an existing arrangement while R11 demonstrates deletion mutating one.
- Consequently "the same spec-set against the same version" is **not** unconditionally reproducible: if `d`'s arrangement was edited between two observations, the delivery changes. This is precisely why R7's *formal* statement is (correctly) conditioned on `Σ.M(dⱼ)|⟦σⱼ⟧ = Σ'.M(dⱼ)|⟦σⱼ⟧`. The prose contradicts the hypothesis the proof actually needs.
- R4 carries the same defect: "In Xanadu the dilemma largely dissolves… Current and as-it-stood coincide because the binding consulted is the one the address selects." Under in-place editing, current ≠ as-it-stood; the dilemma is *resolved in favor of current*, not dissolved. The appeal to "permanent tumbler address" (4/19) is also misapplied — permanence belongs to **I-addresses** (content, S0), whereas a V-spec cites **V-positions**, which are arrangement-relative and rebindable.

**Required**: Correct the R4/R7 prose to match the formal content: a document's arrangement is mutable (K.μ⁻/K.μ⁺/K.μ~), so RETRIEVEV always delivers the *current* `Σ.M(d)`; repeatability holds exactly when the consulted restriction is unchanged (R7's hypothesis), which a caller secures by citing a version it does not subsequently edit. The permanent-citation guarantee is the immutable content store (S0) — the bytes at an I-address never change — not an impossibility of in-place arrangement editing.

### Issue 2: The override rationale asserts it "only bites shallow" without justifying the deep-start case

**ASN-0115, §"What a spec-set is" (act override rationale)**: "so the override only *bites* when the start has gone too shallow (`#s < m_S(d)`), forcing empty lest the intersection capture deeper content the citation never named."

**Problem**: The override forces `act = ∅` on **any** mismatch `#s ≠ m_S(d)`, which includes the deep case `#s > m_S(d)`. The discontinuity argument (the `m_S(d) = 3`, `[S,1]`-vs-`[S,2]` micro-example) only justifies the *shallow* sub-case. The parenthetical "only bites when `#s < m_S(d)`" silently asserts that the deep sub-case is benign — i.e. that `#s > m_S(d) ⟹ dom(Σ.M(d)) ∩ ⟦σ⟧ = ∅`, so force-empty discards nothing the geometric intersection would have found. That assertion is load-bearing (if false, the override would discard legitimately-named deep-start content by design) and is non-trivial (it needs the Confinement lemma plus a prefix-ordering step), yet no argument is given. This is a claim presented as proven prose with the proof omitted.

**Required**: Supply the one-paragraph deep-case argument or soften the claim. The argument: for `#s > m_S(d)`, Confinement gives `p ≼ t` for every `t ∈ ⟦σ⟧` with `p` the length-`(#s−1)` prefix of `s`, so `#t ≥ #s−1 ≥ m_S(d)`; a bound subspace-`S` position has depth exactly `m_S(d)` (S8-depth), so it can lie in `⟦σ⟧` only when `#s = m_S(d)+1`, and even then `#t = m_S(d) = #p` forces `t = p ≺ s`, hence `t < s` (T1 case (ii)), excluding it from `⟦σ⟧`. So the geometric intersection is already empty for every `#s > m_S(d)`, and force-empty is harmless there. One sentence to this effect closes the rationale.

## OUT_OF_SCOPE

The Open Questions section already defers the genuinely-future territory cleanly — straddling (non-ordinal) spans, dangling references under relaxed S3★, channel faithfulness, inline provenance, and fail-whole-vs-partial — and each is matched by a precondition or frame limit in the body (ordinal-level requirement, S3★ reliance, R2 frame limit). These deferrals are correctly placed; I am not asking for any of them to be pulled into this ASN. No new out-of-scope topic surfaced.

VERDICT: REVISE
