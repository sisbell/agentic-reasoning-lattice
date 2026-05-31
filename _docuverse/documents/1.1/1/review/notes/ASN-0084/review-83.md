# Review of ASN-0084

I checked the displacement and permutation arithmetic, the well-definedness lemmas (R-PIV, R-SWP), the bijection proofs (R-PPERM, R-SPERM), the run-transformation lemma (R-BLK), the invariant-preservation audit, and all six worked examples. The correctness content is sound: the region partition is exhaustive and disjoint, the tiling arguments close, the surjectivity-from-finiteness arguments are valid, R-COMM correctly underwrites the run-reassembly consistency, and the S8-uniq coverage argument via π's bijectivity on V_S(d) is airtight. The OrdShiftHom citations are all (a) — the previously-declined finding is resolved and I do not resurface it. One genuine gap remains.

## REVISE

### Issue 1: The `+` operator is defined only for depth-2 V-positions but used on I-addresses

**ASN-0084, "State and Vocabulary" (Notation) vs. "Correspondence-Run Decomposition Transformation" (Split, Merge)**: The Notation paragraph defines the operator narrowly — "We write `c₀ + j` for the V-position `[S, ord(c₀) + j]`" — and Extended Associativity is stated for that V-position form: "For all j, k ∈ ℕ, `(c + j) + k = c + (j + k)`." But Split and Merge then perform `+` arithmetic on **I-addresses**: the S8 recall writes "`M(d)(v_s + k) = a_s + k`"; Split derives "`(a + c) + k = a + (c + k)`"; Merge uses "`a₂ = a₁ + n₁`" and "`a₁ + k = a₁ + (n₁ + k') = (a₁ + n₁) + k' = a₂ + k'`". I-addresses are element-level (zeros = 3, depth ≥ 4 by S7b), not depth-2 singletons, so neither the Notation definition nor the singleton-identification machinery (which is explicitly scoped "at depth 2") covers them.

**Problem**: The reader must infer that `a + k` denotes `shift(a, k)` (last-component increment, inherited from S8's run convention) and that Extended Associativity's TS3 instance applies to a generic tumbler rather than only to the depth-2 form it is written in. The math is fine — TS3 holds for any `v ∈ T` — but the operator carrying the I-address arithmetic in Split/Merge is never defined in this ASN, and the associativity identity it invokes is stated for an object of the wrong depth.

**Required**: State explicitly (in the Notation paragraph or at the head of the run-decomposition section) that `+` on I-addresses denotes `shift(a, ·)` per ASN-0036's S8 convention, and that Extended Associativity's underlying TS3 instance is depth-agnostic so the identity transfers to I-addresses. One sentence closes the gap.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4, composition of rearrangements, run-count growth bounds, canonical-partition recovery
**Why out of scope**: These are correctly deferred to the Open Questions and are new territory, not defects in the present ASN's 3-/4-cut treatment.

VERDICT: REVISE
