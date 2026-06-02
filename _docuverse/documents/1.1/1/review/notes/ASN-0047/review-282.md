# Review of ASN-0047

## REVISE

### Issue 1: K.μ~ link-subspace fixity is derived three times over
**ASN-0047, *Decomposition of K.μ~***: The fact that every realisable π fixes the link subspace pointwise (`π(v) = v` / `M'(d)|_{dom_L} = M(d)|_{dom_L}`) is established in (a) the clause-(v) independence paragraph ("the full-clearance decomposition cannot realise such a re-seating … every realisable π fixes the link subspace (Step (A), Case s_L)"), (b) Step (A) Case `s_L` ("CL-UNIQ at Σ … then forces `π(v) = v`"), and again in (c) Link-subspace fixity sub-steps (1)–(4) ("CL-UNIQ at Σ … forces `π(v) = v`").
**Problem**: The same conclusion, resting on the same premise (CL-UNIQ at Σ), is re-derived in three overlapping loci. A reader checking the fixity argument must reconcile three near-identical CL-UNIQ invocations to confirm they are one claim, not three obligations. This is exactly the accretion the anti-bloat classifier targets — "two paragraphs in different sections say the same thing in different words."
**Required**: Derive link-subspace fixity once (the sub-step (1)–(4) block is the most complete), and have the clause-(v) and Step (A) Case `s_L` passages cite that single derivation rather than re-run it.

### Issue 2: Organizational meta-prose justifying document layout instead of advancing the claim
**ASN-0047, *The state model* (Bridging lemma / default-value convention)**: "This is the sole statement of the convention; later appeals (the (†) discharge above, the K.δ frame) reference it rather than restating it." And **Definition (Fork)**: "This is the sole statement of both the allocation discipline and the operand-tracking rule; the J4 intro above and steps (i)–(ii) below invoke it by reference rather than re-derive the k-split."
**Problem**: These sentences describe where the document states things and which downstream sites point back, not what the convention or rule *is*. They match the flagged patterns "a definition's introduction enumerates downstream consumers" and "prose justifies document ordering." They add bookkeeping a reader must skip past.
**Required**: Delete the "sole statement / invoked by reference" sentences. The forward/back references at the use-sites are sufficient; the meta-narration about them is not.

### Issue 3: "genuine delta" / "shared discharge" scaffolding in the Class (a) proof
**ASN-0047, Class (a) verification prose** (e.g. "*K.μ~ discharge for the arrangement-shape package (uniform argument)*"): "Each per-property block below adds only its genuine delta over this shared discharge"; "S8a and S8-depth carry no per-property delta — the uniform shape-package discharge above closes them in full. The sole delta is S8-fin(Σ') …".
**Problem**: This is prose about how the proof is factored ("delta over shared discharge"), not the proof itself. It is the essay-in-structural-slot pattern: the substantive content (S8-fin needs an independent finiteness argument; the others follow from admissibility (i) + K.μ~-FIX) can be stated directly without the "delta"/"shared discharge" framing layered on top.
**Required**: State each property's K.μ~ discharge directly. Drop the "genuine delta," "carries no per-property delta," "sole delta" connective tissue.

### Issue 4: Foundation operations K.α and K.λ restated in full rather than referenced
**ASN-0047, *Elementary transitions* (K.α) and *Link allocation* (K.λ)**: Each opens "Per ASN-0093 (foundation K.α, …)" and then re-enumerates the entire precondition structure and both emission cases verbatim ("The precondition structure — `d ∈ E_doc` … — follows ASN-0093's K.α. The emission cases: *First emission* … *Subsequent emission* …").
**Problem**: ASN-0093 is a foundation; the review convention is that an ASN "may use foundation definitions without restating them." The *only* new content these transitions carry is the extended-state frame (`E' = E`, `R' = R`). Restating the full foundation precondition and the `max`-well-definedness argument duplicates verified material; the `max`-well-definedness paragraph in particular reproduces ASN-0093's own reasoning.
**Required**: Reduce K.α/K.λ to "ASN-0093's K.α/K.λ, with frame extended by `E' = E ∧ R' = R`," and keep only genuinely ASN-0047-local additions (e.g. the SubAllocFresh cross-reference). Do not re-enumerate the inherited precondition and emission cases.

### Issue 5: Necessity-direction dependency claim is imprecise
**ASN-0047, *Necessity and sufficiency of the precondition***: "its necessity direction consumes CL-UNIQ at Σ, which holds by the ExtendedReachableStateInvariants inductive hypothesis."
**Problem**: In the necessity proof, π is *assumed admissible*, so subspace-preservation (iv) and link-fixity (v) are hypotheses, not conclusions — CL-UNIQ is consumed only transitively, inside the *realisability* lemma (Link-subspace fixity sub-step (4)), not by necessity per se. The lead sentence asserts a direct dependency the proof body does not exercise, which will mislead a reader auditing what each direction actually rests on.
**Required**: Either state the dependency precisely ("necessity relies on link-fixity, which is established for realisable π via CL-UNIQ") or remove the claim that necessity itself consumes CL-UNIQ.

## OUT_OF_SCOPE

### Topic 1: Interior link withdrawal with renumbering
The ASN's K.μ⁻ contracts the link subspace by suffix removal only; interior link withdrawal with V-position compaction is correctly deferred (it is already raised as an Open Question and concerns the contraction *operation*, not this ASN's invariants).

### Topic 2: Type-only / one-sided links (K.λ endset minimality)
Whether K.λ should require `e₁ ∪ e₂ ≠ ∅` is a future-ASN design decision; the ASN correctly lists it as open rather than legislating it here.

VERDICT: REVISE
