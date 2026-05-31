# Review of ASN-0093

This note is correct on the mathematics I checked — the anchor construction (`inc(d,2) → inc(·,0) → inc(·,1)`), the first/subsequent-emit branching, the Cross-document disjointness case split (incomparable vs. properly-prefixing), and the simultaneous-induction framing all hold up, and the worked example exercises both branches and both cross-document cases. The findings below are the accumulated meta-prose the `anti-bloat` classifier targets, plus one citation-precision slip.

## REVISE

### Issue 1: Frame preamble defends a redundant two-clause frame
**ASN-0093, Substrate primitive operations / *Arrangement frame***: "The K.α and K.λ frames carry both `dom(M') = dom(M)` and the pointwise `(A d' ∈ dom(M) :: M'(d') = M(d'))`; under partial-function semantics the two together force `M' = M`, so C2 and L1a at `Σ` transfer to `Σ'` directly", with both ops then writing "(forcing `M' = M` per the *Arrangement frame* preamble)."
**Problem**: The preamble exists only to explain why two equivalent clauses are written where one would do, and both operations forward-reference it. This is prose justifying a notational choice — exactly the "multiple sections defer to the same location" pattern. The recent commit history ("factor frame preamble") confirms it was abstracted rather than removed.
**Required**: Write `M' = M` directly in each op's Frame and delete the preamble.

### Issue 2: Discharge-bookkeeping meta-prose on the per-chain disciplines
**ASN-0093, Per-chain disciplines**: "Their conclusions are determined per-chain and not by system state, so as ASN-0040 citations they require no per-transition discharge."
**Problem**: This explains the discharge bookkeeping rather than advancing any discipline's content — "why X needs no discharge" prose.
**Required**: Delete. The CITATION status in the Properties table already carries this.

### Issue 3: Adequacy justification of the abstract stream
**ASN-0093, Sub-allocator chains are ASN-0040 sibling streams**: "ASN-0040's `SiblingStream` is infinite, defined for every `n ≥ 1`, so a chain element exists at every index for the emission rule's pinning step to land on."
**Problem**: Defensive justification of why the abstract stream suffices; not load-bearing for any stated claim.
**Required**: Delete, or fold the single needed fact (chain element exists at every index) silently into the emission rule where it is used.

### Issue 4: Scope and Open Questions both point at the same deferred content
**ASN-0093, Scope**: "Link withdrawal. … deferred to a higher-layer retraction mechanism (see Open Questions for the invariant it must revisit)." **Open Questions**: "*Link withdrawal — which invariant must a withdrawal mechanism revisit?* The load-bearing constraint is L12's value-equality clause `L'(a) = L(a)`…"
**Problem**: Two locations cross-referencing one deferred topic — the "multiple paragraphs defer to the same downstream location" pattern.
**Required**: Keep the single substantive sentence (L12's value-equality clause is what withdrawal must revisit) in one place; drop the cross-pointer.

### Issue 5: Content↔link prose duplicated where the "symmetric" device is available
**ASN-0093, FirstEmissionFreshness** spells all four sub-cases (content-vs-`dom(C)`, content-vs-`dom(L)`, link-vs-`dom(L)`, link-vs-`dom(C)`) in full, though content-vs-`dom(L)` and link-vs-`dom(C)` are the same T7 argument, and content-vs-`dom(C)` / link-vs-`dom(L)` are the same T10 argument. The K.α and K.λ binding-precondition freshness inventories are likewise near-identical paragraphs.
**Problem**: "Two paragraphs say the same thing in different words." The note already uses the correct device elsewhere — the L1c subsequent-emit case says "Identical to the C1c subsequent-emit case above under the content↔link substitution" — so the duplication is inconsistent, not necessary.
**Required**: Prove the content case (against both `dom(C)` and `dom(L)`) once and discharge the link case by the content↔link substitution, as L1c already does.

### Issue 6: Freshness inventory in the precondition slot, with an imprecise citation
**ASN-0093, K.α binding precondition (subsequent emission)**: "Freshness of `a` … is discharged by three governing results: within-document freshness … via ChainEnumerationInjectivity + ChainMembershipForOrigin; cross-document freshness … via ChainPrefixExtension + Cross-document disjointness + T10; cross-subspace freshness against `dom(L)` via the same machinery that derives L14 … (ChainElementT4Validity + L0 + SC-NEQ + T7)."
**Problem**: (a) This is a use-site dependency inventory parked in the precondition slot — it belongs in (and duplicates) the discharge matrix. (b) The cross-subspace clause cites **L0** to supply the *fresh key* `a`'s subspace identifier, but L0 is the invariant under proof and does not yet hold at `a`; `E(a)₁ = s_C` comes from **DisjointSubAllocatorChains** (`a ∈ A_C(d)`), exactly as the L0 discharge-matrix row correctly records. The precondition prose contradicts the matrix.
**Required**: Remove the inventory (defer to the discharge matrix), and where the subspace identifier of the fresh key is needed, cite DisjointSubAllocatorChains, not L0. Same fix mirrored in K.λ.

### Issue 7: "Depends on no state component" restated repeatedly
**ASN-0093**: State model ("a pure structural projection on tumblers and depends on no state component"), C1b discharge ("`E(·)` is T4b's structural projection on the address alone, depending on no state component"), and the C2 rows each re-assert the same structural fact about `origin`/`E`.
**Problem**: The same justification recurs in several slots.
**Required**: State once (at the `origin(·)` definition in State model) that the tumbler projections are state-independent; let the frame rows cite it without re-deriving.

## OUT_OF_SCOPE

(none — all findings are in-scope prose/citation issues, not deferred machinery.)

VERDICT: REVISE
