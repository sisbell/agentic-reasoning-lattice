# Review of ASN-0100

## REVISE

### Issue 1: Spurious I3 dependency for the shift clause

**ASN-0100, §Effect Three (Shift) and "Only I3's shift clause transfers"**: "This clause is exactly the I3 postcondition (PostInsertionShift) of ASN-0082... I3 establishes the shift-image clause unchanged in either model."

**Problem**: INS.M-shift (`shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v,n)) = M(d)(v)`) is *part of the specified effect of INSERT's step-3 K.μ⁺*, which adds exactly these mappings by construction. I3 is a postcondition of a *different* operation defined in ASN-0082, whose `M'(d)` is not INSERT's `M'(d)`. The ASN itself admits the arrangements differ and then reconciles them by asserting "both apply the same shift rule" — but that sameness is just INSERT's own K.μ⁺ specification. So I3 contributes nothing the K.μ⁺ effect does not already give: the clause is established by INSERT's construction, not derived from I3. The discharge of I3's five preconditions (i)–(v) and the multi-paragraph reconciliation are apparatus around a citation that does no work.

**Required**: Either state precisely what I3 contributes that K.μ⁺'s specified effect does not (and only that), or drop the I3 dependency and present INS.M-shift as the K.μ⁺ effect directly. The well-formedness (S8a, S8-depth) and functionality (TS1/TS2) consequences are already re-derived elsewhere without I3.

### Issue 2: The same "we do not import / the foundation frame fails" justification is restated in five sections

**ASN-0100, §Effect Three, §Arrangement functionality, §Referential integrity, §Post-state V-position well-formedness, §Per-subspace span decomposition**: e.g. "we do not import ASN-0082's I3-S2, whose shift-only justification rests on the failing frame"; "We do not import ASN-0082's I3-S3... via dom(C') = dom(C) (I3-C) — exactly the frame that fails here"; "their justifications run through I3's whole-post-state frames — which fail here"; "We do not appeal to M2 on the whole post-state arrangement..."

**Problem**: This is one idea — *INSERT extends `dom(C)`, so any foundation lemma whose proof assumes the store is frozen cannot be imported; we re-derive instead* — repeated as defensive prose in five places. Per the anti-bloat guidance, the same point said in different words across sections is accretion the reader must wade through.

**Required**: State the non-import principle once (the "Only I3's shift clause transfers" paragraph is the natural hub) and let each section silently re-derive without re-explaining why it is not importing.

### Issue 3: Atomicity-level statement repeated three times

**ASN-0100, "Composite atomicity" paragraph, closing "Both atomicity levels INSERT relies on..." paragraph, and INS.atomicity table row**: each states that elementary atomicity comes from SequentialTransitionAxiom and composite atomicity is definitional under ValidComposite★.

**Problem**: The identical decomposition of "two atomicity levels" appears three times. The closing paragraph adds nothing over the opening one and the table row.

**Required**: Keep one statement (the table row plus one prose location) and remove the duplicate.

### Issue 4: Effect Two refutes an imagined alternative proof route

**ASN-0100, §Effect Two (Placement)**: "the set-membership characterisation `p ∈ V_{s_C}(d) ∪ {[s_C,1,…,1]}` would fail for the append case (`p_m = N + 1`...) so we appeal to the predicates' postconditions directly."

**Problem**: This paragraph constructs an alternative argument route, shows it fails, then takes a different route. The reader only needs the route that works ("S8a transfers from `p` via ValidInsertionPosition/ValidFirstInsertionPosition postcondition (b)"). Refuting a rejected route is meta-prose.

**Required**: State the working derivation; delete the refutation of the set-membership route.

## OUT_OF_SCOPE

### Topic 1: Failure recovery to canonical order
Raised in Open Questions; partial-failure recovery during the composite is implementation-level and correctly deferred.

### Topic 2: Concurrent INSERTs at the same V-position
Raised in Open Questions; concurrency control is explicitly below this ASN's abstraction level.

VERDICT: REVISE
