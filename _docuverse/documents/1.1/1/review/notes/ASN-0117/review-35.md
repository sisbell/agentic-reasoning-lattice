# Review of ASN-0117

## REVISE

### Issue 1: Image notation declared, never used, and in conflict with restriction usage
**ASN-0117, §"A weakest precondition"**: "We refine the subset to the *exact* loss. Writing `M(d)|_Y` for the image of the position set `Y`, … where `A_del^{excl} = A_del \ M(d)(L ∪ R)`"
**Problem**: The convention sentence declares `M(d)|_Y` to denote the *image* of a position set, but the very next formula writes the image as `M(d)(L ∪ R)` — application notation — and the declared notation is never used anywhere in the ASN. Worse, the `|_` symbol is used elsewhere in the document with its standard *restriction* meaning, which is incompatible with the declared convention: P4's derivation writes `ran(M(d)|_{V_{s_L}(d)})` (restriction-then-range — malformed if `|_` already denoted an image), and the S8★ paragraph writes "the partition of `M(d)|_{V_S}`" (again restriction). The sentence is a leftover that contradicts the document's own established usage.
**Required**: Delete the convention sentence, or replace it with the convention actually in force (`M(d)(Y)` for the image of a set `Y`, `M(d)|_Y` for restriction), and confirm every occurrence conforms.

### Issue 2: Trace-validity chain derived twice in full
**ASN-0117, §"What shifts" (*Effect*, end of coupling paragraph) and §"The document remains one coherent sequence" (opening)**: The coupling paragraph concludes "With clause 2 thus discharged, DELETE is a valid composite appended to the valid trace whose final boundary is the pre-state Σ …, so the extended trace is itself valid and the post-state Σ' is a composite boundary of it…". The coherence section then re-derives the identical chain: "The pre-state Σ is a composite boundary of a valid trace (DELETE's precondition), and DELETE is a valid composite of elementary K.μ⁻/K.μ⁺ steps (or a lone elementary K.μ⁻ when R = ∅), so the extended trace is valid, its post-state is a composite boundary of it…".
**Problem**: Two paragraphs in different sections establish the same conclusion (precondition boundary + valid composite ⟹ extended trace valid ⟹ post-state is a composite boundary) in different words. The second passage's only new content is consuming the per-state invariant package; the validity chain itself is pure repetition. This is the anti-bloat accretion pattern flagged for this note. Related, smaller instance of the same accretion: the precondition paragraph's closing clause "and the trace stands ready to be extended by a further valid composite" states the same point a third time, forward-looking, before either derivation occurs.
**Required**: Keep the derivation once (the *Effect* coupling paragraph is the natural site, since it discharges clause 2 there); in the coherence section, replace the re-derivation with a one-clause citation of the established conclusion ("Σ' is a composite boundary of the extended valid trace, as discharged above, so the per-state invariant package holds there"). Drop the "stands ready to be extended" clause from the precondition.

## OUT_OF_SCOPE

### Topic 1: DELETE at V-position depths m > 2
**Why out of scope**: The operation inherits the depth-2 restriction (`#p = 2`) directly from the foundation contraction (ASN-0082, stated only for depth-2 text positions). Generalizing the left-shift displacement to deeper text subspaces requires first generalizing the foundation contraction, which is a future ASN, not an error here. The ASN states the restriction explicitly in its precondition.

### Topic 2: Link-subspace contraction
**Why out of scope**: DELETE is text-only by precondition (`S = subspace(p) = s_C`). Removing a link V-position from a document's arrangement (the link-subspace analogue of this contraction, with its CL-OWN/CL-UNIQ obligations) is a distinct operation the foundation's per-subspace K.μ⁻ permits but this ASN deliberately does not specify.

### Topic 3: Totalization, concurrency, backtrack reconstruction
**Why out of scope**: All three are correctly carried as Open Questions — caller-facing rejection vs. clipping of out-of-containment spans, unserialized concurrent edits, and exact reconstructibility of prior arrangements are new specification territory, and the ASN's containment precondition plus the Q4 corruption evidence properly fence them off rather than hand-wave them.

The technical core is sound: both realisations (K.μ⁻ + K.μ⁺ for `R ≠ ∅`, lone K.μ⁻ for `R = ∅`) discharge their elementary preconditions including K.μ⁺'s strict-extension constraint at the `R = ∅` boundary; the J0/J1★/J1'★ couplings are correctly shown vacuous (range-shrinkage defeats J1★'s trigger conjunct); the `ran(M'(d)) = ran(M(d)) \ A_del^{excl}` refinement correctly handles the link-subspace summand via S3★ + SD and within-document sharing via the `M(d)(L ∪ R)` subtraction; the wp's per-link existential is the genuinely weakest form; and the worked examples cover lone-suffix, multi-position suffix, leading-span (empty-then-refill with S8-depth re-pinning), suffix-delete, delete-everything, within-document sharing, and cross-document transclusion. The two findings above are prose/notation defects, not gaps in the argument.

META: not warranted — the ASN defines an operation on abstract state with explicit preconditions, postconditions, frames, and invariant discharge, squarely within specification territory.

VERDICT: REVISE
