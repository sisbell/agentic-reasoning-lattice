# Review of ASN-0086

I checked the proofs (R0–R7a), the operation definitions, the wp computations, and the worked examples. The mathematical core is solid: the cross-home freshness derivation in R0 (subsequent branch) is correct and conformance-free, R0a's two-case antichain argument is sound, R0a-Cor2's zero-position-stability induction holds, and the wp necessity arguments each supply a valid single counterexample per conjunct. I did not find a logical gap.

The findings below are all instances of the forward-reference / meta-prose accretion the `review-mode.anti-bloat` classifier flags. They are genuine — each forces the reader to skip past justification-about-the-argument to reach the argument.

## REVISE

### Issue 1: Emit_K definition enumerates its own downstream consumers
**ASN-0086, Definition — Emit_K**: "This full state space is the common domain of quantification for Emit_K, the Lemma — Emit_K function-ness (below), and every weakest-precondition computation in this note: ranging over it rather than the conforming sub-space is what makes conformance conjuncts such as P2c genuinely dischargeable rather than vacuous standing invariants."
**Problem**: This is a use-site inventory ("the common domain of quantification for Emit_K, the Lemma…, and every wp computation") plus a justification for why the domain choice matters — meta-prose about the argument, not the argument. The relevant fact ("Σ ranges over the full ↝*-reachable state space") is already stated in the preceding clause; the consumer list and the P2c-dischargeability rationale add nothing to the definition's meaning.
**Required**: Cut the sentence. State the domain once; let P2c's load-bearing role be demonstrated where the wp is actually computed (it already is, under "Necessity" in wp Case 1).

### Issue 2: R7a's contingency caveat is stated three times
**ASN-0086, R7a "Scope of the conclusion" paragraph and Properties Introduced table**: the "Scope of the conclusion — contingent on conforming-layer clause (b)" paragraph and the table's "**Contingency:**" block restate the same point — that `Σ_m.L = Σ'.L` is conditional on clause (b), strong for layers satisfying it, silent otherwise, and not an unconditional substrate guarantee for composite steps.
**Problem**: Two paragraphs in different sections say the same thing in different words; the proof body also restates it inline ("which the discharge (4)(iii) below consumes"). The caveat is load-bearing once — it does not need three carriers.
**Required**: State the contingency once, at the lemma statement. The table entry should point to it, not re-prosecute it.

### Issue 3: R7a Decomposition Example appendix justifies its own placement and defers to the Worked Sketch
**ASN-0086, R7a Decomposition Example**: "This appendix collects the worked decomposition that exercises R7a's interleaving structure non-trivially, kept out of the lemma's proof body so that R7a carries only its case discharges." And: "*Same-home multi-key subsequent-emission replay — see Worked Sketch.* … is not re-derived here because the Worked Sketch's Steps 1–3 already walk through the identical … A reader wanting the subsequent-emission replay in isolation should read Worked Sketch Steps 1–3 as a single composite ↝-step decomposed by R7a."
**Problem**: The first sentence justifies document ordering (placement out of the proof body). The second is a deferral-to-downstream-location pattern — a whole sub-paragraph whose content is "this case is elsewhere, go read it." The R7a proof tail also points forward to this appendix ("exercised in the R7a Decomposition Example appendix (after the Worked Sketch)"), completing a deferral chain proof-body → appendix → Worked Sketch.
**Required**: Drop the placement justification (the appendix's existence needs no defense). Either inline the one cross-reference where the case is discharged or delete the "see Worked Sketch" paragraph entirely — the Worked Sketch already exercises the machinery; a paragraph announcing that fact is noise.

### Issue 4: Nullify definition repeats "P1/P2 do not gate emission"
**ASN-0086, Definition — Nullify**: "Neither P1 nor P2 gates emission… P1 is required for the *postcondition*… though not for emission to execute. P2 restricts the operation… rather than making the operation undefined." Earlier in the same paragraph: "two further *postcondition-establishing conditions* that do **not** gate emission."
**Problem**: The non-gating status of P1 and P2 is asserted three times in one paragraph. The substantive content (P1 establishes `a ∈ nullified(Σ')`; P2 scopes to arity-3) is stated once and is correct; the repeated "does not gate emission" framing is defensive padding around it.
**Required**: State each condition's role once. "P0 gates emission; P1 establishes the nullification postcondition; P2 scopes the active-subset effect to arity-3" suffices.

## OUT_OF_SCOPE

### Topic 1: Observe_K result ordering and Emit/Observe atomicity
The Open Questions already park these. No claim in this ASN turns on them; they are future-ASN territory, not defects here.

### Topic 2: Elevating the unit-depth retraction discipline to a substrate guarantee
The note correctly treats this as a layer convention and flags the design tradeoff as an open question. Whether to introduce a dedicated retraction K-operation belongs in a future substrate ASN, not this one.

VERDICT: REVISE
