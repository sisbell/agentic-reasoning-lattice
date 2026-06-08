# Review of ASN-0107

## REVISE

### Issue 1: R2's decrement bound silently assumes a single consulted slot
**ASN-0107, R2 (ContentDeletionUnbounded)**: "let `k` be the number of matching links reaching some `a ∈ D` in the consulted slot. The contraction can drop up to `k` links from the discovery count in one operation: `Δnum_disc ∈ {−k, …, 0}`."
**Problem**: R2 is stated for a general `K.μ⁻` on `d_q`, but a single contraction on `d_q` can change `Q₁`, `Q₂`, and `Q₃` simultaneously whenever `W₁`, `W₂`, `W₃` all draw positions from `d_q`. The phrase "the consulted slot" (singular) re-imports R1's `(P-slot)` single-slot assumption without stating it as a precondition. In the multi-slot case `D` spans addresses that leave different slots, and a matching link drops when it loses its *last* reach in *any* consulted slot — so `k` as defined ("links reaching `a ∈ D` in the consulted slot") is ill-formed: it neither fixes which slot nor accounts for a link at risk through more than one slot. The worked example exercises only the from-slot, so it does not cover the configuration R2 claims to bound.
**Required**: Either add an explicit single-consulted-slot precondition to R2 (paralleling R1's `(P-slot)`), or redefine `k` for the general case as the number of previously-matching links that lose their last reach in *some* consulted slot, and re-derive the bound accordingly.

### Issue 2: Deferral paragraph adds no claim
**ASN-0107, end of "How the Count Changes: Links Retracted"**: "These per-operation laws assemble into a conservation statement that is anchoring-conditional — already settled by the E/D split: against a fixed permanent `Q` conservation holds (E4), and under discovery anchoring it fails (D2)."
**Problem**: The sentence promises "a conservation statement" but introduces none; it defers entirely to E4 and D2 and restates their content. This is the forward/backward-reference accretion the anti-bloat classifier targets — prose that points at existing claims instead of advancing the argument.
**Required**: Delete the paragraph, or fold its one substantive observation (conservation is anchoring-conditional) into E4/D2 where it is actually proved.

### Issue 3: Cross-ASN reference by number to a non-foundation ASN
**ASN-0107, "State and the Counting Request"**: "returning the matched links is the separate FINDLINKS retrieval operation (ASN-0099), out of scope here."
**Problem**: ASN-0099 is not a foundation ASN; per the self-containment standard, referencing another ASN by number is a REVISE item. (The same boundary can be drawn without the numeral.)
**Required**: Name the operation (FINDLINKS) without the ASN number, consistent with how the Open Questions already refer to "the corresponding retrieval operation."

## OUT_OF_SCOPE

### Topic 1: Independently-anchored multi-document requests
**Why out of scope**: The first Open Question (three parts anchored to separately-evolving documents) is genuinely new territory — a different request-resolution model — not a defect in this ASN's single-`d_q` discovery anchoring.

### Topic 2: Count-versus-retrieval consistency
**Why out of scope**: The third Open Question (agreement between `num` and the cardinality FINDLINKS would return) depends on the retrieval operation, explicitly excluded by the scope (ASN-0099).

VERDICT: REVISE
