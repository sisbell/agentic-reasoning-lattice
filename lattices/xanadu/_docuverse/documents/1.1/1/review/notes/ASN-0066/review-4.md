# Review of ASN-0066

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Operation preservation of D-CTG and D-MIN
**Why out of scope**: The ASN correctly identifies this as a verification obligation for each operation's ASN. Establishing the constraints is this ASN's job; showing INSERT, DELETE, COPY, REARRANGE preserve them is future work.

### Topic 2: Implications of D-SEQ for span decomposition
**Why out of scope**: D-SEQ forces correspondence runs (S8) to tile a gapless ordinal block, which strengthens the span decomposition guarantee. This is a natural consequence of the constraints introduced here, but deriving it belongs in a future ASN connecting arrangement structure to span decomposition.

---

**Observations** (not defects — noted for completeness):

**D-CTG-depth argument.** The proof is given through a single depth-3 example ([S,1,5] and [S,2,1]). The pattern generalizes cleanly: if two positions first differ at component j with 2 ≤ j ≤ m−1, then incrementing the last component of the smaller position produces infinitely many intermediates that remain below the larger position (because they still lose at component j). The example is representative and the general structure is immediate, so no case analysis is missing.

**D-SEQ derivation uses D-MIN before its formal statement.** The derivation paragraph restates D-MIN's content inline ("By D-MIN, min(V_S(d)) = [S, 1, …, 1]"), so there is no forward-reference ambiguity. The formal D-MIN definition follows in the next section.

**Statement type DESIGN.** The foundation uses `INV, predicate; design requirement` for design constraints (S7a, S7b, S8-depth). This ASN uses `DESIGN` as a standalone type. The meaning is clear and the distinction is arguably sharper, but it deviates from the established convention.

VERDICT: CONVERGED
