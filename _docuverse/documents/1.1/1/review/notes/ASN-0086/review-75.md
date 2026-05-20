# Review of ASN-0086

## REVISE

### Issue 1: R6c-Corollary's "→*-subsequence" framing isn't a valid →*-chain

**ASN-0086, R6c-Corollary proof Step 1**: "Restricting to the `→`-steps yields a `→*`-chain `Σ = Σ_{i_0} → Σ_{i_0 + 1} → ... → Σ_{i_m + 1}` (consolidating each `→`-step with the arrangement-modifying tail that follows it into a single jump to the next `→`-step's source)"

**Problem**: The asserted "→*-chain" isn't actually one. Between consecutive →-steps in the original ↦*-chain there can be arrangement-modifying steps that change Σ.M while preserving Σ.L. The proof "consolidates" these tails into a "jump to the next →-step's source", but the source of each →-step (after the first) is *not* the target of the previous →-step — they differ in Σ.M values. The chain `Σ_{i_0} → Σ_{i_0+1} → Σ_{i_1+1}` requires `Σ_{i_0+1} → Σ_{i_1+1}` to be a real →-step, which it isn't. The single application of R6c to this "subsequence" implicitly relies on R6c depending only on Σ.L (via LinkStoreInvarianceUnderArrangement), but that dependency isn't formally invoked.

**Required**: Replace the subsequence reduction with a direct induction over the ↦*-chain. Base: precondition + Definition of A_K. Step: split on whether `Σ_n ↦ Σ_{n+1}` is a →-step (apply R6a + R3 to maintain `(a, F, G) ∈ L_K^{Σ_{n+1}}` and `a ∈ nullified(Σ_{n+1})`) or arrangement-modifying (apply LinkStoreInvarianceUnderArrangement to transfer pointwise). Both branches conclude `(a, F, G) ∉ A_K^{Σ_{n+1}}`. This is shorter than the "subsequence reduction" and rigorously valid.

### Issue 2: R5's claim is silent about the emission precondition

**ASN-0086, R5 statement**: "for any state Σ and any `a ∈ A_rel^Σ`, the unit-depth span `(a, δ(1, #a))` is well-formed and may appear in the from-set or to-set of an emitted tuple"

**Problem**: "May appear in ... of an emitted tuple" presupposes an emission, which invokes R0 — whose precondition is `dom(Σ.M) ≠ ∅`. The R5 claim makes no mention of this. The proof Steps 3 and 5 pick "any `d ∈ dom(Σ.M)`" as if it's a given, but the claim's only explicit precondition is `a ∈ A_rel^Σ`. The derivation `a ∈ A_rel^Σ ⟹ dom(Σ.M) ≠ ∅` (via L1a — `home(a) ∈ dom(Σ.M)`) is straightforward but unstated.

**Required**: Either add an explicit `dom(Σ.M) ≠ ∅` precondition to R5's statement, or open the proof with the one-line derivation: "By L1a applied to `a ∈ A_rel^Σ`, `home(a) ∈ dom(Σ.M)`, so `dom(Σ.M) ≠ ∅`, discharging R0's precondition for the chosen home below."

### Issue 3: ChainMembershipForOrigin uniqueness for re-enumeration in R7a's discharge (4)(iii)

**ASN-0086, R7a proof discharge (4)(iii)**: "Re-order the Δ-enumeration so that fresh addresses homed at the same d_k appear in chain-order from least to greatest chain index (a permissible re-enumeration by (ii) since Δ is finite and within-home chain-order is well-defined by (i))."

**Problem**: "Within-home chain-order is well-defined by (i)" requires that each `a_k` homed at `d_k` have a *unique* chain index in `A_L(d_k)`. R0a-Cor1 at Σ' says the homed-set at `d_k` in Σ' is a contiguous initial segment `{inc^j(d_k.0.s_L.1, 0) : 0 ≤ j ≤ J_{d_k}^{Σ'}}`. Combined with ChainEnumerationInjectivity (ASN-0093), each address corresponds to a unique chain index. But the proof doesn't cite ChainEnumerationInjectivity at this discharge step — it cites it earlier for cross-iteration freshness but not for within-home index uniqueness. The argument relies on this implicitly.

