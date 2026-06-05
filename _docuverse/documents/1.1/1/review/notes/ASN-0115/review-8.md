# Review of ASN-0115

## REVISE

### Issue 1: Novel boundary claims asserted but never verified against a concrete scenario

**ASN-0115, "What co-delivery reveals: transclusion" / Synthesis**: The ASN supplies exactly one worked instance (the transclusion example under R8), exercising R5, R8.i, and R8.iii.

**Problem**: The ASN itself foregrounds two claims as the genuinely surprising boundary behaviors — R11 ("the decisive distinction between *deletion* and *removal of content*") and R10 (subspace crossing observable as a change of item kind). Neither is exercised by any concrete scenario. The one example covers the *least* surprising case (two positions resolving to a shared address). The reviewing standard requires verifying the key/novel postconditions against a specific scenario from the implementation evidence; transclusion alone does not discharge that for the claims most likely to be gotten wrong.

**Required**: Add at least one concrete instance for R11 — e.g., content address `a` created under document `d`, a later version `d'` that still binds a V-position to `a`, then a K.μ⁻ contraction of `d`'s arrangement removing `a`'s binding; show a spec over `d'` still delivers `Σ.C(a)` (orphaned-relative-to-`d`, still deliverable) — and one for R10, showing a two-spec spec-set (one `s_C` spec, one `s_L` spec) producing a heterogeneous `⟨content, …⟩ / ⟨ref, …⟩` stream with the boundary visible in the tagging.

### Issue 2: R11's weakest-precondition statement is non-minimal — condition (ii) is entailed by (i)

**ASN-0115, R11 discussion**: "for the delivery of a spec to include the value at `a`, it suffices that (i) the consulted arrangement binds some named position to `a`, and (ii) `a ∈ dom(Σ.C)`."

**Problem**: For a *content* item (R11's stated scope), the named position is a content position with `subspace(v) = s_C`, and S3★ gives `M(d)(v) = a ⟹ a ∈ dom(Σ.C)` directly. So (ii) is not an independent precondition — it follows from (i) via S3★. Presenting the wp as a conjunction of two conditions overstates it; the genuine weakest precondition is (i) alone. The prose even asserts deliverability "turns on *exactly* two conditions," which is the imprecision: it turns on one, with the second automatically discharged by referential integrity (not merely by immutability, as the text claims).

**Required**: State the wp as (i) alone, and note that S3★ discharges `a ∈ dom(Σ.C)` whenever (i) holds for a content position (with immutability then holding it forever). If the intent is to separate the permanent part from the live part, say so as a decomposition, not as two independent necessary conditions.

## OUT_OF_SCOPE

### Topic 1: Single-span subspace straddling

The ASN explicitly defers boundary-crossing single spans (`actionPoint(ℓ) = 1`) to the Open Questions and confines V-specs to ordinal-level spans. This is correctly scoped out; designating both subspaces is achieved by composing per-subspace specs.

### Topic 2: Inline provenance, outright-failure conditions, channel faithfulness

The four Open Questions (inline vs. recoverable provenance, permitted failure, unbound resolved references, transmission-channel faithfulness) are correctly identified as future territory rather than gaps in this ASN.

VERDICT: REVISE
