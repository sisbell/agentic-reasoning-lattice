# Regional Review — ASN-0034/TA5-SIG (cycle 1)

*2026-04-24 08:06*

### Defensive meta-prose in NAT-sub about Consequence vs. Axiom placement
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: NAT-sub, the two paragraphs beginning "Strict monotonicity — `m ≥ p ∧ n ≥ p ∧ m < n ⟹ m − p < n − p` — is exported as a *Consequence:* rather than an additional axiom clause, because its content derives from..." and "Strict positivity — `m > n ⟹ m − n ≥ 1` — is exported as a *Consequence:* rather than an additional axiom clause, because its content is not purely subtractive..."
**Issue**: Both paragraphs open by justifying the placement of the fact within the Formal Contract structure (Consequence vs. Axiom), citing axiom-minimality discipline and cross-referencing how NAT-order chose to export `¬(m < n ∧ m = n)`. This is architectural meta-commentary about the contract slots, not claim content. The justification is reasonable but competes with the actual derivation that follows; a reader tracking the mathematical argument must skip past it to reach the proof. The derivations themselves are sound and walked in full — the issue is strictly the framing.

### NAT-addbound opens with a use-site inventory
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: NAT-addbound, first paragraph: "The two facts are derivable from four NAT foundations and recorded jointly as a named theorem so that NAT-sub's right-telescoping clause `(m + n) − n = m` can discharge the implicit precondition `m + n ≥ n`, and its left-telescoping clause `(n + m) − n = m` can discharge the implicit precondition `n + m ≥ n`..."
**Issue**: The opening paragraph explains why NAT-addbound exists in terms of a specific downstream consumer (NAT-sub's telescoping clauses) rather than stating what the claim asserts. The reader arrives expecting right/left dominance and is instead handed the consumer's perspective. The claim statement itself — one sentence at the top — already makes the content clear; the use-site framing belongs, if anywhere, in NAT-sub's Depends annotation (which already carries it).

### TA5-SIG uses `1` as a literal without citing NAT-closure in Depends
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: TA5-SIG Depends list (T0, NAT-wellorder, NAT-order, NAT-discrete, NAT-sub, NAT-addcompat) and prose use of `1` throughout the `max(S)` derivation ("we have `1 ≤ i₀`", "hence `m ≥ 1`", "conditional closure at `m ≥ 1` supplies `m − 1 ∈ ℕ`", etc.)
**Issue**: The literal `1` is posited in NAT-closure (`1 ∈ ℕ`), which TA5-SIG invokes by name throughout its derivation. NAT-closure is available transitively through NAT-discrete / NAT-sub / NAT-addcompat, but other Depends entries in this very ASN (e.g., NAT-discrete's entry explicitly citing NAT-closure "because `m + 1 ∈ ℕ`") follow a stricter convention of citing the source whose axiom supplies a symbol used by name. The omission is soft — no derivation step breaks — but it departs from the citation discipline observed in its peer claims.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 393s*
