# Review of ASN-0124

I checked every introduced claim's derivation, the two constructions (FD-NEUT(c), FD-LOSSY), the insertion composite (FD-FRESH), the weakest-precondition analyses (FD-CWP, FD-VDYN(d) absorption), and the worked illustration. The mathematics is sound: the FD-IMGC equality is proved both inclusions, the FD-FRESH composite's couplings are checked initial-to-final with the grounding restriction `I ⊆ dom(Σ.C)` correctly load-bearing against fresh-allocation collision, the FD-VDYN four-case split is exhaustive over the vocabulary, and the FD-LOSSY/FD-NEUT(c) constructions respect the K.μ⁻ prefix-retention model and discharge J0/J1★/J1'★. Boundaries (`I = ∅`, `Ret = ∅`, empty arrangement, `p = N+1` append, single-document stratum) are handled. The historical-companion derivations (FD-SUPER/FD-WITNESS/FD-GHOST/FD-COINC) check against P4★/P4a/P2. One defect remains.

## REVISE

### Issue 1: Malformed foundation citation `ASN-0093/S7`
**ASN-0124, FD-NEUT(c)**: "K.α allocating fresh `a` on `d₁`'s content chain `A_C(d₁)` (so `origin(a) = d₁`, ASN-0093/S7)"

**Problem**: ASN-0093 has no claim labeled `S7`. Its claim set is M0–M2, C0/C1/C1b/C1c/C2, L0/L1/L1a/L1b/L1c/L3/L12, SD, the chain lemmas (FirstEmission, ChainMembershipForOrigin, …), the axioms, and K.σ/K.α/K.λ. The supported fact — content allocated on `A_C(d₁)` has `origin = d₁` — is correct, but a reader chasing the citation finds nothing. The note holds itself to per-claim foundation citation throughout (every other reference resolves), so this stray label is a genuine blemish. `S7` is an existing label in *ASN-0036* (StructuralAttribution: `origin(a)` is the allocating document), which is almost certainly the intended source confused for 0093.

**Required**: Repoint to the actual source of `origin(a) = d` for content-chain emissions — ASN-0093/FirstEmission (`origin(·) = d`) or ASN-0047/AllocatorHierarchy (`A_C(d)` outputs satisfy `origin(a) = d`), or ASN-0036/S7 if the structural-attribution claim is what was meant. Whichever is chosen, the label must name a claim that exists in the cited ASN.

## OUT_OF_SCOPE

### Topic 1: General mid-document deletion-with-shift stability
The note proves insertion-composite invariance in full (FD-FRESH) and the atomic contraction behavior (FD-STEP K.μ⁻ clause, FD-CWP), but states no symmetric "delete a mid-span, shift the remainder, other queries invariant" composite analogous to FD-FRESH.
**Why out of scope**: Editing operations are declared out of scope, and any such deletion composite decomposes into atomic K.μ⁻ + K.μ⁺ steps each already governed by FD-STEP, so the guarantee is derivable rather than absent. The Open Questions and the explicit scope statement cover this territory; it is not an error in this ASN. The eight Open Questions otherwise enumerate the genuine future work (interior states, timing, attribution, past-state reach, availability, authority, compaction, multiplicity) appropriately, leaving nothing further to add here.

VERDICT: REVISE
