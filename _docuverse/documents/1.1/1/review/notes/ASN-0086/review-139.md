# Review of ASN-0086

## REVISE

### Issue 1: R0's L-invariant discharge asserts `#E(a) = 2`, which is false over R0's own domain

**ASN-0086, R0 — TupleAddressFreshness, "L-invariant preservation across the K.λ-step":** "The address-structural L-invariants at `a` — L0 (`E(a)₁ = s_L`), L1 (`zeros(a) = 3`), L1b (`#E(a) = 2 ≥ 2`), and `home(a) = d ∈ dom(Σ.M)` for L1a — were already established in the freshness bullets above (... subsequent branch by the *well-formedness* bullet, which carried `zeros`, `E(·)₁`, and `origin` across the single `inc(·, 0)` step)."

**Problem:** R0 is stated and proved over **state-local-conforming** states, which the note explicitly says "need *not* satisfy ... R0a's antichain" and which include the `Remark — NestedLinkWitness` states where a link `a''=inc(a,1)` has `#E(a'') = #E(a)+1 ≥ 2`. In the subsequent-emission branch, `a = inc(ℓ_prev, 0)`, and the well-formedness bullet establishes only `#a = #ℓ_prev`, hence `#E(a) = #E(ℓ_prev)`. If `ℓ_prev` is a nested witness with `#E(ℓ_prev) = 3`, then `#E(a) = 3 ≠ 2`. The parenthetical "`#E(a) = 2`" is the substrate-conforming fact (R0a-Cor1), silently imported into a proof whose domain is strictly larger. `#E(a) = 2` is **not** what the well-formedness bullet established, contrary to the cited justification.

**Required:** State L1b's discharge as it actually follows: first branch `#E(a) = 2` (FirstEmission); subsequent branch `#E(a) = #E(ℓ_prev) ≥ 2`, with the `≥ 2` supplied by L1b holding at Σ (a state-local invariant). The conclusion (L1b holds) survives; the justification "`#E(a) = 2`" must be corrected for the subsequent branch.

### Issue 2: "frontier-landing consequence" is not a consequence of the at-most-one-key-per-home discipline

**ASN-0086, Definition — substrate-conforming state:** "Concretely, clause (b) rests on the **at-most-one-key-per-home discipline**: every transition ... deposits at most one fresh link key per home per step ... Its **frontier-landing consequence** is the index-contiguity fact: ... that key occupies exactly chain index `J+1` ... — no gap, no index skipped."

**Problem:** Frontier-landing does not follow from at-most-one-key-per-home. The note's own `Remark — NestedLinkWitness` exhibits a transition that adds exactly one fresh key at a home (`a'' = inc(a,1)`) yet lands *off* the sibling frontier (nested, not at chain index `J+1`). So at-most-one-per-home is satisfied while frontier-landing fails. Frontier-landing is therefore an independent constraint (it is clause (b)'s "next contiguous chain segment past the frontier" text), not a "consequence" of the at-most-one discipline. The "Its ... consequence is" wording — with "Its" reading against the immediately preceding "at-most-one discipline" — misattributes the entailment. R7a discharge (4)(iii) and L-ContiguousPrefix lean on frontier-landing, so the definitional structure here is load-bearing and must be stated cleanly.

**Required:** Present frontier-landing as a defining clause of substrate-conformance (it is clause (b)), not as a consequence of at-most-one-key-per-home. Make explicit that at-most-one-per-home is a separate, auxiliary commitment.

### Issue 3: Non-circularity justification prose in L-ContiguousPrefix (anti-bloat)

**ASN-0086, L-ContiguousPrefix proof:** "This proof rests only on conformance clause (b) and ASN-0093's chain machinery — it does not invoke R0a; hence R0a's same-home case may consume this lemma without circularity."

**Problem:** This is meta-prose justifying document/dependency ordering rather than advancing the proof — exactly the "prose justifies ... the forward pointer is non-circular by Y argument" pattern named in the accretion checklist. The dependency direction is already visible from what each proof cites; the sentence exists only to reassure the reader about circularity.

**Required:** Delete. If a dependency note is genuinely needed, it belongs in a one-line dependency annotation, not in the proof body.

### Issue 4: R0a Case 1 derives a direction the claim does not require (anti-bloat)

**ASN-0086, R0a — FlatLinkDomain, Case 1:** "R0a quantifies over *ordered* pairs `(a, a') ∈ dom(Σ.L) × dom(Σ.L)`, so the swapped pair `(a', a)` — equally distinct-home — instantiates the same argument and yields `¬(a' ≼ a)`; no separate derivation is required."

**Problem:** R0a's statement is the implication `a ≼ a' ⟹ a = a'`. Once Case 1 establishes `¬(a ≼ a')`, the implication is vacuously true and the proof is complete. The swapped-pair paragraph establishes `¬(a' ≼ a)`, which the claim's quantifier already covers by re-instantiation and which is not needed to discharge the implication for the pair `(a, a')`. This is the "a paragraph imagines a case the claim's ... already excludes" / redundant-exhaustiveness pattern.

**Required:** Remove the swapped-pair paragraph; `¬(a ≼ a')` alone discharges Case 1.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity of Emit vs. Observe, and ordering of Observe results
**Why out of scope:** These are raised in the Open Questions and concern a consistency model the note does not (and need not) define. They are future-ASN territory, not defects in this note's single-authority, sequential-transition model.

### Topic 2: Higher-arity typed relations `L_K^{(n)}` and dynamic type-address collision
**Why out of scope:** The note deliberately restricts to standard-triple links and flags higher-arity handling as future work. Not an error in the arity-3 development.

VERDICT: REVISE
