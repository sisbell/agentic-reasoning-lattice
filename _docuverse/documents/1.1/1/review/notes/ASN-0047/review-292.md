# Review of ASN-0047

I checked the elementary transitions, the K.δ allocation discharge, the K.μ~ decomposition, the D-SEQ★ derivation (both m=2 and m≥3 cases), FrontierEquivalence, and the worked examples. The core correctness argument is sound — boundary cases (full clearance, empty arrangement, single-position subspace, node nesting in CrossNodeAccountBase, the m=3 degeneracy of the inner-tuple range) are genuinely covered, and the proofs do not lean on "by similar reasoning." The findings below are the repeated-meta-prose patterns the anti-bloat classifier directs me to surface, plus one accretion observation.

## REVISE

### Issue 1: P4a's "trace property" classification is restated in four locations
**ASN-0047, P4a definition box / ExtendedReachableStateInvariants preamble / Class (b) prose / Composite-boundary matrix row**: The definition box says "P4a is *not* a state-local invariant... We classify it explicitly as a *trace property*"; the preamble repeats "P4a is a *trace property* (defined and discharged in its definition box)"; the matrix row repeats "P4a is a trace property whose witnessing existential ranges over composite boundaries"; the Class (b) prose again defers to "the induction-along-the-witnessing-trace mechanism of its definition box."

**Problem**: The same classification-and-deferral is asserted four times in different words, each pointing back to the definition box. This is the "multiple paragraphs defer to the same downstream location" / "two paragraphs say the same thing" pattern. A reader tracking P4a's discharge must read the same meta-statement four times to confirm none of them adds content.

**Required**: State the trace-property classification and its discharge once (the definition box), and reduce the other three to a bare pointer or drop them. The matrix row and preamble do not need to re-explain *why* it is a trace property.

### Issue 2: K.μ~ clause-(v) "forced, not a guarantee" is restated four times with bidirectional cross-references
**ASN-0047, Decomposition of K.μ~ (clause (v) in the admissibility list) / Step (A) / Link-subspace fixity and realisation / Link V-position permanence**: Clause (v)'s prose says it "is *not* an independent design choice in the manner of (iv); it is *forced by the chosen full-clearance realisation*... This fixity is thus a property of the chosen full-clearance realisation, not a lifetime guarantee on a link's V-position (see *Link V-position permanence* below)." "Link-subspace fixity and realisation" repeats "it is forced by the full-clearance realisation (above), not posited freely." "Link V-position permanence" repeats "Single-K.μ~ link fixity is a *realisation artifact* of the full-clearance decomposition (clause (v)), not a lifetime guarantee."

**Problem**: The single point — clause (v) is realisation-forced, not a global non-rearrangeability guarantee — is made four times, with forward ("see... below") and backward ("(above)") pointers between the copies. This is defensive justification of why the clause exists rather than prose advancing the proof, and the reader must skip past it repeatedly to follow the actual fixity derivation (LRP + CL-UNIQ, sub-step (4)).

**Required**: Make the "forced, not a lifetime guarantee" observation once — at clause (v) — and let "Link V-position permanence" simply exhibit the re-seating composite without re-litigating the distinction. Remove the bidirectional cross-references.

### Issue 3: GlobalLineage is a derived corollary with no consumer in this ASN
**ASN-0047, Cross-layer invariants**: "GlobalLineage (Derived corollary)... `(A x ∈ E ∪ dom(C) ∪ dom(L) :: n₀ ≼ x)`."

**Problem**: NodeLineage is load-bearing (K.δ case (i) precondition, the GlobalLineage derivation itself). GlobalLineage, by contrast, is derived and then never used — no operation precondition, invariant discharge, or downstream lemma consumes it. Together with NodeBaptism, NodeLineage, TrackedEmission, FrontierEquivalence, and CrossDocEntityDisjoint, it is part of a recently-added entity-lineage cluster; a terminal corollary that nothing depends on is accretion, not a derived consequence the argument requires.

**Required**: Either cite the specific later claim GlobalLineage supports (in which case state that consumer at the corollary), or drop it. If it is retained as motivation, say so explicitly rather than presenting it as a load-bearing derivation.

## OUT_OF_SCOPE

### Topic 1: Interior/front content insertion and renumbering
The elementary K.μ⁺ appends content positions only at the suffix (D-MIN★/D-SEQ★ force `V_{s_C}(d) = {[s_C,1..n]}` and K.μ⁺ preserves existing positions), so inserting content at an interior or initial V-position requires a renumbering composite. The named INSERT operation and its renumbering semantics are explicitly out of scope; the open question on `DELETEVSPAN`-style link renumbering already flags the analogous gap. No revision needed here.

### Topic 2: Concurrent allocation under one home document
The open questions raise serialization of link/content allocation under concurrent operations. Operation atomicity and concurrency are out of scope; correctly deferred.

VERDICT: REVISE
