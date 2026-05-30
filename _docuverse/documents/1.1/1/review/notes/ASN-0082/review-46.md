# Review of ASN-0082

This note carries `review-mode.anti-bloat`, so the bulk of findings below concern forward-reference accretion and meta-prose. The underlying mathematics (I3 / D-SHIFT and their preservation lemmas) is sound and the worked examples are correct and exhaustive across boundaries — the problems are prose that does not advance reasoning.

## REVISE

### Issue 1: "Necessity from TA4 (mathematical)" is a why-the-axiom essay with internal repetition
**ASN-0082, Post-Contraction Shift / Scoping axioms**: the subsection running from "*Necessity from TA4 (mathematical).*" through "...are not discharged here."
**Problem**: This is ~6 paragraphs of prose explaining *why* the depth axiom `#p = 2` is needed rather than stating what it constrains — the flagged pattern "new prose around an axiom explains why the axiom is needed." It also repeats itself: "The obstruction is irreducibly joint" is asserted, then re-derived ("dropping (i) and (ii) would relax (iv)'s range..."), and the contrast with I3 ("never invokes TA4... different arithmetic primitives") is stated twice. The Open Question already asks whether the result generalizes past depth 1, making the necessity essay partly redundant with the document's own forward pointer.
**Required**: Reduce to a short statement of the constraint and the single load-bearing reason (TA4's joint constraints (i)+(ii) force a non-empty zero-prefix range at depth > 2, colliding with S8a positivity). Drop the restatements and the I3-contrast paragraph.

### Issue 2: OrdinalExceedsDisplacement carries a use-site inventory and refactor-history meta-prose
**ASN-0082, Ordinal Extraction**: "We use it at D-SHIFT's well-definedness, D-BJ's order-preservation derivation, D-S's span-level derivation, and the S8a-post wp analysis." and "This lemma packages a recurring step... into a single tumbler-grounded citation, replacing the earlier ad-hoc ℕ-arithmetic chains."
**Problem**: The first sentence is exactly the flagged "definition's introduction enumerates downstream consumers" pattern; the second narrates the editing history ("replacing the earlier...") rather than advancing the lemma's content.
**Required**: Delete both sentences. The lemma stands on its statement and proof; consumers cite it where they need it.

### Issue 3: Duplicate commutativity-reliance flag
**ASN-0082, I3-S derivation (a)** and **D-S derivation (a)**: both contain the same disclaimer — "commutativity[/associativity] of ℕ + [is/are] not among the minimal NAT-* axioms ASN-0034 extracts... we flag [this/the] reliance explicitly rather than name an axiom the foundation does not supply."
**Problem**: Two paragraphs in different sections saying the same thing — the flagged "multiple paragraphs say the same thing in different words" pattern. Separately, the reliance itself is a real gap: both round-trip identities depend on a ℕ property the cited foundation does not establish, so the flag does not discharge the obligation.
**Required**: State the reliance once (e.g., a single note that ℕ-addition commutativity/associativity is assumed beyond the extracted NAT-* set), and either confirm the foundation supplies it or record it as a foundation gap to resolve — not repeat the apology at each use site.

### Issue 4: OrdAddHom closes with a downstream-consumer enumeration
**ASN-0082, Ordinal Extraction (OrdAddHom)**: "This three-part contract is the bridge between full-address arithmetic and ordinal-level arithmetic: clauses (a) and (c) license computation in either form, and (b) licenses the V-position reconstruction in D-SHIFT."
**Problem**: Use-site inventory dressed as a summary — names where each clause is consumed rather than advancing the lemma's meaning.
**Required**: Remove. If a one-line gloss is wanted, state what the lemma says (addition commutes with ord-extraction when the displacement has a zero first component), not who uses which clause.

### Issue 5: Contraction Scope paragraph is a protocol-rationale / asymmetry essay
**ASN-0082, Post-Contraction Shift / Scope**: "The asymmetry with the post-insertion shift (I3) is structural... DELETE has no content-side counterpart... so the contraction therefore needs no content-allocation companion..."
**Problem**: This is meta-prose comparing this ASN's structure to the insertion half and justifying why no composing operation is required — document-organization rationale rather than the contraction's content. The same point (D-I is stronger than S0 because no allocation occurs) is then re-stated at D-I itself.
**Required**: Keep the one substantive fact (contraction is the complete V-arrangement transformation; content store exactly unchanged, recorded at D-I) and cut the I3-asymmetry comparison and the duplicated S0-vs-D-I strength discussion.

### Issue 6: D-DOM justification explains why the clause is needed by analogy to I3-CS
**ASN-0082, Post-Contraction Shift (D-DOM)**: "D-DOM is needed as an independent closure clause, just as I3-CS is for insertion: without it, D-L and D-SHIFT alone would only constrain..."
**Problem**: Mostly why-the-clause-is-needed prose with a cross-reference to the insertion analogue. The genuine content (closure fixes dom = L ∪ Q₃, otherwise underdetermined) is one clause; the "just as I3-CS is for insertion" framing and the parallel-role sentence ("D-CS plays the parallel role... and D-CD for other documents") are accretion.
**Required**: Compress to the one-sentence closure rationale; drop the I3-CS analogy and the parallel-role inventory.

## OUT_OF_SCOPE

### Topic 1: Spans straddling the cut point
I3-S requires `s ≥ p` (span fully within the shifted region) and D-S requires `s ∈ R`. A span whose denotation straddles the insertion point p (start < p < reach) or the contraction interval X is not addressed — such a span is split/closed by the operation, not uniformly translated.
**Why out of scope**: These lemmas characterize uniform translation of within-region spans; straddling spans require the composing INSERT/DELETE operation's content placement and span-split logic (ASN-0053 S4/S3), which is future territory.

### Topic 2: Depth > 1 ordinals
The contraction is fixed at `#p = 2` and the Open Question already flags generalization. Gap-closure (D-SEP) and dense partition (D-DP) for ordinals of depth > 1 are not derived.
**Why out of scope**: This is a deliberate scoping axiom with a stated mathematical obstruction (TA4); generalization is a separate ASN, not a defect in this one.

VERDICT: REVISE
