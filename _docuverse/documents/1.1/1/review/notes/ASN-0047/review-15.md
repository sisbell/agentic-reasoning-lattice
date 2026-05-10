# Review of ASN-0047

## REVISE

### Issue 1: P4 inductive proof miscounts K.μ~ as elementary

**ASN-0047, P4 (Provenance bounds), inductive step**: "Five of the six elementary transitions preserve the invariant individually; the remaining case — K.μ⁺ — requires its coupling with K.ρ."

**Problem**: The proof lists six cases (K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.ρ) and calls them "six elementary transitions." But the ASN explicitly defines K.μ~ as "a distinguished composite, not a primitive transition" in the elementary transitions section, and the completeness argument correctly identifies "five primitive kinds — K.α, K.δ, K.μ⁺, K.μ⁻, K.ρ." The P4 proof contradicts both.

The proof logic is sound — the K.μ~ case is correctly verified (ran preservation means Contains is unchanged). The error is terminological, but it undermines the ASN's own primitive/composite distinction, which is load-bearing for the completeness argument and the valid composite definition.

**Required**: Rephrase to "five elementary transitions and one distinguished composite" or "six transition kinds." Handle K.μ~ as a composite case (noting it follows from K.μ⁻ + K.μ⁺ analysis, or independently from ran preservation). The same issue appears in the P5 proof ("By case analysis on K.α–K.ρ" lists K.μ~ alongside primitives) — fix both.

## OUT_OF_SCOPE

### Topic 1: Compound operation composition from elementary transitions

The ASN defines five elementary transitions and notes that split, merge, and replacement compose from them. A future ASN should define the standard compound operations (INSERT, DELETE, COPY, REARRANGE, FORK) as specific composite patterns and verify that each satisfies the valid composite conditions. The worked example informally demonstrates this for fork and insert, but the general composition rules are not formalised.

**Why out of scope**: The ASN explicitly excludes "Named operations and their specifications." The elementary transition taxonomy is the right foundation; operation composition is the next layer.

### Topic 2: Version DAG structure from fork chains

J4 defines a single fork. Nelson's model has chains of forks forming a version DAG. The relationship between successive forks of the same source, the resulting DAG structure, and what invariants the DAG must satisfy (e.g., can a document be forked from two different sources?) is not addressed.

**Why out of scope**: This requires version identity semantics beyond the transition model. The open questions section correctly identifies the version-lineage question.

VERDICT: REVISE
