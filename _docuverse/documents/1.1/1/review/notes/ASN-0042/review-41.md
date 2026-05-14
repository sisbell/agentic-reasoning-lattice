# Review of ASN-0042

## REVISE

### Issue 1: O12 cited where O13 is required (two instances)
**ASN-0042, Delegation section, "Delegation preserves O1a"**: "...the existing principals are unchanged by O12. O1a is maintained."
**ASN-0042, Delegation section, "Delegation preserves T4"**: "Existing principals' prefixes are unchanged by O12. T4 is maintained across the transition."
**Problem**: O12 (PrincipalPersistence) is `Π_Σ ⊆ Π_{Σ'}` — it asserts persistence of principals in Π, not immutability of their prefixes. The arguments require prefix unchangedness, which is O13 (PrefixImmutability)'s content. The second instance is especially explicit ("prefixes are unchanged"), which is a direct misattribution. Without O13, existing principals could in principle have their prefixes altered across a transition, breaking O1a (a prefix's `zeros` count could change) and T4 (a previously valid prefix could become invalid).
**Required**: Cite O13 in both places. The complete argument needs O12 (persistence) and O13 (prefix immutability) together to conclude existing principals still satisfy O1a / T4 in `Σ'`.

### Issue 2: NestingByDelegation derivation list omits O15
**ASN-0042, Properties Introduced table**: The NestingByDelegation entry reads "from O1b, O12, O13, O14(vi), delegation condition (vi), covering-chain lemma".
**Problem**: The proof of NestingByDelegation explicitly uses O15 in the inductive step: "(by O15, at most one new principal per step; if none is introduced, the invariant is preserved trivially...)". The case split between "no newcomer" and "exactly one newcomer π'" is load-bearing for the structure of the induction and is grounded in O15's `|Π_{Σ'} ∖ Π_Σ| ≤ 1` clause. The bootstrap-exclusion sub-argument also leans on O15's enumeration of introduction modes (bootstrap or delegation).
**Required**: Add O15 to the derivation list.

### Issue 3: Delegation O1b preservation argument implicitly assumes O13 for existing-vs-existing case
**ASN-0042, Delegation section, "Delegation preserves O1b"**: The argument handles the new-vs-existing prefix collision via length contradiction, and notes by O15 that there is at most one newcomer (so no new-vs-new collision). The existing-vs-existing case is left implicit: O1b held in `Σ`, so existing prefixes were pairwise distinct; preserving this in `Σ'` requires that existing prefixes don't change.
**Problem**: The proof does not cite O13 for the existing-vs-existing case. A reader following the chain rigorously must supply this step independently.
**Required**: Add an explicit sentence: existing principals retain their prefixes by O13, so the existing-vs-existing pairwise distinctness preserved in `Σ` carries to `Σ'`.

### Issue 4: O7(c) recursive-delegation construction proves existence but skips the verification chain
**ASN-0042, O7 postcondition (c)**: "Conditions (ii) and (vi) can be met in a sequential construction in which each `π_k` is delegated by `π_{k-1}` at a state where no other principal yet covers `pfx(π_k)` — they constrain the *moment* of delegation, not the prefix family, and are satisfiable inductively."
**Problem**: The conclusion "satisfiable inductively" is stated rather than proved. The family `pfx(π_k) = [1, 0, 1, …, 1]` is exhibited explicitly with (i), (iv), (v) checked, but for (ii) (most-specific covering of `pfx(π_{k+1})` by `π_k` in `Π_{Σ_k}`) and (vi) (no existing principal extends `pfx(π_{k+1})`) the reader is left to verify by induction. A one- or two-sentence inductive verification — at `Σ_k`, the covering principals of `pfx(π_{k+1})` are `π_0, …, π_k` with prefix lengths `1, 3, 4, …, k+1`, so `π_k` is most-specific; existing prefixes are bounded by `k+1 < k+2 = #pfx(π_{k+1})`, so condition (vi) holds — would close the gap.
**Required**: Spell out the inductive verification of (ii) and (vi) for the exhibited family, or cite that the inductive content is the same case analysis as in the proof of NestingByDelegation.

## OUT_OF_SCOPE

(None. The ASN's Scope section and Open Questions list correctly defer ownership transfer, prefix-overlap enforcement, identity federation, delegation-history reconstruction, and related concerns to future ASNs without smuggling claims about them into the body.)

VERDICT: REVISE
