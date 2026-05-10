# Regional Review — ASN-0034/TA-Pos (cycle 4)

*2026-04-24 03:13*

### NAT-closure body paragraph defends axiom shape rather than advancing reasoning
**Class**: REVISE
**Foundation**: n/a (meta-prose / reviser drift)
**ASN**: NAT-closure body, second paragraph: "The two additive-identity clauses `0 + n = n` and `n + 0 = n` are posited independently because no commutativity axiom on `+` has been introduced at this layer. Left-identity does not imply right-identity without commutativity, so callers appealing to either side must cite the matching clause; positing both sides eliminates the otherwise-needed commutativity premise for what is meant to be a basic identity rewrite."
**Issue**: This paragraph explains *why* the axiom posits both identity clauses (anticipating a would-be derivation from one side under a commutativity premise that has not been introduced). It is essay content about the shape of the contract, matching the "new prose around an axiom [that] explains why the axiom is needed rather than what it says" drift pattern. The sibling NAT-order body does genuine derivational work (at-least-one + irreflexivity + transitivity ⟹ exactly-one); NAT-closure's paragraph here justifies a design choice instead. Prior findings removed structural-choice meta-prose from this claim; the same pattern has reappeared in a new guise.
**What needs resolving**: Either drop the paragraph, or replace it with derivational content (e.g., a Consequence that actually uses the identity clauses, a semantic unpacking of what totality and closure rule out at composition sites). If the non-commutativity observation belongs anywhere, it is in a design note, not the claim body.

### NAT-closure body closes with a use-site framing of `0 < 1`
**Class**: REVISE
**Foundation**: n/a (meta-prose / use-site inventory)
**ASN**: NAT-closure body, final sentence: "Beyond distinctness, `0 < 1` pins `1` strictly above `0` — the strict-above reading callers need when they use `1` as a positive reference rather than merely a second name."
**Issue**: "the strict-above reading callers need when they use `1` as a positive reference" is a use-site justification — it explains which downstream consumer relies on the clause and what they rely on it for. This is the use-site inventory pattern flagged at TA-Pos in prior cycles, relocated to NAT-closure. The preceding half-sentence ("`0 < 1` pins `1` strictly above `0`") already states the mathematical content; the "callers need… when they use…" trailer adds no reasoning and anticipates external consumers that have not been introduced.
**What needs resolving**: End the sentence at "`0 < 1` pins `1` strictly above `0`." — or drop the sentence entirely if the content collapses into the surrounding distinctness discussion.

### NAT-closure's Depends entry for NAT-order understates body use
**Class**: REVISE
**Foundation**: n/a (Depends justification)
**ASN**: NAT-closure Depends: "NAT-order (NatStrictTotalOrder) — supplies the strict-order primitive `<` used in the distinctness clause `0 < 1`." Body: "`0 < 1` entails `0 ≠ 1` against NAT-order's exactly-one trichotomy, which forbids `0 < 1 ∧ 0 = 1`."
**Issue**: The body invokes NAT-order's *exactly-one trichotomy* Consequence (specifically the mutual-exclusion conjunct `¬(m < n ∧ m = n)`) to derive `0 ≠ 1`, but the Depends justification only mentions the `<` primitive from the Axiom slot. A reader auditing whether the body's reasoning is grounded by declared dependencies sees `<` listed and has to infer the Consequence-level use. If the derivation `0 < 1 ⟹ 0 ≠ 1` is load-bearing enough to appear in the body, its source should be declared.
**What needs resolving**: Either extend the NAT-order Depends justification to name the exactly-one trichotomy Consequence (not just `<`), or drop the `0 ≠ 1` sidebar from the body so the body's use of NAT-order is exactly the `<` primitive that the Depends entry already covers.

VERDICT: REVISE
