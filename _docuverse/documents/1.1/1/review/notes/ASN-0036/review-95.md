# Review of ASN-0036

## REVISE

### Issue 1: S5's frame note overstates the proof's verification scope
**ASN-0036, S5 (Unrestricted sharing), Frame**: "the witnesses are well-formed strand states that incidentally exhibit unbounded sharing"
**Problem**: The proof verifies S0–S3 (and notes S8a, D-MIN, D-CTG, D-SEQ are incidentally satisfied for V-positions). But the I-address `a` is left abstract — `C_N = {a ↦ w}` does not specify `a`'s tumbler structure, so neither S7b (`zeros(a) = 3`) nor S7c (`#E(a) ≥ 2`) is established. Likewise the document tumblers `dᵢ = [1, 0, 1, 0, i]` are exhibited as concrete tumblers but not argued to arise from T10a allocation events (S7d). Calling these "well-formed strand states" overreaches the proof.
**Required**: Either (a) fix `a` as an explicit element-level tumbler (e.g., `1.0.1.0.1.0.1.1`) and verify S7b–S7c, plus argue the `dᵢ` could arise from a T10a allocator tree (siblings via repeated `inc(·, 0)` from a common base) to satisfy S7d; or (b) qualify the frame note to say "states satisfying S0–S3 (with V-positions additionally satisfying S8a, D-MIN, D-CTG, D-SEQ); the I-address structure and document allocation discipline are not verified by this proof."

### Issue 2: S8's auxiliary lemma asserts conclusion (i) before establishing the structural premise (iii) it relies on
**ASN-0036, S8 (Span decomposition), Auxiliary lemma proof**: "the component at position `#aⱼ − δⱼ + 1` is copied unchanged, establishing conclusion (i): `subspace_I(shift(aⱼ, k)) = subspace_I(aⱼ)`"
**Problem**: The prefix-copying argument shows `shift(aⱼ, k)` at position `#aⱼ − δⱼ + 1` equals `aⱼ` at that position = `subspace_I(aⱼ)`. But to identify this with `subspace_I(shift(aⱼ, k)) = E(shift(aⱼ, k))_1`, we need `#E(shift(aⱼ, k)) = δⱼ` (conclusion (iii)) and `zeros(shift(aⱼ, k)) = 3` (conclusion (ii)) so that T4b's element-field projection on `shift(aⱼ, k)` recovers the same boundary. The proof derives (ii) and (iii) after (i), so the narrative asserts (i) using a fact not yet in hand.
**Required**: Reorder the proof to derive (ii) and (iii) first (prefix-copying preserves the three separator zeros; the action-point component `aⱼ_{#aⱼ} + k` is strictly positive by T4 plus `k ≥ 1`, so no new zero; hence `zeros = 3` and the element-field boundary is unchanged). Then derive (i) by noting that *given* the preserved field structure, position `#aⱼ − δⱼ + 1` is still the subspace_I position of `shift(aⱼ, k)`, and prefix-copying preserves its value.

### Issue 3: OrdAddS8a's second equivalence is stated but not derived
**ASN-0036, OrdAddS8a, Postconditions**: "`v ⊕ w satisfies S8a ⟺ (A i : actionPoint(w) < i ≤ m : wᵢ > 0)`. Equivalently, `ord(v ⊕ w) ∈ S ⟺ v ⊕ w satisfies S8a`."
**Problem**: The proof derives the first equivalence via TumblerAdd's three-region formula. The second equivalence is asserted by a gestural sentence — "the ordinal-domain S-membership and the V-position S8a property are two views of the same constraint on the displacement's tail" — but no derivation is given. The argument requires: (a) S8a on `v ⊕ w` reduces to componentwise positivity (since `#v ⊕ w = m ≥ 2` and `zeros = 0` iff all components positive); (b) `(v ⊕ w)_1 = v_1 > 0` unconditionally (since `w_1 = 0` forces `actionPoint(w) ≥ 2` so position 1 is prefix-copied, with `v_1 > 0` from S8a on `v`); (c) hence S8a on `v ⊕ w` iff positions 2..m are all positive iff `ord(v ⊕ w)` has all components positive iff `ord(v ⊕ w) ∈ S`.
**Required**: Add the explicit chain (a)–(c) showing why the equivalence holds — in particular, why `(v ⊕ w)_1 > 0` is unconditional and therefore irrelevant to the iff, leaving only positions 2..m to match between the S8a property on `v ⊕ w` and S-membership of `ord(v ⊕ w)`.

## OUT_OF_SCOPE

(None — the ASN's Scope section enumerates deferred topics, and operation-layer preservation of D-CTG/D-MIN, link-subspace contiguity, subspace alignment, and operation semantics are all properly delegated to future work.)

VERDICT: REVISE
