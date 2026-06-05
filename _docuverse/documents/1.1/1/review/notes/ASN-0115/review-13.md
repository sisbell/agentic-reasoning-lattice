# Review of ASN-0115

## REVISE

### Issue 1: R6's "no interior hole" claim is contradicted by the ASN's own worked instance

**ASN-0115, R6 (SilentGapFiltering)**: "the unbound portion of `⟦σⱼ⟧` is always a *terminal overrun* of the subspace's contiguous active range — the named positions past the bound frontier — never an interior hole within that range." And in the proof: "within `⟦σ⟧` the only free coordinate is `k`."

**Problem**: Both statements quantify over all of `⟦σⱼ⟧`, but `⟦σⱼ⟧` contains tumblers of depth **greater than** `m_S`, and these are unbound named positions that fall T1-*interior* to the active range. The ASN's own R6 worked instance makes the counterexample explicit: with `s = [1,2]`, `reach = [1,7]`, it states "the full denotation `⟦σ⟧` ... also contains deeper tumblers such as `[1,2,1]`." Now `[1,2,1]` is depth-3, hence unbound (the arrangement binds only depth-2 positions), and `[1,2] < [1,2,1] < [1,3]` under T1 with both `[1,2]` and `[1,3]` in `act`. So `[1,2,1]` is an unbound member of `⟦σⱼ⟧` sitting interior to the bound positions — a direct counterexample to "never an interior hole" and to "the only free coordinate is `k`." The proof only characterizes the depth-`m_S` members of `⟦σ⟧`, yet the headline claim is asserted over the whole interval.

Separately, the proof's support for the depth-`m_S` characterization is miscited: it invokes D-CTG★/D-SEQ★ to conclude that `⟦σ⟧`'s "depth-m_S, subspace-S members share the inner-component shape `[S,1,…,1,k]`." But D-SEQ★ governs the *active* (bound) set `V_S(d)`, not arbitrary named positions of `⟦σ⟧`. The correct support is T5 (ContiguousSubtrees) applied at the prefix of length `m−1` — both endpoints `s` and `s ⊕ ℓ` agree on positions `1..m−1` because `ℓ = δ(n,m)` acts at position `m` — which forces every depth-`m` member of `⟦σ⟧` to share `s`'s first `m−1` components; combined with the fact that `act ≠ ∅` forces `s` itself to be canonical `[S,1,…,1,s_m]`.

**Required**: Either (a) scope the no-interior-hole claim explicitly to the depth-`m_S`, subspace-`S` slice of named positions, and acknowledge that deeper-than-`m_S` named positions of `⟦σ⟧` are unbound, T1-interior, and harmlessly filtered out of `act` (consistent with R6's main thrust); and (b) replace the D-SEQ★ citation with the T5 prefix-`(m−1)` argument, including the step that `act ≠ ∅` forces a canonical start. As written the claim is false over `⟦σⱼ⟧` and self-contradicted by the worked instance.

## OUT_OF_SCOPE

### Topic 1: Single-span subspace straddle

**Why out of scope**: The ASN explicitly defers boundary-crossing single spans (`actionPoint(ℓ) = 1`) to the Open Questions and restricts V-specs to ordinal-level spans. This is correctly handled as future territory, not an omission in this ASN.

VERDICT: REVISE
