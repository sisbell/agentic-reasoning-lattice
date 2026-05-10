# Cone Review — ASN-0034/TA0 (cycle 1)

*2026-04-25 20:54*

### TumblerSub claimed as constructed but never defined
**Class**: REVISE
**Foundation**: n/a (foundation ASN, internal consistency)
**ASN**: Tumbler arithmetic introduction: "Its inverse — tumbler subtraction (⊖), which recovers the displacement between two positions — is constructed as TumblerSub."
**Issue**: The prose asserts that TumblerSub *is constructed* (present tense, no citation) but no TumblerSub claim appears anywhere in this ASN. There is also no pointer to where the construction lives. A reader following the introduction will look for the construction in this document, fail to find it, and be left without a reference. This is a broken promise — either the construction belongs here and is missing, or the prose should cite the ASN that provides it.
**What needs resolving**: Either supply the TumblerSub construction in this ASN, or rewrite the introduction so it does not claim TumblerSub is constructed (e.g., name it as future/external work with a forward pointer that does not assert delivery).

### Definitional ordering with forward textual references
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: Document order: T0 → TumblerAdd → ActionPoint → TA-Pos → T1 → T3 → TA0.
**Issue**: TumblerAdd's prose states `Pos(w)` and `actionPoint(w)` as preconditions before TA-Pos and ActionPoint are defined; ActionPoint's prose uses `Pos(w)` before TA-Pos defines it; T1's proof cites T3 before T3 is stated. The Depends lists capture the logical structure correctly and there is no circularity (each forward reference is to a definition that does not depend back), so soundness is unaffected — but a linear reader hits operators before their definitions. A natural order would be T0 → T3 → TA-Pos → ActionPoint → T1 → TumblerAdd → TA0.

VERDICT: REVISE
