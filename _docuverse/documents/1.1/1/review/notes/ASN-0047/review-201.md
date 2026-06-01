# Review of ASN-0047

I checked the state model, the seven elementary transitions plus K.μ~, the coupling constraints, and the per-state/composite-boundary invariant proofs against boundary cases (empty subspaces, full clearance, interior replacement, fork from empty source, orphan links). The operational logic is tight — I could not break S3★, S8★, the K.μ⁻ constructive/post-state equivalence, the CrossDocDisjoint lemma, or the P4a recording-boundary discharge (the trace states are composite boundaries, so J1'★ does place the witness at the recording boundary; that argument holds). The findings below are accretion/reviser-drift in the K.μ~ section, which the anti-bloat classifier on this note asks me to surface.

## REVISE

### Issue 1: K.μ~ "Framing" meta-block is re-cited four times rather than stated once
**ASN-0047, *Decomposition of K.μ~*, opening "Framing: admissibility is a filter"**: "Two distinct roles run through this section, and keeping them apart removes an apparent circularity between Step (A) and Step (B.3)... All cross-references below cite this *Framing* rather than re-deriving the distinction."

**Problem**: The genuine content here is one inference: *S3★(Σ') in admissibility clause (i) is a hypothesis on the candidate π, not derived from the preconditions; Step (B) shows the filter is non-empty.* That single point is expanded into a ~250-word preamble and then re-cited verbatim at three downstream sites — Step (A) ("Per the *Framing* above, admissibility clause (i) hands us `S3★(Σ')` as a hypothesis on the candidate π (the filter)"), Step (B) ("Per the *Framing* above, this step discharges the *non-vacuity* obligation"), and the admissibility definition ("Per the *Framing* above, this is a hypothesis on the candidate π (the filter), whose non-vacuity Step (B) establishes"). This is the "new prose explains why the construction is non-circular rather than what it does" and "multiple paragraphs defer to the same location" pattern. A reader must hold the Framing block in mind and re-resolve the pointer at each step.

**Required**: Replace the Framing block with one sentence at the admissibility definition (clause (i) is a filter hypothesis; Step (B) discharges non-vacuity), and delete the three "Per the *Framing* above" re-citations — the local sentences already state what they consume.

### Issue 2: "Necessity and sufficiency" re-walks Steps (A)/(C)/(D) already proved
**ASN-0047, *Necessity and sufficiency of the precondition*, necessity bullet**: "Step (A) of the dependency chain above derives subspace preservation... Step (C) (derived above) gives `M'(d)|_{dom_L} = M(d)|_{dom_L}`... and Step (D) gives `π|_{dom_L} = id` pointwise..."

**Problem**: The necessity argument restates the entire Step (A)→(C)→(D) chain that was just established immediately above (each tagged "derived above" / "the dependency chain above"), then adds only the new content-subspace inference. The restatement is the load-bearing chain re-narrated, not new reasoning — exactly the "paragraph looks like a prior derivation relocated rather than referenced" pattern.

**Required**: Collapse the recap to a single citation ("by Steps (A), (C), (D), π fixes dom_L pointwise and preserves each subspace") and keep only the new step — that a constant `M(d)|_{dom_C}` forces `M'(d)|_{dom_C} = M(d)|_{dom_C}`, contradicting clause (ii).

### Issue 3: Verification-matrix cells carry embedded essays
**ASN-0047, Class (a) matrix, S8★ row under K.μ⁻**: "restriction to trivial length-1 decomposition on survivors per subspace (the trivial length-1 form survives any contraction; an arbitrary restriction of a pre-state decomposition may break a length-`n` run, but the trivial length-1 fall-back — the same route used for the link-subspace S8★(s_L) cell — is always available on each subspace after contraction)"; and the S2 row under K.μ~.

**Problem**: The matrix preamble states each cell "summarises the load-bearing argument" and points to body prose for non-trivial cases. Several cells instead inline multi-clause justifications with their own parentheticals and cross-references, defeating the cell's role as an index — the reader is reading proof prose inside a navigational slot.

**Required**: Reduce these cells to a discharge name plus a pointer to the matching body paragraph (e.g., the *S8★* prose), and move the parenthetical reasoning there.

## OUT_OF_SCOPE

### Topic 1: Interior link withdrawal under D-CTG★/D-MIN★
The strengthened D-CTG★/D-MIN★ remove ASN-0036's link-subspace tombstoning exemption, so K.μ⁻ admits only link-subspace suffix truncation — withdrawing an interior link requires withdrawing every later link.
**Why out of scope**: The ASN flags this consciously (Orphan links section, open question on a separate link-withdrawal mechanism); reconciling tombstoning with D-CTG★ belongs in a future operations ASN, not here.

### Topic 2: Forked-document arrangement depth relative to source
The fork composite permits d_new's content-subspace depth to differ from d_src's; nothing pins them equal.
**Why out of scope**: This is open question #1 in the ASN — the invariant relating a fork's arrangement to its source is deferred deliberately.

VERDICT: REVISE
