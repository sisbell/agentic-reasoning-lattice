# Review of ASN-0086

This is a mature ASN. The R0–R7 chain, the conformance machinery, the wp analysis, and the worked sketch are substantively sound — I checked R0a's two-case antichain argument, L-ContiguousPrefix's induction, R-Scope's arity-independence, the CoverageEqualityDecidable cell argument, and the worked sketch's tumbler arithmetic (a₁=1.0.1.0.1.0.2.1 through a₃=…2.5), and all hold. The findings below are the forward-reference/drift patterns the `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: P2 over-billed as a Nullify precondition; the "three named conditions" enumeration misrepresents the actual precondition structure
**ASN-0086, Definition — Nullify**: "Nullify carries three named conditions — P0: `d_retr ∈ dom(Σ.M)`, P1: `a ∈ A_rel^Σ`, P2: `|Σ.L(a)| = 3` — whose distinct roles the derivation below establishes rather than presupposes."

**Problem**: Two distinct drift symptoms in one sentence.

(a) P2 gates nothing. R-Scope (SingleTupleScope) proves single-tuple scope is *arity-independent* ("it holds equally when `a` is a higher-arity address"), and the definition itself states nullifying a higher-arity address "is a well-formed Emit_R that deposits `a` into `nullified(Σ')`." The wp Case 1 then confirms "P2 ... is consequently absent from the wp." So P2 is a scope remark given billing parallel to genuine conditions P0/P1 — exactly the "scope content dressed as a precondition" pattern.

(b) The enumeration is simultaneously *under*-inclusive: Nullify's correct execution and single-tuple-scope conclusion require Σ to be substrate-conforming (PC) — Emit_R is partial over state-local-conforming states and total only over the substrate-conforming sub-domain, and the wp Case 1 explicitly carries PC as a load-bearing conjunct. PC is a real precondition for the subsequent-emission branch to admit a K.λ-edge, yet it is omitted from the "three named conditions" while the non-gating P2 is included.

(c) "whose distinct roles the derivation below establishes rather than presupposes" announces that the roles will be derived downstream (wp Case 1) instead of stating them at the definition — the deferral pattern. This is reinforced by the parenthetical lower in the same definition: "(The wp Case 1 analysis below derives the gating roles of P0, P1, and P2.)"

**Required**: Demote P2 to a scope/observability remark (not a numbered "condition"), name the substrate-conformance precondition at the definition alongside P0/P1, and state the P0/P1 roles in place rather than deferring them to wp Case 1.

### Issue 2: The substrate-conformance/NestedLinkWitness partiality rationale is restated at three sites
**ASN-0086, Definition — Emit_K**: "`Emit_K` is *partial* over this sub-space and *total* over the substrate-conforming sub-domain: ... Remark — NestedLinkWitness exhibits a state-local-conforming Σ at which the subsequent-emission `inc(ℓ_prev, 0)` is off-chain, so no legitimate K.λ-edge exists and `Emit_K(Σ, d, F, G)` is undefined."
**ASN-0086, R0 statement**: "Over a merely state-local-conforming Σ this can fail (Remark — NestedLinkWitness permits an off-chain `ℓ_prev = inc(ℓ, 1)`, whose `inc(·, 0)`-successor is a child of `ℓ`, not a chain sibling, so no legitimate K.λ-edge need exist); substrate-conformance is exactly the hypothesis that excludes it ..."
**ASN-0086, wp Case 2 "The discipline alone is insufficient"**: "Witness a state-local-conforming but non-substrate-conforming Σ of the kind Remark — NestedLinkWitness constructs ..."

**Problem**: All three say the same thing in different words — off-chain `ℓ_prev` ⇒ no K.λ-edge ⇒ emission undefined/inadmissible over merely state-local-conforming states — each re-deferring to the same Remark. This is the "multiple paragraphs defer to the same downstream location" + "two paragraphs say the same thing in different words" pattern. A precise reader re-reads the identical rationale three times.

**Required**: Carry the rationale once (the Remark, or one of the three), and have the other sites cite it by name without restating the off-chain-edge argument.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity and Observe ordering
The Open Questions already park Emit/Observe atomicity, consistency model, and Observe ordering. These are genuinely future territory, not gaps in this ASN.

### Topic 2: Higher-arity typed relations `L_K^{(n)}`
The note explicitly restricts to standard-triple links; the n-ary projection question belongs to a future ASN, as the Open Questions note.

VERDICT: REVISE
