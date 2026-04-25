# Regional Review — ASN-0034/TA-assoc (cycle 1)

*2026-04-23 03:58*

### Missing foundation claims T1, NAT-sub, NAT-cancel, NAT-wellorder, NAT-discrete
**Class**: REVISE
**Foundation**: The review header states "Foundation Statements (current) — (none — this is a foundation ASN)"; the ASN metadata shows `Declared depends:` empty.
**ASN**: Multiple citations lack grounding in the shown content:
- TumblerAdd proof: "T1 case (i) at divergence position `k` yields `a ⊕ w > a`"; "`k - 1 ∈ ℕ` and `n - k ∈ ℕ` are well-defined by NAT-sub's conditional closure"; "NAT-cancel's symmetric summand absorption `n + m = m ⟹ n = 0`"; "NAT-wellorder applied to `{j : 1 ≤ j < k ∧ aⱼ > 0}` supplies the least such `j`".
- ActionPoint proof: "By NAT-wellorder, there exists m ∈ S…"; "NAT-discrete's forward direction m < n ⟹ m + 1 ≤ n".
- TA-assoc depends list: includes T1, NAT-addassoc (present), but TumblerAdd's indirect reliance on T1 for its postconditions `a ⊕ w > a (T1)` and `a ⊕ w ≥ w (T1, T3)` propagates here.

The ASN Content section presents T0, TumblerAdd, TA0, TA-Pos, ActionPoint, T3, NAT-addassoc, NAT-addcompat, NAT-closure, NAT-order, NAT-zero, TA-assoc. It does **not** present T1 (LexicographicOrder), NAT-sub (NatPartialSubtraction), NAT-cancel (NatAdditionCancellation), NAT-wellorder (NatWellOrdering), or NAT-discrete (NatDiscreteness). Because foundations are declared empty, these citations are ungrounded.
**Issue**: Every proof in TumblerAdd, ActionPoint, and TA-assoc relies on at least one of these five claims. Without them in scope, (i) the result-length identity `(k − 1) + 1 + (n − k) = n` has no justification (NAT-sub); (ii) uniqueness and minimum-value ≥ 1 of the action point are unproven (NAT-wellorder, NAT-discrete); (iii) the dominance sub-case `aₖ > 0` cannot rule out `aₖ + wₖ = wₖ` (NAT-cancel); (iv) the order-theoretic postconditions `a ⊕ w > a` and `a ⊕ w ≥ w` have no definition of `<` on tumblers at all (T1). TA-assoc's statement of `Pos(b ⊕ c)` likewise needs T1 for its own `Pos`-absorption companion — but more fundamentally, no reader can check TumblerAdd's strict-advancement or dominance claims until T1 exists.
**What needs resolving**: Either add the missing claims (T1 LexicographicOrder; NAT-sub, NAT-cancel, NAT-wellorder, NAT-discrete) to this ASN's content so they are in scope for their use-sites, or move them into an external foundation and record them under Foundation Statements / Declared depends. The current state — citations to named claims that exist nowhere in the review package — cannot be discharged.

### TA-Pos notation note disclaims a dependency the ASN actually has
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: TA-Pos, *Note on notation*: "The lexicographic ordering and its prefix rule alluded to here are supplied by claims outside this region and enter no obligation of TA-Pos."
**Issue**: The note disclaims T1 as "outside this region," but TumblerAdd's proof (same ASN) cites T1 case (i) repeatedly and lists T1 in its Depends slot. If the intent is "outside TA-Pos specifically," the phrasing "outside this region" invites the opposite reading — that T1 is external to ASN-0034 altogether. This is cosmetic once T1's placement is resolved under the REVISE finding above, but the disclaimer should be tightened so it doesn't contradict the rest of the ASN.

VERDICT: REVISE
