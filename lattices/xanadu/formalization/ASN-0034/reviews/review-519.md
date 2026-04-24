# Regional Review — ASN-0034/TA-Pos (cycle 2)

*2026-04-24 11:27*

### Body prose for NAT-order contains a use-site justification for why `≤`-transitivity is exported
**Class**: REVISE
**Foundation**: (foundation ASN; internal)
**ASN**: NAT-order body — "We export `≤`-transitivity as a Consequence so consumers can chain non-strict bounds without re-deriving the case split."
**Issue**: This sentence is a defensive justification for the export — it tells the reader *why* the Consequence slot is populated rather than carrying any step of the derivation. The Consequence slot already signals "exported for downstream", so re-stating that consumers can use it is noise in a structural slot. This is the reviser-drift pattern the rubric calls out: prose around a claim explaining why the claim is exported rather than advancing its derivation. A precise reader has to skip past this line to follow the case-split argument that actually establishes `≤`-transitivity.
**What needs resolving**: Drop the sentence. The case split already establishes the Consequence; the export intent is carried by the bullet's structural position.

### T0 extensionality Axiom has an untyped inner bound variable while peer quantifiers in the ASN type theirs
**Class**: OBSERVE
**Foundation**: (foundation ASN; internal)
**ASN**: T0 Axiom — "Extensionality: `(A a, b ∈ T : #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ) : a = b)`"
**Issue**: The inner quantifier `(A i : 1 ≤ i ≤ #a : ...)` omits the `i ∈ ℕ` typing that other formal quantifiers in this ASN carry explicitly (e.g., T0's own prose writes `i ∈ {j ∈ ℕ : 1 ≤ j ≤ #a}`; TA-Pos uses `(E i ∈ ℕ : 1 ≤ i ≤ #t : ...)`; NAT-order uses `(A m, n ∈ ℕ :: ...)`). The typing is recoverable from the surrounding predicates, so soundness is not at stake — but the stylistic drift forces a precise reader to reconstruct what the peer quantifiers state directly.

### NAT-closure prose expands the signature and the `1`/`0 < 1` pair but is silent on the identity clauses
**Class**: OBSERVE
**Foundation**: (foundation ASN; internal)
**ASN**: NAT-closure body — the prose has a paragraph unpacking `+ : ℕ × ℕ → ℕ` into "totality" and "closure", and a sentence unpacking `1 ∈ ℕ ∧ 0 < 1` as "names a second constant ... locates it in the strict order", but the two-sided identity clauses `0 + n = n` and `n + 0 = n` receive no prose treatment.
**Issue**: Lopsided coverage. Either every axiom clause gets a one-sentence unpacking or none do. As written, the reader is prompted to ask "why these two commitments, not the other two?" — which is not the question the prose should be provoking. Soundness is untouched; this is presentation only.

VERDICT: REVISE
