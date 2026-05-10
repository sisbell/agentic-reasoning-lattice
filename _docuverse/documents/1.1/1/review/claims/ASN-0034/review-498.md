# Regional Review — ASN-0034/T10 (cycle 1)

*2026-04-24 06:48*

### Meta-prose in T3 statement
**Class**: REVISE
**Foundation**: T3 (CanonicalRepresentation)
**ASN**: T3 prose block beginning "Gregory's implementation achieves T3 through a normalization routine (`tumblerjustify`)..." through "...the system might allocate a 'new' address that is actually an alias for an existing one."
**Issue**: Two full paragraphs introduce implementation machinery (`tumblerjustify`, `iszerotumbler`, mantissa/exponent structure) that is not in T0's carrier (finite sequences over ℕ) and plays no role in the proof that follows. The surrounding content — "Gregory's analysis reveals what happens when T3 is violated," "T3 matters because address identity is load-bearing" — is essay content explaining why the axiom is needed rather than what it says, and the "mantissa = [0, 0, 5, ...]" counterexample reasons about a structure the formal model does not admit. This is the reviser-drift pattern: new prose around an axiom explaining motivation rather than the claim.
**What needs resolving**: Either remove the Gregory/address-identity motivational block from T3's statement or relocate it; T3's statement should carry only what T3 claims and its proof dependencies.

### `≤`-transitivity cited but not axiomatized
**Class**: REVISE
**Foundation**: NAT-order (NatStrictTotalOrder); T10 (PartitionIndependence)
**ASN**: T10 proof: "with `k ≤ m` and NAT-order transitivity, `k ≤ #a`" and "with `k ≤ n` and transitivity, `k ≤ #b`"; T10 *Depends* line "NAT-order (NatStrictTotalOrder) — trichotomy and transitivity of `≤` on ℕ."
**Issue**: NAT-order's Axiom axiomatizes transitivity of `<`, not `≤`. `≤` is only introduced by a Definition clause `m ≤ n ⟺ m < n ∨ m = n`. The proof invokes `≤`-transitivity (chaining `k ≤ m` with `m ≤ #a` to get `k ≤ #a`) as if it were an axiom of NAT-order. A precise reader must derive it by case analysis on the `≤`-definition plus `<`-transitivity and indiscernibility of `=`. Either NAT-order should record `≤`-transitivity as a Consequence (with derivation) or T10's Depends must name the actual primitives it uses.
**What needs resolving**: Close the gap between what NAT-order exports and what T10 cites — either add a `≤`-transitivity Consequence to NAT-order or re-route the citation through the primitives actually in NAT-order's contract.

### Nelson citations appended after T10's formal contract
**Class**: OBSERVE
**Foundation**: T10 (PartitionIndependence)
**ASN**: Paragraphs beginning `Nelson: "The owner of a given item..."` and `Nelson: "Whoever owns a specific node..."` positioned after T10's *Depends* block.
**Issue**: Two Nelson quotations and a gloss on "baptism" sit after the Formal Contract closes. They do not feed the proof or any downstream dependency; they supply domain motivation that belongs in a prose/framing slot, not trailing the contract. This is structural — the quotations themselves are accurate to the source.

### Unused `+` operator in NAT-closure
**Class**: OBSERVE
**Foundation**: NAT-closure (NatArithmeticClosureAndIdentity)
**ASN**: NAT-closure Axiom `+ : ℕ × ℕ → ℕ` together with `(A n ∈ ℕ :: 0 + n = n)` and `(A n ∈ ℕ :: n + 0 = n)`.
**Issue**: No claim in this ASN uses `+` or either additive-identity clause; T0's only draw on NAT-closure is `1 ∈ ℕ`. The additive structure is declared but idle within the ASN's closure. This is acceptable for a foundation ASN but worth noting — the carrying weight of the claim is concentrated in `1 ∈ ℕ` and `0 < 1`, and a future reader may wonder which dependents rely on `+`.

VERDICT: REVISE
