# Review of ASN-0126

## REVISE

### Issue 1: Implementation-mechanics citation in Single-source
**ASN-0126, Single-source (¶2)**: "Gregory confirms the implementation is hard-wired to a single `(stream, width)` span at every layer — protocol parse (`getspan`, not `getspanset`), FEBE handler (one stack-allocated `typespan`), core dispatch, and POOM execution (`deletevspanpm` reads `->stream`/`->width` once, no loop over `->next`)"
**Problem**: Function names and struct-field reads (`getspan`, `typespan`, `deletevspanpm`, `->stream`/`->width`, `->next`) are implementation mechanics, not system guarantees. They appear to justify registering R as Binary, but the justification needs only "the implementation carries a single span." The catalog of layer-internal symbols is exactly the kind of detail an abstract spec should not carry.
**Required**: Compress to a one-clause statement that the implementation is single-span at every layer; drop the symbol inventory.

### Issue 2: Defensive "one might object" digression on the G lower bound
**ASN-0126, Three shapes by G span count**: "One might object that the descriptive glosses imply a floor: a 'citation' or 'fan-out' with zero targets is not a fan-out... We hold this admission to be correct, not a gap."
**Problem**: Two paragraphs imagine an objection (zero-target citation) and rebut it with layered Nelson/Gregory citation. The substantive content — zero-G is structurally admitted under Multi; a `1 ≤ |G|` floor is a per-type semantic rule deferred to the operational layer; the only structural floor is already discharged by `|F| = 1` — is one or two sentences. The rest is meta-prose the reader must skip to follow the catalog.
**Required**: Collapse the floor discussion to: Multi admits `|G| = 0`; any non-empty-target requirement is type-semantic and deferred; the no-empty-relation floor is discharged by `|F| = 1`.

### Issue 3: Forward references to the `|·|` span-count measure
**ASN-0126, Single-source**: "`|F| = 1`... (the measure is fixed precisely under Shape-conformance below)" and **Three shapes**: "(the measure `|·|` defined under Shape-conformance below — the number of spans...)"
**Problem**: The load-bearing measure `|·|` (span count, not coverage cardinality) is used in two sections before it is defined, each with a parenthetical forward pointer. The distinction is central enough that readers cannot evaluate `|F| = 1` until they jump ahead.
**Required**: Define `|e|` = span count once, before first use, and delete both forward-pointer parentheticals.

### Issue 4: Gate-vs-landing distinction restated four times
**ASN-0126, The shape-gated emit / P4 / P6 / Worked illustration**: the separation between "the gate fires (enablement)" and "the tuple lands active (the inherited third wp conjunct)" is developed at length in The shape-gated emit, re-explained in P4 ("P4 is the *enablement* half... the wp targets the strictly stronger *landing* postcondition"), re-explained in P6 ("the *liveness* dual of P4"), and demonstrated again in the Worked illustration ("This is the gate-vs-landing distinction made concrete").
**Problem**: The same conceptual point is argued in prose in three places before the single illustration that actually establishes it. P4 and P6 statements re-derive the distinction rather than citing it.
**Required**: State the enablement-vs-landing distinction once (in The shape-gated emit), let the Worked illustration witness it, and reduce the P4/P6 prose to a one-line cross-reference.

### Issue 5: Repeated deferral to the operational successor
**ASN-0126, Three shapes / The idem flag / Registry permanence / Open questions**: "belongs to the operational successor," "the subject of a successor note," "the operational consequences are layered on top," "deferred for the successor note," plus six Open-questions items each deferring downstream.
**Problem**: Multiple paragraphs in different sections defer to the same downstream location. The Open questions section already enumerates the deferrals; the inline restatements are redundant meta-prose.
**Required**: Defer inline at most once per topic; let the Open questions list carry the rest. Remove standalone deferral sentences whose only content is "this is the successor's concern."

### Issue 6: Recurring defensive "not an oversight" phrasing
**ASN-0126, multiple sections**: "This is a deliberate exclusion, not an oversight," "We hold this admission to be correct, not a gap," "This is intentional, not an oversight: Multi is the permissive endpoint" (the Multi-is-intentional point itself appears in both Three shapes and Shape-conformance).
**Problem**: These phrases defend the author against an imagined "you forgot something" reviewer rather than advancing the claim. A correct, stated commitment does not need to assert its own intentionality.
**Required**: State the commitment; drop the "not an oversight / not a gap" defenses. Deduplicate the "Multi is the permissive endpoint" remark to one site.

### Issue 7: Over-caveated conditional simplification
**ASN-0126, The shape-gated emit, "Disciplined-domain simplification (conditional)"**: "we must be careful which condition we attach it to. The condition is *not* ASN-0086's layer-reachability... We condition instead on exactly the property that drives the vacuity..."
**Problem**: A full paragraph deliberates over *which* condition to attach to the simplification (rejecting layer-reachability, selecting UnitDepthRetractionDiscipline) before stating the simplification. The reasoning about why layer-reachability is the wrong hook is process narration; the result is one conditional sentence.
**Required**: State the simplification conditioned on UnitDepthRetractionDiscipline directly, with a single clause noting layer-reachability is too strong (the attributed `|F|=1` retraction leaves it). Drop the deliberation.

## OUT_OF_SCOPE

### Topic 1: Structural absence of a unit-depth-enforcing retraction primitive
The note is explicit that registering R as Binary does not enforce unit-depth, that the constructed `Emit_R(…,[r],{(a,δ(1,#a))})` is a prose convention rather than a `→_sh` primitive, and that a range retraction is therefore reachable (the Worked illustration proves it). Whether the framework should provide a structurally unit-depth-enforcing retraction operation is operational-layer territory (Open questions #1/#4), not a defect in this structural note — the note correctly declines to claim R-Scope holds for framework substrates.

VERDICT: REVISE
