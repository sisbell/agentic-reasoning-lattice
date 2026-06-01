# Review of ASN-0047

## REVISE

### Issue 1: Imagined excluded case in K.μ~ Step (B.2)
**ASN-0047, *Decomposition of K.μ~*, Step (B.2)**: "By Step (A)'s subspace preservation, each `π(v)` for `v ∈ V_{s_C}(d)` satisfies `subspace(π(v)) = subspace(v) = s_C` ... — without Step (A)'s subspace preservation, the K.μ⁺ amendment could fail on a π that maps some content-subspace position to a link-subspace target, blocking the realisation."
**Problem**: The clause after the em-dash imagines a counterfactual π (content→link) that Step (A) has *already* excluded for every admissible π. This is defensive meta-prose justifying why Step (A) is load-bearing; it does not advance the realisation argument and forces the reader past an excluded case.
**Required**: Delete the "without Step (A)..." clause. The forward reference to Step (A) at the head of the sentence already establishes the dependency.

### Issue 2: Document-ordering justification for ValidComposite★
**ASN-0047, *Coupling and isolation***: "Validity of a composite transition `Σ →* Σ'` is defined once, as **ValidComposite★** in *Scoped coupling constraints* below ... The single definition is deferred to that section because clause 2 consumes J1★ and J1'★, which are stated there. The reasoning that follows ... bears on that definition."
**Problem**: This prose justifies *where* the definition is placed ("deferred to that section because... stated there") rather than advancing any claim — a document-ordering / non-circularity justification of the kind the anti-bloat mandate flags.
**Required**: Replace with a bare pointer ("ValidComposite★ is defined in *Scoped coupling constraints*"). Drop the deferral rationale.

### Issue 3: Essay prose on the "form" of a non-assertion
**ASN-0047, *Orphan links and coupling flexibility***: "The wp analysis above shows the *form* of this design choice: it consists of *not* asserting a link-coverage invariant, rather than asserting an 'orphan-permitting' rule."
**Problem**: This sentence restates that no invariant is asserted, in the abstract vocabulary of "the form of the design choice." It carries no obligation and adds nothing to the preceding concrete statement that a K.λ-only composite is valid with J0/J1★/J1'★ vacuous.
**Required**: Delete the sentence; the preceding two sentences already establish that orphan links are an intentional valid state.

## OUT_OF_SCOPE

### Topic 1: Initial arrangement of a k=0 (second+) forked version
The J4 fork definition transcludes step (ii) from `d_src`'s content subspace even when the forked entity arises as a k=0 frontier-advance on `A_v(d_src)` (a version of a version). Whether a later version should fork from its immediate predecessor's arrangement rather than `d_src`'s is a genuine modeling question.
**Why out of scope**: The ASN's Open Questions already record "What invariants must a forked document's initial arrangement satisfy with respect to its source's current arrangement" — this is correctly deferred, not an error here.

META: not needed — the ASN defines extended state, elementary transitions, and per-state/composite-boundary invariants abstractly; it has not drifted into implementation mechanics.

VERDICT: REVISE
