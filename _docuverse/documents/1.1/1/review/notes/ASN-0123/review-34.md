# Review of ASN-0123

The operation is derived cleanly from its guarantees (G1–G3), and the proofs I checked hold: SA's antichain argument (the separator-zero forces `zeros(d') ≥ 3`), VN-B1's K.δ case split (the `k=2`/`k=1`/`k=0` arrivals each pinned to the frontier), V9's severance with its structural O5(ii) discharge (the `w = [pfx(π), 0]` prefix carries `zeros = 2`, contradicting O1a), V13's J1★/J1'★ two-sided pinning of `R'`, and V-WF's ValidComposite★ discharge. The edge cases the topic demands are covered (empty source `n=0`; shared content with `|A| < n`; cross-owner; iterated forks), and the three worked instances verify the postconditions against concrete addresses. Standard #7 is satisfied — every cited ASN is a foundation ASN.

The findings below are accreted meta-prose flagged under the note's anti-bloat classifier, not correctness gaps. I have avoided the foundation non-transfer justifications (B2/B1/B8 avoidance, the VN-B1 reproof) and the V-WF/V9 O5(ii) discharge, which prior cycles have established as load-bearing.

## REVISE

### Issue 1: the atomicity remark names a convention no proof uses
**ASN-0123, Remark (atomicity)**: "Two boundary assumptions must be kept apart. P-bdy … is an invocation-context condition on the predecessor… The interior-unobservability convention — that VERSION's own interior states are unobservable absolutely… — is strictly stronger and bears on VERSION's successor rather than its predecessor; absent it the post-K.δ interior state remains reachable, and the implementation happens to realize it (whole-request serialization)."
**Problem**: The note's proofs consume only two facts: P-bdy (giving P4★ at `Σ` for V9w) and "`Σ'` is the terminal boundary" (giving the composite-boundary properties in V-WF). The "interior-unobservability convention" is introduced, named, and contrasted with P-bdy purely to flag a concurrency concern that the note then explicitly says it does *not* rely on ("absent it… the implementation happens to realize it"). It is Open Question 4 material occupying a remark slot; a reader tracking the operation's guarantees must skip it.
**Required**: Drop the "two boundary assumptions" paragraph, or relocate its one live observation (absent stronger serialization, the post-K.δ interior state is reachable) into Open Question 4. The remark's first half — interior state exists, couplings are initial-to-final, so the terminal boundary carries the snapshot — is load-bearing and should stay.

### Issue 2: PS carries a navigation signpost, a reasonableness gloss, and a downstream-consumer phrase
**ASN-0123, PS (clause iv) and its closing**: "Incumbency is the Π → E direction; the converse E → Π coverage (ω total) is derived next." … "PS is Nelson's design read structurally — a number exists only because some account-holder forked it into being [LM 4/17], so ownership in the allocation sense is total by construction; PS adds only that baptism is the sole entrance." … "carrying a document sub-allocator A_doc (ASN-0047) — the namespace its cross-owner forks descend into."
**Problem**: Three distinct accretions. The first is a signpost duplicating the next paragraph's own opening ("From (i)–(iii), coverage of the registry … is derived"). The second is reasonableness-rationale for the standing assumption — *why PS is acceptable* — rather than content of what PS requires (the flagged "explains why the axiom is needed rather than what it says" pattern). The third enumerates a downstream consumer (cross-owner forks) inside the incumbency clause, where A_doc's role is not yet in play.
**Required**: Cut the "derived next" signpost; cut or compress the Nelson-rationale sentence; drop "— the namespace its cross-owner forks descend into" (A_doc's role is established where cross-owner allocation is actually proved, in V-WF/V9).

### Issue 3: V7's cross-owner caveat trails a restated cross-reference chain
**ASN-0123, V7 (downward bullet)**: "Cross-owner versions are *not* recovered here… severed from the source's subtree (VD establishes this from the failure of the `derives` biconditional, via V9), so no address-based descendant scan reaches it — the cross-owner remainder is decided only by shared content (V9w), never the registry. This is the downward face of severance, the standing limit flagged in Open Question 2."
**Problem**: The load-bearing content is the opening clause — cross-owner versions are not enumerated by the registry scan, which is the genuine scope limit of V7's downward claim. The remainder is a cross-reference chain (VD → V9 → V9w) plus the restatement "the downward face of severance" plus an open-question pointer, all re-saying what V9 (severance), V9w (witness), and VD (derivation) already establish in full. The reader gets the limit from the first clause and skips the rest.
**Required**: Keep the caveat that cross-owner versions fall outside the registry scan with a single citation (V9); drop the "VD establishes this… via V9 / downward face of severance / flagged in Open Question 2" accretion.

## OUT_OF_SCOPE

No misplaced claims. The note correctly defers concurrency serialization, location-fixed windowing, version comparison, and content/link operations to its Open Questions and Scope statement, defining no claims for them; the implementation-evidence deviations (session-layer GC, principal enforcement) are framed as evidence, not as state/operation claims.

VERDICT: REVISE
