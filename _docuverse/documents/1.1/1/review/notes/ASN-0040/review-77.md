# Review of ASN-0040

## REVISE

### Issue 1: The d=1 boundary cluster is accreted meta-prose, and its framing undercuts itself

**ASN-0040, B6 proof (necessity) and "Design rationale for condition (i) at the d = 1 boundary"**: "We then record, for completeness, why a non-T4 parent breaks the stream — establishing that (i) too is required for stream validity, save for one boundary case (pure trailing zero at d = 1) where stream validity does not force it..."

**Problem**: The framing asserts "(i) too is required for stream validity" and then immediately exempts the case where it is not — i.e. it states a necessity it refutes in the same breath. The contract postcondition (b) already concedes "stream validity does not force it" for the d=1 trailing-zero parent, so the honest claim is that (i) is *not* necessary for stream validity; it is a definitional choice. Carrying a full case-(a)/case-(b) necessity argument to reach a conclusion that is partly negative, then patching it with a separate "Design rationale" paragraph, is exactly the accretion this note is flagged to surface. The same boundary is restated four times — proof intro ("for completeness... taken up in the design rationale"), case (b) ("deferred to the design rationale"), the design rationale itself, and contract (b) — the "multiple paragraphs defer to the same downstream location" and "two paragraphs say the same thing" patterns. The design rationale also carries a use-site inventory ("used downstream by B7 and B8"), which advances no reasoning about the claim.

**Required**: Reduce to the contract's actual scope — necessity of (ii) and (iii) given a T4-valid parent — and state the (i) choice in one line: "(i) is imposed by definition, not forced by stream validity; it disambiguates the S2 aliasing of ([1,0],1) and ([1],2)." Drop the "(i) too is required" framing, the repeated deferrals, and the downstream-consumer list.

### Issue 2: S2's only consumer is the boundary cluster

**ASN-0040, S2 (Trailing-Zero Stream Identity)**: "Then S(p, 1) = S(p′, 2)."

**Problem**: S2 is invoked only by the B6 d=1 boundary argument (case (b) and the design rationale). B7's disjointness proof uses the canonical stream form and T3, not S2; B8/B9 do not use it. If Issue 1's cluster is trimmed, S2 is orphaned. As written, a self-contained lemma exists to support meta-prose justifying a definitional choice.

**Required**: Either show S2 earns an independent place (a consumer outside the boundary discussion), or fold the one identity it proves into the trimmed one-line note from Issue 1.

## OUT_OF_SCOPE

None. B3 (ghost validity) is correctly framed as a forward requirement on a future content-storage ASN rather than a claim of this note, and the deferred topics are properly listed in Scope and Open Questions.

The substantive invariants (B0, B0★, B_fin, B1, B2, B8, B9, B10) and the freshness argument in Bop are sound: the freshness proof correctly avoids any appeal to B1 (using only `a ∈ S(p,d)` and `a ∉ children`), B8 correctly restricts to co-reachable acts (acknowledging that cross-branch baptisms can collide), and B7's unequal-length case is fully discharged via TA5-SigValid. No correctness gaps found in these.

VERDICT: REVISE
