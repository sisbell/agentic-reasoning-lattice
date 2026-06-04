# Review of ASN-0087

## REVISE

### Issue 1: Inconsistent foundation attribution for M1 (ArrangementMonotonicity)

**ASN-0087, Inputs / Weakest Precondition for Discoverability**: Inputs states "We write `dom(M)` throughout for the set of allocated documents (`dom(M) = E_doc` by M1, ArrangementMonotonicity, **ASN-0047**)." The wp section then states "M1 (**ASN-0093**) supplies only the inclusion `dom(Σ.M) ⊆ dom(Σ'.M)`."

**Problem**: M1 (ArrangementMonotonicity) is defined identically in *both* ASN-0047 and ASN-0093, and the note cites different foundations for it in different sections without noting they coincide. A precise reader hits two different provenances for the same-named predicate and must stop to reconcile which M1 is canonical and whether they differ (only ASN-0047's M1 carries the `dom(M) = E_doc` note; ASN-0093's carries only the inclusion). The membership-equality argument in the wp section leans on this distinction silently.

**Required**: Cite one canonical M1 (or state once that the two foundations' M1 coincide and which clause — the `E_doc` identity vs. the bare inclusion — each use needs), and make the citation uniform across the document.

### Issue 2: The v_ℓ positioning rule is restated in full across multiple sections

**ASN-0087, Effect and M-Effect (Claims Introduced)**: The empty/non-empty case split for `v_ℓ` — "`v_ℓ = [s_L, 1]` at depth 2 if `V_{s_L}(d) = ∅`, else `shift(max(V_{s_L}(d)), 1)` at depth `m_L(d)`" — is given verbatim in the Effect section and again, near-identically, in the M-Effect claim, after already being introduced under M-DepthConv (Inputs) and re-derived in both the D-SEQ★ and D-MIN★ proofs.

**Problem**: This is the same construction stated in different words in adjacent structural slots (Effect prose ↔ M-Effect claim). The proof-site restatements (D-SEQ★, D-MIN★) are load-bearing and should stay, but the Effect/M-Effect pair duplicates without advancing the argument — the reader re-parses the identical case split twice. This is the anti-bloat pattern the note's classifier targets.

**Required**: State the positioning rule once as the operation's effect; have M-Effect name the effect and point to it rather than re-spell the case split. Keep the proof-site uses.

### Issue 3: Reflexive worked variant does not flag that it exercises non-standard authoring

**ASN-0087, A Worked Example (Reflexive variant)**: The variant replaces `e₁` with `e₁' = {(ℓ, δ(1, #ℓ))}` so that `ℓ ∈ coverage(e₁')`, firing the reflexive disjunct.

**Problem**: The ASN earlier establishes (M-FreshExcl, M-Reflexive) that under `StandardAuthoring(eᵢ, Σ)` the reflexive route is *structurally excluded*, because `ℓ` is fresh and a standardly-authored endset cannot cover it. The reflexive variant therefore necessarily violates standard authoring (its endset covers the unallocated `ℓ ∈ F`), but the worked example does not say so. As written, the example appears to coexist with the standard-authoring discipline rather than illustrating its boundary.

**Required**: One sentence noting the reflexive variant is the non-standardly-authored case (its endset pre-emptively covers the fresh `ℓ`), tying the concrete example back to the M-Reflexive / standard-authoring distinction.

## OUT_OF_SCOPE

None beyond the Open Questions already enumerated; those (forward-reaching endset well-formedness, deferred-consistency model, ghost-type limiting case, intermediate-state visibility) are correctly posed as future-ASN territory rather than defects here.

VERDICT: REVISE
