# Review of ASN-0047

## REVISE

### Issue 1: The "M is the sole mutable layer" decomposition is stated three times in prose
**ASN-0047, *Permanence* (opening) and *Temporal decomposition* (opening)**: The Permanence section opens with "exhibits three distinct permanence contracts: append-only stores with immutable values (C via P0, L via L12), extension-only sets and relations (E via P1/P8, R via P2), and the arrangement family M — the sole mutable component, admitting extension, contraction, and reordering." The *Temporal decomposition* section then re-states the identical content: "decomposes into three temporal layers: an *existential* layer (C, L, E) ...; a *historical* layer (R) ...; and a *presentational* layer (M) that is freely mutable." P3's narrator note ("P3 is the synthesis of P0 ∧ P1 ∧ P2 ∧ L12 — one named per-transition predicate ... covering every component except M") is a third restatement.

**Problem**: This matches the anti-bloat pattern "two paragraphs in the same document say the same thing in different words." P3 is the formal carrier; the *Temporal decomposition* section is the synthesis with table and cross-layer bridges. The Permanence-section opening prose adds no claim the later two do not, and the precise reader must recognize the same partition three times to confirm nothing new is being asserted.

**Required**: Keep P3 (formal) and the *Temporal decomposition* table (synthesis with bridges). Reduce the Permanence-section opening to a roadmap sentence that does not re-enumerate the three contracts, or drop it, so the partition is stated once formally and once in synthesis.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link withdrawal
**Why out of scope**: K.μ⁻ models suffix-only link-subspace contraction; interior `DELETEVSPAN`-style compaction-and-renumbering is a distinct contraction operation. The ASN correctly defers this to a future ASN (open question 9), and named operations are out of scope here.

### Topic 2: Empty from/to endsets (type-only and one-sided links)
**Why out of scope**: K.λ admits `e₁, e₂ = ∅` (only `e₃ ≠ ∅` required). Whether to constrain this is flagged as an open question and concerns endset semantics not covered by this ASN's state/transition taxonomy.

VERDICT: REVISE
