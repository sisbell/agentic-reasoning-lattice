# Review of ASN-0082

## REVISE

### Issue 1: OrdinalExceedsDisplacement is stated for "any V-position v" but its conclusions hold only within subspace 1

**ASN-0082, "Ordinal Extraction", Lemma — OrdinalExceedsDisplacement**: "Fix the contraction parameters: `#p = 2`, ..., `p ∈ V_1(d)`, and `r = p ⊕ w`. For any V-position v with `v ≥ r` (equivalently `ord(v) ≥ ord(r)`): ... (ii) `ord(v) ≥ w_ord` ...; (iii) `ord(v) ⊖ w_ord` ... strictly greater than `ord(p)` ... when `v > r`."

**Problem**: The parenthetical equivalence and the derivations of (ii)/(iii) depend on `OrdinalOrderEquivalence`, which requires `subspace(v) = subspace(r)` and `#v = #r`. For a V-position `v` in subspace 2 with depth 2, `v ≥ r` holds trivially (`2 > 1` at position 1) yet `ord(v) ≥ ord(r)` need not hold, and clause (iii)'s "strictly greater than `ord(p)`" is then simply false. The lemma as literally quantified ("any V-position v with `v ≥ r`") is false. Downstream uses (D-SHIFT, D-BJ, D-S) only ever instantiate `v ∈ R ⊆ V_1(d)`, so no error propagates — but the stated generality is unsound.

**Required**: Add `subspace(v) = 1` (equivalently `v ∈ R`) to the lemma's quantifier, so the appeal to OrdinalOrderEquivalence is licensed.

### Issue 2: I3-S omits the `n ≥ 1` precondition its proof relies on

**ASN-0082, "Span Width Preservation", I3-S**: "For a level-uniform span σ = (s, ℓ) ... the shifted span σ' = (shift(s, n), ℓ) satisfies (a) reach(σ') = shift(reach(σ), n)."

**Problem**: `n` is unbound in the statement. The construction `shift(s, n)` is defined only for `n ≥ 1` (OrdinalShift precondition, ASN-0034), and the derivation invokes TS3 (ShiftComposition), whose preconditions are `n₁ ≥ 1, n₂ ≥ 1`. With `n = 0` neither `shift(s, n)` nor the TS3 steps are well-defined.

**Required**: State `n ≥ 1` as a precondition of I3-S (and mirror in the registry row).

### Issue 3: Anti-bloat — redundant restatement after OrdAddHom

**ASN-0082, "Ordinal Extraction", after the OrdAddHom proof**: "In words: addition commutes with ordinal extraction when the displacement has a zero first component."

**Problem**: This sentence duplicates the gloss already carried in OrdAddHom clause (a) itself ("whole-tumbler addition commutes with ordinal extraction when the displacement has a zero first component"). Two statements in the same section saying the same thing in different words.

**Required**: Delete the trailing "In words:" sentence.

### Issue 4: Anti-bloat — NAT-CA introduction explains why the axiom is needed rather than what it states

**ASN-0082, "Span Width Preservation", NAT-CA**: "The reach derivation below turns on the commutativity of ℕ addition, which we record as a local axiom."

**Problem**: This is the flagged pattern of meta-prose around an axiom that justifies its presence ("the derivation below turns on...") rather than advancing the axiom's content. The axiom statement itself is self-sufficient.

**Required**: Drop the justifying clause; state NAT-CA directly.

## OUT_OF_SCOPE

### Topic 1: NAT-CA belongs in the foundation's NAT-* set
The foundation (ASN-0034) supplies NAT-addcompat, NAT-closure, NAT-discrete, NAT-order, NAT-wellorder but not commutativity/associativity of ℕ addition. ASN-0082 must therefore introduce NAT-CA locally — correct under the current foundation, but a domain-independent arithmetic law of this kind ideally migrates to the NAT-* foundation so dependents cite rather than re-introduce it. Not an error in this ASN.

### Topic 2: The post-insertion-shift intermediate state is not a valid arrangement
I3's preservation lemmas establish S8-depth, S8a, S2, S3, S8-fin, S7 but explicitly leave D-CTG/D-MIN/D-SEQ violated (the gap), since the shift is only INSERT's sub-operation. The composition (shift + content placement) that re-establishes contiguity is the proper subject of the INSERT operation ASN. The contraction half is a complete operation and does re-establish these; the asymmetry is a scoping choice, not a defect here.

VERDICT: REVISE
