# Review of ASN-0128

This note is in strong shape. The proof obligations that matter are discharged with real work: I0's case analysis on where a separating pair could hide is complete (F closed by single-span identity via TA-LC, Unary/Binary G closed the same way, Multi G closed by the result-position observation); I0a proves both inclusions; I1a's induction covers all four step kinds including the K ~ R wrapper instantiation; DR's C3 argument — distinctness from freshness, then the antichain R0a instantiated at the post-state that fires regardless of C3 — is genuinely clever and sound; the DR hit branch re-establishes all four postcondition clauses at the unchanged state rather than hand-waving them; both wp displays handle necessity honestly under the attainability convention, including the case where the postcondition holds vacuously at a rejected call (DR's P0 discussion). The off-discipline failure modes (range-G sterilization, the ghost-target bypass that silently no-ops a later legal self-emit) are exactly the adversarial cases a reviewer would demand. Concrete examples are present and check real clauses (the born-nullified walkthrough correctly notes the covering R-tuple's own nullification is immaterial, per R6b).

The remaining issues are prose-structural, under the anti-bloat mode this note carries.

## REVISE

### Issue 1: Gate-first example duplicated verbatim between I1 and I6
**ASN-0128, I1 (Order — gate first)**: "a two-span F rejected by a `|F| = 1` shape can be I0-equal to an active single-span F'; gate-first rejects that call rather than answering it with the existing address."
**ASN-0128, I6 (necessity discussion)**: "indeed an active tuple satisfying POST's body may stand while the call is rejected (I1's gate-first order: a two-span F failing the `|F| = 1` shape can be I0-equal to an active single-span F')."
**Problem**: The same example, in nearly the same words, appears twice. I6 already cites "I1's gate-first order" — and then restates the example anyway. This is the duplication pattern: the citation does the work; the re-inlined example is noise the second time.
**Required**: Keep the example in one place (I1, where the order is established) and let I6's citation stand bare: "(I1's gate-first order)."

### Issue 2: Four sections defer to DR, two sections downstream
**ASN-0128, I4**: "C3 cannot fail at either (DR, Standard registrations)"; **I6 (Disciplined-domain reduction)**: "the C3 conjunct vanishes (DR, Standard registrations)"; **BH4 (retract_stale)**: "cannot sterilize (DR, Standard registrations)"; **Example (born-nullified case)**: "cannot arise through `Nullify_Binary` (DR, Standard registrations)."
**Problem**: This is the forward-deferral accretion pattern: four sites in three sections lean on a result stated and proved two sections later. The worst case is I6, where the *headline* wp of the exposed surface — the disciplined-domain reduction the note itself calls "the surface this note actually exposes" — rests on a lemma the reader cannot check without jumping to Standard registrations. SD compounds this: it is defined in the Idem section but its only payoff (DR) lives elsewhere, so the definition sits detached from the result it exists to serve.
**Required**: Consolidate. Either state DR (statement only, proof deferred) adjacent to SD in the Idem section so I4 and I6 cite a result above them, or move SD into Standard registrations alongside DR and let the Idem section carry one forward pointer instead of four scattered parentheticals.

### Issue 3: R-VAL and R-C1 disagree on whether the designation check is additional
**ASN-0128, R-VAL**: "The standard-registration designation adds three pairwise non-equivalence tests over the shipped representatives (R-C1, Standard registrations)."
**ASN-0128, R-C1**: "This is a construction check alongside R-VAL's others — three more `CoverageEqualityDecidable` tests … The three entries are mandatory, so a colliding designation would violate C0's key uniqueness … R-VAL's verdict therefore covers the designation."
**Problem**: The two passages state the same check twice and contradict each other on its status. If the three shipped entries are registry entries, C0's pairwise key-uniqueness sweep — already counted in R-VAL's `O(|registry|²)` — includes the three shipped pairs; they are not "three more tests." R-C1's own third sentence concedes this ("would violate C0's key uniqueness … R-VAL's verdict therefore covers the designation"), making the "adds"/"three more" framing in both passages wrong, and making R-C1 largely a restatement of a C0 instance.
**Required**: Pick one framing. Either R-C1 is a named *instance* of C0's uniqueness applied to the shipped representatives — then drop "adds three more tests" from both passages and state R-C1 as the instantiation — or it is a genuinely separate check (e.g., one that must hold before app declarations are merged), in which case say what distinguishes it from the C0 sweep.

## OUT_OF_SCOPE

### Topic 1: The serializing authority I4 presupposes
**Why out of scope**: I4 correctly notes that `→_sh` inherits a sequential, interleaved model and that "a serializing authority orders the two calls before either becomes a step." What that authority is — per-home or global, and whether the dedup-consult-then-deposit pair is atomic against interleaving at the authority's granularity — is a systems-level commitment no foundation ASN yet makes. The note is internally consistent without it; specifying it is a future ASN.

### Topic 2: Rejection-cause observability
**Why out of scope**: The exposed operations are partial — rejection is "no step, no address" — but nothing says whether a caller can distinguish a gate rejection from a home-validation rejection from a P-tgt rejection. The wp analysis is complete without this (rejection falsifies the wp uniformly under the attainability convention), but an operational interface will eventually need error semantics richer than undefinedness. New territory, not an error here.

VERDICT: REVISE
