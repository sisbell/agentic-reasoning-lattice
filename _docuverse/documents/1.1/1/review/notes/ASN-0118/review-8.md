# Review of ASN-0118

This is a thorough, multiply-revised specification. The decomposition into resolution + placement is clean, CP1 is correctly identified as the defining frame condition, the partial-binding decision is handled consistently, the composite decomposition (K.μ⁻/K.μ⁺/K.ρ) is carefully split on append-vs-displacing, the wp for link discoverability is non-trivial, and the worked example exercises the key postconditions including both provenance branches. I find no correctness hole or missing boundary case in the operation itself. Two issues remain, both of clarity/precision.

## REVISE

### Issue 1: The symbol `p` is overloaded — spec-set arity and insertion position
**ASN-0118, "What a spec-set names" and "The COPY operation"**: The spec-set is defined as `R = ⟨ρ₁, …, ρₚ⟩ ... with p ≥ 1`, using `p` as the sequence length. Then the operation introduces "let `p` be a V-position in its text subspace at which the material is to land," and `p` thereafter denotes the insertion position in nearly every claim (CP2: `Σ'.M(d)(p + i)`, CP3, the tiling, the worked example `p = [1,2]`).
**Problem**: `p` is one of the most-referenced symbols in the ASN (the insertion position), and it collides with the spec-set arity in the ContentReferenceSequence definition (`ρₚ`, `p ≥ 1`). A reader meeting `p ≥ 1` and later `p + i` must disambiguate two unrelated quantities sharing one letter.
**Required**: Rename the spec-set length (e.g. `q` or `P`, matching ASN-0058's own use of `p` only locally), reserving `p` exclusively for the insertion position.

### Issue 2: CP3 prose attributes post-state function-ness to I3-S2, which covers only the shift
**ASN-0118, "The destination's prior arrangement is preserved"**: "ASN-0082's I3 lemmas supply the per-position facts — that the shifted positions stay well-formed (I3-VP), preserve depth (I3-VD), and keep the arrangement a function (I3-S2) and finite (I3-fin)."
**Problem**: ASN-0082's I3 describes the shift only; by I3-CS the gap `[p, p+W)` is *empty* in I3's `M'(d)`. COPY fills that gap with the placement positions (CP2), so the function-ness of COPY's actual `Σ'.M(d)` is *not* established by I3-S2 — it requires the placement/shift/left disjointness from the tiling argument. The decomposition section gets this exactly right ("the placement positions ... are gap-fill, not shifted content, so I3-VP does not cover them"), but the CP3 summary prose overstates the borrowing by lumping function-ness under the I3 lemmas.
**Required**: Scope the CP3 prose to the shifted region (as the decomposition section already does), and point function-ness/no-holes at the tiling argument + K.μ⁺ contract rather than at I3-S2.

## OUT_OF_SCOPE

### Topic 1: Width-preservation under partial binding (loss of ASN-0058 C2)
Correctly flagged in Open Questions — the relationship between a partially-bound span's nominal extent and its smaller placed width `W` is new territory, not an error here.

### Topic 2: Overlapping/repeated source spans, mixed-depth assembly, link-subspace transclusion
All correctly deferred to future ASNs via the Open Questions.

VERDICT: REVISE
