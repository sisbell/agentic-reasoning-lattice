# Review of ASN-0111

## REVISE

### Issue 1: wp derivation reasons from a prose postcondition whose well-formedness is asserted, not exhibited
**ASN-0111, "Deriving the read" (RL0 derivation)**: "Reasoning backward from the postcondition 'the result is the recorded relationship at a' — a postcondition that does not dereference `Σ.L` off its domain — the weakest precondition is precisely membership … Both postconditions are well-formed on every state"
**Problem**: The success postcondition is an English phrase, and on states with `a ∉ dom(Σ.L)` the phrase "the recorded relationship at `a`" denotes `Σ.L(a)` — a dereference of a partial function off its domain, exactly what the parenthetical claims it avoids. The guard that makes the postcondition well-formed everywhere is asserted in the parenthetical but never written down, so the load-bearing claim "Both postconditions are well-formed on every state" is asserted rather than established. The surrounding ASNs (e.g., LP12a's wp, the foundations' contracts) state wp postconditions as formulas; this one is the only step in the section that cannot be checked by substitution as written.
**Required**: State the success postcondition as the guarded formula `a ∈ dom(Σ.L) ∧ result = Σ.L(a)` (and dually `result = ⊥`). The wp computation then becomes a one-line substitution of `result := readlink(a, Σ)`, and well-formedness on every state is discharged by the guard rather than by the parenthetical.

### Issue 2: RL5 carries a defensive parenthetical that re-litigates its relation to RL0 instead of advancing the claim
**ASN-0111, RL5, failure-branch paragraph**: "(RL0's 'a failed screen guarantees `⊥` without an invocation' is the per-state instance of this; the permanence asserted here is the new content, obtained by quantifying that per-state fact over every reachable `Σ'`.)"
**Problem**: The sentence immediately preceding already carries the entire derivation — "the invariants behind RL0's necessity claims … hold at every reachable state — so a screen-failing `a` satisfies `a ∉ dom(Σ'.L)` throughout the future." The parenthetical adds no inferential step; it explains why the claim is not redundant with RL0. That is prose addressed to a reviewer anticipating a duplication finding, the anti-bloat pattern of explaining why content is needed rather than what it says. A reader following the permanence argument must skip past it.
**Required**: Delete the parenthetical. The quantification over reachable `Σ'` is already explicit in the derivation sentence.

### Issue 3: RL4 closes with a forward-reference inventory of what the worked read does and does not prove
**ASN-0111, RL4, final parenthetical**: "(The worked read below instantiates this address scaffolding — `a' = inc(a, 0)` and `c = inc(a', 0)` on `d₁`'s link sub-allocator — and verifies the unflattened-disclosure corollary at a single state; it does not exhibit the two-state witness.)"
**Problem**: This is a use-site inventory of a downstream section — it catalogs what a later part of the document will and will not demonstrate, advancing no claim in RL4 itself. The two-state witness is fully exhibited in RL4's own paragraph, so the caveat "it does not exhibit the two-state witness" protects nothing; and the worked read's "A nested instance (RL4)" paragraph already states on its own behalf what it verifies ("This verifies RL4 against a concrete link→link target"). This is the deferral/inventory meta-prose pattern that accumulates across cycles.
**Required**: Delete the parenthetical. If the single-state-versus-two-state distinction must be recorded anywhere, the worked read's nested-instance paragraph is its home — and that paragraph already characterises itself correctly.

## OUT_OF_SCOPE

### Topic 1: Guarantees connecting a read to endset resolvability and link identity
**Why out of scope**: The three Open Questions (validity conclusions from a read alone, FOLLOWLINK's empty-versus-unwitnessed distinction, reader-side distinguishability of value-identical links) are correctly posed as future work — FOLLOWLINK and identity-disclosure machinery belong to their own ASNs, and ASN-0111 makes no claims about them. No finding.

The technical core is in good shape: RL0's screen evaluability argument (left-to-right guard discharge via T4a/T4b, with the `[1, 0, 0, 2, 0, 3]` non-example) checks out; the RL4 branched-history witness is constructed in full — the bootstrap scaffold `inc([1], 2) = [1.0.1]`, `inc([1.0.1], 2) = [1.0.1.0.1]` satisfies K.δ's per-case preconditions and TA5a's zero-count bounds, both K.λ branches are enabled at the same frontier with identical state-dependent conjuncts, and the second step allocates the same `c` in both branches; RL5's two permanent-absence families verify (the depth witness `[1.0.1.0.1.0.2.1.1]` passes all four screen conjuncts yet lies off every `A_L(d)` chain by the `#E = 2` induction via TA5(c)/TA5-SigValid; the lineage witness fails NodeLineage through two P8 applications); and the worked read's interval decomposition `[…1.1, …1.3) = subtree(…1.1) ∪ subtree(…1.2)` is exactly right by PrefixSpanCoverage at the two unit-depth spans. The three issues above are precision and accretion repairs, not structural defects.

VERDICT: REVISE
