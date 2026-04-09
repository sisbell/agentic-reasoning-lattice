# Review of ASN-0036

## REVISE

### Issue 1: I-address ordinal shift `a + k` lacks formal definition
**ASN-0036, S8-depth section**: "We write `v + k` for ordinal displacement applied to V-positions, and `a + k` for the same applied to the element ordinal of I-addresses."
**Problem**: The V-position notation `v + k = shift(v, k)` receives a precise symbolic definition (extending OrdinalShift to k = 0). The I-address notation `a + k` receives only a verbal description. This asymmetry matters because `a + k` appears in the formal definition of correspondence runs — the core construct of S8 — and in the Properties table statement for S8 itself: "`M(d)(vⱼ + k) = aⱼ + k`". Every other notation in this ASN has a symbolic definition grounded in ASN-0034 operations; this one relies on the reader reconstructing the intent from prose.

The fix is one sentence. Since `a` is a full I-address with `#a ≥ 1`, `shift(a, k) = a ⊕ δ(k, #a)` is well-defined by TumblerAdd: the action point `#a` falls at the element field's last component (S7c guarantees δ ≥ 2, so the last component of the full address IS the element ordinal's last component), all earlier components — including field separators and the subspace identifier — are copied unchanged by TumblerAdd's prefix rule, and the result length equals `#a`. So `a + k = shift(a, k)` gives the correct semantics without requiring field extraction and reconstruction.

**Required**: Define `a + k` for I-addresses formally: `a + 0 = a` and `a + k = shift(a, k)` for `k ≥ 1`, with a brief justification that the action point of `δ(k, #a)` falls within the element field (by S7b and S7c), preserving all higher-level structure. This brings the correspondence run definition to the same formalization level as the rest of the ASN.

## OUT_OF_SCOPE

(none — the ASN's Open Questions already cover the natural extensions)

VERDICT: REVISE
