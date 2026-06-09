# Review of ASN-0126

## REVISE

### Issue 1: The gate-vs-landing (enablement vs active-subset) distinction is restated four-plus times

**ASN-0126, The shape-gated emit / Worked illustration / P4 / P6**: the same point — "the gate enables but does not guarantee active landing" — appears as:
- "So the proper statement is: the gate rejects exactly the unregistered/non-conforming and non-triple calls and is the *enablement* (safety) half that P4 records 'by construction'; the *active-subset* wp is a separate, strictly stronger condition..."
- "This is the gate-vs-landing distinction made concrete: P4 (the gate's enablement guarantee) is satisfied, while the strictly stronger active-subset wp is violated..."
- "P4 records the gate's *enablement* half only."
- "The two halves bracket the gate exactly: it fires on *precisely* the conforming triples... no more (P4), no fewer (P6)."

**Problem**: Within "The shape-gated emit" alone the enablement-vs-landing point is made three times (the wp paragraph, the "strictly stronger" paragraph, and the closing "proper statement" sentence). The Worked illustration then re-derives it concretely — which is the right place — and P4/P6 restate it yet again. This is the anti-bloat target's core accretion: the reader skips past the same observation repeatedly.

**Required**: State the distinction once in "The shape-gated emit," let the Worked illustration carry the concrete witness, and trim the restatements in P4/P6 to a bare pointer.

### Issue 2: L4/L9 ghost / no-residence-check inheritance stated in full twice

**ASN-0126, Three shapes by G span count** and **Shape-conformance**:
- Three shapes: "Endset targets are unrestricted. `F` and `G` spans may point anywhere... This is L4 (EndsetGenerality) and L9 (TypeGhostPermission, ASN-0043) inherited without narrowing. The framework constrains the *span count* per shape; it never constrains the residence..."
- Shape-conformance: "`Sh-conf` consults nothing about content residence. Endset spans may reference any address, including ghost addresses... L4 and L9 (ASN-0043) permit this, Nelson is explicit that 'endset addresses do NOT need to resolve to stored content'... The framework inherits that permission unchanged."

**Problem**: Two paragraphs in different sections make the identical claim (span-count constrained, residence not; L4/L9 inherited). The Worked illustration P5 then demonstrates it a third time concretely. This is the "two paragraphs say the same thing in different words" pattern.

**Required**: Keep the no-residence commitment where it does work — in Shape-conformance, where it grounds P5 state-independence — and delete the redundant statement in Three shapes (or reduce it to a one-line pointer).

### Issue 3: C0 prose explains why the axiom is needed rather than stating it

**ASN-0126, Registration entries**: "Without the finiteness conjunct a partial function over the infinite domain `T_admissible/~` need not be finitely representable and membership need not be decidable; finiteness is what closes that gap." Also "It is the condition that makes the intro's 'finite shape catalog' literal and that grounds the central guarantee..." and "C0 constrains the one degree of freedom P1 does not touch... sitting beside the implicit well-formedness... The Properties below are stated... and C0 is now among those commitments."

**Problem**: This is the flagged "new prose around an axiom explains why the axiom is needed rather than what it says" pattern. The decidability payoff of finiteness is already established one paragraph earlier ("Finiteness bounds the number of comparisons and CoverageEqualityDecidable discharges each one"). The "Without the finiteness conjunct..." sentence and the "C0 constrains the one degree of freedom..." paragraph are motivation, not content.

**Required**: State C0 (well-formed, finite partial function, unique coverage-class keys) and its one decidability consequence. Drop the counterfactual justification and the meta-paragraph about C0's place among commitments.

### Issue 4: Defensive asides reassuring the reader the substrate is not "refusing"

**ASN-0126, The shape-gated emit**: "This framework does not pretend `→` already rejects them — it **refines** the emit step." / "This is not a refusal by the substrate: higher arity is available off-gate (Single-source)." / "ASN-0086 is deliberate here: it claims wp/precondition coincidence only for Case 1... We follow suit."

**Problem**: These are defensive justifications that do not advance the argument — they reassure rather than establish. "We follow suit" and "not a refusal by the substrate" are precisely the meta-prose the precise reader must skip.

**Required**: Remove the reassurance clauses; the off-gate availability is already stated in Single-source, and the wp-coincidence scoping is carried by the formal statement.

### Issue 5: The abutting-span resolution is over-justified

**ASN-0126, Shape-conformance**: the paragraph beginning "One edge follows from counting spans rather than coverage..." through the Gregory `spanf1.c`/`orglinks.c` no-coalescing confirmation.

**Problem**: The whole edge reduces to: `|e|` is set cardinality of `Endset = 𝒫_fin(Span)`, so two abutting spans are two elements and fail a one-span shape; coalescing is the app's job. The Gregory implementation-trace ("`insertspanf`," "consolidation hook commented out") is evidence for a design choice that the set-cardinality definition already forces — it does not change the formal content. This is essay content in a structural slot.

**Required**: Keep the one-sentence rule ("a single-span slot means a single span as emitted; coalescing abutting spans is the app's responsibility") and the P5 state-independence note. Cut the implementation trace to a single citation or drop it.

## OUT_OF_SCOPE

### Topic 1: The `idem` flag carries no conformance role in this note

`Sh-conf` never reads `idem`; the flag's semantics are entirely deferred to Open Question 1. Registering the slot now and proving P3 (its stability) is defensible as reserving the registry field, and the deferral is explicit — so this is successor-note territory, not an error here. Worth confirming the P3 prose stays one line rather than growing to match P2.

### Topic 2: Provenance of the attribution span `r` in re-expressed retraction

Single-source leaves `r` "an unbound attribution parameter." Where attribution content originates is a layer/operational concern, correctly deferred (Open Questions); the framework only commits `|F| = 1`.

VERDICT: REVISE
