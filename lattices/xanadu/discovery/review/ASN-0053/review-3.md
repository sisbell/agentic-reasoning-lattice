# Review of ASN-0053

## REVISE

### Issue 1: Mutual determination claim is false for (width, reach) → start
**ASN-0053, The reach function**: "The three quantities — start, width, reach — are mutually determining: any two fix the third, when the span is level-uniform (#start = #width)."
**Problem**: The many-to-one property of TumblerAdd (noted in ASN-0034) directly refutes this. When the action point k < #s, positions k+1..#s of the start are replaced by the width's tail and are unrecoverable from the reach. Counterexample: s₁ = [1, 3, 5] and s₂ = [1, 3, 7] both yield reach [1, 5, 4] with width [0, 2, 4] (action point k = 2 < 3 = #s). Both spans are level-uniform. Same width and reach, different starts, different denotations. The claim holds only for start+width→reach and start+reach→width, not for width+reach→start.
**Required**: Correct to: "start and width determine reach (by definition); start and reach determine width (by D1). Width and reach do not determine start when the action point falls before the last component." This is a two-out-of-three result, not mutual determination.

### Issue 2: D1 a = b remark is undefined
**ASN-0053, The reach function**: "The identity holds trivially when a = b (no displacement needed)."
**Problem**: D1 is stated for a < b. When a = b, TumblerSubtract produces the zero tumbler, and TumblerAdd requires w > 0 (TA0 precondition). The expression a ⊕ (b ⊖ a) is undefined when a = b. The remark claims a trivial extension that doesn't exist.
**Required**: Remove the a = b remark or restate it correctly: "When a = b, no displacement is needed; the degenerate case is handled separately since the round-trip expression is not well-formed."

### Issue 3: Constructed spans not verified against T12
**ASN-0053, S1, S3, S4**: In S1, γ = (s', r' ⊖ s'); in S3, γ = (s, r ⊖ s); in S4, λ = (s, d) and ρ = (p, d').
**Problem**: Each proof constructs a span and asserts properties of its denotation without verifying T12 — that the width is positive and its action point falls within #start. The well-formedness holds in all cases (e.g., for S4: s < p implies d = p ⊖ s has a positive component at the divergence point, and that divergence point is ≤ #s since #s = #p), but the verification is omitted. The proofs jump from "these are the endpoints" to "this is a span" without the intermediate step.
**Required**: Each proof should state explicitly: (1) width > 0 (from the strict ordering of endpoints at the divergence point), and (2) action point of width ≤ #start (from the divergence falling within the tumbler length). Two sentences per proof.

### Issue 4: S11 statement lacks level preconditions
**ASN-0053, S11**: "For spans α and β with ⟦β⟧ ⊆ ⟦α⟧, the set difference ⟦α⟧ \ ⟦β⟧ is expressible as a span-set of at most two spans."
**Problem**: The proof explicitly requires level-uniformity ("representable as a span when α and β are level-uniform"), but the formal statement imposes no level constraint. Every other closure property (S1, S3, S4, S5) states its level requirements. S11 is the exception, creating an inconsistency: the statement claims unconditional representability, the proof establishes it only for level-uniform, level-compatible spans.
**Required**: Add level preconditions to S11's statement: "For level-uniform spans α and β with level_compat(start(α), start(β)) and ⟦β⟧ ⊆ ⟦α⟧, ..."

### Issue 5: S8 does not prove denotation preservation
**ASN-0053, S8**: "The result is a sequence of spans satisfying N1 and N2 whose union equals ⟦Σ⟧."
**Problem**: The construction (sort, sweep-line merge) is described and its output is claimed to satisfy N1, N2, and equivalence with the input. N1 and N2 are verifiable from the construction. But "whose union equals ⟦Σ⟧" is asserted without proof. The argument requires showing: (a) every position in ⟦Σ⟧ is in some output interval (no loss during merge/emit), and (b) every position in an output interval was in some input span (no spurious coverage). The merge step extends r to max(r, reach(σᵢ)) — this preserves coverage of σᵢ but the connection to the full input set needs to be made explicit.
**Required**: Add a loop invariant: "At each step, the union of emitted spans plus the current interval [s, r) equals the union of all input spans processed so far." Verify it holds on initialization (first span), on merge (extending r covers σᵢ's positions), and on emit (the emitted interval covers exactly the positions accumulated).

### Issue 6: SC exhaustiveness asserted without case analysis
**ASN-0053, SC**: "five mutually exclusive cases arise" and "This exhaustive classification is forced by the total order; no implementation can introduce a sixth case."
**Problem**: The claim that five cases exhaust all possibilities for two half-open intervals requires at minimum a sketch showing how the possible orderings of {start(α), reach(α), start(β), reach(β)} — subject to start < reach for each span — map onto exactly these five cases. "Forced by the total order" is a claim, not a proof. Mutual exclusivity between cases (iii) and (iv) is particularly non-obvious without checking: overlap has reach(α) < reach(β), while containment has reach(β) ≤ reach(α) — these are distinguished by a single inequality direction on the reaches.
**Required**: Add a WLOG sketch: "Assume start(α) ≤ start(β). Then reach(α) vs start(β) gives separated/adjacent/overlapping. In the overlapping case, reach(α) vs reach(β) distinguishes proper overlap from containment. The case start(α) = start(β) forces containment or equality. Five cases total, no ordering of the four boundary points is unaccounted for."

### Issue 7: S7 proof is a single sentence
**ASN-0053, S7**: "In the degenerate case, each position can be covered by a unit span."
**Problem**: The proof doesn't construct the unit span, doesn't verify T12 for it, and doesn't verify it covers the target position. The construction is straightforward (for tumbler t, take ℓ = [0, ..., 0, 1] with #ℓ = #t; the action point is #t ≤ #t, and ℓ > 0, so T12 is satisfied), but "each position can be covered" is a claim, not a proof.
**Required**: Construct the unit span explicitly: "For any tumbler t, define ℓ = [0, ..., 0, 1] with #ℓ = #t. Then ℓ > 0 and action point k = #t ≤ #t, so (t, ℓ) satisfies T12. Since t ∈ [t, t ⊕ ℓ), the span covers t. Taking one such span per position in P gives Σ with ⟦Σ⟧ ⊇ P."

## OUT_OF_SCOPE

### Topic 1: Span-set intersection and difference
**Why out of scope**: The ASN covers span-set union and normalization (S8–S10) but not span-set intersection or general span-set difference. These are derivable: span-set intersection is the union of pairwise span intersections (S1) followed by normalization (S8); span-set difference generalizes S11 via case decomposition. These are natural extensions belonging in a follow-up ASN on span-set operations.

### Topic 2: Exact representability
**Why out of scope**: S7 guarantees covering (⟦Σ⟧ ⊇ P) but not exact representation (⟦Σ⟧ = P). A span over tumbler t also covers t's sub-tree. Characterizing which finite sets are exactly representable as span-set denotations is a separate question requiring content-layer structure.

### Topic 3: Start recovery and right cancellation
**Why out of scope**: Issue 1 reveals that TumblerAdd lacks right cancellation (x ⊕ a = y ⊕ a does not imply x = y). Characterizing the equivalence classes of starts that produce the same reach under a given width — and whether the restriction to valid addresses (T4) narrows these classes — is a tumbler arithmetic question that could strengthen ASN-0034.

VERDICT: REVISE
