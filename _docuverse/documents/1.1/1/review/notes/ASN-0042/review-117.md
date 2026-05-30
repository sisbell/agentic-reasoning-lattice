# Review of ASN-0042

The mathematical content is in strong shape — the longest-match machinery (O2), the reachable-state induction (O1a/O1b/T4 consolidated into one site), the refinement chain (O3 → O8 → OwnershipDomainPermanence), and the O10 fork construction are internally consistent, and the worked example's tumbler arithmetic checks out end to end (e.g., `next(Σ_pre.B,[1,0,2],2) = [1,0,2,0,6]`, `next(Σ.B,[1],2) = [1,0,3]`). The findings below are accretion/forward-reference patterns flagged under the `review-mode.anti-bloat` classifier, not correctness defects.

## REVISE

### Issue 1: Document-ordering meta-prose in the O1a induction
**ASN-0042, *The Account-Level Boundary***: "(The delegation step forward-references the delegation predicate conditions (i)–(v) of O15, defined in *State Axioms*.)"
**Problem**: This parenthetical exists only to justify the note's section ordering (why a later definition is cited early). It advances no reasoning — the delegation step itself names conditions (iii)/(v) where it uses them. This is exactly the "prose justifies document ordering / non-circular forward pointer" pattern.
**Required**: Delete the parenthetical. The per-condition citations in the delegation step already tell the reader where the conditions live.

### Issue 2: Standalone deferral paragraph duplicating the consolidated-induction pointer
**ASN-0042, *Delegation***: "The delegation steps for O1a, T4-validity, and O1b (PrefixInjectivity) — discharged with the delegation predicate conditions now in hand — were given as part of the single reachable-state-invariance induction in *The Account-Level Boundary*."
**Problem**: This paragraph carries no reasoning; it only announces that work done elsewhere is done. The same back-pointer already appears inline at the O1b statement ("established by the shared induction in *The Account-Level Boundary*"). Two sections deferring to the same proof site — the flagged "multiple paragraphs in different sections defer to the same location" pattern. The consolidation into one induction was the right call; the residual signpost paragraph is the leftover.
**Required**: Remove this paragraph. The O1b inline pointer is sufficient.

### Issue 3: O7(c)'s next-reachability qualifier restated three times
**ASN-0042, O7(c)** — theorem body, proof close, and Formal Contract each state the same restriction:
- body: "Condition (v) constrains p'' to a next-reachable address ... not an arbitrary strict descendant."
- proof: "Condition (v) (next-reachability ...) constrains p'' to a single-step stream extension of an already-baptized prefix ..."
- contract: "by (v) the admitted p'' is a next-reachable single-step stream extension ... not an arbitrary strict descendant."

**Problem**: Three near-verbatim statements of one fact ("p'' is a single-step stream extension, not an arbitrary descendant") — the "two paragraphs say the same thing in different words" pattern, here tripled.
**Required**: Keep the constraint in one canonical slot (the Formal Contract), and let the theorem body and proof reference condition (v) without re-paraphrasing its content.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer and provenance/owner divergence
The Open Questions already isolate this correctly. O3/O8 describe a refinement-only regime ("Gregory's codebase contains no transfer mechanism; O3 describes the refinement regime for the system as specified"). Transfer would make `pfx(ω(a))` diverge from `acct(a)`'s recorded provenance (O6) — a new invariant landscape, not a defect here.

### Topic 2: Cross-node identity federation
O9 establishes node-locality and explicitly notes the docuverse is "a forest of independently owned trees." Federation invariants reconciling separate node-rooted principals are new territory, correctly deferred to the Open Questions.

VERDICT: REVISE
