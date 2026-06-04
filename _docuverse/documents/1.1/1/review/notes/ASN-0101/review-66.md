# Review of ASN-0101

This is a carefully constructed ASN. The core operation (D0), the gap-closure bijection (D1), the frame-preservation claims (D2–D7), the well-formedness preservation (D8), and the projection/wp results (D9, D11) are mathematically sound; I traced the worked examples and the region arithmetic and found no errors. The findings below concern accumulated meta-prose around D10, consistent with the `review-mode.anti-bloat` classifier — prior cycles have layered redundant framing onto the composite-boundary argument.

## REVISE

### Issue 1: D10 restates the same framing point three times before deriving anything
**ASN-0101, D10**: Three consecutive paragraphs each open by re-stating that ASN-0047's theorem covers only the pre-DEL vocabulary and that DEL obliges re-establishment of P4★/P4a/P7a:
- *Composite-boundary obligations*: "ASN-0047's ExtendedReachableStateInvariants theorem guarantees these at composite boundaries only for the pre-DEL vocabulary; admitting DEL obliges us to re-establish them for a DEL-terminated composite."
- *Neutrality*: "they are guaranteed only at *composite boundaries*, not at every reachable state."
- *Boundary derivation*: "ASN-0047's ExtendedReachableStateInvariants theorem — proved over the pre-DEL vocabulary — does not by itself establish P4★/P7a at such a boundary."

**Problem**: This is the same observation in three forms ("multiple paragraphs say the same thing in different words"). The reader must skip past two restatements to reach the actual induction in *Boundary derivation*.
**Required**: State the framing once (it belongs immediately before the inductive derivation), and delete the *Composite-boundary obligations* and *Neutrality*-preamble restatements.

### Issue 2: P4a is fully argued twice within D10
**ASN-0101, D10, Neutrality bullet**: "*P4a (trace-witnessing).* `R' = R`, and any pair `(a, d) ∈ R` witnessed at some `Σ_k` in the pre-state history remains witnessed at that same `Σ_k` ... DEL cannot break P4a."
**ASN-0101, D10, Boundary derivation closing**: "P4a at `Σ'` follows directly from the neutrality bullet: `R' = R`, so DEL records no new pair, and every `(a, d) ∈ R'` keeps its pre-DEL witnessing trace state."

**Problem**: The second sentence claims to "follow directly from the neutrality bullet" but then re-states the bullet's entire argument (R'=R / no new pair / witnesses persist) rather than citing it. More broadly, the *Neutrality* section proves DEL "cannot break" three properties that are *not* per-state invariants, while the *Boundary derivation* separately establishes them at the boundary — two parallel structures over the same three properties, with the only fact the derivation consumes from neutrality being "Contains_C shrinks and R is fixed."
**Required**: Collapse to a single argument per property. Either the per-step neutrality facts are lemmas the boundary induction cites by name (with no recap), or fold them into the induction directly.

### Issue 3: Defensive exhaustiveness clause in the boundary cases
**ASN-0101, Boundary cases, "Non-singleton interior deletion"**: "When `|Λ|` or `|Q|` exceeds 1 (e.g. `n_S = 6, n = 2, p = 3` ...) the same discharge applies pointwise to each element of either region — the proof is not specialised to singleton cardinalities anywhere."

**Problem**: The trailing clause "the proof is not specialised to singleton cardinalities anywhere" is a defensive exhaustiveness assertion anticipating a reviewer objection rather than advancing the verification. D8's justification is already explicitly uniform over regions; the worked example plus the singleton/non-singleton cases already establish generality.
**Required**: Drop the defensive clause; the concrete `n_S = 6` instance carries the point without the assertion.

## OUT_OF_SCOPE

### Topic 1: Reconstruction / reversibility of pre-DELETE arrangements
The Open Questions correctly defer arrangement reconstruction, DELETE-then-INSERT recovery, and causal ordering across transcluding documents to a versioning mechanism. These are genuinely future territory, not gaps in this ASN.

VERDICT: REVISE
