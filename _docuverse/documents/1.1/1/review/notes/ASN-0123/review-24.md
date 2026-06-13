# Review of ASN-0123

This ASN is unusually rigorous. The hard proofs — VN-B1's direct re-derivation of version-namespace contiguity over the K.δ vocabulary (rather than importing ASN-0040's B1), the structural O5(ii) maximality and severance argument in V9, the coverer-set inheritance in V8, SA's antichain lemma, and the two worked instances (which actually exercise the `|A| < n` shared-address subtlety) — hold up under checking. I verified the boundary cases the rubric demands (empty source `n=0`, links-only source, iterated forks, both ownership branches) and they are handled. One genuine defect remains.

## REVISE

### Issue 1: V0 cites B8 same-namespace, whose preconditions the ASN itself proves do not transfer

**ASN-0123, V0 (FreshUniquePermanentIdentity)**: "Distinctness from *all* other allocation events … is GlobalUniqueness (ASN-0034); **within one version namespace it is B8's same-namespace case under the owner's serialized commits (B-Seq)**, and across namespaces it is unconditional (B7, B8)."

**Problem**: ASN-0040's B8 same-namespace case carries the stated preconditions "in a system conforming to B-Seq, B0★ …, B0a, **B1, B2**, and B4" — these are invariants of ASN-0040's *own* transition system (Bop/baptize), not of ASN-0047's K.δ. The ASN establishes elsewhere that exactly these do not transfer: in the `nextv` discussion it writes "ASN-0040's B1 is an invariant of *its* transition system … it does not transfer to ASN-0047's K.δ vocabulary by citation," and of B2, "Taken as a black box with its stated hypothesis, B2 is therefore unavailable here." It then re-proved the contiguity it needed as VN-B1 precisely to avoid this. But for B8 in V0 it does not supply the analogous re-derivation — it cites the black box. The clause therefore rests on hypotheses the ASN has declared unavailable. This is internal inconsistency, not merely pedantry: the same B2 the ASN refuses for `nextv` is silently assumed for B8 one section later.

The conclusion (same-namespace distinctness) is nonetheless true — but via the *first* clause, GlobalUniqueness (ASN-0034), which explicitly covers "whether from the same allocator, sibling allocators, or allocators at different hierarchy depths," and applies because the version sub-allocator `A_v(d)` is T10a-conforming (siblings by `inc(·,0)`, spawned by `inc(d,1)` with `k'=1 ∈ {1,2}`). So the B8 same-namespace clause is redundant *and* unsupported.

**Required**: Delete the B8 same-namespace clause and let GlobalUniqueness carry same-namespace distinctness (it already does in the first clause), or supply the VN-B1-style re-derivation that discharges B8's B1/B2 hypotheses over the K.δ vocabulary. The cross-namespace "B7, B8 (unconditional)" citation is fine and may stay.

## OUT_OF_SCOPE

None. The scope boundary is well-drawn — the content-subspace restriction (V2b), the cross-owner severance limit (V9, V7), and the eight Open Questions faithfully enumerate the deferred territory (concurrent-fork serialization, derivation-direction recovery, windowing-vs-isolation, withdrawal semantics). The cross-owner fork's reading of the source without an authority check is not a gap: universal readability of published content is a design premise, not an omission, and the abstract model correctly carries no read gate.

VERDICT: REVISE
