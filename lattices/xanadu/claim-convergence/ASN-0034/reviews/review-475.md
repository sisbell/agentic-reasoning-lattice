# Regional Review — ASN-0034/TA-Pos (cycle 2)

*2026-04-24 02:52*

Reading the full ASN and cross-checking against the flagged patterns and new structural issues.

### "A separate consequence" prose but no corresponding Consequence bullet
**Class**: REVISE
**Foundation**: n/a (structural)
**ASN**: TA-Pos, body prose: "A separate consequence concerns the content of the partition: T0's clause `(A a ∈ T :: 1 ≤ #a)` guarantees that every `t ∈ T` has at least one index in range, so `Pos(t)` exhibits a nonzero component and `Zero(t)` makes every component equal to `0`."
**Issue**: The prose explicitly labels this material "a separate consequence" (distinct from the `Pos(t) ⟺ ¬Zero(t)` equivalence), but the formal contract has a single `*Consequence:*` bullet — the equivalence. Either the partition-content claim is an exportable consequence that belongs in the contract, or it is merely an unpacking of the Definition slot and the word "consequence" in the prose is misleading. As written, a reader chasing exports of TA-Pos cannot tell which it is, and the contract–prose disagreement is a structural inconsistency of the kind this review exists to catch.
**What needs resolving**: Either promote the partition-content fact to a second `*Consequence:*` bullet (stated precisely — e.g., `Pos(t) ⟹ (E i ∈ ℕ : 1 ≤ i ≤ #t : ¬(tᵢ = 0))` witness-existence, which does require T0's nonemptiness), or drop the "a separate consequence concerns" framing and treat the sentence as a reading of the Definition.

### Meta-prose relocated into the Depends slot
**Class**: REVISE
**Foundation**: n/a (meta-prose)
**ASN**: NAT-order, Depends slot: "(none). NAT-order is the root of the NAT foundation: the strict-order primitive `<` is posited directly on ℕ by the axiom's first clause, not derived from an earlier axiom, and the non-strict companion `≤` together with the reverse companions `≥` and `>` are defined using only `<` and logical equality."
**Issue**: The previous review removed "axiom slot introduces X before constraining it" meta-prose from NAT-order's body. Equivalent scaffolding has reappeared inside the Depends slot — a prose defense of why the Depends list is empty and a restatement of which slot introduces which symbol. This is the same reviser-drift pattern (essay content about structural choices, defensive justification of a contract shape) displaced one slot over rather than removed. Compounds across cycles if not flagged at source.
**What needs resolving**: Reduce the Depends slot to `(none)`. If the absence of dependencies needs justification, that justification belongs in a commit message or design note, not in the contract.

### Residual slot signposting in NAT-order body
**Class**: REVISE
**Foundation**: n/a (meta-prose)
**ASN**: NAT-order body: "The three clauses jointly export *exactly-one trichotomy* as a Consequence: for any `m, n ∈ ℕ`, exactly one of `m < n`, `m = n`, `n < m` holds." And later: "…a consumer wanting the implicational form unfolds it from the exactly-one trichotomy bullet at the point of use."
**Issue**: "export … as a Consequence" and "the exactly-one trichotomy bullet" are the body prose referring to the contract's slot structure — the same pattern the previous review flagged under "Meta-prose about structural slot choices." The mathematical content ("exactly one of … holds") stands on its own without a signpost to the slot that carries it, and readers do not need a pointer to "the bullet" to unfold `¬(A ∧ B) ⟺ (A ⟹ ¬B)`.
**What needs resolving**: State the exactly-one trichotomy directly without the "export … as a Consequence" framing, and drop the closing sentence that directs the consumer to "the bullet at the point of use."

### Notation note relies on undefined lex ordering to make a concrete claim
**Class**: REVISE
**Foundation**: n/a (forward reference)
**ASN**: TA-Pos, "Note on notation": "the length-1 tumbler `0` is a proper prefix of the length-2 tumbler `0.0`, and under the prefix rule of that ordering `0 < 0.0`, so `0.0 > 0` even though `Zero(0.0)` holds. … The lexicographic ordering and its prefix rule alluded to here are supplied by claims outside this region and enter no obligation of TA-Pos."
**Issue**: The note asserts a specific ordering fact (`0 < 0.0` under a prefix rule) to justify a notation choice, but neither the ordering nor the prefix rule is in scope — the disclaimer acknowledges this. A reader cannot verify the asserted fact from anything TA-Pos or the NAT foundation supplies, so the motivating example is effectively a promissory note. The purpose the note serves — warning against writing `Pos(t)` as `t > 0` — can be achieved without committing to a specific counterexample in undefined machinery.
**What needs resolving**: Either state the warning generically ("`>` is reserved for a separate tumbler ordering under which zero tumblers need not all be minimal; writing `Pos(t)` as `t > 0` would conflate the two relations"), or defer the note entirely until the lex ordering is in scope and the counterexample can be cited by claim label.

VERDICT: REVISE
