# Channel Assignment — ASN-0133 review-46

**Date:** 2026-06-14 15:29

## Issue 1: The "stutter Σ →_sh* Σ" witness does not exist
Reason: The replacement construction's two other premises are in hand — "no PL trigger reads `dom(Σ.C)`" is an ASN-0129 fact (V-DOC/QD-audit) and "no-op fires need a trigger-false argument" is RG's own no-op clause — but the linchpin that both demolishes the original stutter and licenses the `K.α` construction is the operational claim that *every* `→_sh` step strictly grows one of the three foundation domains. That is a "what the substrate steps actually do" property, and given the original error was itself a substrate mis-model, it should be confirmed against the implementation rather than assumed.
Gregory question: Does every primitive substrate step (`K.σ`, `K.α`, `K.λ_sh`) strictly grow one of `dom(Σ.M)`, `dom(Σ.C)`, `dom(Σ.L)` — i.e., is there no domain-preserving primitive step (the substrate strictly monotone/append-only) — and do content (`K.α`) deposits grow `dom(Σ.C)` alone?

## Issue 2: Forward-reference accretion around Q5a (anti-bloat)
Reason: Purely structural — delete a redundant map paragraph and the duplicated closing clause of W; the strict-strengthening relation is proven in Q5a and the forward-referenced case (3) is defined in Q6. The redundancy is evident from the ASN's own organization.

## Issue 3: The "emissions, not bodies" principle is stated twice (anti-bloat)
Reason: Internal de-duplication — RG previews and Q2 names the same "bodies identified by their emission sets" claim; consolidate to Q2 (or have RG cite forward). Derivable entirely from the ASN's own content.

## Issue 4: Mismatched foundation citation in the worked trace (precision/anti-bloat)
Reason: A citation swap whose correct target the reviewer has already pinpointed — I5 (IdemFalseAlwaysFresh) / I1's miss branch — whose content is stated in ASN-0128 and whose name dispositively confirms "idem=⊥ Emit is always a single fresh step," with no concurrency to invoke I4. Verifiable from the cited dependency's lemma statement.
