# Review of ASN-0100

This is an INSERT operation specification — a substrate composite with a thorough, largely correct invariant-preservation argument. The proofs (S2 disjointness, D-CTG★ closed-interval reduction including the off-prefix exclusion at m≥3, the I3-coincidence transport, the projection-shift derivation, the wp analyses, and the per-intermediate atomicity check) are detailed and I found no correctness gap. All cross-ASN references are to foundation ASNs (0034/0036/0047/0058/0082/0093/0098) and are permitted.

The note carries `review-mode.anti-bloat`, and the findings below are accreted/duplicated prose, not correctness defects.

## REVISE

### Issue 1: Two-stream point stated twice in different words
**ASN-0100, "Background: The Two-Stream Asymmetry", paragraphs 2–3**: Paragraph 2 — "It grows C by appending fresh entries; it never alters existing entries, never reassigns I-addresses, never identifies one I-address with another." Paragraph 3 — "Existing content keeps its permanent I-address across INSERT. Its V-position within d may shift, but the I-address — and the value stored there — is invariant."
**Problem**: The two paragraphs restate the same content-immutability / permanent-I-address fact. This is the "two paragraphs in the same document say the same thing in different words" pattern.
**Required**: Collapse to one paragraph; keep the link-survivability consequence ("Since links attach to I-addresses … insertion cannot break them") as the single forward-looking sentence.

### Issue 2: L0 content-clause discharged redundantly, with a deferral chain
**ASN-0100, §"Link store unchanged (L12, L0, L1, L3)" and §"Atomicity and Canonical Order"**: §"Link store unchanged" fully discharges L0's content clause for each fresh `a_k` ("subspace_I(a_k) = s_C because a_k is an emission of A_C(d) … Hence L0's content clause is preserved"). The §Atomicity Link-store bullet then says L0's content clause "is discharged with the other per-address content invariants in the grouped paragraph below," and the grouped paragraph discharges it a third time ("S7a, S7b, C1b, C1c, and L0's content clause … each is established at its K.α commit and persists by P0 … so it holds at every K.α intermediate as well as at Σ'").
**Problem**: The grouped paragraph already covers both intermediate states and Σ', so the §"Link store unchanged" discharge is fully subsumed; the §Atomicity bullet's "discharged in the grouped paragraph below" is a deferral to that same location. This is the "multiple paragraphs in different sections defer to the same downstream location" pattern.
**Required**: Discharge L0's content clause once (the grouped per-address paragraph is the natural single home, since it already covers intermediate + boundary). In §"Link store unchanged", reduce L0's content clause to a one-line pointer; drop the deferral sentence in the §Atomicity bullet.

### Issue 3: "Branch selection keys on dom(C), not the arrangement" explained three times
**ASN-0100, §"Effect One: Allocation", the "Re-insertion into a cleared content subspace" example, and claim INS.alloc**: §Effect One devotes a full paragraph to "The branch selection keys on the content store, not the arrangement … An empty content subspace V_{s_C}(d) = ∅ does not entail an empty content store …". The re-insertion example re-states it in prose: "The branch keys on dom(C), not on the arrangement (INS.alloc): the residual set is non-empty, so the subsequent-emission branch fires." The point recurs again around INS.alloc.
**Problem**: The example is the demonstration and is legitimate; but the inline parenthetical there *re-explains* the rule rather than exhibiting it, duplicating the §Effect One paragraph. The mechanism is stated as spec (Effect One), re-explained in the example, and gestured at again at the claim.
**Required**: State the dom(C)-keying rule once in §Effect One. In the re-insertion example, let the worked steps show it (drop the explanatory re-statement, keep only the cross-reference).

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion semantics
**Why out of scope**: The ASN explicitly bounds itself to the content subspace and routes link-subspace insertion (K.μ⁺_L) to a future ASN; the corresponding Open Question is correctly scoped, not a defect here.

VERDICT: REVISE
