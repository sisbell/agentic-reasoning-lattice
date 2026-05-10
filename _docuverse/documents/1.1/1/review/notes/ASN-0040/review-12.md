# Review of ASN-0040

## REVISE

### Issue 1: B1 proof — B6(iii) not verified for the stream-identity sub-case

**ASN-0040, B1 (Contiguous Prefix), other-namespaces case**: "Since p' satisfies T4 (p₁ > 0, no adjacent zeros, p'_{#p'} = p_{#p−1} > 0 since the trailing zero was the sole defect) and (p', 2) satisfies B6, two sub-cases arise."

**Problem**: The claim "(p', 2) satisfies B6" is asserted but B6(iii) is not derived. The verification requires: (1) "sole defect" entails zeros(p) ≤ 3 — otherwise the zero-count violation would be a second defect; (2) zeros(p') = zeros(p) − 1 since the trailing zero was removed; (3) therefore zeros(p') + (2 − 1) ≤ 3. The T4 verification for p' similarly omits the zeros(p') ≤ 3 check, which follows from the same chain. Each step is one line, but in a proof that elsewhere shows every case explicitly, leaving three inferential steps to the reader is inconsistent with the standard the rest of the ASN sets.

**Required**: After showing p' satisfies T4's syntactic conditions, add: "The sole-defect hypothesis gives zeros(p) ≤ 3 (a second violation would contradict sole defect). Removing the trailing zero yields zeros(p') = zeros(p) − 1 ≤ 2. B6(iii): zeros(p') + (2 − 1) = zeros(p') + 1 ≤ 3. B6(i) and B6(ii) hold by the argument above. Therefore (p', 2) satisfies B6."

### Issue 2: Properties Table — B1 dependency list omits B10

**ASN-0040, Properties Table, B1 row**: "from B₀ conf., B0, B0a, B4, B7, Bop, S0, TA5(c)"

**Problem**: The B1 preservation proof's other-namespaces case relies on B10 for the sub-case where all stream elements violate T4: "since a satisfies T4, a ∉ S(p, d). Moreover, B10 for the current state ensures every element of B satisfies T4, so children(B, p, d) = ∅." The B1 Formal Contract correctly mentions B10, but the summary table omits it. Since B1 and B10 are co-inductive invariants proved in the same inductive step (B10's preservation proof uses B1 to identify cₘ for the m ≥ 1 case), the mutual dependency should be explicit in the table. The same table also omits B0 from Bop's dependency list, though Bop's proof uses B0 both in the monotonicity postcondition and in B1 preservation ("By B0, existing elements persist").

**Required**: Add B10 to B1's "from" list. Add B0 to Bop's "from" list. Verify other rows against their Formal Contracts for similar omissions.

### Issue 3: Post-proof B1 recap is redundant with the formal proof

**ASN-0040, B1 section, paragraph beginning "The argument proceeds by induction on the sequence of baptisms within a namespace"**

**Problem**: After the B1 proof closes (∎), three paragraphs re-argue the inductive step using a different induction strategy ("induction on the sequence of baptisms within a namespace" — per-namespace induction — versus the formal proof's per-state-transition induction). The simplified re-argument omits the other-namespaces case entirely, then acknowledges this gap: "This argument rests on two additional properties. First, no operation outside this namespace inserts an element into S(p, d)..." The full proof above already handles all cases rigorously. The recap neither adds rigor nor introduces new results — the "no-skip property" observation ("The gap between T9 and B1 is the no-skip property") appears in a separate paragraph after the recap and is the only new content in this passage.

**Required**: Remove the re-argued inductive step. Retain the no-skip observation and the dependency identification (B7, B0a) as standalone remarks following the proof.

## OUT_OF_SCOPE

### Topic 1: Parent prerequisite chain
**Why out of scope**: Whether p ∈ Σ.B is required before baptizing children beneath p depends on the ownership model (deferred to Tumbler Ownership). The ASN correctly defers this in Bop's precondition and in the Open Questions. Resolving it here would require importing authorization semantics that belong in a separate ASN.

### Topic 2: Content-occupation binding
**Why out of scope**: B3 states that `occupied(t) ⟹ t ∈ Σ.B` as a requirement on downstream content operations but does not formalize the `occupied` predicate. This belongs in a content storage ASN — B3 correctly records the interface contract without defining the other side.

VERDICT: REVISE
