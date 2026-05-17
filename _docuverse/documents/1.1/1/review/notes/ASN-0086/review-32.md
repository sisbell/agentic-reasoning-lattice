# Review of ASN-0086

The ASN is unusually rigorous: hypotheses are explicitly tagged ([Setup-required], [Setup-free], [discipline-conditional], [stipulation-conditional]), the dependency table makes propagation visible, R0 Step 4 enumerates each L-invariant preservation, R5 Stage 2 enumerates non-opposition exhaustively, R7's PROVEN/STIPULATED decomposition is honest, and the Worked Sketch exercises every R-claim against concrete tumbler values across 6 steps. Below are the items worth flagging.

## REVISE

### Issue 1: "Uniform argument" for ASN-0036/0034 invariants is invoked twice without being a named lemma
**ASN-0086, R0 Step 4 (ASN-0036 S-invariants bullet) and R5 Stage 2 (ASN-0036 and ASN-0034 invariants — orthogonal by scope paragraph)**: Both sites invoke the same structural argument — every predicate over (Σ.C, Σ.M) is preserved by class-(iii) transitions because the frame holds (Σ.C, Σ.M) identical, and predicates over the tumbler algebra or allocator history are scoped to address-level structural relations that the endset choice doesn't affect.
**Problem**: The argument is sound, but it carries load at two distinct claims and is re-derived in prose each time. A future relational-layer ASN that adds new invariants over (Σ.C, Σ.M, Σ.L) would have to re-derive it a third time. The "uniform argument" framing also obscures that the argument is essentially a substitutivity-of-equals discharge, which deserves explicit statement.
**Required**: Lift to a named lemma — e.g., "Lemma — FramePreservation: any predicate whose free variables range only over a frame-fixed component of Σ is preserved across the framing transition." Cite the lemma at both sites instead of re-deriving.

