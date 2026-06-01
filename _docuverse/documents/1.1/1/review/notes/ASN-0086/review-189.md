# Review of ASN-0086

## REVISE

### Issue 1: CoverageEqualityDecidable — garbled soundness justification
**ASN-0086, Lemma CoverageEqualityDecidable**: "were some gap empty, both coverages would restrict to ∅ there regardless, yet their boolean gap-indicators could differ, **falsely reporting unequal coverages as equal sets**."

**Problem**: The stated failure mode is backwards. If a gap were empty as a set, both coverages restrict to ∅ (equal there), while differing gap-indicators would make the algorithm declare the indicator vectors — hence the sets — *unequal*. The hazard is a false "unequal" verdict on coverages that are in fact equal. As written, the clause describes the opposite (reporting unequal coverages as equal), which is not the risk the non-emptiness discharge guards against. The conclusion (gaps are non-empty, so indicators are faithful) is correct; the justification sentence misstates what it is protecting.

**Required**: Reword to "falsely reporting equal coverage sets as unequal" (or equivalent), so the soundness argument names the actual failure it rules out.

### Issue 2: Deferral chain — Nullify's precondition semantics shipped downstream
**ASN-0086, Definition — Nullify**: "The roles of the two further conditions — P1 ... and PC ... are not execution gates but conditions on the single-tuple-scope postcondition R-Scope; **the precise P0-gate / (P1,PC)-scope distinction, and the load-bearingness of each, are derived once at the wp Case 1 analysis**."

**Problem**: The definition of the operation defers its own precondition semantics to a later section. R-Scope, the Properties table Nullify row ("single execution precondition P0, with P1 and substrate-conformance PC conditioning the ... postcondition"), and wp Case 1 all re-state or point at the same P0/P1/PC distinction. This is the "multiple paragraphs in different sections defer to the same downstream location" pattern: a reader cannot understand Nullify's contract at its definition site without jumping forward. The classifier flags exactly this accretion.

**Required**: State Nullify's execution precondition (P0) and postcondition scope (P1/PC → R-Scope) once, at the definition, in one or two sentences. Remove the forward-deferral and the duplicate restatement in the Properties table.

### Issue 3: K-Step Conformance Preservation — proof is definitional unfolding
**ASN-0086, Lemma — K-Step Conformance Preservation**, proof: "Substrate-conformance of Σ is thus witnessed by a trajectory Σ_init ↝_c* Σ; appending the conformance-preserving step ... extends that trajectory ... so Σ' too is substrate-conforming."

**Problem**: "Substrate-conforming" is *defined* as reachable from Σ_init by conformance-preserving (↝_c) steps. The proof appends one more such step to the witnessing trajectory — i.e., it restates the definition. The only substantive content ("every K-op →-step is conformance-preserving by its ASN-0093 contract") is asserted, not shown. A lemma whose proof is the unfolding of a definition is meta-prose dressed as a result; it inflates the apparatus without adding reasoning.

**Required**: Either collapse this to a one-line remark ("conformance-preservation is closure of substrate-conformance under ↝_c by definition; K-ops satisfy clauses (a)–(c)"), or, if the K-op discharge of clauses (a)–(c) is the real content, prove *that* (especially clause (c) frontier-landing for K.λ) and drop the trajectory-unfolding paragraph.

### Issue 4: Forward-reference pointers in R6d
**ASN-0086, R6d**: "R6a and R6c are proved against → and →* above, but ... Both extend to the ↝-steps of a substrate-conforming layer (**Definition — substrate-conforming layer, below**) ..." and proof: "R7a (**NoExtraClassAffectsL, below**) decomposes ..."

**Problem**: R6d depends on a definition and a lemma (R7a) that appear *after* it, forcing forward jumps. The "see X below" / "deferred to Y" pattern. Either R6d belongs after R7a and the substrate-conforming-layer definition, or those should precede it.

**Required**: Reorder so R6d follows its dependencies (R7a and the substrate-conforming-layer definition), eliminating the forward pointers.

### Issue 5: Redundant non-fixpoint / non-monotonicity essays
**ASN-0086**: the R6c "Consequence" paragraph ("A_K is not monotone; L_K is"), the R6b body, the R6b Properties-table row, and Worked Sketch Step 3 each re-explain the same two facts (audit-slice quantification → retraction-of-retractor is a non-fixpoint; A_K non-monotone while L_K monotone).

**Problem**: "Two paragraphs ... say the same thing in different words." The Consequence paragraph after R6c is essay content restating R6b's semantics already stated at R6b and again concretely in Step 3.

**Required**: Keep the formal statement (R6b) plus one concrete witness (Step 3); trim the duplicate prose Consequence and the table-row gloss to a pointer, not a re-derivation.

## OUT_OF_SCOPE

### Topic 1: Higher-arity typed relations
The note explicitly restricts `L_K` to `|Σ.L(a)| = 3` and defers `L_K^{(n)}` to an Open Question. Correctly future work, not an error here.

### Topic 2: Concurrency / atomicity of Observe vs Emit, ordering of Observe results
The Open Questions raise these; they are genuinely new territory (consistency model), not gaps in the present invariant set.

VERDICT: REVISE
