# Integration Review of ASN-0034

## REVISE

### Issue 1: I8 forward-references TA-assoc
**ASN-0034, Ordinal displacement and shift**: "By TA-assoc: (v ⊕ δ(n₁, m)) ⊕ δ(n₂, m) = v ⊕ (δ(n₁, m) ⊕ δ(n₂, m))"
**Problem**: TA-assoc is stated in the "What tumbler arithmetic is NOT" section, which appears several sections after the ordinal shift section (past Increment, Zero tumblers, and Subspace closure). The derivation of I8 treats it as an established fact, but it hasn't been stated yet at that point in the document.
**Required**: Either relocate the ordinal shift section to after TA-assoc, or rewrite I8's derivation to use TumblerAdd's constructive definition directly (expanding both sides component-wise confirms equality without needing associativity as an intermediate step).

### Issue 2: Formal summary omits integrated properties
**ASN-0034, Formal summary**: The narrative text lists all other property families (T0–T12, TA0–TA7a, TA-assoc, TA-LC/RC/MTO, D0–D2) but does not mention OrdinalDisplacement, OrdinalShift, or I6–I10. The "Required by" table — which claims "Each property is required by at least one system guarantee" — also omits all seven new entries, despite including other lemmas (TA-LC, TA-RC, TA-MTO).
**Problem**: The summary is incomplete after integration. A reader consulting only the formal summary would not know the shift apparatus exists.
**Required**: Add a narrative bullet for the ordinal shift properties (analogous to the D0–D2 bullet) and add entries to the "Required by" table.

### Issue 3: I-prefix labels break document naming convention
**ASN-0034, Ordinal displacement and shift / Properties Introduced**: Properties are labeled I6, I7, I8, I9, I10.
**Problem**: The document uses systematic prefixes — T for tumbler properties, TA for tumbler arithmetic, D for displacement — with numbering starting at 0 or 1 within each family. The "I" prefix appears nowhere else in the document; I1–I5 are not defined here; and no explanation is given for what "I" denotes or why numbering starts at 6. This is a residual artifact from the source ASN (ASN-0060), not adapted to the host document's convention.
**Required**: Re-label to match the document convention — either extend the TA family (e.g., TA-shift1 through TA-shift5, or TS1–TS5) or adopt another convention consistent with the existing T/TA/D pattern, with numbering that doesn't presuppose properties defined elsewhere.

VERDICT: REVISE