### Issue 2: Definition of nullified silently encodes a directional convention that L7 disclaims
**ASN-0086, Definition — Nullified**: `nullified(Σ) = {a ∈ A_rel^Σ : (E (b, F', G') ∈ L_R^Σ :: a ∈ coverage(G'))}` checks only `coverage(G')` (the to-set), not `coverage(F')`.
**Problem**: L7 (DirectionalFlexibility) explicitly says "any directional interpretation is determined by the link type, outside the link structure." The Nullified definition imposes a substrate-level directional commitment for R-typed links: the retraction target must be in the to-set, not the from-set. This is a substrate convention with operational teeth — an L_R tuple with target in the from-set would be a no-op for active-subset machinery — but it's never stated as a labeled convention. A reader could plausibly emit `Emit_R(Σ, d, {(a, δ(1, #a))}, ∅)` (target in from-set, empty to-set) and be surprised that `a ∉ nullified(Σ')`.
**Required**: Add a labeled convention preceding the Definition — "Convention — RetractionDirectionality: by substrate convention, R-typed links place the retraction target in the to-set (slot 2). The Definition below codifies this convention." Or state the asymmetry in the Definition itself: "Note: nullified consults only G'; an L_R tuple with the target in F' is well-formed but operationally inert for active-subset machinery, parallel to the crafted-span case discussed below."

### Issue 3: A_K's non-monotonicity is never stated explicitly
**ASN-0086, R3 / R6 / R6c**: R3 establishes L_K is monotone. R6 establishes A_K is well-defined. R6c establishes that retracted tuples stay out of A_K. But the ASN never states that A_K itself is non-monotone — that the active subset can shrink across a transition (specifically, when a retraction targets an active tuple).
**Problem**: The Worked Sketch Step 1 exhibits A_K^{Σ_0} = {(a₁, F₁, G₁)} shrinking to A_K^{Σ_1} = ∅ after Nullify. This is the operationally salient fact about A_K vs L_K: L_K monotonically accumulates the audit trail, while A_K can both grow (via Emit_K) and shrink (via Nullify). The active/audit distinction is the conceptual contribution claimed for ASN-0086, yet the non-monotonicity that distinguishes them is left implicit.
**Required**: Add a brief consequence after R6 or R6c — "*Consequence [ARCHITECTURE]: A_K is not monotone.* While L_K only grows (R3), A_K can shrink: emitting an L_R tuple targeting an active address (a, F, G) ∈ A_K^Σ moves it to A_K^{Σ'} ∖ {(a, F, G)}. R6c then keeps (a, F, G) out of every subsequent A_K^{Σ''}."

### Issue 4: R6c-Corollary Step 5.2 in the Worked Sketch lifts to ⊑̂ via an abstract transition
**ASN-0086, Worked Sketch Step 5.2**: "Take Σ_4 ↦ Σ_5 to be *any* arrangement-modifying transition admitted at Σ_4 (existence is assumed by the editing-operation ASNs that extend ASN-0036; the specific transition's identity is orthogonal to what is being demonstrated here)."
**Problem**: The justification for abstractness is sound (R6c-Corollary's proof depends only on the frame, not the post-modification arrangement value), and the sketch acknowledges this explicitly. However, the Setup never populates Σ.M(d) entries at any prior step, so the worked sketch cannot exhibit a *concrete* arrangement modification even in principle — the document `d`'s arrangement value is undefined throughout. This is appropriate given the foundation scope (arrangement modifications belong to future editing-operation ASNs), but the disclaimer could be tightened to "no specific arrangement modification is exhibited because the worked sketch never populated Σ.M(d); the lift is justified at the level of generality at which R6c-Corollary holds, which is purely the frame."
**Required**: Tighten the disclaimer to make the asymmetry between Steps 1–4 (dom-extending, concretely exhibited) and Step 5.2 (arrangement-modifying, abstractly justified) explicit, and note that a future worked example built atop an arrangement-populated state could exhibit Step 5.2 concretely.

### Issue 5: The substrate emission primitive permits broader addresses than R0 Step 2 produces, but this asymmetry's full implications for downstream claims could be more visible
**ASN-0086, Substrate emission primitive paragraph and Definition — Emit_K**: The substrate primitive admits emission at any L1c-conforming-fresh-address; `Emit_K` binds the choice to R0 Step 2's sibling-frontier construction.
**Problem**: The discipline-conditionality is well-handled at R0a, R0a-Cor1, R0a-Cor2, and Nullify, but the "Breadth of the primitive vs. the discipline R0a names" paragraph treats this as a property of R0a alone. In fact every claim downstream of R0a inherits the conditionality through dependency: Emit_K's post-condition (sibling-frontier address) is *part of the definition*, not a derived property — meaning Emit_K is only the named operation in this note, not the substrate primitive. The Hypothesis dependency table correctly tracks this, but the prose at the Emit_K Definition could be clearer that callers invoking the bare substrate primitive at a non-sibling-frontier address have not invoked Emit_K and are not covered by R0a-Cor1/Cor2.
**Required**: At the Emit_K Definition, add a single sentence: "Callers that bypass the discipline by invoking the substrate primitive directly at a prefix-extension of an existing link address have *not* invoked Emit_K and are not covered by R0a or its corollaries; the resulting transition is class-(iii) at the substrate level but is outside Emit_K's contract."

## OUT_OF_SCOPE

### Topic 1: Globalizing L14 (admitting non-s_C-resident content)
**Why out of scope**: Already in Open Questions; the slice-wise reformulation of R0/R4/R5 is correctly identified as future work.

### Topic 2: Higher-arity active subsets (A_K^{(n)} for |Σ.L(a)| > 3)
**Why out of scope**: Already in Open Questions; the present scope is correctly limited to standard-triple links.

### Topic 3: Elevating the sibling-frontier discipline to a substrate-level guarantee
**Why out of scope**: Already in Open Questions; the conditionality framework correctly defers the strengthening.

VERDICT: REVISE
