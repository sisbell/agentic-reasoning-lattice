# Review of ASN-0082

## REVISE

### Issue 1: I3-S7 and S7-post incomplete coverage of the S7 family

**ASN-0082, I3-S7 lemma**: "The post-state satisfies S7a (DocumentScopedAllocation), S7b (ElementLevelIAddresses), and S7c (ElementFieldDepth)."

**ASN-0082, S7-post lemma**: same coverage — "S7a, S7b, S7c."

**Problem**: The ASN-0036 foundation supplies four S7-family axioms — S7a, S7b, S7c, **S7d** (DocumentAllocationDiscipline) — and the derived theorem **S7** (StructuralAttribution), which depends on S7a, S7b, and S7d jointly. Both preservation lemmas omit S7d and the theorem S7. Without S7d's preservation, the chain of dependencies for S7 itself is broken — the lemmas establish two of three premises but leave the third unstated, and the theorem they implicitly support is never named. This is a real gap even if both extensions are trivial (dom(C) unchanged ⟹ all predicates over dom(C) preserved; no document allocation ⟹ S7d preserved verbatim).

**Required**: Either (a) extend both lemmas to explicitly state S7d preservation and S7 preservation as a corollary, with a one-line justification, or (b) rename the lemmas to "S7a-S7c Preservation" and add separate preservation arguments for S7d and the derived S7.

### Issue 2: D-S(a) derivation hand-waves a NAT-addbound + NAT-order step

**ASN-0082, D-S(a) derivation**: "From s ∈ R, ord(s) ≥ w_ord (...the same derivation that establishes D-BJ's well-definedness...), and adding [c'] (componentwise positive) only widens the inequality, so ord(reach(σₛ)) = [s₂ + c'] ≥ [c] = w_ord."

**Problem**: The phrase "adding [c'] only widens the inequality" is rhetorical, not formal. The formal step is: NAT-addbound's left-dominance at `(m, n) := (s₂, c')` gives `s₂ + c' ≥ s₂`; NAT-order's `≤`-transitivity Consequence then composes `s₂ + c' ≥ s₂` with `s₂ ≥ c` to yield `s₂ + c' ≥ c`. The ASN is otherwise meticulous about citing NAT-* dependencies inline (PositiveOffsetExceeds, the I3-S(a) commutativity chain, etc.); this step is an inconsistency in the level of rigor.

**Required**: Replace the rhetorical sentence with the explicit NAT-addbound left-dominance citation chained with NAT-order's `≤`-transitivity.

## OUT_OF_SCOPE

### Topic 1: Spans crossing the insertion or contraction boundary
**Why out of scope**: I3-S restricts to `s ≥ p` and D-S restricts to `s ∈ R`. Spans straddling the boundary (start before, reach after) require span-splitting composition with ASN-0053's S4/S11 — natural extension, but its preconditions and case analysis belong in a downstream ASN that composes within-region results with split/merge.

### Topic 2: Deeper-depth contraction (#p > 2)
**Why out of scope**: The Open Questions section flags this. The TA4 obstruction is real (zero-prefix vs S8a positivity collision once `k = m − 1 > 1`); resolution requires either a strengthened TA4 or a from-scratch partial-inverse identity at deeper depth — substantive new foundation analysis, not a revision to this ASN.

### Topic 3: External-system V-position references through shifts
**Why out of scope**: Open Question 1. This is a system-protocol concern (what update mechanism the system must expose to clients holding V-position handles) outside the arrangement-layer specification.

### Topic 4: Link-subspace mutation discipline
**Why out of scope**: The ASN consistently notes that link-subspace mutation uses tombstoning rather than shift-to-close-gap, deferred to a future operation ASN. The current ASN correctly handles the link subspace as either active (subject to I3's typing-only invariants, no contiguity obligations) or cross-subspace (preserved verbatim by I3-X / D-CS); the distinct tombstone-based mutation operations belong elsewhere.

VERDICT: REVISE
