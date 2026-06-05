# Review of ASN-0102

## REVISE

### Issue 1: Standalone-composite restriction imposed for proof convenience, not justified intrinsically
**ASN-0102, Definition (Amendment to ValidComposite★)**: "subject to the restriction that COPY occurs only as a *standalone* (length-1) composite: COPY may not appear as a non-initial step of any composite."
**Problem**: This restriction is load-bearing only for the X14 provenance discharge — it is what makes COPY's pre-state Σ a composite boundary so that P4★ (`Contains_C(Σ) ⊆ R`) is available for the J1'★ `Old`-branch. The note presents it as definitional fiat with no statement of whether COPY is *intrinsically* non-composable or whether the restriction is an artifact masking an incomplete provenance treatment for the mid-composite case. A precondition introduced to close a proof, rather than for a stated property of the operation, should be flagged.
**Required**: State explicitly why COPY's direct write to `Σ.R` forces non-composability, or treat the mid-composite case and drop the restriction. If composition is deferred, say so and name the consequence.

### Issue 2: Meta-prose roadmap in "The cardinal question"
**ASN-0102, The cardinal question**: "So the question 'what is the effect of placing existing content' resolves into three sub-questions, and we will answer each as a consequence of one decision. *What is preserved?* … *What shifts?* … *What invariants must hold at completion?* … We take these in turn, but first we must say what the operation *is*."
**Problem**: This is essay scaffolding announcing the document's structure rather than advancing any claim. The anti-bloat classifier on this note targets exactly this accretion. The three questions are answered by X1–X16 regardless of the framing paragraph.
**Required**: Remove the roadmap framing; let the X-claims carry the structure.

### Issue 3: X15 parenthetical explains why a design choice is needed rather than stating the claim
**ASN-0102, X15 derivation**: "(Were COPY instead a composite, ValidComposite★ would admit observable states between its atomic steps, and this clause would weaken to a composite-boundary guarantee; the elementary declaration is what licenses the strong 'no intermediate state' form here.)"
**Problem**: This is justification-of-the-axiom-choice prose, one of the named accretion patterns ("explains why the axiom is needed rather than what it says"). The claim X15 is fully established by the prior sentence (single elementary transition ⇒ SequentialTransitionAxiom applies directly). The parenthetical adds counterfactual rationale, not reasoning the claim requires.
**Required**: Delete the parenthetical.

### Issue 4: X15 restates X10(b)'s snapshot-resolution argument
**ASN-0102, X15**: "This same axiom pins `resolve_Σ(R)` to the pre-state — the source is read *before* any displacement (cf. X10), so self-transclusion sees a frozen image."
**Problem**: X10(b) already derives snapshot resolution from SequentialTransitionAxiom ("`resolve_Σ(R)` reads `Σ.M(d)` *before* the displacement opens the gap … resolves against the frozen pre-state image"). X15 repeats the same derivation from the same axiom. Two paragraphs saying the same thing — the "cf. X10" pointer acknowledges the duplication but restates it anyway.
**Required**: In X15, cite X10(b)'s snapshot result by reference without re-deriving it.

### Issue 5: Closing essay recapitulates conclusions
**ASN-0102, A remark on what COPY is**: "Every consequence in this note — shared instance, transitive origin, source non-interference, cross-origin separation, permanent containment — follows from that combination of reference and displacement. The word 'copy' is, as Nelson observed, a misnomer; the operation is inclusion, and inclusion is reference."
**Problem**: The K.μ⁺-vs-COPY contrast earlier in the section is substantive (it states what COPY does and does not do, which is permitted). But the closing inventory of consequences plus the rhetorical "misnomer … inclusion is reference" flourish restates results already proven in X1–X16 and adds no reasoning. This is the essay-content-in-structural-slot pattern the anti-bloat mode targets.
**Required**: Trim the consequence inventory and rhetorical close; keep only the COPY/K.μ⁺ distinction that carries content.

## OUT_OF_SCOPE

### Topic 1: Composition of COPY with DELETE to realize MOVE
**Why out of scope**: Whether COPY can compose with contraction (the natural MOVE = DELETE + COPY) is operation-composition mechanics, explicitly excluded. It is the right home for resolving the tension raised in Issue 1, but not a correctness gap in this ASN's definition of COPY itself.

VERDICT: REVISE
