# Review of ASN-0093

## REVISE

### Issue 1: FirstEmission misattributes the anchor's T4-validity to B6(a)

**ASN-0093, FirstEmission lemma proof**: "T4-validity is TA5a's `k = 1` case, whose side condition `zeros(b_C(d)) ≤ 3` is discharged by `b_C(d)`'s T4-validity (T4 forces `zeros ≤ 3`) — here `b_C(d)` is T4-valid by B6(a) (verified above)."

**Problem**: B6(a) (ValidDepth sufficiency, ASN-0040) is the implication `p T4-valid ∧ depth-conditions ⟹ every cₙ ∈ S(p,d) is T4-valid`. It *consumes* the anchor (parent `p = b_C(d)`) being T4-valid as a hypothesis; it does not *establish* it. Citing B6(a) to prove the anchor T4-valid is circular — B6(a) needs that fact as input. The anchor's T4-validity is actually grounded elsewhere (the B6-verification paragraph under *Sub-allocator chains are ASN-0040 sibling streams*: `b_C(d) = inc(d, 2)` preserves T4 via TA5a, `k = 2` side condition `zeros(d) ≤ 2` discharged by M0's `zeros(d) = 2`).

**Required**: Cite the anchor-T4 grounding (M0 + TA5a on `inc(d, 2)`), not B6(a). The same misattribution should be checked in the link case ("The link case is symmetric").

### Issue 2: Duplicate circularity parentheticals in FirstEmissionFreshness

**ASN-0093, FirstEmissionFreshness proof**: the content-against-`dom(L)` paragraph carries "(The new key `a` is not yet committed to `dom(C)` at the K.α event firing the first-emit predicate, so L0 at `Σ` does not apply to `a`; L0 at `Σ'` would be circular since L0 at `Σ'` itself depends on FirstEmissionFreshness via the discharge matrix's K.α entry.)" and the link-against-`dom(C)` paragraph carries the identical note with `ℓ`/`dom(L)`/K.λ substituted.

**Problem**: This is the flagged "prose justifies non-circularity" pattern, and the two parentheticals are verbatim duplicates under content↔link substitution. The proof has already declared the two cases "follow parallel structure with one substitution rule," so stating the circularity caveat twice is accreted noise.

**Required**: State the soundness caveat once (the simultaneous-induction framing already owns this concern) and let the substitution rule carry it across both cases; remove the duplicate.

### Issue 3: Defensive use-site aside in ChainMembershipForOrigin

**ASN-0093, ChainMembershipForOrigin lemma statement**: "The further *partition* claim — pairwise disjointness of the chains across distinct origins together with joint coverage of `dom(C)` and `dom(L)` — is recoverable as a corollary but not needed by downstream consumers: covering follows from C2 + L1a …; cross-document disjointness … follows from the Cross-document disjointness lemma…"

**Problem**: This is a "not needed by downstream consumers" inventory aside that does not advance the lemma's statement or proof — it states something the lemma deliberately does not claim, then justifies its omission. Reader must skip past it to reach the proof.

**Required**: Delete. If the partition corollary is genuinely consumed nowhere, its absence needs no justification.

### Issue 4: SubAllocatorAxiom prose explains why, not what

**ASN-0093, SubAllocatorAxiom**: "…without claiming that they are embedded in any global allocator tree. The substrate makes no commitment about whether an implementation realises the chains as standalone allocators with spawning triples or as discipline-conforming streams within a flatter structure."

**Problem**: This is the flagged "new prose around an axiom explains why the axiom is needed (or its scope/non-commitments) rather than what it says" pattern. The axiom's object-level content is one clause: the chains are `S(b_·(d), 1)`. The implementation-non-commitment editorializing is meta-prose, and the subsequent "*Chain discipline (SubAllocatorAxiom.ChainDiscipline)*" sub-paragraph then restates the same clause a second time.

**Required**: Reduce to the single object-level clause. Drop the implementation-realization disclaimer and the restating sub-paragraph.

### Issue 5: Intro / Scope redundancy on downstream-dependency framing

**ASN-0093, intro vs Scope**: intro — "Downstream ASNs that reason about address allocation into the three stores without lifting the entity/provenance layer can depend on this note directly, without inheriting the additional state components…"; Scope — "Downstream ASNs that operate on the link store without needing arrangement mutation, entity stratification, or provenance recording can cite this substrate directly. Downstream ASNs that need any of the deferred machinery cite a higher-layer transition model…"

**Problem**: Two paragraphs in different sections state the same downstream-dependency rule in different words ("two paragraphs say the same thing").

**Required**: State the dependency rule once (the Scope section is the natural home) and remove the intro restatement.

### Issue 6: K.σ cross-store and cross-anchor freshness repeat one argument

**ASN-0093, K.σ**: *Cross-store freshness* argues `d ∉ dom(C) ∪ dom(L)` because `zeros = 2` cannot equal the stores' `zeros = 3`; *Cross-anchor freshness* argues `d ≠ b_C(d'), b_L(d')` because the anchors have `zeros = 3` against the precondition's `zeros = 2`.

**Problem**: The two sub-paragraphs run the identical `zeros = 2` vs `zeros = 3` distinctness argument against two target sets, and each "imagines a case the precondition already excludes." Stating it twice is accretion.

**Required**: Merge into one freshness remark covering `dom(C) ∪ dom(L)` and the anchors jointly via the single `zeros = 2`-vs-`3` observation.

### Issue 7: Simultaneous-induction framing carries defensive restatement

**ASN-0093, Simultaneous-induction framing**: "…the lemmas and the matrix invariants are mutually entangled and sound only under this simultaneous-induction discipline. The ChainMembershipForOrigin proof above records the per-transition discharges; StoreT4Validity transfers via frame…"

**Problem**: The framing's first half (which properties are state-independent vs transition-indexed, and that the IH is the conjunction with no same-step self-use) is load-bearing and should stay. The trailing sentences re-narrate, in prose, the per-transition discharges that the discharge matrix and the ChainMembershipForOrigin proof already supply — restating the entanglement claim a second time.

**Required**: Keep the decomposition and the no-same-step-use discipline; cut the re-narration of discharges already carried by the matrix.

## OUT_OF_SCOPE

### Topic 1: Link withdrawal / tombstoning (Open Questions, three-path discussion)
**Why out of scope**: The Open Questions paths (a)/(b)/(c) for withdrawal correctly defer this to a higher-layer ASN and commit to none; this is appropriate deferral, not a substrate claim. (Noted for completeness per the OUT OF SCOPE list — no action required, though the (a)/(b)/(c) treatment is longer than the deferral strictly needs.)

META: (not applicable — the ASN defines abstract state, three allocation operations, and the invariants they preserve, stated implementation-independently; it has not drifted into mechanics.)

VERDICT: REVISE
