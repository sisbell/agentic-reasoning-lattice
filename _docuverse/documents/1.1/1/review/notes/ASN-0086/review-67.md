# Review of ASN-0086

## Analysis

The proofs are thorough. R0 explicitly discharges every L-invariant through ASN-0093's K.λ contract. R0a Case 1 establishes cross-home prefix-incomparability via NUDE-prefix arithmetic with explicit forward and reverse symmetry. R0a-Cor1/Cor2 specialize ASN-0093 chain machinery correctly. R5 builds the self-targeting proof carefully through five steps with generalization. R6a/R6b/R6c carry the active/audit distinction with proper inductions. R7a's decomposition into K.σ-prefixed K.λ-sequences is verified by two worked examples (length-2 and length-4).

Edge cases checked: empty link store (Σ_{-1}), first-emission branch, subsequent-emission branch, self-targeting at either slot, multi-document interleaving (Worked example 2), arity-3 restriction explicitly scoped.

Foundation references: only ASN-0034, ASN-0036, ASN-0043, ASN-0093 — all foundation. No non-foundation cross-references.

Invariant coverage in R0: L0, L1, L1a, L1b, L1c, L2, L3, L5, L6, L8, L11a, L12, L12a, L12b, L13, L14, L14a, L-fin all addressed; S-invariants discharged via K.λ frame conditions. The L14a verification correctly distinguishes the emitter address from endset target addresses.

Depth: Consequences sections present for R2, R3, R4, R5, R6c with [COROLLARY]/[POLICY]/[ARCHITECTURE] typology. Concrete worked sketch with explicit tumblers (`a₁ = 1.0.1.0.1.0.2.1`, etc.). Two wp computations with regime analysis. Properties Introduced table summarizes deliverables.

Scope: The ASN defines abstract state (typed relations as views), operations (Emit_K, Observe_K, Nullify), and invariants (R0–R7a). It does not drift into implementation territory.

The two routes for R0a-Cor2 (TA5(c)+TA5-SigValid; ChainPrefixExtension) provide robust redundancy. The wp Case 2's three-regime structure correctly identifies (i) unit-depth discipline, (ii) crafted-span retractions, (iii) self-nullifying R-typed emission as orthogonal concerns and yields a correct conjunctive wp. The relational-layer discharge of regimes (ii) and (iii) is correct: Nullify-as-sole-R-producer + unit-depth shape force the simplified form.

The R6a circular-looking step (using L11a at Σ as IH) is correctly framed as inductive — invariants hold at reachable states by inductive preservation, and R0/R6a is the inductive step.

## REVISE

(none)

VERDICT: CONVERGED
