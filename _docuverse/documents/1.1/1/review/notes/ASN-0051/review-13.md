# Review of ASN-0051

## REVISE

### Issue 1: Worked example constructs an invalid state

**ASN-0051, Worked Example, "After contraction"**: "A K.μ⁻ step removes the mapping at v₃, producing M'(d) with dom(M'(d)) = {v₁, v₂, v₄, v₅} and ran(M'(d)) = {a₁, a₂, a₄, a₅}"

**Problem**: The domain {v₁, v₂, v₄, v₅} has a gap at v₃, violating D-CTG (VContiguity). K.μ⁻'s postcondition requires D-CTG; by D-SEQ, valid contractions remove from the maximum end of V_S(d) only. Removing v₃ from the interior is not a valid K.μ⁻ step.

The valid composite that removes a₃ from ran(M(d)) is K.μ~ (rearrange a₃ to the end) followed by K.μ⁻ (remove the last position). This yields dom(M'(d)) = {v₁, v₂, v₃, v₄} with, e.g., M'(d) = {v₁↦a₁, v₂↦a₂, v₃↦a₄, v₄↦a₅}. Consequences:

- locate(F, d) = {v₂, v₃}, not {v₂, v₄}
- Block decomposition: β₁ = (v₁, a₁, 2), β₂ = (v₃, a₄, 2) — not β₂ = (v₄, a₄, 2)
- The subsequent reordering analysis ("swaps v₂ and v₄") references invalid positions

The projection π(F, d) = {a₂, a₄} is coincidentally correct (it depends only on ran, which matches), but every V-side detail — domain, locate set, block starts, and the reordering — is wrong.

**Required**: Reconstruct the worked example using a valid composite (K.μ~ + K.μ⁻). Correct the V-domain to {v₁, v₂, v₃, v₄}, the locate set to {v₂, v₃}, and the block decomposition accordingly. The reordering section must use positions from the valid post-contraction state.

### Issue 2: Interior contraction claim conflicts with D-SEQ

**ASN-0051, Partial Survival section**: "The number of fragments can grow through repeated contractions: a single contraction that removes I-addresses from the interior of a contiguous endset region splits one fragment into two."

**Problem**: K.μ⁻ cannot remove I-addresses from the interior. By D-SEQ, valid contractions remove from the maximum end of V_S(d) only. Interior removal requires a composite — K.μ~ to rearrange interior content to the end, then K.μ⁻ to remove it. "A single contraction" is false as stated. The fragment splitting does occur, but as a consequence of the composite's rearrangement altering the block structure, not of contraction alone.

**Required**: Replace "a single contraction that removes I-addresses from the interior" with language reflecting the composite operation (rearrangement + end-removal) that produces the net effect of interior removal.

### Issue 3: SV13(f) embeds a conditional claim within a theorem

**ASN-0051, SV13(f)**: "Same-origin coverage growth depends on the allocation regime — closed at the byte level by sequential sibling allocation, open at broader address levels by design (the byte-level closure follows from allocation discipline assumptions not formalised in this ASN...)"

**Problem**: SV13 is labeled "SurvivabilityTheorem" and synthesizes the complete guarantee. Part (f) mixes the formally proved SV6 (cross-origin exclusion) with a conditional claim about byte-level closure that depends on an assumption ("sequential sibling allocation") explicitly acknowledged as unformalised. A theorem statement should contain only claims derivable from stated premises. The conditional observation is valuable context but belongs outside the theorem body.

**Required**: Split (f) into a formally proved part — cross-origin exclusion (SV6) under its stated preconditions — and a separate remark or conjecture for byte-level closure conditioned on the unformalised allocation discipline. The remark can reference the architectural analysis section without diluting the theorem.

## OUT_OF_SCOPE

### Topic 1: Formalization of byte-level allocation discipline

The ASN honestly acknowledges that byte-level coverage closure "follows from allocation discipline assumptions not formalised in this ASN." Formalizing sequential-sibling-only allocation as a design requirement or axiom, and deriving byte-level closure from it, is new territory — not an error in the current ASN.

**Why out of scope**: The ASN correctly identifies the gap and locates the architectural evidence. The formalization belongs in the allocation discipline or content mapping ASN.

### Topic 2: Link-subspace contribution to endset projection

The ASN defines π(e, d) over the full ran(M(d)) but SV11 decomposes only the text-subspace projection. The link-subspace contribution — endsets referencing link addresses via L13 (ReflexiveAddressing) — is explicitly deferred.

**Why out of scope**: The ASN states the deferral clearly: "The link-subspace contribution to projection... is deferred to the Link Subspace ASN." This is deliberate scoping, not an omission.

VERDICT: REVISE
