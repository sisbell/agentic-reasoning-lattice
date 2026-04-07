# Review of ASN-0051

## REVISE

### Issue 1: SV4 omits resolve analog, breaking SV13(e) citation
**ASN-0051, SV4 (ArrangementIsolation)**: The formal statement and proof cover only projection: `π_{Σ'}(e, d') = π_Σ(e, d')`. SV2 and SV3 each prove both the projection and resolve versions with explicit proof paragraphs. SV5 proves the resolve version with a full bijection argument. SV4 alone lacks a resolve statement.

**Problem**: SV13(e) cites SV4 for the claim "Changes to M(d) cannot affect resolve(e, d') for d' ≠ d. [SV4]." But SV4 does not state or prove this. The citation is to an unstated result.

**Required**: Add the resolve analog to SV4:

`resolve_{Σ'}(e, d') = resolve_Σ(e, d')`

with the one-line proof: since `M'(d') = M(d')` (frame), `resolve_{Σ'}(e, d') = {v ∈ dom(M'(d')) : M'(d')(v) ∈ coverage(e)} = {v ∈ dom(M(d')) : M(d')(v) ∈ coverage(e)} = resolve_Σ(e, d')`. This restores consistency with SV2/SV3/SV5 and makes the SV13(e) citation valid.

---

### Issue 2: SV12 attributes a fabricated quote to Nelson
**ASN-0051, Content Fidelity section**: "Nelson: 'The link holder can rely on the strongest possible content guarantee short of cryptographic verification: the system's fundamental architecture makes it impossible to change content at an I-address through any defined operation.'"

**Problem**: This is formatted as a direct Nelson quote ("Nelson: '...'") but carries no page reference. The language — "I-address," "defined operation," "fundamental architecture" — is the ASN author's formal vocabulary, not Nelson's prose style. Compare with the properly cited Nelson quotes elsewhere in the ASN (LM 4/43, LM 4/42, LM 2/14, LM 4/25, LM 4/23), which are conversational and use Nelson's terminology. This reads as the author's synthesis presented as quotation.

**Required**: Either provide the LM page reference for this quote, or rephrase as the author's analysis — e.g., "The guarantee is that the system's architecture makes it impossible to change content at an I-address through any defined operation." Drop the "Nelson:" attribution.

## OUT_OF_SCOPE

### Topic 1: Link-subspace V-positions in SV11
SV11 restricts to text-subspace projection (π_text) and correctly notes the link-subspace contribution is deferred to the Link Subspace ASN. When link-subspace V-positions are introduced, SV11's fragment decomposition will need extension. The ASN's note that "π_text(e, d) = π(e, d) for all reachable states" in the current model is accurate.
**Why out of scope**: No operation currently creates non-text V-positions; the gap is a future ASN's responsibility.

### Topic 2: Byte-level coverage closure formalization
SV6 proves cross-origin exclusion from the foundations. Same-origin coverage stability at the byte level is described as architectural ("closed at the byte level by sequential sibling allocation") but relies on "allocation discipline assumptions not formalised in this ASN." The architectural analysis is sound but the formal gap is acknowledged.
**Why out of scope**: Formalizing the byte-level closure requires a dedicated allocation-discipline ASN, not a revision of this one.

VERDICT: REVISE
