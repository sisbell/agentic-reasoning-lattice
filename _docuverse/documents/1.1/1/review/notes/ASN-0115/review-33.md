# Review of ASN-0115

The mathematics here is solid and unusually thorough. I verified the Confinement lemma proof (T5 application with `p ≼ s`, `p ≼ reach(σ)`, `s ≤ t ≤ reach(σ)` — correct), the `act = ∅` discharge when `V_S(d) = ∅`, the exhaustiveness of `item`, the full D-SEQ★ no-interior-hole argument in R6 (both `act ≠ ∅` and `act = ∅` branches, with the canonical-start derivation and the `k > n_S` terminal-tail), the R7 proof including the load-bearing comparability subtlety, the R8 share-subspace dispatch and the CL-OWN/CL-UNIQ vacuity of the link sub-case, and all five worked instances (R6 arithmetic `s=[1,2], ℓ=[0,5], reach=[1,7]`; R8 spec-order; R9 distinct origins via S7; R10 tag-asymmetry; R11 K.μ⁻ frame). I found no correctness defect. The findings below are the prose-accretion patterns this note's classifier targets, plus one dangling reference.

## REVISE

### Issue 1: The disclosure-retraction claim is restated at four sites in and around R8

**ASN-0115, R8 (box, "Three points" Second, worked instance) and Synthesis**: the single claim "each item carries the value, never the address (R1), so co-delivery is byte-indistinguishable from two coincidentally-equal contents at distinct addresses (S4), disclosing nothing about the sharing" appears verbatim-in-substance four times:

1. R8 box: "…each item carries the value `Σ.C(a)`, never the address `a` (R1), so the co-delivery is byte-indistinguishable from the delivery of two coincidentally-equal contents at distinct addresses (S4) and discloses nothing about the shared origin (cf. R9)."
2. R8 "Second" point: "…because each delivered item carries the value `Σ.C(a)`, never the address (R1), the output does not disclose the sharing at all — it is byte-indistinguishable from the delivery of two coincidentally-equal contents at distinct addresses (S4)…"
3. R8 worked instance: "…carries two byte-identical values indistinguishable from two coincidentally-equal contents at distinct addresses (S4). Co-delivery adds nothing here that two separate single-span deliveries would not."
4. Synthesis: "…the shared address is a fact of resolution, not of the output, which carries values, not addresses (R1, R9), and so cannot be told apart from coincidental value-equality (S4)."

**Problem**: This is the "two paragraphs say the same thing in different words" pattern, compounded into four. The "Three points deserve emphasis" section largely re-narrates the box's (i)/(ii)/(iii) and disclosure sentence — First ↔ (ii), Second ↔ disclosure, Third ↔ (iii) — so a reader who has read the box must work past three paragraphs to extract the marginal new content (the "First" point's reference-vs-copy framing; the "Second" point's genuinely novel per-position/no-comparison argument that co-delivery carries no information a pair of isolated requests lacks; the "Third" point's R3-derivation that no-merge is forced by exactness). The load-bearing additions are buried inside re-statements of claims the box already makes.

**Required**: State the byte-indistinguishability/S4 disclosure claim once (the box is its natural home, as it is part of the claim). Trim the "Second" point to its novel content (the no-extra-information argument) and let it reference the box rather than re-derive the indistinguishability. The worked-instance and synthesis recaps may then point to the claim rather than re-stating its full S4 derivation.

### Issue 2: R9 cites "Open Question 1" but the Open Questions are unnumbered

**ASN-0115, R9 prose and Claims table**: the R9 box reads "(inline content provenance deferred, Open Question 1)" and the claims-table R9 row repeats "(inline content provenance deferred, Open Question 1)".

**Problem**: The Open Questions section lists four questions with no labels or numbers, so "Open Question 1" resolves to nothing. A reader following the pointer finds no labeled target. (The intent is recoverable — the first question is the inline-provenance one — but the reference is dangling.)

**Required**: Either number the Open Questions and make the reference land on the numbered label, or replace "Open Question 1" with a phrase that names the question by its subject ("the inline-provenance open question below").

## OUT_OF_SCOPE

None. The ASN correctly confines RETRIEVEDOCVSPAN-style extent reporting, link-structure reading, and the boundary-straddling-span case to its Open Questions rather than introducing claims for them, and the channel-faithfulness frame limit in R2 is properly deferred rather than asserted.

VERDICT: REVISE
