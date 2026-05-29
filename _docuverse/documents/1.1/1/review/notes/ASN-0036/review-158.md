# Review of ASN-0036

## REVISE

### Issue 1: V-position "definition" rests on an undefined term

**ASN-0036, S8a (V-position well-formedness)**: *"Definition: A V-position is, by definition, an isolated element field of depth at least 2."* and the proof: *"From the Definition, `zeros(v) = 0` and `#v ≥ 2` hold directly."*

**Problem**: The entire derivation of `zeros(v) = 0` is discharged "directly" from the phrase "isolated element field," but that phrase is never formally defined — not in this ASN, not in the foundation (ASN-0034), not in the shared vocabulary. A precise reader cannot verify that "isolated element field" entails `zeros(v) = 0` rather than, say, `zeros(v) = 3` (which is what an *element-level address* carries — and is exactly what `ran(M(d))` uses per S7b). The load-bearing structural fact (V-positions live in the `zeros = 0` subset, distinct from the `zeros = 3` I-addresses) hangs on an informal term doing formal work.

**Required**: State the V-position definition formally — e.g., "a V-position is a tumbler `v` with `zeros(v) = 0` and `#v ≥ 2`" — and let positivity follow from T0 + NAT-discrete as the proof already does. Drop the informal "isolated element field" framing or relegate it to motivating prose, not the definitional slot.

### Issue 2: Forward-reference accretion around the OrdinalShift consequence

**ASN-0036, S8 section**: *"We record here the consequence of OrdinalShift's postconditions invoked throughout this section: for `m ≥ 2`, `shift(v, n)` agrees with `v` on positions `1 ≤ i < m` ..."*

and in the ValidInsertionPosition section, two separate deferrals: *"By the OrdinalShift consequence recorded for S8 (for m ≥ 2, shift preserves the subspace identifier) ..."* and *"By the OrdinalShift consequence recorded for S8 (preserves components < m, increments the ordinal at position m) ..."*

**Problem**: This is the cross-section deferral pattern the anti-bloat pass targets. One paragraph restates a foundation (OrdinalShift) postcondition with the use-site-inventory tell "invoked throughout this section," and two later paragraphs in a different section defer back to it ("the OrdinalShift consequence recorded for S8"). A reader following the insertion-position derivation must skip back to S8 to recover a specialization of a foundation result that could be cited directly. The deferrals carry no reasoning the local citation of OrdinalShift wouldn't.

**Required**: Either cite OrdinalShift (ASN-0034) directly at each use with the one-line specialization inline, or keep a single specialization but drop the "invoked throughout this section"/"recorded for S8" cross-references. Remove the use-site framing.

### Issue 3: Notational-reservation meta-prose in a structural slot

**ASN-0036, S8-depth section**: *"We reserve the symbol `+` for NAT addition on components and indices throughout this ASN; tumbler ordinal displacement is always written `shift(v, k)` ... never `v + k`."*

**Problem**: Borderline — disambiguation is sometimes earned — but here it sits as a standalone meta-paragraph asserting a global convention rather than advancing the local claim (consecutive V-positions). The convention is already evident from usage (`shift` appears everywhere; `+` only on naturals).

**Required**: Fold the disambiguation into the first place `shift` and `+` co-occur, or drop it. Do not let it stand as its own reasoning-free paragraph.

## OUT_OF_SCOPE

### Topic 1: Operation preservation of D-CTG / D-MIN / S2

The Open Questions correctly defer "what must each well-formed editing operation (DELETE, INSERT, COPY, REARRANGE) ... guarantee in order to preserve the contiguity invariants" and the insertion-coincides-with-occupied-position case. These belong to the operations layer, explicitly scoped out. No flag — the ASN draws the line correctly.

### Topic 2: Contiguity semantics for the link subspace (S = 2)

D-CTG/D-MIN/D-CTG-depth/D-SEQ all bind `S = 1` and explicitly state link-subspace contiguity is out of scope. Appropriate — link arrangement is a future ASN.

VERDICT: REVISE
