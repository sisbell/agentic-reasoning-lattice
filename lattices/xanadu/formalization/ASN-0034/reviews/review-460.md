# Regional Review — ASN-0034/NAT-addbound (cycle 3)

*2026-04-24 00:00*

### NAT-addbound opening prose says "three NAT foundations" but declares four
**Class**: REVISE
**Foundation**: n/a (foundation ASN)
**ASN**: NAT-addbound prose — "The fact is derivable from three NAT foundations and recorded as a named theorem…"
**Issue**: The Depends slot of NAT-addbound lists four distinct foundations: NAT-zero, NAT-addcompat, NAT-closure, NAT-order — and the proof walks each one (NAT-zero's minimality clause, NAT-order's `≤` and `≥` definitions, NAT-addcompat's right order compatibility, NAT-closure's left identity). The opening prose count "three" contradicts both the proof it introduces and the Depends list below it. A precise reader who counts dependencies from the prose to cross-check the Depends slot will flag the mismatch, and a reader who cites the theorem downstream will not know which three foundations the prose claims suffice.
**What needs resolving**: Correct the count to match the actual dependency set (four, as declared), or — if the intent is that one of the four is redundant to the proof — remove it from Depends. Either way, the prose count and the Depends cardinality must agree.

### NAT-sub strict monotonicity is derivable; axiom set is non-minimal
**Class**: REVISE
**Foundation**: n/a
**ASN**: NAT-sub axiom — "Strict monotonicity: `m ≥ p ∧ n ≥ p ∧ m < n ⟹ m − p < n − p` for every `m, n, p ∈ ℕ`."
**Issue**: This clause is derivable from other NAT-sub axioms together with NAT-addcompat and NAT-order — the same pattern as the previously-flagged disjointness clause. Assume `m ≥ p`, `n ≥ p`, `m < n`. Right-inverse at `(m, p)` and `(n, p)` gives `(m − p) + p = m` and `(n − p) + p = n`; substituting into `m < n` via indiscernibility of `=` yields `(m − p) + p < (n − p) + p`. Set `a := m − p`, `b := n − p`; by NAT-order's exactly-one trichotomy on `(a, b)`, either `a < b` (the desired conclusion), `a = b` (then `a + p < a + p` against irreflexivity), or `b < a` (then NAT-addcompat's right order compatibility at `b ≤ a` yields `b + p ≤ a + p`, whose two branches collide with `a + p < b + p` via exactly-one trichotomy's `¬(x < y ∧ y < x)` and irreflexivity). So `m − p < n − p` follows from inverse + NAT-addcompat + NAT-order. The axiom is therefore not primitive, and NAT-sub's axiom list is non-minimal in the same way the disjointness finding identified for NAT-order.
**What needs resolving**: Either relocate strict monotonicity from Axiom to Consequence (with a derivation like the one above) and add any needed dependencies to Depends, or justify in prose why the clause must be primitive despite being derivable. As written, the axiom launders the derivation through itself, and downstream consumers cannot tell which NAT-sub facts are truly primitive.

### NAT-discrete Depends bullet uniquely annotates "(this ASN)"
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: NAT-discrete Depends — "NAT-closure (NatArithmeticClosureAndIdentity, this ASN) — posits `1 ∈ ℕ` and closes ℕ under addition…"
**Issue**: Every other Depends entry across all seven claims (NAT-zero, NAT-closure, NAT-addcompat, NAT-order, NAT-sub, NAT-cancel, NAT-addbound) renders dependencies as `NAME (FullName) — …` without a scope annotation. NAT-discrete's single bullet adds ", this ASN" inside the parenthetical — a one-off annotation that does nothing: every NAT-* claim listed in any Depends slot is in this ASN (it is a foundation). The annotation reads as either vestige of an earlier scope-tracking convention or a reviser artifact, and a downstream consumer reading it alongside the other bullets will wonder whether its presence encodes something the other bullets lack.
**What needs resolving**: Remove the ", this ASN" parenthetical to match the rest of the document, or — if the annotation is meaningful — apply the scheme consistently to every Depends entry and state what the scope tag means.

VERDICT: REVISE
