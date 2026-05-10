# Cone Review — ASN-0034/TS3 (cycle 1)

*2026-04-26 10:21*

Reading the ASN as a system — checking precondition chains, definition consistency, and proof completeness across claims.

### Meta-prose in NAT-addassoc body
**Class**: OBSERVE
**ASN**: NAT-addassoc — entire body paragraph "Two primitives appear in the axiom that are not introduced here. The binary operation `+` is the one posited by NAT-closure's signature clause… A single Depends entry on NAT-closure therefore suffices: it grounds `+` directly and `ℕ` transitively, matching the precedent NAT-closure itself sets…"
**Issue**: The body's only paragraph is defensive justification of the Depends list — explaining why one entry suffices and citing precedent — rather than developing the axiom or its consequences. The axiom itself is a one-liner; the prose around it argues for the contract slot rather than advancing reasoning.

### Essay content in NAT-closure body
**Class**: OBSERVE
**ASN**: NAT-closure — "The signature `+ : ℕ × ℕ → ℕ` carries two load-bearing commitments. Its domain `ℕ × ℕ` makes `+` total on the naturals — every pair of naturals has a sum — and its codomain `ℕ` closes the operation under addition…"
**Issue**: This paragraph explains what the signature notation means (totality, closure) — content the precise reader already extracts from `+ : ℕ × ℕ → ℕ` itself. The next paragraph ("The pair `1 ∈ ℕ` and `0 < 1` names a second constant…") similarly restates the axiom. Both are essay content in the body of an axiom claim.

### Defensive prose in NAT-carrier body
**Class**: OBSERVE
**ASN**: NAT-carrier — "The declaration is irreducible at this level: `ℕ` is taken as a primitive — not constructed from a more elementary substrate, not extracted from the meta-language by ambient definability, but committed-to as a set…" and the catalog paragraph "Every Cartesian product `ℕ × ℕ`… every membership `x ∈ ℕ`… and every set-builder `{j ∈ ℕ : ...}` presupposes this primitive commitment."
**Issue**: First paragraph defends the choice to take ℕ as primitive (justifying the absence of a constructive definition); second performs use-site inventory across the rest of the document. Neither advances the claim that ℕ is a set.

### Use-site inventory paragraph in NAT-sub body
**Class**: OBSERVE
**ASN**: NAT-sub — the paragraph beginning "The axiom body invokes symbols beyond ℕ's primitive membership. The strict order `<` together with its non-strict companion `≤` and reverse companions `≥`, `>` — all defined in NAT-order by `m ≤ n ⟺ m < n ∨ m = n`…"
**Issue**: This paragraph itemizes every appearance of `<`, `≤`, `+`, `1` in the axiom body and ties each to its supplier — precisely the work the Depends list already performs. Reads as bookkeeping copied from the contract back into the prose. The strict-monotonicity and strict-positivity derivations preceding it carry the actual content; this paragraph is structural noise the reader skips past.

### TS3 prose imprecision: "transitivity of <" instead of "≤-transitivity"
**Class**: OBSERVE
**ASN**: TS3, in the right-side n₁ + n₂ ≥ 1 derivation: "NAT-order (NatStrictTotalOrder) — defining clause `m ≤ n ⟺ m < n ∨ m = n` and transitivity of `<` compose the chain into `n₁ + n₂ ≥ 1`."
**Issue**: The chain `n₁ + n₂ ≥ 1 + n₂ ≥ 1 + 1 ≥ 1` is a chain of `≤`-statements, so the composing principle is `≤`-transitivity (a Consequence of NAT-order), not transitivity of `<`. The cited NAT-order Consequence does cover this, but the prose names the wrong primitive. Sound, but loose attribution.

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 832s*
