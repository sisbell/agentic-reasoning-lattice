# Review of ASN-0034

## REVISE

### Issue 1: "Addition is not associative" is unsupported for the abstract algebra

**ASN-0034, "What tumbler arithmetic is NOT"**: "**Addition is not associative.** We do NOT require `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)`."

**Problem**: The bold heading asserts non-associativity as a property of the abstract algebra. The only evidence is implementation-level: "Gregory's implementation does not implement carry propagation in `tumbleradd` — ... This makes the operation fast but non-associative for operands at different hierarchical levels." The constructive definition given in this ASN yields an operation that IS associative wherever both compositions are well-defined. I verified all three cases exhaustively:

**Case k_b < k_c** (b acts shallower than c). Left side `(a ⊕ b) ⊕ c`: positions `i < k_b` from `a`; position `k_b` is `a_{k_b} + b_{k_b}`; positions `k_b < i < k_c` from `b`; position `k_c` is `b_{k_c} + c_{k_c}`; positions `i > k_c` from `c`. Right side `a ⊕ (b ⊕ c)`: action point of `b ⊕ c` is `k_b` (since `(b ⊕ c)_i = b_i` for `i < k_c`, and `b_{k_b} > 0`). So: positions `i < k_b` from `a`; position `k_b` is `a_{k_b} + b_{k_b}`; positions `i > k_b` from `b ⊕ c`, which gives `b_i` for `k_b < i < k_c`, then `b_{k_c} + c_{k_c}` at `k_c`, then `c_i` beyond. Identical.

**Case k_b = k_c = k.** Left: `a_k + b_k + c_k` at position `k`, `c_i` beyond. Right: `a_k + (b_k + c_k)` at position `k`, `c_i` beyond. Natural-number addition is associative. Identical.

**Case k_b > k_c** (b acts deeper than c). Left: `r = a ⊕ b`; then `r ⊕ c` with action point `k_c < k_b`, so `r_{k_c} = a_{k_c}` (untouched by `b`). Result: `a_{k_c} + c_{k_c}` at `k_c`, `c_i` beyond. Right: `b ⊕ c` has action point `k_c` (since `b_{k_c} = 0`, giving `(b ⊕ c)_{k_c} = c_{k_c}`). Then `a ⊕ (b ⊕ c)`: `a_{k_c} + c_{k_c}` at `k_c`, `c_i` beyond. Identical.

The domain of definition is asymmetric — the left side requires `k_b ≤ #a` while the right requires only `min(k_b, k_c) ≤ #a` — but on the intersection (where both are defined), the values agree. The abstract operation is associative.

This contradicts the bold heading and creates tension with the open question "Under what conditions can shift composition hold — when does `(a ⊕ w₁) ⊕ w₂ = a ⊕ (w₁ ⊕ w₂)`?" The answer, derivable from the constructive definition in this ASN, is: always, when both sides are well-defined.

**Required**: Either (a) produce a counterexample for the abstract constructive definition, or (b) correct the heading to state that the abstract operation is associative where both compositions are defined, that the design does not depend on associativity, and that implementations with finite representations may break it. Resolve or remove the shift-composition open question accordingly.

## OUT_OF_SCOPE

### Topic 1: Well-formed displacement characterization
The ASN discusses T4 preservation under `inc` (TA5) but not under addition. A displacement whose tail introduces extra zero-valued components in non-separator positions (e.g., `w = [0,0,0,0,3,0,0,1]` applied to an element address) can produce a result violating T4 (four zeros). The ASN correctly states that "the hierarchy is convention layered over flat arithmetic," so this is by design — but characterizing which displacements preserve T4 is natural future work.
**Why out of scope**: The algebra is intentionally flat; T4 enforcement belongs to the allocation/span layer, not the arithmetic.

### Topic 2: Crash recovery and allocation counter durability
Mentioned in the open questions. Not addressable from the algebraic properties alone.
**Why out of scope**: Requires operational semantics and system-level recovery guarantees beyond the algebra.

VERDICT: REVISE
