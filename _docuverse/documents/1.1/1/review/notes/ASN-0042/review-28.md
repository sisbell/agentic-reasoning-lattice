# Review of ASN-0042

## REVISE

### Issue 1: O10 proof uses incorrect baptism granularity

**ASN-0042, O10 (DenialAsFork) proof**: "the constructed `a'` extends `pfx(π)` by several components and a single baptism step extends a tumbler by one component" and "k equals `#a' - #pfx(π)`, which is `6` for the `zeros(pfx(π)) = 0` construction and `4` for the `zeros(pfx(π)) = 1` construction"

**Problem**: ASN-0040's baptism mechanism extends a tumbler by 0 (sibling via `inc(·, 0)`) or `d ∈ {1, 2}` components per baptism (child via `inc(·, d)`). Single-component extensions don't exist. Worse, the implied intermediates like `pfx(π).0` or `pfx(π).0.u.0` are not valid T4 tumblers (trailing zero), so baptism cannot produce them.

**Required**: Restate the trajectory using actual baptism operations. For the `zeros(pfx(π)) = 0` construction, the chain is (i) baptize siblings in `S(pfx(π), 2)` via `inc(pfx(π), 2)` and then `inc(·, 0)` until reaching `pfx(π).0.u`, then (ii) `inc(pfx(π).0.u, 2)`, then (iii) `inc(pfx(π).0.u.0.1, 2)`. The k-count is wrong as stated.

### Issue 2: O10 glosses over sub-delegate coordination

**ASN-0042, O10 proof**: "At each step `Σ_j → Σ_{j+1}` the intermediate target `b_{j+1}` lies within `dom(π)` ... and is not covered by any sub-delegate of `π`"

**Problem**: For `zeros(pfx(π)) = 0` and `u > 1`, `next(B, pfx(π), 2)` returns the lowest un-baptized sibling, e.g. `pfx(π).0.1`. If `1 ∈ S` (some sub-delegate has prefix `pfx(π).0.1`), then `π` is *not* the most-specific covering principal for this intermediate; by O5, `π` cannot baptize it. The baptism stream's high-water-mark advances past these positions only when sub-delegates baptize their own prefixes. The proof asserts "no sub-delegate covers any extension" but the Form-A/Form-B analysis only excludes coverage of `a'` itself, not of intermediates `pfx(π).0.k` for `k ∈ S`.

**Required**: Either argue that the existence quantifier `Σ →⁺ Σ'` permits including sub-delegate baptisms in the transition sequence (and show this resolves the stream advancement), or weaken the postcondition to "in some Σ' where sub-delegates have baptized their prefixes".

### Issue 3: Citation error — Prefix relation conflated with T5

**ASN-0042, "Domains nest" proof**: "Suppose `a ∈ dom(π₂)`, so `pfx(π₂) ≼ a`: by T5 (ContiguousSubtrees) of ASN-0034, this expands to `#a ≥ #pfx(π₂)` and `pfx(π₂)ⱼ = aⱼ`..."

**Also in O7 proof**: "the Covering-chain lemma (cited). O2 (OwnershipExclusivity)'s proof — which uses the Prefix (PrefixRelation) definition together with T5 (ContiguousSubtrees) — establishes that any two tumbler prefixes of the same address are linearly ordered..."

**Problem**: The componentwise expansion of `≼` is the *definition* supplied by Prefix (PrefixRelation), not T5. T5 (ContiguousSubtrees) is about lexicographic contiguity of prefix-defined intervals — a distinct property unused in these derivations. The covering-chain lemma needs only Prefix's definition.

**Required**: Replace these T5 citations with Prefix (PrefixRelation). Reserve T5 for the "dom(π) is a contiguous interval under T1" claim where it actually applies.

### Issue 4: AccountLevelPermanence★ "chain begins with π" claim not formally proven

**ASN-0042, AccountLevelPermanence corollary remark**: "the only way for the chain to start consistently is for `π` itself to be the first delegator ... Hence the first delegator in any chain of `dom(π)`-internal changes is `π`"

**Problem**: This strengthens the formal corollary (which only proves `pfx(π) ≼ pfx(π_d^{(i)})` per transition) to claim the chain *originates* at π. The backward-induction argument is sketched but uses an unstated termination property (chain is finite because |Π_Σ| < ∞ by FiniteRegistry). The required ingredients (O14 non-nesting forbidding pfx(π) ≼ pfx(π_A) for distinct π, π_A ∈ Π₀; chain finiteness via FiniteRegistry) are present in the ASN but not assembled.

**Required**: Either prove this as a formal sub-corollary (assemble the argument from O14 non-nesting + FiniteRegistry + iterated application of condition (ii) backward through the delegation chain), or remove the assertion and let the formal corollary stand alone.

### Issue 5: Reachability assumption used but not stated

**ASN-0042, O3 proof**: "Iterated O12 (PrincipalPersistence) gives `Π₀ ⊆ Π_Σ`; combined with `π' ∉ Π_Σ`, the bootstrap case is excluded."

**Problem**: Iterated O12 to obtain `Π₀ ⊆ Π_Σ` requires Σ reachable from Σ₀. O3's preconditions list only `a ∈ Σ.B, Σ → Σ', ω_{Σ'}(a) ≠ ω_Σ(a)` — reachability is not explicit. The same implicit assumption appears in O8's proof and the AccountLevelPermanence proofs ("`π ∈ Π_Σ` presumes `Σ` arose by some — possibly empty — transition sequence from `Σ₀`" is stated only in passing).

**Required**: Add "Σ reachable from Σ₀" to the preconditions of O3, O8, and AccountLevelPermanence, or state once globally that all state-quantified claims range over reachable states.

## OUT_OF_SCOPE

None — the ASN correctly cordons off authentication (O11), transfer (open questions), baptism mechanism (referenced via ASN-0040), and content modification rights.

VERDICT: REVISE