**Required**: Add an explicit citation of ChainEnumerationInjectivity at (4)(iii): "Within-home chain-order is well-defined: by R0a-Cor1 each homed-set is a contiguous initial segment, and by ChainEnumerationInjectivity each address corresponds to a unique chain index, so within-home ordering is total."

### Issue 4: Worked Sketch silently assumes content addresses were K.α-emitted

**ASN-0086, Worked Sketch Setup**: "c₁ = 1.0.1.0.1.0.1.1, c₂ = 1.0.1.0.1.0.1.2 — two content addresses in dom(Σ_{-1}.C)"

**Problem**: The setup places c₁, c₂ in `dom(Σ_{-1}.C)` without noting the K.α invocations that allocated them. The reader can verify (by ASN-0093's SubAllocatorAxiom.FirstEmission and SiblingRecurrence applied to A_C(d)) that c₁ = `[d.0.s_C.1]` is the first K.α emission and c₂ = `inc(c₁, 0)` is the second, but this isn't stated. The Step 0 narrative is careful about K.λ structural details for a₁ but skips the analogous step for c₁/c₂.

**Required**: Add one sentence to the Setup: "Both c₁ and c₂ result from prior K.α invocations at home `d`: c₁ is the first emission of A_C(d) per SubAllocatorAxiom.FirstEmission, and c₂ = inc(c₁, 0) per SiblingRecurrence." This grounds the example state in the substrate's K-operations.

### Issue 5: "Properties Introduced" table conflates definitions with disciplines

**ASN-0086, Properties Introduced table**: Entries labeled DEF for "Unit-depth retraction discipline" and "Relational layer".

**Problem**: The "Unit-depth retraction discipline" is a layer-level *commitment* about retraction to-span shape, not a definition. Similarly, "Relational layer" labels a commitment to the operation set `{Emit_K, Observe_K, Nullify}` with Nullify-as-sole-R-producer discipline. Labeling these DEF conflates substrate-level definitions (like `A^Σ`, `L_K^Σ`, `nullified(Σ)`) with layer-level commitments. The functional content is correct; only the labeling is misleading.

**Required**: Introduce a separate label (e.g., COMMITMENT or DISCIPLINE) for layer-level conventions, and re-label these two entries. This makes the substrate/layer boundary explicit at the table level.

### Issue 6: R0a-Cor2's "equivalent route" remark dangles

**ASN-0086, R0a-Cor2 proof, final paragraph**: "An equivalent route via ChainPrefixExtension (ASN-0093) is available as a cross-check ... Downstream citations of R0a-Cor2 invoke the TA5(c) + TA5-SigValid route above as the canonical witness."

**Problem**: The "equivalent route" is mentioned but not developed. If it's a cross-check, either develop it (so a reader can verify the result two ways) or omit the mention. Half-developed alternative routes invite a reader to verify them and find they aren't fully fleshed out.

**Required**: Either develop the ChainPrefixExtension route as a parallel one-paragraph derivation, or remove the dangling reference. The TA5(c) + TA5-SigValid route is sufficient on its own.

## OUT_OF_SCOPE

### Topic 1: Concurrency and atomicity guarantees
What happens with concurrent Emit/Observe calls — atomicity model, observation consistency across emission boundaries — is acknowledged as open and belongs to a future ASN about concurrency.

### Topic 2: Active subsets for higher-arity relations
L_K^Σ restricts to arity-3 by definition; the extension to `A_K^{(n),Σ}` for higher-arity links is explicitly deferred. A future ASN can develop this without changing the present claims.

### Topic 3: Ordering on Observe results
Observe returns `℘_fin(L_K^Σ)` — a set. Whether downstream consumers should see results in emission order, address order, or unordered is a query-language design question.

### Topic 4: Dynamic admissible-type registration and collisions
Two layers independently choosing colliding type addresses (per L9) is an open question and isn't a defect in this ASN.

### Topic 5: K.α reconstruction in R7a
R7a reconstructs only the Σ.L-affecting effect. A future strengthening that also reconstructs Σ.C extensions (interleaving K.α steps) would be a separate result.

VERDICT: REVISE
