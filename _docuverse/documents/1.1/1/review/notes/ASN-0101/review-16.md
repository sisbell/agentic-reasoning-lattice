# Review of ASN-0101

## REVISE

### Issue 1: K.σ silently added to ValidComposite★ vocabulary

**ASN-0101, "The operation" preamble and D10**: "DEL is a new atomic transition kind extending the foundation's transition vocabulary `{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ, K.σ}`" and D10's vocabulary lists "`{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ, K.σ, DEL}`".

**Problem**: ASN-0047's ValidComposite★ explicitly enumerates 8 transitions (no K.σ): K.α (amended), K.δ, K.λ, K.μ⁺ (amended), K.μ⁺_L, K.μ⁻ (amended), K.μ~, and K.ρ. K.σ is the substrate-level operation from ASN-0093, whose registration effect (`dom(M') = dom(M) ∪ {d}` with `M'(d) = ∅`) coincides with K.δ-IsDocument's effect. D10 claims to extend ASN-0047's ValidComposite★ "to admit DEL as an elementary transition" but silently adds K.σ as well, without explaining the relationship between K.σ and K.δ-IsDocument or justifying the second extension.

**Required**: Clarify the K.σ status. Options: (a) note that K.σ is being promoted alongside DEL as an independent extension; (b) remove K.σ if subsumed by K.δ-IsDocument; (c) explicitly acknowledge K.σ and K.δ-IsDocument as alternative document-registration operations and state both belong to the vocabulary. Whichever option, the choice should be visible to the reader.

### Issue 2: D8 worked example verification omits three invariants

**ASN-0101, "A worked example" section, "Verification of D8"**: traces S8a, S8-depth, S2, S3★, D-CTG★, D-MIN★, D-SEQ★.

**Problem**: D8 Group (i) enumerates 12 invariants. The first worked example explicitly verifies 7. The link-subspace example adds CL-OWN and CL-UNIQ (2 more). S8-fin, S3★-aux, and S8★ are not explicitly verified by any of the three concrete examples. While their general justification appears in D8's prose, a Dijkstra-style verification should trace every invariant against at least one concrete instance.

**Required**: Add one-line verifications for the three omitted invariants in at least one example. For instance: "S8-fin: `|V_1(M'(d))| = 2 < ∞`. S3★-aux: both post-state V-positions have subspace `1 ∈ {s_C, s_L}`. S8★: trivial singleton decomposition `{([1,1,1], a_1, 1), ([1,1,2], a_4, 1)}` satisfies S8's conditions (a) and (b) with run width 1."

## OUT_OF_SCOPE

None of substance — the ASN's Open Questions section appropriately defers downstream concerns (recoverability mechanism, INSERT inverse, causal ordering across documents) to future ASNs.

VERDICT: REVISE
