# Review of ASN-0047

I checked the elementary transitions, the K.δ case analysis, the K.μ~ decomposition with link-subspace fixity, the D-SEQ★ derivation, and the Class (a)/(b) invariant matrix. The formal machinery is internally consistent — the K.δ-ID identities, TA5a bounds, FrontierEquivalence, and the cross-document/cross-subspace disjointness chain all hold up, and the worked examples discharge their named checks correctly. No correctness defect surfaced. The findings below are accretion/meta-prose at source, per this note's `review-mode.anti-bloat` directive.

## REVISE

### Issue 1: Duplicated claim across adjacent blocks (no-retyping / partial-M)
**ASN-0047, §The state model + Bridging lemma (M–E_doc)**: The state-model paragraph states "M is the arrangement family carrying the foundation's typing verbatim — `M(d) : T ⇀ T` is *partial* (ASN-0036, ASN-0093), with `dom(M)` the set of allocated documents exactly as in the foundations." The immediately following Bridging lemma restates: "This ASN introduces *no* retyping of the arrangement family: `M(d) : T ⇀ T` remains partial and `dom(M)` retains its single foundation meaning, the set of allocated documents."
**Problem**: Two adjacent blocks assert the same thing (M is partial, dom(M) = allocated documents, no retyping). The load-bearing content of the Bridging lemma is (†) `dom(M) = E_doc`; the no-retyping sentence is a defensive restatement of the preceding paragraph.
**Required**: State the typing once (in the state model), and open the Bridging lemma with its actual content — the identity (†) and its justification — without re-asserting partiality/no-retyping.

### Issue 2: Mechanism essay in a restatement-table slot (L1c inherited row)
**ASN-0047, *Inherited from foundation* table, L1c row**: The row carries "The anchor traversal `d → b_C(d) → b_L(d) → [d.0.s_L.1]` and the first link emission inhabit no T10a-tracked allocator domain — their activation discharge goes through SubAllocatorBundle rather than T10a's child-spawning rule."
**Problem**: This table's stated purpose is to "restate" an inherited statement plus its foundation source ("every statement and every preservation argument is supplied by the cited foundation"). The activation-mechanism essay is body content — it already appears in the L1c Class (a) verification prose — relocated into a structural slot whose job is statement + source.
**Required**: Reduce the L1c row to the inherited statement and source; keep the activation-discharge mechanism only in the body verification.

### Issue 3: Derivation-comparison meta-prose in J1'★
**ASN-0047, §Scoped coupling constraints (J1'★ derivation)**: "J1'★ is the *converse* coupling, and it is not symmetric to J1★: where J1★ runs wp forward from P4★ (`Contains_C ⊆ R`) under the content-range-extending K.μ⁺, J1'★ runs wp backward from a *different* invariant — P4a..."
**Problem**: The symmetry-vs-asymmetry commentary explains the *shape* of the two derivations relative to each other rather than advancing either. The wp computation that follows is the substantive content; the comparative framing is reviser-style justification a precise reader must read past.
**Required**: Drop the "it is not symmetric ... where J1★ runs forward ... J1'★ runs backward" framing and lead directly with the wp computation from P4a.

### Issue 4: Repeated dom(C)→dom(L) substitution rationale in S8★
**ASN-0047, §Amendments (S8★ definition)**: The argument "the membership conjuncts of both (a) and (b) carry `dom(Σ.C)` ... which is false for link-subspace labels: they reside in `dom(L)`, disjoint from `dom(C)` by L14" is stated in the definition lead, re-derived in the link-subspace route ("cannot use ASN-0036's S8 directly because its range lies in `dom(L)` not `dom(C)`, falsifying S3; S7b/C1b also do not apply"), and summarized a third time ("the `dom(C) → dom(L)` substitution replaces ASN-0036's failed S3 (and S7b/C1b) preconditions").
**Problem**: The same substitution rationale appears three times within one definition. Each restatement makes the reader re-confirm a point already established.
**Required**: State the substitution rationale once (the link-subspace route is the natural home) and have the lead reference it rather than re-derive it.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
**Why out of scope**: The fork composite (J4) deliberately starts the forked document's link subspace empty, and the ASN's own text and Open Questions defer a link-inheritance mechanism. This is correctly future territory, not a defect.

VERDICT: REVISE
