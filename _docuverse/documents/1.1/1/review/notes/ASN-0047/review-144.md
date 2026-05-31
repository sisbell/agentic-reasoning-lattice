# Review of ASN-0047

## REVISE

### Issue 1: Document revision-history narration in normative prose
**ASN-0047, *Amendments to existing transitions* (K.α paragraph)**: "Earlier drafts of this ASN used the shorthand 'K.α amendment' for this inherited precondition; the term has been retired to avoid the false reading of a local strengthening."
**Problem**: This sentence narrates the document's own editorial history. It advances no reasoning about the state model — a reader picking up the ASN cold gains nothing from knowing a term was once used and retired. The same pattern recurs in the *Entity distinctness* prose ("The earlier formulation through `[A.0.1]` is superseded...") and in K.μ⁻ ("Earlier drafts..."-style supersession narration).
**Required**: Delete the revision-history sentences. State the current precondition/derivation directly; supersession belongs in a changelog, not in the claim body.

### Issue 2: "Consumes / Produces / Does not consume" dependency-chain block is essay content in a structural slot
**ASN-0047, *Decomposition of K.μ~*, Steps (A)–(E)**: each step carries a "*Does not consume:* link-subspace fixity, CL-UNIQ" line and a paragraph asserting non-circularity (e.g., "Subspace preservation is the *root* of the K.μ~ dependency chain — every downstream step (B)–(E) builds on it").
**Problem**: This is a defensive non-circularity apparatus wrapped around the proof rather than the proof itself. The "Does not consume" annotations exist only to preempt a circularity objection; the closing sentence "the chain makes explicit that admissibility (i) is the stipulation source, not a derived consequence of preconditions" is meta-commentary on the argument's shape. The actual content (Steps A–E proofs) is restated immediately afterward in prose, so the annotation block is a duplicate index.
**Required**: Collapse the dependency-chain annotation block. Present Steps (A)–(E) once as proofs in order; if ordering must be justified for non-circularity, one sentence suffices, not a per-step "Consumes/Produces/Does not consume" ledger.

### Issue 3: Self-referential "single normative discharge gloss" notes
**ASN-0047, Class (a) verification matrix preamble**: "This note is the single normative discharge gloss for every link-row 'frame' cell under K.α, K.μ⁺, and K.μ⁻ in the matrix below." — and the parallel "This note is the single normative discharge gloss for every K.μ~ cell in the matrix below."
**Problem**: These sentences are commentary about the document's own consolidation strategy. A reader does not need to be told that a note is "the single normative gloss"; either the cells are self-explanatory or they are not. This is meta-prose announcing that repetition was removed — itself a residue of the removal.
**Required**: Keep the substantive content of each note (what "frame" / "full-clearance" means) but delete the self-referential framing sentences.

### Issue 4: Use-site inventories attached to definitions and lemmas
**ASN-0047, multiple sites**: "Downstream sites cite this lemma as **CrossDocDisjoint**"; "Downstream prose cites these identities by name (K.δ-ID.zeros-0/1, ...) rather than unpacking the TA5/T4b derivation chain at each invocation site"; the K.δ-ID table's "Derivation" column embeds "Cited by the multi-version invariant chain..."; FrontierEquivalence's *Significance* paragraph ("Downstream K.δ case (ii) k = 0 discharge and the S4 row ... cite this lemma rather than re-deriving the three-premise chain in place").
**Problem**: Enumerating downstream consumers does not advance the meaning of the definition or lemma. These inventories rot as the document changes and force the reader past bookkeeping to reach the claim.
**Required**: Remove the consumer inventories. A named lemma is citable by virtue of being named; the citing sites already reference it.

### Issue 5: `m_L ≥ 2` lower-bound justification is a non-sequitur and redundant with inherited S8a
**ASN-0047, *Link-subspace extension* (LinkVPositionDepthAxiom)**: "The lower bound `m_L ≥ 2` is structural (ordinal shift at depth 1 alters the subspace identifier, violating TA7a); LinkVPositionDepthAxiom instantiates it at 2."
**Problem**: Every V-position already satisfies `#v ≥ 2` by S8a (ASN-0036: `dom(Σ.M(d)) ⊆ {t : zeros(t) = 0 ∧ #t ≥ 2}`), which this ASN carries as a Class (a) per-state invariant. The lower bound `m_L ≥ 2` therefore follows immediately from S8a. The offered justification — a one-line appeal to TA7a (SubspaceClosure, which concerns ⊕/⊖ membership in the all-positive subspace, not V-position depth) — neither establishes the bound nor matches the actual source. It is both redundant and an unsupported inference.
**Required**: Either delete the parenthetical and derive `m_L ≥ 2` from S8a, or, if a TA7a argument is genuinely intended, supply the multi-step derivation connecting depth-1 shift to a TA7a violation rather than asserting it in one clause.

### Issue 6: Multiple paragraphs defer to the same downstream location
**ASN-0047, *Decomposition of K.μ~* / *K.μ⁻ admissible contraction shape***: the necessity/sufficiency split, the admissibility-clause prose, and several matrix cells each defer to "*Decomposition of K.μ~* below," "*K.μ⁻ admissible contraction shape* below," and "Steps 1–3 of the link-subspace fixity proof." The K.μ~ section forward-references its own subsections repeatedly before stating them.
**Problem**: Repeated deferral to the same downstream block (the flagged accretion pattern) signals that the material wants to be stated once at the point of use. The reader must hold open several forward pointers to one location.
**Required**: State the load-bearing decomposition once, at the first point it is needed, and let later sites refer back rather than forward; consolidate the scattered forward pointers into a single placement.

### Issue 7: K.δ k = 0 rationale re-derives an already-excluded conjunct
**ASN-0047, *Elementary transitions*, K.δ "Rationale (k = 0 conjuncts)"**: "Although `¬IsNode(t)` follows from the structural identity `zeros(t) = zeros(e)` together with the case-level `¬IsNode(e)` (`zeros(e) ≥ 1`), it is stated explicitly so the operand admissibility is visible at the definition site rather than left as a consequence of partial-function evaluation."
**Problem**: A paragraph that states a conjunct, then explains that the conjunct is derivable but is being restated anyway "for visibility," is the reviser-drift pattern of re-imagining something the precondition structure already settles. The justification for the redundancy is itself the noise.
**Required**: Either keep `¬IsNode(t)` as a stated precondition without the meta-justification, or drop it and note its derivation once. Do not state-and-then-explain-why-restated.

## OUT_OF_SCOPE

### Topic 1: Link-withdrawal mechanism (status flags / tombstones) reconciling D-CTG★ with interior withdrawal
**Why out of scope**: The ASN itself defers interior link withdrawal to a future mechanism (Open Questions) and the present K.μ⁻ contract is correctly confined to suffix truncation. Specifying the withdrawal-marker invariants is new territory, not an error here.

### Topic 2: Node-allocation registry protocol (issuing, persistence, concurrency)
**Why out of scope**: NodeUniqueAllocation/NodeRegistryBootstrap correctly treat the registry as an external commitment at this ASN's abstraction boundary; the registry's internal protocol is a separate concern flagged in Open Questions.

VERDICT: REVISE
