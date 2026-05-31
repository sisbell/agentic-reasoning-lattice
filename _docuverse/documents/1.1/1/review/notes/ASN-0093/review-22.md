# Review of ASN-0093

## REVISE

### Issue 1: TA5a's k=1 branch misstated as having "no zero-count side condition"
**ASN-0093, C1c/L1c chain exhibition, FirstEmission lemma, worked-example Steps 2/6/7**: "TA5a at k = 1 applies unconditionally on T4-valid inputs (no zero-count side condition)"
**Problem**: TA5a (ASN-0034) explicitly states the k=1 branch as `k = 1 ∧ zeros(t) ≤ 3` — there *is* a zero-count side condition. The conclusion is sound (T4-validity entails `zeros ≤ 3`, so the condition is always met), but the parenthetical "(no zero-count side condition)" literally contradicts the cited foundation contract. A reader checking TA5a finds the condition and is misled. This phrasing recurs in at least five places.
**Required**: Replace "no zero-count side condition" with "the side condition `zeros(t) ≤ 3` is discharged by T4-validity," matching how the contrast with the k=2 case (where `zeros ≤ 2` is *not* automatic) is actually load-bearing.

### Issue 2: "(equivalently L14 at the pre-state)" conflates the invariant with fresh-key disjointness
**ASN-0093, K.α and K.λ subsequent-emit preconditions**: "cross-subspace freshness against `dom(L)` via the ChainElementT4Validity + L0 + SC-NEQ + T7 triad (equivalently L14 at the pre-state)"
**Problem**: L14 (`dom(C) ∩ dom(L) = ∅`) quantifies over *committed* members; the new key `a` (resp. `ℓ`) is not yet in either store, so L14-at-Σ does not yield `a ∉ dom(L)`. The actual mechanism is the per-pair T7 triad applied to `(a, ℓ)`. The note's own FirstEmissionFreshness proof is careful here ("the new key `a` is not yet committed... L0 at Σ does not apply to `a`"), so the "(equivalently L14)" gloss is internally inconsistent with that care.
**Required**: Drop the "(equivalently L14 at the pre-state)" parenthetical, or restate it as "the same machinery that derives L14, applied to the fresh key against each committed peer."

### Issue 3: Triple repetition of "no commitment about implementation realisation"
**ASN-0093, *Sub-allocator chains* intro, SubAllocatorAxiom statement, SubAllocatorAxiom.ChainDiscipline bullet**: the claim that the substrate makes no commitment about whether chains are "standalone allocators with spawning triples or discipline-conforming streams within a flatter structure" appears three times in adjacent prose.
**Problem**: Anti-bloat — the same disclaimer is stated three times within one section.
**Required**: State once, at the axiom; delete the other two.

### Issue 4: Duplicate factoring rationale in the introduction
**ASN-0093, opening paragraphs**: paragraph 1 ("all of which the substrate restates verbatim, modulo the single notational substitution detailed in the next paragraph") and paragraph 3 ("every operation and invariant here is identical to its counterpart in the fuller model except for one notational substitution — `E_doc` ... replaced by `dom(M)`").
**Problem**: Two paragraphs assert the same fact (verbatim restatement modulo `E_doc → dom(M)`); the first is a forward pointer to the second.
**Required**: Merge into one statement of the substitution.

### Issue 5: Defensive existence-justification around an axiom
**ASN-0093, SubAllocatorAxiom block and Properties table**: "so no separate existence postulate is required" / "Chain existence is unconditional from ASN-0040's SiblingStream ... not postulated."
**Problem**: New prose around the axiom explains why a clause is *absent* rather than stating what the axiom says — the named anti-bloat pattern — and it appears twice (body and table).
**Required**: If chain existence follows from B6-validity, simply omit the existence clause silently; do not narrate its omission.

### Issue 6: Repeated deferral to the same downstream location
**ASN-0093, K.α and K.λ subsequent-emit preconditions**: both say freshness is "discharged by three governing results, with the full multi-step derivation kept once in the [C1c/L1c] chain exhibition subsequent-emit case and the discharge matrix's L14 entry below."
**Problem**: Two preconditions in different operations defer to the same two downstream sites — the named "multiple paragraphs defer to the same downstream location" pattern. The reader must hold two forward pointers to follow a precondition.
**Required**: State the freshness discharge once and cross-reference it from a single place, or inline the short version at the precondition.

### Issue 7: L14 discharge-matrix cells restate a near-identical derivation
**ASN-0093, discharge matrix, L14 row**: the K.λ cell is labeled "symmetric to K.α with content↔link" yet then fully restates the entire T7-triad derivation (L0 C-clause/L-clause, SC-NEQ, StoreT4Validity, C1/L1, T7) with only the symbols swapped.
**Problem**: Redundant — "symmetric" plus a full restatement defeats the point of "symmetric." Same content twice.
**Required**: Either state the derivation once with the content↔link substitution rule, or keep the "symmetric" label and delete the restatement.

## OUT_OF_SCOPE

### Topic 1: Open-Questions link-withdrawal essay (paths a/b/c)
**Why out of scope**: Link withdrawal/tombstoning is explicitly deferred, and the three-path discussion correctly commits to nothing. It is appropriately placed in Open Questions. Noting only that the implementation-level detail (udanax-green `DELETEVSPAN`, `find_links`) is heavier than a forward pointer needs to be; trimming would help, but the placement is not an error.

VERDICT: REVISE
