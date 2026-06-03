# Review of ASN-0077

## REVISE

### Issue 1: S3★ used unconditionally where it only yields conditional membership

**ASN-0077, O7 (step 3), O11 (⊆ step 3), O11' (⊆ direction), and SHOWORIGIN_V postcondition well-formedness**: e.g. O7 — "Let `a = M(d)(v)`... By S3★ (ASN-0047), `a ∈ dom(Σ.C) ∪ dom(Σ.L)`."

**Problem**: S3★ (ASN-0047) is purely conditional: `subspace(v)=s_C ⟹ M(d)(v)∈dom(C)` and `subspace(v)=s_L ⟹ M(d)(v)∈dom(L)`. To conclude the *unconditional* `a ∈ dom(C) ∪ dom(L)`, you must first know `subspace(v) ∈ {s_C, s_L}` — which is supplied by S3★-aux (SubspaceExhaustiveness), not by S3★. O2's derivation does this correctly ("Two cases by subspace of `vⱼ`, exhaustive by S3★-aux applied to `vⱼ ∈ dom(M(d))`"), but O7, O11 step (3), O11', and the operation's postcondition-well-formedness argument all cite S3★ alone. This is an internal inconsistency in an ASN that otherwise enforces the per-step citation convention rigorously, and the conclusion that `origin(M(d)(v))` is even defined depends on it (origin is total only on `dom(C) ∪ dom(L)`).

**Required**: In each of O7, O11, O11', and the SHOWORIGIN_V postcondition, cite S3★-aux alongside S3★ to discharge `subspace(v) ∈ {s_C, s_L}` before concluding `M(d)(v) ∈ dom(C) ∪ dom(L)` — matching the treatment already given in O2.

## OUT_OF_SCOPE

### Topic 1: Link-subspace I-span attribution, intermediate-chain surfacing, native-vs-transcluded distinction, historical containment
**Why out of scope**: The ASN's four Open Questions correctly defer these. The I-span lift's definitional restriction to `dom(C)` (Open Question 1), surfacing the transclusion chain (Open Question 2), the native/transcluded distinction (Open Question 3), and the `Σ.R`-based historical-containment operation (Open Question 4) are all new operations or new state coupling, not defects in SHOWORIGIN as specified here.

VERDICT: REVISE
