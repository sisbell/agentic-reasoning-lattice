# Review of ASN-0070

This is a mature, unusually rigorous note. The inverse-image framing (F0), the V-restricted denotation, and the canonical-uniqueness theorem (F-canonical) are all developed with explicit case analysis rather than hand-waving. I checked the dense proofs — the Step 1 finiteness argument forcing `k = m_S(d)`, the consecutivity Characterisation (forward and the position-`p` induction in reverse), the inter-component left/right-closure in Step 2a, and the F-subspace biconditional — and found them sound. The five worked configurations exercise partial reach (C1), multiplicity (C2), no-reach (C3), state-dependence (C4), and the link-subspace branch (C5). One gap remains.

## REVISE

### Issue 1: The fragmentation sub-case and partial-block intersection are claimed but never demonstrated

**ASN-0070, "Sub-cases as One Phenomenon" / "Computation via Decomposition"**: "When an endset's I-coverage is contiguous but the corresponding V-positions are non-contiguous ... the result has multiple disjoint V-spans." And: "If a single endset I-span `σ` intersects two non-adjacent mapping blocks of `d` in the same subspace, it produces two non-adjacent V-runs in the result ... No special logic handles fragmentation; the decomposition delivers it automatically."

**Problem**: Of the three sub-cases the note explicitly elevates — *multiple occurrences*, *fragmentation*, *empty resolution* — two are verified against concrete configurations (C2 exercises F-multi, C3/C4 exercise F-empty), but **fragmentation is never exercised by any worked example**. Relatedly, F-contig's offset machinery — the contiguous sub-progression `{a + j + k : 0 ≤ k < c}` with `j > 0` or `c < n` — is never instantiated: in every configuration the intersection is either the full block I-extent (C1: `j = 0, c = n = 2`) or empty. The note's standard ("the ASN should verify its key postconditions against at least one specific scenario from the implementation evidence") is met for the inverse-image core but not for F-contig, which is the lemma carrying the entire "fragmentation delivered automatically" claim. A claim that "no special logic" is needed is exactly the kind of assertion that warrants a concrete witness.

**Required**: Add a worked configuration in which one endset I-span intersects two non-adjacent same-subspace mapping blocks of `d` (yielding `Σ_V^{s_C}` with two disjoint, non-adjacent normalised spans), and in which at least one block is hit at a non-zero offset (`j > 0`, `c < n`). Verify F-sound, F-complete, and F-contig (offset `j`, width `c`, the resulting V-run start) against the result, exactly as C1–C5 do for their respective properties.

## OUT_OF_SCOPE

### Topic 1: Straddling-endset (coverage spanning both subspaces) worked example
The note proves the partition `R(d,e)|_{s_C} = M(d)⁻¹(coverage(e) ∩ dom(C))` and the `s_L` analogue, admitting endsets whose coverage straddles both I-subspaces (L4). No single example exercises a straddling endset (C5 is link-only; C1–C4 are content-only). This is closer to example completeness than the fragmentation gap and could reasonably be folded into Issue 1's new configuration, but on its own it is desirable polish rather than a correctness defect — the partition derivation is complete.

VERDICT: REVISE
