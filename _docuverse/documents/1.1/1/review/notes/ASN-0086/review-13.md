# Review of ASN-0086

## REVISE

### Issue 1: Unexplained "S" labels in Consequences sections
**ASN-0086, multiple sections**: "*Consequences (S1, S2 in the original presentation).*" (after R2); "*Consequences (S3).*" (after R3); "*Consequences (S4).*" (after R4); "*Consequences (S5).*" (after R5); "*Consequences (S6).*" (after R6c).
**Problem**: "The original presentation" is undefined in this document — it appears nowhere else and has no introduction. The bare "(S3)", "(S4)", etc. tags follow without explanation. These labels also collide with ASN-0036's S-prefix invariants (S0–S9), creating namespace confusion when a reviewer encounters "(S3)" and must determine whether it refers to ASN-0036's S3 (ArrangementReferentialIntegrity) or this note's third consequence cluster.
**Required**: Either introduce the S-numbering convention at first use ("the consequences derived in this section are numbered S1–S6 for cross-reference within this note") or drop the labels and use plain enumeration.

### Issue 2: `inc` iteration composition asserted without justification in R0a Sub-case B
**ASN-0086, R0a proof, Induction Sub-case B**: "Composing, `a = incⁱ(b, 0) = incⁱ(incᵏ(d.0.s_L.1, 0), 0) = incⁱ⁺ᵏ(d.0.s_L.1, 0)`."
**Problem**: The composition step `incⁱ(incᵏ(t, 0), 0) = incⁱ⁺ᵏ(t, 0)` is correct but non-obvious. It requires that each `inc(·, 0)` along the iteration modifies the same position — i.e., that `sig` stays at the final component across the iteration. This holds because (a) the base `d.0.s_L.1` is T4-valid (T10a.4), (b) every `inc(·, 0)` preserves T4 unconditionally (TA5a at `k = 0`), and (c) for T4-valid inputs, `sig(t) = #t` (TA5-SigValid). Without this chain, the substitution would not be valid in general.
**Required**: Cite TA5-SigValid + TA5a (k=0) + TA5(c) at the composition step, or state a one-line lemma "iterated `inc(·, 0)` on T4-valid inputs commutes with addition on the iteration count".

### Issue 3: Hand-wave on remaining S-invariants in R0 Step 4
**ASN-0086, R0 Step 4**: "S0 (ContentImmutability) is preserved because no `Σ.C` entry is touched. S3 (ArrangementReferentialIntegrity) is preserved because... S7a, S7d... operate on `dom(Σ.M)`, unchanged. The remaining S-invariants similarly inherit from `Σ` because the transition's frame on `Σ.C, Σ.M` is the identity."
**Problem**: The "remaining S-invariants" — S1, S2, S4, S5, S7b, S7c, S8a, S8-depth, S8-fin, D-CTG, D-MIN, D-SEQ — are a substantial list. In a Step that otherwise verifies each L-invariant individually (including trivial frame inheritances like L7 and L13), summarizing the entire ASN-0036 obligation as "similarly inherit" is a hand-wave by Dijkstra's standard. The frame argument is uniform, but its uniformity needs to be stated rather than implied.
**Required**: Either enumerate each remaining S-invariant with its Σ.C-vs-Σ.M domain, or replace the hand-wave with an explicit meta-argument: "every ASN-0036 S-invariant is a predicate over (Σ.C, Σ.M); class-(iii) Frame fixes both pointwise; so each S-invariant is preserved by identity on its domain."

### Issue 4: "Subspace distinctness consumed at R5" — direct vs. inherited
**ASN-0086, Properties Introduced table, Subspace distinctness row**: "consumed at R0 Step 4 (L14a, L14), R4, and R5"
**Problem**: R5's text does not directly invoke the subspace-distinctness axiom. Its Stage 1 appeals to R0's emission construction, which uses the axiom at R0 Step 4 (L14a preservation). The table phrasing reads as if R5 directly consumes the axiom, but the dependence is via R0. This is the same kind of indirect dependence the Setup-requirement tagging takes pains to make explicit at R5's section header ("inherits R0's L14a-preservation Setup-requirement").
**Required**: Reword the table entry as "consumed directly at R0 Step 4 (L14a, L14) and R4; consumed indirectly at R5 via R0".

### Issue 5: R6c's broader transition extension rests on an uncharacterized parallel vocabulary
**ASN-0086, R6c proof footnote**: "the user-facing reading 'every future active subset' is intended in the *broad* sense — across both dom-extending and arrangement-modifying successors — and the claim extends to that broader relation without further work... arrangement modifications change only `Σ.M`, leaving `Σ.L` invariant"
**Problem**: The "broader transition relation (dom-extending ∪ arrangement-modifying)" is named but not formally defined in this note. The proof asserts the frame condition "arrangement modifications change only Σ.M" as if given, but no arrangement-modification frame is stated alongside the Frame conditions for classes (i)/(ii)/(iii). A future reader cannot verify the R6c extension without leaving the document to reconstruct the arrangement-modification frame from ASN-0036.
**Required**: Either (a) state the arrangement-modification frame explicitly in the "Frame conditions on the primitive transitions" subsection (one bullet: "arrangement modification: `Σ'.M(d) ⊃ Σ.M(d)` for one document; `Σ'.C = Σ.C` and `Σ'.L = Σ.L`"), or (b) declare R6c's broad-sense extension as inheritance from ASN-0036 with a specific citation.

## OUT_OF_SCOPE

### Topic 1: Higher-arity relations (`|Σ.L(a)| > 3`)
**Why out of scope**: The note explicitly scopes `L^Σ`, `L_K`, and `A_K` to standard-triple links and flags higher-arity active subsets as an open question. Treating arity-N relations would require redefining slot conventions and is a separate piece of work.

### Topic 2: Relation algebra (composition, inverse, transitive closure)
**Why out of scope**: The substrate exposes typed relations and Observe/Emit primitives. Higher-level relation-algebraic operations (R₁ ∘ R₂, R⁻¹, R*) are layered on top of Observe; defining them belongs in a relational-query-language ASN, not the substrate.

### Topic 3: Concurrency model and atomicity guarantees on Emit vs. Observe
**Why out of scope**: The note's open questions explicitly defer concurrent Emit/Observe semantics, and `→` is a sequential transition relation. A concurrency model is a substantive separate concern.

### Topic 4: Elevation of the sibling-frontier discipline to a substrate guarantee
**Why out of scope**: The note flags this in its open questions. Whether to bind R0a's discipline into the substrate primitive's spec (making R0a unconditional and Nullify's P3 automatic) is a downstream substrate-tightening decision.

### Topic 5: Slice-wise reformulation under L14's native form (dropping Setup)
**Why out of scope**: Properly stated as an open question. The reformulation touches R0/R4/R5 and would require auxiliary slice-preservation arguments that don't belong in this ASN.

VERDICT: REVISE
