# Review of ASN-0099

## REVISE

### Issue 1: F10 omits the empty-result presentation
**ASN-0099, "Result Ordering" (F10)**: "The result set admits a unique presentation as a sequence ⟨a₁, a₂, ..., aₙ⟩ ... Any non-empty finite totally-ordered set admits a unique enumeration by finite induction."

**Problem**: `findlinks(I, Σ)` is empty whenever no link matches even though `dom(Σ.L) ≠ ∅` (e.g., Query 5's `findlinks_V({v_a^2}, d_a, Σ_5) = ∅` with a non-empty link store). The justification explicitly restricts to the *non-empty* case, and the Empty Query section only addresses the `dom(Σ.L) = ∅` situation. The empty result is a mandatory boundary case and its presentation (the empty sequence) is asserted nowhere.

**Required**: State that the empty result presents as the empty sequence and confirm uniqueness covers `n = 0`, or fold the empty case into F10's justification rather than excluding it.

### Issue 2: Open Questions closing paragraph is pure deferral meta-prose
**ASN-0099, "Open Questions"**: "The scope exclusions listed under *What We Have Not Specified* — out-of-store query semantics, partition tolerance, the consistency model, access-control composition, and the inverse direction — each remain open research questions; they are not restated here."

**Problem**: This paragraph advances no reasoning. It re-inventories a list from another section solely to point back at it and announce non-restatement — the deferral/pointer accretion pattern. Naming "they are not restated here" is itself the only content.

**Required**: Delete the paragraph. The exclusions already stand in "What We Have Not Specified."

### Issue 3: "What Completeness Demands" and "Reflection" duplicate the Completeness section
**ASN-0099, "What Completeness Demands of Implementations"**: "The spec's demand is exactly F2 ∧ F3 ... Any implementation whose `result(I, Σ)` differs from the set comprehension is non-conforming, regardless of cause." **And "Reflection"**: "The discovery operation reduces to a single set comprehension ... The abstract specification is just the comprehension."

**Problem**: Both sections restate what the Completeness section already established (`result(I, Σ) = findlinks(I, Σ)`, "Completeness must hold unconditionally," soundness forbids false positives). Three sections now say "it is just the comprehension" in different words — the same-thing-in-different-words pattern, essay content padding structural slots.

**Required**: Remove the duplicated restatements; if any operationally new commitment survives (e.g., "regardless of mechanism"), fold the single surviving sentence into the Completeness section.

### Issue 4: Intersection-vs-containment justification duplicates F4
**ASN-0099, "The Match Predicate"**: "Intersection (rather than containment) is forced by symmetry: a link is about every byte its endsets cover (L13), one shared byte suffices, and to require containment in either direction would impose a circular precondition ..."

**Problem**: F4 (MatchIndividuation), via Strengthening 1 and Strengthening 2, already formally establishes that both containment directions define a *different* operation, with explicit witnesses. The prose argues the same conclusion informally before F4 proves it. This is defensive justification of a design choice the formal claim carries on its own.

**Required**: Trim the prose to a one-line pointer that F4 individuates intersection against the containment variants, or delete it; do not argue the choice twice.

## OUT_OF_SCOPE

### Topic 1: Inverse direction (FOLLOWLINK / RETRIEVEENDSETS), index witness, latency bound
**Why out of scope**: The ASN correctly defers resolving result endsets back to V-positions, index auditability, and any K.λ-to-visibility timing bound to future work; these are new territory, not defects here.

VERDICT: REVISE
