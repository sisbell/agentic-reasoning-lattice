# Review of ASN-0100

I checked the substrate decomposition, the three-region effect, every invariant discharge (S0/P0, S2, S3★, D-CTG★/D-MIN★/D-SEQ★, S8 family, S8★, L0/L12, coverage/projection, provenance), the worked examples, and the wp analysis. The mathematics is sound: the disjointness arguments, the closed-interval reduction (including the off-prefix exclusion at `m ≥ 3`), the K.μ⁻-fires condition with strict-contraction discharge, the I3-coincidence restriction-equality (correctly inheriting only arrangement-only lemmas while re-deriving S3/S7 because INSERT violates I3-C), and the `ran(M'(d)) = ran(M(d)) ∪ {a_k}` step all hold. I found no correctness or missing-case gap.

The findings below are anti-bloat — the classifier flags this note for meta-prose accretion around examples and forward references.

## REVISE

### Issue 1: Comparative meta-narrative opening the re-insertion example
**ASN-0100, §A Worked Example, "Re-insertion into a cleared content subspace"**: "The empty-document example fired K.α's first-emission branch; the complementary subsequent-emission branch shares the same composite skeleton (a K.α batch + one K.μ⁺ + a K.ρ batch, K.μ⁻ omitted, empty Left and Shifted-right regions) and the same D-MIN★/D-SEQ★ outcome — it differs in *one delta*, which I-addresses the K.α firings produce."
**Problem**: This is a narrative about how this example relates to the prior one ("shares the same skeleton... differs in one delta"), not content that advances the example. The reader must read past it to reach the substantive point (V-index / I-chain-index decoupling). Comparative framing in an example slot is exactly the accretion pattern flagged.
**Required**: Open directly with the setup (cleared content subspace, residual frontier `a_prev`); let the decoupling demonstration stand on its own.

### Issue 2: Duplicated statement of the decoupling point within the same example
**ASN-0100, §A Worked Example, "Re-insertion..."**: "This exposes the *decoupling* of the V-position index from the I-address chain index..." followed by "D-MIN★ and D-SEQ★ are stated over `V_{s_C}(d')` alone... and so are blind to the chain frontier index: the post-state V-positions are identical to the empty-document outcome whether the images are `[d.0.s_C.1..2]` or `[d.0.s_C.3..4]`."
**Problem**: The same observation (V-positions are independent of the I-chain index) is made twice in adjacent sentences. Two paragraph fragments saying the same thing in different words.
**Required**: State the decoupling once.

### Issue 3: Self-justifying example motivation
**ASN-0100, §A Worked Example, "Deep-subspace interior insertion (`m_C = 3`)"**: "The examples above all run at depth `m_C = 2`... We now exercise a multi-level content subspace, where the closed-interval reduction's hardest step — excluding off-prefix slice tuples — is actually live."
**Problem**: Prose that justifies why the example is included ("the hardest step... is actually live") rather than advancing the example. The example itself is valuable (it does exercise off-prefix exclusion concretely); the motivational framing is the flaggable part.
**Required**: Drop the meta-justification; the off-prefix exclusion check in the example body already demonstrates its own relevance.

## OUT_OF_SCOPE

None. §Bounding the Scope correctly enumerates DELETE, COPY, REARRANGE, link-subspace insertion, version derivation, and replication as out of scope; the Open Questions raise legitimate future-ASN topics. No claims drift into excluded territory.

VERDICT: REVISE
