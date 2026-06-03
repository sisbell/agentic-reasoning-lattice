# Review of ASN-0069

## REVISE

### Issue 1: Use-site justification prose that does not advance the proof
**ASN-0069, "The Fork Composite" (K.δ sub-case discharges)**: 
> "(ChildSpawnFreshness packages the case analysis over the system's allocation history — the at-most-once-per-(t, k') constraint, cross-allocator disjointness, within-stream injectivity — that we would otherwise re-derive from T10a, T10a.6, and T10a.7.)"

and the parallel
> "(FrontierEquivalence packages the within-stream injectivity, monotone-emission, and cross-allocator-disjointness reasoning that we would otherwise re-derive from T10a.7, SequentialTransitionAxiom, P1, and T10a.6.)"

**Problem**: Both parentheticals explain *why a lemma is convenient* rather than discharging any precondition. The freshness obligations are already discharged by the biconditionals immediately above them; the "what we would otherwise re-derive" inventory is meta-prose the reader must skip to follow the argument. This is the use-site-rationale pattern the anti-bloat classifier flags.
**Required**: Delete both parentheticals. The lemma citation alone discharges the obligation.

### Issue 2: Same statement repeated in two sections in different words
**ASN-0069, paragraph after V7** and **link-only vignette in "Worked Example"**:
> "...so V6's equation is established by total arrangement emptiness rather than by the selective subspace exclusion of the non-empty case." (post-V7)
> "...confirming V6 in this regime: the fork's link subspace is empty, as before, but now via total arrangement emptiness rather than the selective subspace exclusion of the non-empty case." (vignette)

**Problem**: Two paragraphs assert the identical point (V6 holds in the empty case by total emptiness, not selective exclusion) in near-identical words. This is the "two paragraphs say the same thing in different words" pattern.
**Required**: Keep the statement once (in V7's discharge) and drop the restatement in the vignette, or have the vignette simply cite V7.

### Issue 3: V10(b) assumes "d_new¹ is the first fork" but V10's premise does not establish it
**ASN-0069, V10(b)**: "d_new¹ is the first fork of d_src, so its d_op¹ = d_src, and it reads M(d_src) at Σ."
**Problem**: V10's premise is only "Let Σ →* Σ¹ be *a* fork of d_src producing d_new¹." Nothing requires d_new¹ to be the *first* fork. If d_src had been forked before Σ, then by V1's subsequent-fork sub-case d_new¹'s content operand would be a prior version, not d_src, and "reads M(d_src) at Σ" is false. The property's operand-tracking claim is sound only under an unstated assumption.
**Required**: Either add "d_new¹ is the first fork of d_src" to V10's premises, or restate (b) in terms of each fork's own J4 operand d_op^i without pinning d_op¹ = d_src.

### Issue 4: "Transitive correspondence" between d_src and d_new asserted without derivation
**ASN-0069, paragraph after V8**: "The named source d_src corresponds to d_new transitively, on those positions where d_op was itself unedited since being forked from d_src (full correspondence when d_op = d_src)."
**Problem**: V8 establishes correspondence between d_op and d_new only. The transitive d_src ↔ d_new correspondence for the subsequent-fork case (d_op = d_prev ≠ d_src) is stated as a fact with the qualifier "on those positions where d_op was unedited," but no chain of premises is given — there is no V-property carrying correspondence across the d_src → d_prev → d_new hops. A derived guarantee labeled as holding "transitively" must name its premises and show the composition (cf. V11, which does this carefully for the all-first-fork chain).
**Required**: Either derive the transitive claim explicitly (it appears to need a V11-style unedited-source premise on d_prev), or restrict the sentence to the d_op = d_src case and defer the general transitive claim to V11.

## OUT_OF_SCOPE

### Topic 1: Source-as-transcludent forks
**Why out of scope**: The behavior of forking a source whose arrangement references foreign-origin I-addresses is correctly deferred to an Open Question; it is new territory, not a defect here.

VERDICT: REVISE
