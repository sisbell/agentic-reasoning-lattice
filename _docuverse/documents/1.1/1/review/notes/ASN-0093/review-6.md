# Patch Review of ASN-0093

## REVISE

### Issue 1: L3 invariant statement not reverted
**ASN-0093, Link store invariants → L3**: "L3 (TripleEndsetStructure, narrowed form). `(A a ∈ dom(L) :: L(a) = (F, G, Θ) where F, G, Θ ∈ Endset ∧ Θ ≠ ∅)` Every link in the link store has exactly three endsets... This is a substrate-level *narrowing* of ASN-0043's L3... the substrate pins fixed-three-arity rather than retaining ASN-0043's foundation `N ≥ 3` form. ASN-0043's `N ≥ 3` generality is preserved in principle for foundation-level extensions, but the substrate's transition model is closed under fixed-three arity."
**Problem**: The patch explicitly instructed to revert L3 to ASN-0043's general `N ≥ 3` form. The current L3 still narrows to exactly three endsets via `L(a) = (F, G, Θ)`, still labels itself "narrowed form" in the header, and still asserts "substrate's transition model is closed under fixed-three arity" — directly contradicting the patch.
**Required**: Replace the L3 statement with the general form, e.g.: "L3 (NEndsetStructure). `(A a ∈ dom(L) :: |L(a)| ≥ 3 ∧ (A i : 1 ≤ i ≤ |L(a)| : L(a).eᵢ ∈ Endset) ∧ L(a).e₃ ≠ ∅)`. Every link is a sequence of at least three endsets, with the type endset (slot 3) non-empty. The three-endset convention (slot 1 = from, slot 2 = to, slot 3 = type, written `(F, G, Θ)`) is preserved as the default but not enforced structurally." Remove "narrowed form" from the header and remove the "narrowing" explanation paragraph.

### Issue 2: K.λ operation signature still locks to three-arity
**ASN-0093, Substrate primitive operations → K.λ**: Signature `K.λ(d, ℓ, F, G, Θ)`; precondition `(F, G, Θ) ∈ Endset × Endset × Endset ∧ Θ ≠ ∅`; effect `L' = L ∪ {ℓ ↦ (F, G, Θ)}`.
**Problem**: With L3 reverted to `N ≥ 3`, the substrate must admit construction of links with N > 3. K.λ's hardcoded three-tuple signature and precondition make it structurally impossible to construct a link with `|L(a)| > 3`, contradicting the patch's intent that arity be unconstrained at the substrate. The L3 invariant cannot have an N ≥ 3 form if the only operation that introduces links cannot produce non-3 arities.
**Required**: Revise K.λ to accept a variable-arity link value. Replace parameters `F, G, Θ` with a sequence `(e₁, …, eₙ)`; replace the precondition with `N ≥ 3 ∧ (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset) ∧ e₃ ≠ ∅`; replace the effect with `L' = L ∪ {ℓ ↦ (e₁, …, eₙ)}`. The arity-3 default can be retained as a notational convenience in worked examples.

### Issue 3: Parameter semantics paragraph not updated for K.λ
**ASN-0093, Substrate primitive operations → Parameter semantics**: "For `K.α(d, a, v)` and `K.λ(d, ℓ, F, G, Θ)`, the address parameters `a` and `ℓ` appear in the operation signatures..."
**Problem**: The K.λ signature here is the fixed-three-arity form. Should match the revised K.λ signature.
**Required**: Update the citation of K.λ's signature to match the revised arity-N form.

### Issue 4: Registry entry for L3 not updated
**ASN-0093, Properties Introduced**: "| L3 | TripleEndsetStructure | INV | Narrowed form of ASN-0043's L3 (fixed-three-arity); established at K.λ (precondition pins `(F, G, Θ) ∈ Endset × Endset × Endset ∧ Θ ≠ ∅`); preserved at K.σ/K.α by frame on `L` |"
**Problem**: The Name column ("TripleEndsetStructure"), Status description ("Narrowed form... fixed-three-arity"), and discharge description (citing the three-tuple precondition) all reflect the pre-patch fixed-three-arity form.
**Required**: Rename to "NEndsetStructure" (matching ASN-0043's L3 name). Replace the Source column with: "ASN-0043; established at K.λ (precondition pins `|L(ℓ)| ≥ 3 ∧ (e₃) ≠ ∅`); preserved at K.σ/K.α by frame on `L`."

### Issue 5: Discharge matrix entry for L3 cites fixed-three-arity precondition
**ASN-0093, Discharge of stated invariants → matrix row for L3**: "| **L3** (TripleEndsetStructure, narrowed) | Preserved: `L` in frame | Preserved: `L` in frame | Discharged at new key: precondition pins `(F, G, Θ) ∈ Endset × Endset × Endset ∧ Θ ≠ ∅` |"
**Problem**: Label "(narrowed)" and discharge text both reflect the fixed-three-arity form.
**Required**: Update label and discharge text to reflect the N ≥ 3 form, citing the revised K.λ precondition.

### Issue 6: Open Questions item contradicts patch
**ASN-0093, Open Questions**: "*Higher-arity links.* L3 here pins three-arity. ASN-0043's general `N ≥ 3` form is preserved in principle for foundation-level extensions; this substrate is closed under fixed-three arity."
**Problem**: This item asserts that the substrate pins three-arity and is "closed under fixed-three arity" — directly contradicting the patch's revert of L3 to N ≥ 3. Higher-arity links are no longer an open question at this layer; they are admitted.
**Required**: Either remove the item entirely (it is no longer an open question), or replace it with a forward-looking note acknowledging that L3 now admits N ≥ 3 and that higher-layer ASNs may impose further constraints if needed.

### Issue 7: Worked example consistency check
**ASN-0093, Worked example**: All K.λ calls in Steps 3, 7, 8 use the three-tuple form `K.λ(d, ℓ, F, G, Θ)`.
**Problem**: While the patch preserves three-endset as the default, the worked example invokes the K.λ signature that is itself misaligned (per Issue 2). Once K.λ is revised to accept N-tuples, the example signatures should be cited in a form compatible with both the revised operation and the arity-3 convention (e.g., explicitly noting that the example uses the arity-3 default).
**Required**: Once K.λ is revised, reconcile the worked example invocations either by updating to the variable-arity form (e.g., `K.λ(d, ℓ, (F, G, Θ))`) or by adding a one-line note that the worked example exhibits the arity-3 default permitted by K.λ's general signature.

VERDICT: REVISE
