# Review of ASN-0047

## REVISE

### Issue 1: Class (a) enumeration omits L1c

**ASN-0047, ExtendedReachableStateInvariants proof, Class (a) opening**: "These are all per-state properties except P4★, P4a, and P7a: S2, S3★, S3★-aux, S4, S7a, S7b, C1b, S7d, S8a, S8-fin, S8-depth, S8★, C-fin, D-CTG★, D-MIN★, D-SEQ★, P6, P7, P8, NodeLineage, L0, L1, L1a, L1b, L3, L14, L-fin, CL-OWN, CL-UNIQ."

**Problem**: This enumeration jumps from L1b directly to L3, dropping **L1c**. But the top-level ExtendedReachableStateInvariants statement *does* include L1c ("...∧ L1b ∧ L1c ∧ L3 ∧..."), the verification matrix has an L1c row, and the prose has a dedicated "*L1c (Link allocator conformance).*" paragraph. The Class (a) enumeration — which is supposed to be the authoritative list of what the proof discharges step-by-step — is inconsistent with the invariant set it claims to enumerate.

**Required**: Add L1c to the Class (a) enumeration between L1b and L3, matching the top-level conjunction and the matrix/prose.

### Issue 2: "Decomposition of K.μ~" proves Steps (A)/(B) before stating the bijection equation and admissibility clauses they reason about

**ASN-0047, *Decomposition of K.μ~***: The section opens with "*Proof of Step (A) — Subspace preservation under π from admissibility (i) + L14*" and "*Proof of Step (B)...*" (with sub-claims B.1–B.3). Step (A)'s proof reads "from S3★(Σ) (inductive hypothesis), the admissibility-stipulated S3★(Σ'), the bijection equation `M'(d)(π(v)) = M(d)(v)`, and L14...". But the bijection equation and the admissibility clauses (i)/(ii) are first stated *several paragraphs later* ("For `d ∈ E_doc` with `M(d)|_{dom_C}` taking at least two distinct values, K.μ~ realises the *bijection equation*: ...").

**Problem**: The proofs precede the definition of the object proved about. A reader cannot verify Step (A) or Step (B) at the point they appear — the admissibility filter, the bijection equation, and clause (ii)'s net-effect requirement are all defined downstream. This is forward-reference disorder of exactly the kind the anti-bloat note flags ("prose justifies document ordering"; claims that require skipping ahead to follow). It also makes the necessity/sufficiency argument (which consumes Steps (A)/(C)/(D)) read before its premises are in scope.

**Required**: Reorder so the K.μ~ definition (preconditions, bijection equation, admissibility clauses (i)/(ii)) precedes the proof obligations (Step (A) subspace preservation, Step (B) realisability, K.μ~-FIX, Steps (C)/(D) link-fixity). State the object, then prove its properties.

### Issue 3: FrontierEquivalence "Three load-bearing premises" carries disambiguation meta-prose

**ASN-0047, FrontierEquivalence lemma, premise (i)**: "T10a.7 (EnumerationInjectivity, ASN-0034) plays only the framing role of identifying which address occupies which chain index — the map `n ↦ tₙ` is injective, so different chain positions have different addresses and the notion of 'frontier' is well-defined — but it does *not* establish the determinism of inc; that is TA5(c)'s contribution."

**Problem**: This passage does not advance the derivation — it adjudicates which foundation property "really" does the work and pre-empts a misattribution the reader has not made. The actual derivation (TA5(c) determinism + P1 monotonicity + precondition) is already stated; the "T10a.7 plays only a framing role … does not establish … that is TA5(c)'s contribution" sentence is defensive disambiguation. The note flags prose that the precise reader must work around.

**Required**: State what each premise contributes and delete the comparative adjudication of T10a.7's role; if T10a.7 is cited only for well-definedness of "frontier," say that in one clause without the contrast against TA5(c).

### Issue 4: Axiom prose explains why the axiom is needed rather than what it states

**ASN-0047, LinkVPositionDepthAxiom** has a "*Design intent.*" sub-paragraph: "Link depth is a permanent per-document commitment (a link is named by its link-subspace V-position...), whereas content depth is supplied fresh at the first insertion... content's permanent identity is its I-address, not its V-position...". Similarly **J0** carries "This is an axiom of the state transition model, not a theorem of ASN-0036. S7a tells us that the prefix of a identifies the creating document, but it does not tell us that the creating document's arrangement must contain a...".

**Problem**: Both are "why the axiom is needed" essays in structural slots — exactly the pattern the anti-bloat note names ("new prose around an axiom explains why the axiom is needed rather than what it says"). The axiom's content (a fixed per-document `m_L(d) ≥ 2`; K.α co-occurs with K.μ⁺) is stated elsewhere; the design-intent and not-a-theorem passages do not constrain the model.

**Required**: Reduce each to its normative content. The contrast between link-depth permanence and content-depth freshness, and the "not a theorem of ASN-0036" justification, are commentary — drop or compress to a single clause.

### Issue 5: "Temporal scoping of J0" paragraph defers downstream without advancing the claim

**ASN-0047, after J0**: "*Temporal scoping of J0 (composite-boundary, not per-state).* J0 binds the initial state Σ and the final state Σ' of a composite, not each intermediate atomic state; its existential may transiently fail mid-composite... and is restored at Σ'. The composite-boundary verification matrix in *Class (b)* below catalogues this scoping (P7a row)."

**Problem**: This restates the Class (b)/per-state distinction already established in *Extended reachable-state invariants* and defers to the matrix "below" — a deferral to a downstream location for content stated generally there. It is meta-prose about scoping that the general Class (a)/(b) split already governs for *every* coupling, not J0 specifically.

**Required**: Remove; the composite-boundary scoping of all couplings is established once in the Class (a)/(b) framing. If J0 needs a per-coupling note, fold it into that single framing rather than repeating per coupling.

## OUT_OF_SCOPE

### Topic 1: Account-level depth-1 extension and node-allocation registry protocol
These appear in Open Questions and are correctly deferred to future ASNs (entity-allocation discipline extensions, registry mechanism specification). No action needed.

### Topic 2: Interior link withdrawal / tombstoning mechanism
The ASN correctly catalogues this as outside K.μ⁻'s suffix-truncation contract and defers a separate withdrawal mechanism to a future ASN. Appropriate.

VERDICT: REVISE
