# Review of ASN-0086

This ASN is mature and its proof obligations are, on the whole, discharged with real rigor — R0a's two-case antichain argument, R-Scope's arity-independence, and the wp Case 2 biconditional all hold up under scrutiny, and the Worked Sketch supplies concrete tumbler-level verification. The findings below are confined to accreted forward-reference/defensive prose that the `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: Step 4 parenthetical carries a clause irrelevant to its own point
**ASN-0086, Worked Sketch, Step 4**: "we note only, separately, that the call does not itself break the discipline — its to-span `{(a₃, δ(1, #a₃))}` is likewise unit-depth — yet it drives the disjunction false.)"

**Problem**: Step 4 exists to witness the wp Case 2 disjunction failing (`K ~ R` ∧ `a_emit ∈ coverage(G)`) while the home-precondition holds. Whether the call *breaks the unit-depth discipline* is orthogonal to that point — the disjunction falsification turns only on `K ~ R` and self-coverage, not on the to-span's shape. The clause preempts an objection the claim does not raise, and the surrounding parenthetical already over-explains ("This is *not* a relational-layer `Nullify`... The call is admissible... Σ_3 lies within the wp's domain... The new call's to-span shape is irrelevant to pre-state domain membership"). The reader must skip past this to follow the witness.

**Required**: Drop the "does not itself break the discipline" clause; the to-span-shape-irrelevance sentence already says all that is needed for domain membership.

### Issue 2: R0's "L-invariant preservation" paragraph duplicates RT-closure
**ASN-0086, R0 proof, final paragraph**: "By RT-closure, Σ' is `→*`-reachable. The invariants published in ASN-0093's K.λ contract (M*, C*, L0–L3, L12, SD, L-fin, C-fin) hold at the fresh key `a` by that contract directly."

**Problem**: The RT-closure definition already states the load-bearing fact: "Each `→`-step is a single K.σ/K.α/K.λ primitive, which preserves the full L/S/M/C invariant catalog (ASN-0036, ASN-0043, ASN-0093)." R0's conclusion needs only "Σ' is `→*`-reachable," which RT-closure delivers in one citation. The subsequent re-enumeration of the invariant catalog (and the "one obligation not closed structurally is..." sub-argument for L3/L14/L14a) re-derives what reachability already carries. This is the "two paragraphs say the same thing in different words" pattern compounding across cycles.

**Required**: Collapse to the RT-closure citation for reachability. If R5's downstream appeal ("R0's emission discharges every L-invariant except L3") genuinely needs more than reachability-implies-invariants, expose that as a one-line R0 postcondition rather than re-proving the catalog inside the body.

## OUT_OF_SCOPE

### Topic 1: Higher-arity typed relations
**Why out of scope**: `L_K` is confined to `|Σ.L(a)| = 3`; links of arity > 3 inhabit `dom(Σ.L)` but index no tuple. The note explicitly defers their relational treatment to Open Questions. Extending `L_K` to `℘(A)^n` is new territory, not a defect here.

### Topic 2: Substrate-level enforcement of the unit-depth retraction discipline
**Why out of scope**: The discipline is a layer commitment, and the wp Case 2 load-bearingness argument correctly shows why a direct K.λ caller can violate it. Whether to elevate it to a substrate K-operation with a shape constraint is already posed as an Open Question and belongs to a future ASN.

VERDICT: REVISE
