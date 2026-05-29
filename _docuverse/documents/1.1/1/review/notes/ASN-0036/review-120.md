# Review of ASN-0036

## REVISE

### Issue 1: Triple-redundant restatement of T4b projection well-definedness in S7a
**ASN-0036, S7a Formal Contract**: The fact that S7b's `zeros(a) = 3` makes `N(a), U(a), D(a)` well-defined is asserted three times in one contract:
- Axiom note: "By S7b (stated above), every `a ∈ dom(Σ.C)` satisfies `zeros(a) = 3`, so T4b's projections `N(a)`, `U(a)`, `D(a)` are everywhere defined…"
- Depends/S7b: "supplies `zeros(a) = 3` for every `a ∈ dom(Σ.C)`, so T4b's projections `N(a)`, `U(a)`, `D(a)` are defined throughout the domain…"
- Depends/T10a.4: "…so `N(a)`, `U(a)`, `D(a)` are well-defined on `dom(Σ.C)`."

**Problem**: The same well-definedness claim is stated three ways in three adjacent slots. This is the "two paragraphs say the same thing in different words" accretion pattern, compounded across cycles.
**Required**: State the projection well-definedness once (in the axiom note); the Depends entries should name what each foundation supplies, not re-derive the conclusion.

### Issue 2: "Specific value of m is not fixed by the strand model" restated four times
**ASN-0036, ValidFirstInsertionPosition section**: The identical point appears in four slots:
- empty-case Definition: "The strand model fixes only the lower bound `m ≥ 2`; the specific value is an allocation convention."
- necessity paragraph: "The specific value of `m` beyond the bound `m ≥ 2` is not fixed by the strand model."
- Frame: "The specific value of `m` is set by the placing operation, not by the strand model…"
- Open Questions: "The strand model fixes only the lower bound `m ≥ 2`…; the specific value is a one-time allocation convention…"

**Problem**: Four restatements of one design decision (and three of them cite the same Nelson "subdivision by further digits, LM 4/31" hook). Redundant essay prose the reader must skip past.
**Required**: State it once at the empty-case definition; remove the duplicate sentences from the necessity paragraph and Frame. The Open Question may stay since it poses a *different* question (which value to choose), not a restatement of the bound.

### Issue 3: S3 contract carries a forward-reference to Open Questions as meta-prose
**ASN-0036, S3 Formal Contract**: "(Whether this must hold in every observable state or only in the quiescent states between operations is posed as an Open Question below.)"
**Problem**: A structural slot (the axiom of S3) is interrupted by prose that defers the question downstream rather than stating what the invariant asserts. The Open Question already records this; the parenthetical is a use-site pointer that does not advance S3.
**Required**: Drop the parenthetical. The Open Question already owns the unresolved temporal-scope question.

### Issue 4: Implementation-cost essay prose around S8 does not advance any invariant
**ASN-0036, after S8 Formal Contract**: "What matters architecturally is that the number of runs `#runs(d)` is typically far smaller than `|dom(M(d))|`…" and "The run count drives V↔I translation cost — each correspondence run requires an independent tree traversal — so any implementation of the two-stream architecture must either consolidate adjacent runs or accept translation cost proportional to the fragmentation level."
**Problem**: This is narration about representation cost and traversal counts — implementation mechanics that define no state, operation, or invariant. It restates content the "Non-canonicality" remark already covered (that non-trivial runs depend on operations-layer behavior).
**Required**: Cut to the load-bearing sentence (run count fluctuates with editing while distinct allocation events are monotone by S1) or move the cost discussion to an Open Question. Remove the duplicated "non-trivial runs arise operationally" observation.

### Issue 5: S8 run-corollary is non-vacuous only for decompositions the theorem never constructs
**ASN-0036, S8 Postconditions (Corollary)**: "For any correspondence run `(vⱼ, aⱼ, nⱼ)` satisfying conjunct (b), every image `shift(aⱼ, k)` with `0 ≤ k < nⱼ` preserves the structural properties…"
**Problem**: The existence proof exhibits only the singleton decomposition (`nⱼ = 1`), for which the corollary's `k ≥ 1` content is vacuous (only `shift(aⱼ, 0) = aⱼ`). The corollary thus has content solely for runs whose existence the theorem does not establish — a phantom guarantee that reads as substantive but discharges nothing for the proven decomposition.
**Required**: Either state the corollary conditionally on a hypothesized non-trivial run (making the dependency on unproven structure explicit), or move it to the future ASN that establishes when `nⱼ > 1` arises.

## OUT_OF_SCOPE

### Topic 1: Whether editing operations (INSERT/DELETE/COPY/REARRANGE) preserve D-CTG, D-MIN, S2
**Why out of scope**: Operation-specific frame and preservation conditions are explicitly deferred (Open Questions; Scope list excludes operation effects). The ASN correctly states D-CTG/D-MIN as design constraints on well-formed states and notes preservation is an operations-layer obligation.

### Topic 2: Link-subspace (S = 2) contiguity semantics
**Why out of scope**: The ASN explicitly defers link-subspace contiguity to a future ASN and binds D-CTG/D-MIN/D-SEQ to `S = 1`. The S8a Remark noting link positions satisfy the same well-formedness conjuncts is legitimate scope-clarification (S8a quantifies over all of `dom(M(d))`), not drift.

VERDICT: REVISE
