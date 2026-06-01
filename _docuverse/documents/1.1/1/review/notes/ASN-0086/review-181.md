# Review of ASN-0086

The technical core — R0/R0a freshness and antichain, L-ContiguousPrefix, the R1–R7 chain, CoverageEqualityDecidable (including the gap-non-emptiness discharge), and the wp Case 1/Case 2 analyses — checks out. I verified the worked example's tumbler arithmetic (a₁ through a₃, the K.λ first/subsequent branches, coverage computations) and found it consistent. The findings below are the meta-prose / forward-reference patterns the note's `anti-bloat` classifier asks to be surfaced.

## REVISE

### Issue 1: Pre-computed sub-consequences parked far from their use sites (forward-reference accretion)
**ASN-0086, Remark — NestedLinkWitness**: "*Off-chain-edge consequence.* Over such a Σ the chain frontier is ill-formed... *Prefix-inheritance consequence.* When a proper nested key `b' ≺ ℓ_prev` exists at home `d`..."

**Problem**: The Remark legitimately witnesses the strict inclusion claimed in the immediately following *Definition — state-local-conforming state*. But the two named sub-consequences are not used there — they are consumed only hundreds of lines downstream (Off-chain-edge in *Definition — Emit_K*'s partiality clause; Prefix-inheritance in the wp "discipline alone is insufficient" paragraph). A reader processing the opening foundational definitions must work through a non-conforming-case digression with two essay-labeled consequences whose payoff arrives much later. This is the forward-reference accretion pattern: content computed upstream and parked away from its single use.

**Required**: Keep in the Remark only the bare strict-inclusion witness that *Definition — state-local-conforming state* actually cites. Move the *Off-chain-edge consequence* into *Definition — Emit_K* and the *Prefix-inheritance consequence* into the wp domain-restriction paragraph, where each is consumed.

### Issue 2: Forward reference from a result to the lemma it depends on
**ASN-0086, R0 proof, subsequent-emission branch**: "Σ is substrate-conforming, so L-ContiguousPrefix (ContiguousPrefix, below) gives that the homed-set..."

**Problem**: R0's proof consumes L-ContiguousPrefix, which is stated *after* R0. The "(below)" pointer is forced by ordering, not by any genuine dependency direction (L-ContiguousPrefix does not depend on R0 — its extension case rests only on ASN-0093 lemmas and clauses (b)/(c)). The same downstream-pointer pattern recurs (R-Scope, R7a discharge (4) both lean on L-ContiguousPrefix).

**Required**: Reorder so L-ContiguousPrefix (and its Cor1) precede R0, eliminating the "(below)" pointers; R0, R-Scope, and R7a then cite an already-established lemma.

### Issue 3: Defensive "why the operation is partial" prose in a definition slot
**ASN-0086, Definition — Emit_K**: "`Emit_K` is *partial* over this sub-space and *total* over the substrate-conforming sub-domain: R0's substrate-conformance hypothesis is exactly what makes K.λ's emission admissible (R0; over a merely state-local-conforming Σ the emission can be undefined, by the off-chain-edge consequence...)."

**Problem**: This explains *why* the operation is partial rather than stating *what* its domain is — a defensive justification embedded in the signature definition. The substantive content (the domain is the substrate-conforming sub-space) is one clause; the rest re-litigates R0's hypothesis and points at the parked Remark consequence.

**Required**: State the domain as a fact ("`Emit_K` is defined over substrate-conforming Σ"); drop the justificatory clause, or relocate the partiality rationale to the *Lemma — Emit_K function-ness* where domain-of-definition is already in scope.

## OUT_OF_SCOPE

### Topic 1: Elevating the unit-depth retraction discipline to a substrate-level guarantee
**Why out of scope**: The note correctly leaves this as the layer convention it is and records the design tradeoff in Open Questions. Introducing a dedicated retraction K-operation with a shape constraint is new substrate vocabulary, properly a future ASN.

### Topic 2: Higher-arity typed relations (`L_K^{(n)}`) and binary projections of `|Σ.L(a)| > 3` links
**Why out of scope**: The note explicitly restricts to standard triples and flags higher-arity handling as future work; no error in confining `L_K` to arity 3 here.

VERDICT: REVISE
