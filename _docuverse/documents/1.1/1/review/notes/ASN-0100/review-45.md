# Review of ASN-0100

## REVISE

### Issue 1: Spurious K.σ references contradict the stated operative vocabulary
**ASN-0100, §Atomicity and Canonical Order**: "The entity set E ... is unchanged at every intermediate: no K.δ fires, no K.σ fires." (also in the uniqueness "Other components" paragraph: "by the frame of every elementary step in the composite (no K.λ, no K.δ, no K.σ fires)")
**Problem**: §The Operation: Formal Contract explicitly fixes the operative substrate as ValidComposite★ (ASN-0047), whose vocabulary is `{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ}`, and states "document registration in this framework is K.δ in its IsDocument sub-case." K.σ (DocumentRegistration) belongs to ASN-0093's substrate, *not* ASN-0047's. Asserting "no K.σ fires" references an operation the ASN has just declared excluded from the operative vocabulary — internally inconsistent and redundant with the `E' = E` / "no K.δ document-registration" frame already given.
**Required**: Drop "no K.σ fires" in both sites; the document-non-registration fact is fully carried by "no K.δ in its IsDocument sub-case."

### Issue 2: INS.chain-shift derivation re-enumerated at its use site (anti-bloat)
**ASN-0100, §Per-subspace span decomposition (S8★)**: "By INS.chain-shift (Effect One above), `a_{k+1} = shift(a_k, 1)` exactly — established there from the T4-validity of each chain element (ChainElementT4Validity; ASN-0093) via TA5-SigValid (so `sig = #`), TA5 ..., TA5a ..., and TS3 ..."
**Problem**: The em-dash clause re-states the entire proof chain (TA5-SigValid → TA5 → TA5a → TS3) that was already derived in full under Effect One ("Chain emissions in ordinal-shift form"). The citation "By INS.chain-shift (Effect One above)" alone discharges the I-adjacency obligation; the re-enumeration is duplicated mechanism, the pattern of restating an already-established derivation rather than citing it.
**Required**: Replace the em-dash clause with the bare citation — "By INS.chain-shift, `a_{k+1} = shift(a_k, 1)`, which is the I-adjacency M7 demands."

### Issue 3: C1a preconditions discharged twice in the same section (anti-bloat)
**ASN-0100, §Per-subspace span decomposition (S8★)**: existence paragraph enumerates "(i) `f` is functional ... (ii) `dom(f)` is finite ... (iii) every position ... has first component `s_C`"; the uniqueness paragraph then re-enumerates "(i) functionality from S2, (ii) finite `dom(f)` from S8-fin, (iii) single-subspace ... from S8-depth — **are the same preconditions discharged for existence above**."
**Problem**: The section itself acknowledges the second enumeration repeats the first ("are the same preconditions discharged for existence above"). Two paragraphs in one section discharging the identical three-precondition checklist for the identical restriction `f = M'(d)|_{V_{s_C}(d')}`.
**Required**: Discharge C1a's preconditions once, then for uniqueness state "C1a, whose preconditions were discharged above, lifts M12 to the restriction, factoring through M12a/M12b" without re-listing (i)–(iii).

## OUT_OF_SCOPE

(none — the Scope and Bounding-the-Scope sections correctly defer DELETE, COPY, REARRANGE, link-subspace insertion, version derivation, and replication; the Open Questions defer them as questions, not claims.)

VERDICT: REVISE
