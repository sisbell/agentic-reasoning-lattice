# Review of ASN-0054

## REVISE

### Issue 1: A12 overstates its scope — bidirectional equivalence fails for the full arrangement

**ASN-0054, A12 (Arrangement Equality)**: "M(d₁) = M(d₂) as partial functions iff their canonical decompositions agree"

**Problem**: The canonical decomposition covers only V(d) = {v ∈ dom(M(d)) : v₁ = 1} — the text domain. The forward direction is fine: equal full arrangements imply equal text-domain restrictions, hence equal decompositions. The reverse direction is too strong: equal decompositions only recover M(d₁)|_{V(d₁)} = M(d₂)|_{V(d₂)}. The link subspace (v₁ < 1) is invisible to the decomposition.

Concrete counterexample: d₁ has text content {[1,1] → a} and link content {[0,1] → b}; d₂ has the same text content but link content {[0,1] → b'}. Their canonical decompositions agree, but M(d₁) ≠ M(d₂) as partial functions.

**Required**: Restrict A12 to the text domain: "M(d₁)|_{V(d₁)} = M(d₂)|_{V(d₂)} iff their canonical decompositions agree." The proof's reverse direction then holds, and the "arrangement descriptor completely determines the V→I mapping" claim in the Span Representation section should carry the same qualifier.

## OUT_OF_SCOPE

### Topic 1: Link subspace invariants
**Why out of scope**: The ASN explicitly restricts to v₁ = 1 and lists "What invariants govern the link subspace (v₁ < 1)?" as an open question. A0-style contiguity likely does not hold for links (permanent addresses, deletion leaves gaps). This is genuinely new territory requiring its own treatment.

### Topic 2: Formal operation composites
**Why out of scope**: INSERT, DELETE, REARRANGE, and COPY are described by their effects on V(d), not as explicit sequences of K.α/K.δ/K.μ⁺/K.μ⁻/K.μ~/K.ρ. The ASN frames the preservation arguments as existence proofs (each operation *can* satisfy A0), which is appropriate for the coupling-constraint framework. Formal composite definitions would belong in an operations ASN.

### Topic 3: Contiguity for other text subspaces
**Why out of scope**: The analysis restricts to v₁ = 1. If text subspaces with v₁ ≥ 2 exist, the same structural analysis would apply by symmetry, but this ASN does not claim results for them. Extending A0 to all text subspaces is straightforward future work.

VERDICT: REVISE
