# Review of ASN-0102

This is a thorough, well-developed ASN — X1–X16 are derived rather than asserted, the wp(COPY, S3★) analysis is non-trivial, and the worked examples exercise the firing cases of the merge predicates (coalescing example) as well as the failing ones. My findings are a definitional imprecision and accreted meta-prose flagged by the anti-bloat classifier.

## REVISE

### Issue 1: The ValidComposite★ amendment states two different restrictions
**ASN-0102, Definition (Amendment to ValidComposite★)**: "subject to the restriction that COPY occurs only as a *standalone* (length-1) composite: COPY may not appear as a non-initial step of any composite."
**Problem**: The clause before the colon ("standalone, length-1") and the gloss after it ("may not appear as a non-initial step") are not the same constraint. "Standalone length-1" forbids COPY from being *any* step of a multi-step composite, including the *initial* one. "May not appear as a non-initial step" permits COPY as the initial step of a longer composite — directly contradicting "length-1." A reader cannot tell which restriction governs, and this is precondition-level: it determines in which composites COPY is admissible, and the J0/J1★/J1'★ initial-to-final coupling evaluation in X14 relies on the composite being exactly `[COPY]`.
**Required**: State one restriction. If the intent is length-1 (as X15's "single elementary transition" and X14's "length-1 composite" suggest), the gloss should read "COPY must be the sole step of its composite," not "non-initial step."

### Issue 2: Composite-boundary status is established twice
**ASN-0102, Definition (Amendment) and X14**: The Amendment paragraph already establishes "A standalone COPY Σ → Σ' is then a valid composite ... so its endpoints Σ and Σ' are composite boundaries, at which the composite-boundary properties of ASN-0047, in particular P4★ ..., hold." X14 then re-derives the same fact: "Because the Definition amends ValidComposite★'s atomic enumeration to admit COPY, a one-step COPY is itself a valid composite, and its pre- and post-states Σ, Σ' are composite boundaries ... and the composite-boundary property P4★ holds at Σ."
**Problem**: Two paragraphs in the same document say the same thing in different words. The composite-boundary status and the availability of P4★ are load-bearing once (for the J1'★ Old-branch); establishing them in the Definition and re-establishing them at the head of X14 is duplication of the kind this anti-bloat pass exists to remove.
**Required**: Establish the composite-boundary status once (in the Definition) and have X14 reference it rather than re-derive it.

### Issue 3: Implementation-divergence parenthetical in X8 does not advance the abstract claim
**ASN-0102, X8**: "(Gregory's POOM is observed to coalesce a same-origin, I-abutting boundary in place, realising the canonical count, while the spanfilade containment index keeps one entry per reference; this divergence is a property of which concrete index one inspects, not a guarantee the abstract specification imposes — Q8.)"
**Problem**: The abstract content of X8 — that the constructed `k`-block form and the canonical `≤ k` form denote the *same* arrangement — is already stated in the preceding sentence. The parenthetical is implementation mechanics plus a justificatory tail ("not a guarantee the abstract specification imposes") that defends the spec against an observation the spec does not make. It is meta-prose the precise reader must work around.
**Required**: Drop the parenthetical (or reduce to the bare evidentiary citation) — the abstract claim stands without it.

### Issue 4: Justificatory framing around X1
**ASN-0102, X1**: "This is immediate from the definition `Σ'.C = Σ.C`. But it is not an arbitrary stipulation; it is *what the act of inclusion means*."
**Problem**: "it is not an arbitrary stipulation" is defensive prose explaining why the clause is justified rather than what it asserts. The Nelson quote that follows supplies the semantic grounding on its own; the framing sentence adds no reasoning.
**Required**: Cut the "not an arbitrary stipulation" sentence; let the definition and the quote carry it.

## OUT_OF_SCOPE

The Open Questions correctly defer discoverability-under-displacement, transitive containment-as-source, time-varying views, and identity under unreachable allocators to future ASNs — these are not gaps in this ASN.

VERDICT: REVISE
