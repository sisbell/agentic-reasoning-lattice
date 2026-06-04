# Review of ASN-0087

## REVISE

### Issue 1: `d'` overloaded — "post-state document" vs "other document"

**ASN-0087, Effect / Invariant Preservation**: The frame clauses use `d'` for *documents other than the home document* — e.g. "`(A d' ∈ dom(Σ.M), d' ≠ d :: Σ'.M(d') = Σ.M(d'))`" and in M-Frame "in `M(d')` for `d' ≠ d`". But the Invariant Preservation tables and prose use `d'` for the *post-state of the home document* — e.g. the S8a row "`#v_ℓ = m_L(d') ≥ 2`", "post-state depth `m_L(d') = 2` when `V_{s_L}(d) = ∅`", and the D-SEQ★ paragraph "`V_{s_L}(d') = {v_ℓ}`", "fixing `m_L(d') = 2`".

**Problem**: The same symbol `d'` denotes two distinct things in the same note (a sibling document under the frame; the home document at the post-state under the invariants). The worked example compounds this by binding `d'` to a concrete *third* meaning, the sibling document `[1,0,1,0,2]`. A precise reader must re-infer the referent of `d'` per section.

**Required**: Use a depth notation indexed by state (e.g. `m_L^{Σ'}(d)`, or simply "the post-state link depth of `d`") in the invariant section, reserving `d'` exclusively for "documents `≠ d`."

### Issue 2: Essay flourish in a structural slot ("What Does Not Change")

**ASN-0087, What Does Not Change**: "This is not a separate guarantee. It is a direct consequence of the composite's structure: … The bytes remain where they were. That creating a link has zero effect on referenced content is Nelson's phenomenology, here realized structurally."

**Problem**: M-NoContentEffect is fully stated by the section's first sentence (the total frame `Σ'.C = Σ.C`). The "This is not a separate guarantee" framing and the closing "Nelson's phenomenology, here realized structurally" are meta-prose/essay content that does not advance the claim. (The intervening "referencing is read-only — the endset stores spans, not bytes" sentence is a legitimate statement of what the operation does *not* do and should stay.)

**Required**: Drop the "not a separate guarantee" framing and the closing phenomenology sentence; keep the read-only/spans-not-bytes statement.

### Issue 3: Predictability-of-`ℓ` restated in three places

**ASN-0087, Inputs / wp Case 2 / Worked example (reflexive variant)**: Inputs: "The address `ℓ` is *derived* by the system from the current state (the next emission of `A_L(d)`)." wp Case 2: "Although `ℓ` is not a parameter, it is deterministically derivable from `Σ`: a caller predicts `ℓ` by evaluating `A_L(d)`'s emission rule…". Worked example: "the caller predicts `ℓ = [d, 0, 2, 1]` from `Σ` via `A_L(d)`'s deterministic first-emission rule."

**Problem**: The same point — `ℓ` is system-derived but caller-predictable from `A_L(d)`'s emission rule — is asserted three times. The wp Case 2 statement and the worked-example instance are the substantive uses; the duplication of the general principle across them is accretion of the kind this review mode flags.

**Required**: State the predictability principle once (at its first load-bearing use, wp Case 2), and let the worked example simply *apply* it without re-deriving the rule.

## OUT_OF_SCOPE

### Topic 1: Well-formedness of forward-reaching endsets

The Open Questions ask what constraints govern endsets whose spans reference not-yet-allocated addresses. This is correctly left to a future ASN — L4 (EndsetGenerality) already permits such spans, and tightening that is new territory, not an error here.

### Topic 2: Protocol-layer atomicity of the composite

M-CompAtomicity correctly identifies that composite-level atomicity is a protocol-layer concern outside the substrate. Specifying that guarantee belongs to a future protocol-layer ASN.

VERDICT: REVISE
