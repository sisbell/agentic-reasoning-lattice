# Review of ASN-0036

This is a strong, well-structured note. The core proofs (S1, S4, S5, S7, S8, D-CTG-depth, D-SEQ) are sound: S8's within- and across-subspace uniqueness via the incompatibility lemma + T5/T10 holds up, the D-CTG-depth infinite-intermediate construction correctly contradicts S8-fin, and the empty-document edge case is handled vacuously throughout. No cross-ASN violations (all references are to foundation ASN-0034). The findings below are the anti-bloat/clarity items the `review-mode.anti-bloat` classifier asks me to surface, plus one rigor clarification.

## REVISE

### Issue 1: S8-fin restates "finite" three times
**ASN-0036, S8-fin**: "For each document d, `dom(Σ.M(d))` is finite. A document contains finitely many V-positions at any given state. This is a design requirement on every reachable state: no document arrangement is permitted to hold infinitely many V-positions."
**Problem**: Three consecutive sentences assert the same proposition (`dom(M(d))` finite). The second and third add no information beyond the axiom. This is the "two paragraphs say the same thing in different words" pattern.
**Required**: Keep the axiom statement and one sentence of intent; drop the redundant restatements.

### Issue 2: S2 duplicates non-injectivity across postcondition and frame, with a same-document deferral
**ASN-0036, S2 Formal Contract**: postcondition reads "distinct V-positions may collide in the range (the map is not injective — see Frame)"; the Frame then reads "Distinct V-positions may map to the same I-address (sharing — S5); injectivity is *not* asserted."
**Problem**: Non-injectivity is stated twice, and the "see Frame" pointer is a deferral to a slot in the same contract that merely repeats the same fact. Skipping between slots to read one claim twice is noise.
**Required**: State non-injectivity once (in the Frame, where it belongs), and remove the "see Frame" cross-pointer from the postcondition.

### Issue 3: ValidInsertionPosition restates "m is read from state, not a parameter" twice
**ASN-0036, ValidInsertionPosition**: the Definition prose says "The common V-position depth `m` of V_1(d) is fixed by S8-depth and read from state — it is *not* a parameter of the predicate"; the Formal Contract Signature repeats "The common V-position depth `m` is determined by `d` via S8-depth and read from state."
**Problem**: The same clarification appears in the definition and again in the signature. One placement suffices.
**Required**: Keep the statement in the Signature (the structural slot for it) and drop the duplicate from the prose, or vice versa.

### Issue 4: S5 vacuous-transition witness needs one sentence of justification
**ASN-0036, S5 proof**: "we exhibit `Σ_N` as an isolated state with no incident transition, so the universal quantification is vacuous. S0 ... and S1 ... quantify over state transitions `Σ → Σ'` and therefore hold vacuously of `Σ_N`."
**Problem**: S0 and S1 are conditionals universally quantified over transitions; discharging them by positing a state with *no* incident transitions is a legitimate consistency-model move, but the proof asserts it without noting that a consistency/non-entailment claim is satisfied by *any* model of S0∧S1∧S2∧S3 (the witness need not be a reachable state of a particular operation set). As written, a careful reader pauses to check whether a no-transition state is admissible.
**Required**: Add one sentence stating that S5 is a non-entailment result, so a model in which S0/S1 hold vacuously is a sufficient witness — i.e., the construction shows consistency, not reachability.

## OUT_OF_SCOPE

### Topic 1: Operation-level preservation of D-CTG/D-MIN/S2
The final Open Question already routes INSERT/DELETE/COPY/REARRANGE preservation obligations forward; these belong to the operation ASNs per the stated Scope. No action needed here — flagged only to confirm the routing is correct, not as a defect.

VERDICT: REVISE
