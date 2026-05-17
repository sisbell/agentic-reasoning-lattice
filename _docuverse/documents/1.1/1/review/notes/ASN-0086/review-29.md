# Review of ASN-0086

## REVISE

(no items)

The ASN is unusually rigorous and self-aware. Every claim is either proven with explicit derivation chains or explicitly stipulated (R7b). Hypothesis dependencies (Setup, subspace-distinctness, sibling-frontier discipline, R7b stipulation) are tracked in a dedicated table and flagged at each consumption site. Each R-claim's proof discharges its preconditions step-by-step against foundation ASN invariants:

- R0 Step 4 enumerates every L-invariant from ASN-0043 and discharges each (including the L14a/L14 preservation steps that use Setup, and the uniform argument for ASN-0036's S-invariants by signature scope).
- R0a's induction strengthens to the sibling-stream invariant explicitly because direct induction on antichain doesn't go through — a real technique, not hand-waving. Sub-case B's `incⁱ ∘ incᵏ = incⁱ⁺ᵏ` composition is justified via TA5a's unconditional k=0 T4-preservation.
- R0a's Case 2 sub-argument (zero-count additivity along prefix-extension forcing `home(a) = home(a')`) is sound and independent of the discipline.
- R5 Stage 2 exhaustively enumerates ASN-0043's L-invariants for non-opposition; the scope argument for ASN-0034 invariants is appropriate.
- R6a's coverage-purity argument correctly identifies that `coverage(·)` is state-independent and `G'` is preserved by R2.
- R6b's single-depth observation is grounded in the deliberate choice of `L_R^Σ` (not `A_R^Σ`) at the existential in `nullified(Σ)`'s definition.
- R6c's induction on `→`-chain length is correct; R6c-Corollary's lift to `⊑̂` rests on the arrangement-modification frame inherited from S9 + L12 + L12a.
- R7's decomposition (R7a proven from L12 + L12a + Frame; R7b stipulated as model commitment) is logically sound and explicit.

The Worked Sketch is exceptionally detailed — six steps with concrete tumbler values (`a₁ = 1.0.1.0.1.0.2.1`, etc.), L-invariant verification at each fresh address (L0/L1/L1a/L1b/L1c/L11a/L12/L14/L14a all checked pointwise), cross-document retraction (Step 3), Observe hist-vs-oper distinction (Step 4), multi-step R6c persistence (Step 5), and R6b under second-order retraction (Step 6). Boundary cases — empty `L_K`, first link sited under document (Case A), subsequent siblings (Case B), self-targeting endsets, cross-document retraction — are all exercised concretely.

The discipline-conditional and stipulation-conditional tags are unusual but appropriate: the ASN distinguishes substrate-level guarantees from implementation/model commitments and propagates the dependencies through corollaries (R0a-Cor1, R0a-Cor2, Nullify's single-tuple scope). Appendix B exhibits a concrete failure mode demonstrating the discipline's necessity, building on the worked sketch's instantiation.

## OUT_OF_SCOPE

The ASN's own Open Questions section adequately enumerates future-ASN topics (multi-arity links, arrangement-modification interaction with L_K visibility, concurrent Observe semantics, slice-wise reformulation under L14's native form, discipline elevation, deeper-sited link addresses, dynamic type catalog extension). No additional out-of-scope items beyond these.

VERDICT: CONVERGED
