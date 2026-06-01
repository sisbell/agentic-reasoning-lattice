# Review of ASN-0086

## REVISE

### Issue 1: A_K computability leans on a mis-cited decidability of coverage-equality

**ASN-0086, "The Typed Relation" / "The Active Subset"**: "We require only that type-equality is decidable by endset comparison — which it is, by L8 (TypeByAddress)." and later "`A_K^Σ` is computable from `Σ.L` alone: `L_K^Σ` is a slice of `Σ.L`, and `nullified(Σ)` is a finite, computable set."

**Problem**: L8 (TypeByAddress, ASN-0043) establishes that `same_type` is *determined by* coverage equality and is an equivalence relation; it does **not** establish that coverage-set-equality is *decidable*. The note's computability argument is rigorous for `nullified(Σ)` — it reduces membership to per-address `s ≤ a < s ⊕ ℓ` tests decidable by T2 over a finite domain. But the defining test for the slice `L_K^Σ` itself, `coverage(Σ.L(a).e₃) = coverage(K)`, is a *set-equality* of two finite unions of half-open T1-intervals, and this is asserted ("a slice of `Σ.L`") rather than reduced to decidable primitives. `Observe_K` with `View = oper` returns a subset of `A_K^Σ`, so the slice must be computed — the asymmetry between the carefully-derived `nullified` decidability and the asserted `L_K` decidability is a real gap.

**Required**: Derive decidability of coverage-set-equality (finite unions of half-open T1-intervals, compared via T2), or cite the actual basis. Do not lean on L8, which speaks only to the equivalence relation, not to decidability.

### Issue 2: R7a's full ↝-decomposition generality is unused by its only cited consumer

**ASN-0086, reduction corollary (end of "Three Operations")**: "R7a is the general decomposition lemma — it covers layers that publish composites touching `Σ.L` across several K-steps; the relational layer is its degenerate instance, since `Emit_K`, and its alias `Nullify`, is a single K.λ `→`-step ... so R7a's decomposition collapses to the one-step sequence (`m = 1`)."

**Problem**: The relational layer is *defined* (Definition — relational layer) to publish only `{Emit_K, Observe_K, Nullify}`, where `Emit_K` is a single K.λ step and `Observe_K` is read-only. The reduction "to `{Emit_K}`" therefore follows directly from the layer's own definition; none of R7a's machinery — the K.σ-interleaving, discharges (1)–(4), the at-most-one-key-per-home routing — is exercised by the corollary, which immediately collapses it to `m = 1`. The heavyweight general statement is proved for hypothetical composite-publishing layers that this ASN never instantiates.

**Required**: Either present R7a (NoExtraClassAffectsL) as a standalone substrate closure theorem with motivation independent of the reduction (its name suggests it is intended as one), or trim it to what the reduction actually consumes. As written, the corollary over-claims R7a's role.

### Issue 3: R0a proof states the same premise-inventory fact twice

**ASN-0086, R0a proof**: opening — "Case 1 (cross-home) uses only L1 + L1a — a zero-counting argument over the NUDE-prefix `home` projection, with no appeal to chain machinery"; then Case 1 body — "We show this case directly from L1's element-level constraint plus L1a's NUDE-prefix `home` projection — no chain machinery is required."

**Problem**: The proof opening's premise-set inventory and the first sentence of Case 1 assert the identical fact ("Case 1 needs only L1 + L1a, no chain machinery") in two places. This is the duplicated-prose pattern the note's anti-bloat classifier targets ("two paragraphs ... say the same thing in different words"); the inventory is meta-commentary the reader must skip past to reach the argument.

**Required**: State it once. Drop the opening premise-inventory paragraph or the Case-1 restatement.

## OUT_OF_SCOPE

### Topic 1: Decidability/consistency model for concurrent Observe vs Emit
Several Open Questions (atomicity of Emit vs Observe, ordering of Observe results, cardinality bounds on `nullified`) are correctly deferred — they concern a concurrency/consistency layer not yet specified, not errors in this ASN.

VERDICT: REVISE
