# Review of ASN-0042

## REVISE

### Issue 1: O1b preservation by delegation is unstated
**ASN-0042, Ownership as a Structural Predicate / Delegation**: O1b (PrefixInjectivity) is load-bearing — O2's well-definedness depends on it. Delegation is the only operation that introduces new principals, yet the ASN never shows that delegation preserves O1b.
**Problem**: The `delegated` definition's conditions (i) and (ii) *do* prevent prefix collision, but the argument is not made. Specifically: if `pfx(π') = pfx(π''')` for some existing `π''' ∈ Π_Σ`, then `pfx(π''') ≼ pfx(π')`, so by condition (ii), `#pfx(π''') ≤ #pfx(π)`. But from condition (i), `pfx(π) ≺ pfx(π')`, giving `#pfx(π) < #pfx(π') = #pfx(π''')`. Contradiction. This argument exists but is nowhere in the ASN.
**Required**: State explicitly that delegation preserves O1b, and give the argument. This closes the proof chain from delegation through O1b to O2's well-definedness.

### Issue 2: O2 well-definedness — linear ordering of covering prefixes is a parenthetical
**ASN-0042, The Exclusivity Invariant**: "(ii) any two containing prefixes are linearly ordered by the prefix relation (if `p₁ ≼ a` and `p₂ ≼ a`, either `p₁ ≼ p₂` or `p₂ ≼ p₁` — because both are prefixes of the same tumbler, and the prefix relation on a single path in the tree is total)"
**Problem**: This is the well-definedness argument for `ω` — the central definition of the entire ASN. The proof is a parenthetical remark. The ASN elsewhere expands multi-step arguments (O3's proof gets four sentences; O4's derivation gets a full paragraph; O8's argument is laid out step by step). The linear ordering claim requires: (1) WLOG `#p₁ ≤ #p₂`; (2) for `i ≤ #p₁`, `p₁ᵢ = aᵢ` and `p₂ᵢ = aᵢ`, hence `p₁ᵢ = p₂ᵢ`; (3) therefore `p₁ ≼ p₂`. These steps are simple but the claim is load-bearing — it is what makes longest-match well-defined.
**Required**: Expand the parenthetical into a short explicit argument showing the three steps. The claim is correct; the proof depth should match its centrality.

### Issue 3: Corollary cites O5 for delegation authorization
**ASN-0042, Permanence and Refinement (Corollary)**: "by O5, only the effective owner of a domain may allocate or delegate within it"
**Problem**: O5 is formally stated for allocation only: "Only the principal with the longest matching prefix may allocate new addresses within its domain." Delegation authorization lives in the `delegated` definition's condition (ii): "π is the most-specific covering principal for `pfx(π')` at the time of delegation." The Corollary's argument is correct in substance — both O5 and condition (ii) enforce the same most-specific-covering-principal constraint — but it cites only O5 and extends it to delegation without justification.
**Required**: Either (a) cite both O5 (for allocation) and the `delegated` definition's condition (ii) (for delegation), or (b) state explicitly that O5's subdivision authority principle extends to delegation via condition (ii), then cite that extension in the Corollary.

### Issue 4: O6 derived property — `pfx(ω(a)) ≼ acct(a)` proof skips intermediate steps
**ASN-0042, Structural Provenance**: "Since `zeros(pfx(ω(a))) ≤ 1` (O1a), all components of `pfx(ω(a))` fall within the node-and-user portion of `a`, which is `acct(a)`; hence `pfx(ω(a)) ≼ acct(a)`."
**Problem**: The step from "zeros ≤ 1" to "falls within the node-and-user portion" is a multi-step argument presented as a single inference. The missing chain: (1) by T4, a valid tumbler with `zeros ≤ 1` has at most node and user fields — no document or element components; (2) since `pfx(ω(a)) ≼ a`, the prefix's components match `a`'s leading components; (3) those leading components, being confined to node + user fields by (1), are exactly the components captured by `acct(a)`; (4) hence `#pfx(ω(a)) ≤ #acct(a)` and `pfx(ω(a)) ≼ acct(a)`. The same implicit step appears in the main O6 proof ("the prefix `pfx(π)` sits within the node-and-user portion of the address").
**Required**: Show why `zeros ≤ 1` implies the prefix cannot extend past the user field boundary, and why this makes it a prefix of `acct(a)`. The argument uses T4's field structure and should cite it explicitly.

## OUT_OF_SCOPE

No items. The ASN's scope section and open questions are comprehensive. The topics that might otherwise be flagged — delegation mechanism, cross-node federation, ownership transfer, principal lifecycle — are either explicitly excluded by the scope section or already recorded as open questions.

VERDICT: REVISE
