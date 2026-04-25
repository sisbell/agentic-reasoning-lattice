# Regional Review — ASN-0034/T1 (cycle 1)

*2026-04-23 17:18*

Reading the eight claims shown (T0, T3, NAT-order, NAT-addcompat, NAT-cancel, NAT-discrete, NAT-wellorder, T1) against the four prior cycles of findings.

### Dependency-justification prose across foundation claims
**Class**: OBSERVE
**Foundation**: N/A (pattern spans the ASN's NAT-foundation tier)
**ASN**: T0, NAT-order, NAT-addcompat, NAT-cancel, NAT-discrete, NAT-wellorder each carry a paragraph whose job is to justify *why* the Depends slot lists what it lists, rather than to state or motivate the axiom content. Examples:
- NAT-addcompat: "The left/right compatibility clauses invoke the non-strict `≤` *defined* in NAT-order ... Both foundations are declared in the Depends slot so that the axiom body can be read without silently importing them."
- NAT-discrete: "The axiom body invokes two symbols beyond ℕ's primitive `<` and `=` ... Both are declared in the Depends slot so that the axiom body can be read without silently importing foundations."
- NAT-wellorder: "NAT-order is therefore declared in the Depends slot so that the axiom body can be read without silently importing the definition."
- NAT-cancel: the two-paragraph "Two primitives appear in these clauses that are not introduced here ... NAT-closure and NAT-zero are therefore both declared in the Depends slot; NAT-zero is named directly rather than reached transitively" is a use-site inventory of the Depends contents.
- T0: "The numeral `1` bounding the length from below is the `1 ∈ ℕ` posited by NAT-closure; the relation `≤` is the non-strict order on ℕ defined by NAT-order."

This matches the "new prose around an axiom explains why the axiom is needed rather than what it says" pattern in the review guidance. The Depends slot is the canonical place for this information; mirroring it in prose duplicates the contract in a looser register and displaces content about the axiom itself. Previous cycles flagged individual Depends omissions and miscitations but did not name the systemic prose pattern.

### NAT-cancel independence paragraph argues more than it shows
**Class**: OBSERVE
**ASN**: NAT-cancel: "Each of these three clauses is independent of the remaining NAT-* axioms of this ASN. Left and right cancellation are independent of each other because the NAT-* axioms do not include commutativity of addition on ℕ — without `m + n = n + m`, neither cancellation form is derivable from the other."
**Issue**: Asserting independence is a model-theoretic claim (exhibit a model satisfying all-but-one axiom). The paragraph only observes that the most obvious derivation route (go through commutativity) is unavailable. The conclusion happens to be correct for this axiom set, but the argument given discharges only one direction of derivability, not independence. This is defensive justification in prose — if the clause set is minimal, the Depends-level rationale plus the posited mirror-form theorem (which *is* derived, explicitly) already carries the discrimination; the independence paragraph reaches past what it can support.

### NAT-cancel summand-absorption posited form phrased asymmetrically from narrative
**Class**: OBSERVE
**ASN**: NAT-cancel Axiom lists only `m + n = m : n = 0` (standard form). Narrative then says the mirror form is omitted "because it is a theorem of the three clauses above together with NAT-closure," and supplies the derivation through `n + m = 0 + m` and right cancellation at `p := 0`.
**Issue**: The asymmetry is correctly tied to NAT-closure's left-identity-only posit. But the phrase "the three clauses above" names left cancellation, right cancellation, and *standard* summand absorption as the contributors — only right cancellation plus NAT-closure's left identity are actually used; left cancellation and standard absorption do not participate in the mirror-form derivation. The narrative overcounts the clauses that carry the theorem.

### T1 Case 3 trichotomy step is a re-derivation of the branch already under examination
**Class**: OBSERVE
**ASN**: T1 proof, part (b) Case 3: "Both clauses force `m ≠ n` ... So `a ≠ b` by T3. NAT-order's trichotomy at `(m, n)` resolves `m ≠ n` into `m < n ∨ n < m`. If `m < n`, then `k = m + 1 ≤ n` ..."
**Issue**: Clause (β) *already* supplied `m + 1 ≤ n` and thereby `m < n`; clause (γ) *already* supplied `n + 1 ≤ m` and thereby `n < m`. The trichotomy step folds the two sub-branches into a disjunction and then the "if `m < n`" / "if `n < m`" re-casing re-separates them. The argument works; the phrasing loops through trichotomy where a direct "under (β), `m < n`; under (γ), `n < m`" would read straight. (Related to a cycle-1 OBSERVE on the same step, but that entry framed the redundancy as "merges and re-derives"; the specific issue is that `m ≠ n` never needs synthesis because (β)/(γ) supply the stronger asymmetric facts directly.)

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 229s*
