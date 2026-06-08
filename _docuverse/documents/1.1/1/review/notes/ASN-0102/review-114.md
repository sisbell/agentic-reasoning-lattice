# Review of ASN-0102

I worked through the operation definition, all sixteen claims, the wp computation, the full invariant discharge in X16, and verified all five worked examples by hand. The mathematics is sound: the tiling in X15 is correct, the merge/absorption conditions in X7/X10/X11 hold, the forced-atomicity argument in X14 correctly exhibits invariant-violating intermediate states for both decomposition orderings, and the `ExtendedReachableStateInvariants` conjunction (including P4★/P4a/P7a and the transition theorem P3) is discharged conjunct-by-conjunct. I found no correctness gaps. The issues below concern presentation under the note's anti-bloat classifier.

## REVISE

### Issue 1: COPY's transition status is stated two contradictory ways and never cleanly resolved
**ASN-0102, X14 and Claims table**: "COPY is a single elementary transition (Definition), not a composite of K.μ steps ... the non-displacing cases (`p = n_S+1` append, `n_S = 0` empty subspace) displace nothing and **are also expressible as a valid composite**."
**Problem**: The Amendment fixes COPY as a single elementary transition unconditionally, and X16's invariant discharge relies on exactly that (Σ → Σ' directly, no intermediate state to check). The "also expressible as a valid composite" asides (in the X14 body and again in the Claims table) are pure design-rationale: they justify *why* the elementary status was chosen rather than stating what COPY *is* or guarantees. For the elementary COPY there is no intermediate state, so the decomposability of the non-displacing cases is moot to every invariant obligation in the note. A reader is left unsure whether COPY is sometimes elementary and sometimes a composite. This is the anti-bloat pattern "prose justifies the design choice / explains why X is needed rather than what it says."
**Required**: State once, cleanly, that COPY is elementary in all cases (per the Definition). Keep the forced-atomicity argument (it establishes the genuine Atomicity *guarantee* — no observable intermediate state), but drop or clearly quarantine the "non-displacing cases are also expressible as a composite" remarks as non-load-bearing rationale, and remove the dual framing from the Claims-table entry.

### Issue 2: The singleton-composite framing is set up twice
**ASN-0102, X16 ("Composite-boundary reading" paragraph) and X16 (P4a paragraph)**: both establish that COPY-as-singleton-sequence is a valid composite, that its pre-state is read as the initial boundary `Σ_0 = Σ`, and that the post-state `Σ'` is the final boundary / trace extension.
**Problem**: Two paragraphs in the same section perform the same setup ("COPY is a valid composite, read `Σ` as the boundary, extend the trace") before doing their distinct work. This is the named pattern "multiple paragraphs defer to the same framing."
**Required**: Hoist the singleton-composite reading into a single sentence once, then have both the boundary-property discharge and the P4a induction reference it rather than re-deriving it.

## OUT_OF_SCOPE

### Topic 1: Re-displacement, transitive containment, and unreachable-allocator identity
**Why out of scope**: The four Open Questions (continued discoverability of re-displaced content, containment when a by-reference document is itself a source, time-varying resolution views, identity when the allocating document is unreachable) are correctly posed as future territory. They are not errors in this ASN; this note's job is the single COPY transition, which it completes.

VERDICT: REVISE
