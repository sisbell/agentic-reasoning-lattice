# Review of ASN-0086

This ASN is mathematically mature. I checked R0, R0a, R0a-Cor1, R6a–R6c, R7a, both wp cases, and verified the Worked Sketch arithmetic (a₁=1.0.1.0.1.0.2.1 through b₂=1.0.1.0.1.0.2.4, all freshness and coverage claims hold). The substantive proofs carry their multi-step arguments and the boundary cases (first emission, Nullify of a non-`A_rel` address, self-nullification) are covered. Case 2 is a genuine weakest precondition with a load-bearing disjunction. My findings are presentation/bloat, which the `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: Justification and forward pointer embedded in the R7a lemma statement
**ASN-0086, R7a (statement)**: "(Clause (b) of substrate-conformance — frontier-contiguous deposition — holds at every in-scope step by the leading hypothesis, and the replay relies on it; see discharge (4).)"
**Problem**: A lemma *statement* should state what is claimed. This parenthetical instead justifies the hypothesis and forwards to a proof step ("see discharge (4)"). The reader must skip it to reach the actual conclusion (`Σ_m.L = Σ'.L`, …). This is the forward-reference/justification accretion the classifier flags.
**Required**: Move the clause-(b) reliance into the proof (it already reappears at discharge (4)). Keep the statement to the claim and its premises.

### Issue 2: The unit-depth retraction discipline is defined, restated, and justified across three locations
**ASN-0086, "Definition — Unit-depth retraction discipline", "Definition — relational layer", wp "Domain restriction"**: the discipline's content appears in its own Definition, is re-derived "by construction" in the relational-layer definition, and is re-explained as a domain precondition in the wp analysis.
**Problem**: "Two paragraphs say the same thing in different words." The relational-layer paragraph adds "explains-why" prose — *"Together these two commitments make the layer satisfy the unit-depth retraction discipline … by construction … rather than as a separately-tracked caller obligation"* — which justifies the design rather than advancing a claim.
**Required**: Define the discipline once; have the relational-layer definition and the wp cite it by name without re-deriving or re-motivating it.

### Issue 3: R6b's restriction repeats a justification already given, by cross-reference
**ASN-0086, R6b**: "The restriction `a ∈ A_rel^Σ` is carried for the reason given at Definition — Nullify."
**Problem**: The same restriction and the same rationale already appear at "Definition — Nullified" ("The set-builder restriction `a ∈ A_rel^Σ` is intentional…"). R6b's sentence adds nothing but a pointer back to it. Combined with R6b being labeled "DEF-Consequence" (it unfolds the definition of `nullified`), the restated restriction is pure cross-reference overhead.
**Required**: Drop the back-reference sentence; the restriction needs no second justification.

### Issue 4: Properties-Introduced table defers repeatedly to proofs
**ASN-0086, Properties Introduced table**: R0 "(see proof for the per-branch freshness discharge)", R6b "(see R6b statement and proof for the audit-vs-active mechanism)", R7a "(see proof for the premise list and per-step discharge)".
**Problem**: A summary table entry that defers its content to the proof is an empty pointer. The classifier flags multiple sections deferring to the same downstream location.
**Required**: Either state the one-line essence in the table cell or omit the parenthetical deferrals; a summary that says "see proof" is not a summary.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity model for Emit vs. Observe
**Why out of scope**: The note correctly confines itself to sequential `→`/`↝` semantics (SequentialAtomicTransitions is inherited). The consistency model under concurrent Observe over a non-monotone `A_K` is genuinely new territory, already parked as an Open Question, not a defect here.

### Topic 2: Higher-arity typed relations `L_K^{(n)}`
**Why out of scope**: The note explicitly restricts to standard-triple links and flags multi-arity projections as future work. Nullify's P2 scoping (`|Σ.L(a)|=3`) is consistent with this; extending the active/audit machinery to `|Σ.L(a)|>3` is a separate ASN.

VERDICT: REVISE
