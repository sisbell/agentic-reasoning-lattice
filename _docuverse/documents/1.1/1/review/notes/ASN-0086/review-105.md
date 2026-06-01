# Review of ASN-0086

## REVISE

### Issue 1: WP Case 1 omits the substrate-conformance conjunct its sufficiency argument requires

**ASN-0086, Weakest-Precondition Analysis, Case 1**: "`wp(Nullify(Σ, d_retr, a), single-tuple scope at Σ') ≡ P0(Σ, d_retr) ∧ P1(Σ, a)`"

**Problem**: The sufficiency half discharges the "no other link address falls within `{t : a ≼ t}` at Σ'" requirement by citing "the result proved absolute under R0a." But R0a holds only at *substrate-conforming* states. The note deliberately maintains a distinction between the full state space and the conforming subset — the Emit_K function-ness Lemma explicitly states it "holds over the full state space rather than only at substrate-conforming states." So Σ here ranges over the full state space, where non-conforming states exist.

Counterexample to weakest-ness: take a non-conforming Σ with `a, a'' ∈ dom(Σ.L)`, `a ≼ a''`, `a'' ≠ a`. Then P0 ∧ P1 holds, but after Nullify, `a''` persists (L12a) and `{t : a ≼ t} ∩ A_rel^{Σ'} ⊇ {a, a''} ≠ {a}` — the postcondition fails. Hence `P0 ∧ P1` is sufficient only under conformance, so it is *not* the weakest precondition as written.

**Required**: Add the conjunct `Σ substrate-conforming` to the Case 1 wp (it excludes the pre-existing-nested-pair pre-state via R0a at Σ), or declare substrate-conformance a standing assumption of the WP section and reconcile it with the function-ness Lemma's explicit full-state-space scope. (Case 2's general four-conjunct form is self-contained via the direct `NoCraftedSpanReachesD` universal and does not have this gap; only the regime-(i) simplification leans on R0a.)

### Issue 2: Meta-prose in the substrate-conforming-layer Invariant Catalog clause

**ASN-0086, Definition — substrate-conforming layer, clause (a)**: "This catalog already subsumes the `Link`-record value-shape commitments: L5 (EndsetSetSemantics) and L6 (SlotDistinction) are themselves ASN-0043 invariants, and L8 (TypeByAddress) is the ASN-0043 link-model definition every conforming state obeys; **they are listed here only to make the value-shape content of the catalog explicit, not as a strengthening of it**."

**Problem**: This is a use-site inventory plus a defensive justification ("listed here only to make explicit, not as a strengthening") — the `review-mode.anti-bloat` pattern. It explains why items appear rather than advancing the definition. If L5/L6/L8 are already subsumed by the named catalog, naming the catalog suffices.

**Required**: Delete the L5/L6/L8 enumeration and the "listed here only…" clause; clause (a) need only name the ASN-0036/0043/0093 catalog it adopts.

### Issue 3: The two substrate-conforming definitions restate the same two clauses

**ASN-0086, Definition — substrate-conforming state** vs. **Definition — substrate-conforming layer**: the state definition gives clause (a) invariant-preservation and clause (b) frontier-emission; the layer definition re-enumerates the identical (a)/(b) pair, with (a) reduced to "the same catalog named in clause (a) of the Definition — substrate-conforming state, with no additional condition imposed at the layer level," and closes with "Clauses (a) and (b) here are exactly the two conditions of the Definition — substrate-conforming state."

**Problem**: Two paragraphs in different sections say substantially the same thing in different words (flagged anti-bloat pattern). The load-bearing content unique to the layer definition is only: (b) is imposed as an *obligation*, and layer-conformance implies post-state state-conformance.

**Required**: Collapse the layer definition to its sole non-redundant content — "a layer is substrate-conforming iff every operation it publishes carries conforming states to conforming states (clauses (a)/(b) of the state definition), discharged by emitting fresh link keys at the home sibling frontier" — without re-enumerating the catalog.

## OUT_OF_SCOPE

### Topic 1: Substrate-level retraction K-operation with shape constraint
The final open question (elevating the unit-depth retraction discipline to a substrate guarantee) is correctly deferred — it would require a new K-operation contract in ASN-0093, not a revision here.

META:

VERDICT: REVISE
