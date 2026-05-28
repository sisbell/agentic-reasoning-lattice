# Review of ASN-0101

## REVISE

### Issue 1: K.σ missing from foundation vocabulary list

**ASN-0101, "The operation" §2**: "DEL accordingly enters the foundation's transition vocabulary as a new elementary transition kind ... extending the foundation's transition vocabulary `{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ}` (ASN-0047, ASN-0093)."

**Problem**: K.σ (DocumentRegistration, ASN-0093) is part of the foundation's vocabulary but absent from this list. D10's extended vocabulary correctly includes K.σ, so the opening list is inconsistent with the ASN's own D10 statement.

**Required**: Add K.σ to the initial vocabulary list.

### Issue 2: Notation overload between span width and link addresses

**ASN-0101, D0**: "a level-uniform V-span `σ = (s, ℓ)`" (here ℓ is the width); "every link `ℓ ∈ dom(L)`" (D9, here ℓ is the link); "with σ = (s, ℓ_σ) of subspace `S`" (D11, disambiguating).

**Problem**: The variable `ℓ` carries two distinct meanings — span width (D0 effect, the worked example "`ℓ = δ(2, 3)`") and link address (D3, D9, D11, the link-example "every chain element `b` of `A_L(d_0)`"). D11 introduces `ℓ_σ` for the width to disambiguate, but D0 and D9 do not adopt this convention. The worked example uses `ℓ_σ` nowhere, and the D9 statement writes `DEL[d, σ]` without separately naming σ's width, leaving the reader to infer from context.

**Required**: Use `ℓ_σ` consistently for span width throughout (D0 onward) and reserve `ℓ` for link addresses, or explicitly note the local convention at each redefinition.

### Issue 3: D11 wp not verified against the worked examples

**ASN-0101, "A worked example"**: The example exhaustively verifies D0, D1, D5, D7, D8, D9 against concrete data. The link and cross-document examples likewise verify D9.

**Problem**: D11 introduces three wp formulas — discoverability from `d`, cross-document discoverability, and projection cardinality — but none is traced through any of the three worked examples. The ASN's own standards-aligned justification ("Postconditions without derived consequences ... is REVISE") suggests at least one wp should be exercised, e.g., compute `wp(DEL[d, σ], Q_disc(ℓ_0, d))` for the worked example's DEL parameters and verify the result against the explicit post-state projection.

**Required**: Add at least one wp verification — e.g., show `project(L(ℓ_0).e_1, d, Σ) ⊄ X` for the content-example slot and conclude `discoverable_from(ℓ_0, d, Σ')` holds; or compute `|project| − |project ∩ X|` and match it against the post-state cardinality.

### Issue 4: D10 out of numerical order in Claims Introduced table

**ASN-0101, "Claims Introduced"**: The table rows appear in the order D0, D1, ..., D9, D11, D10.

**Problem**: D10 is listed after D11, breaking the otherwise ascending order. Readers scanning the table for D10 must hunt past D11.

**Required**: Reorder the final two rows so D10 precedes D11.

### Issue 5: D7 statement uses informal pre-state quantification

**ASN-0101, D7**: "every I-address `a` that appeared in `ran(M(d))` before the operation".

**Problem**: "Appeared ... before" is informal compared to the rest of the formal contracts. The condition is `a ∈ ran(M(d))` at the pre-state `Σ`. The justification uses this precise form, but the statement does not.

**Required**: Replace "appeared in `ran(M(d))` before the operation" with `a ∈ ran(M(d))` at the pre-state `Σ`, matching the formal style of D2–D6.

## OUT_OF_SCOPE

None — the ASN explicitly identifies versioning, link semantics, INSERT, COPY, and BEBE protocols as out of scope, and these align with the prompt's scope restrictions. The Open Questions section appropriately defers cross-operation interactions (DELETE+INSERT reversibility, causal ordering, full historical reconstruction) to future ASNs.

VERDICT: REVISE
