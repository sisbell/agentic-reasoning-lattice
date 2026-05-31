# Review of ASN-0043

I checked the proofs of L1c (with CPP), FSP, FSE, L9 (Cases A and B), PrefixSpanCoverage, L10, the L8 equivalence/coverage machinery, and the six-step worked example against the foundation contracts (T4/T4a/T4b, TA5/TA5a/TA5-SigValid, T10a family, T12, OrdinalShift) and ASN-0036's S-invariants. The mathematics is sound: the chain constructions conform to T10a, the home-equals-seed derivation discharges correctly via the two CPP invocations, the interval-tiling in Step 6 (`[g,g') ∪ [g',h) = [g,h)`) is correct, and the L8 coverage discrimination/match cases check out. I did not re-raise the three previously declined findings (PrefixSpanCoverage promotion, L1b grounding, FSP/L1c conjunct derivation), each of which is adequately handled in the current text.

The remaining issues are the meta-prose / structural patterns this review mode is tasked with surfacing.

## REVISE

### Issue 1: Redundant paraphrase of the Nelson quote in L8
**ASN-0043, L8 — TypeByAddress**: Immediately after quoting Nelson — *"The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address."* — the next paragraph opens: *"Nelson's account grounds the choice: the type designation is consulted by address, not by what is stored there."*
**Problem**: This sentence restates the quoted material in the reviewer's words and advances no new reasoning; it is the "two adjacent passages say the same thing in different words" pattern. The reader must read it to discover it only re-says the quote before reaching the substantive Gregory evidence.
**Required**: Drop the paraphrase and let the Gregory sentence follow the quote directly (e.g., "Gregory confirms at the implementation level: …").

### Issue 2: Worked-example extension announces "six steps" but omits the Step 2 heading
**ASN-0043, Worked Example, "Extension"**: The intro states *"We extend the state in six steps, naming each intermediate state."* The headers present are *Step 1* (a'), then the meta-link `a₂ → Σ_2` block with **no "Step 2" heading**, then *Step 3* (a₃), *Step 4*, *Step 5*, *Step 6*.
**Problem**: The `a₂`/`Σ_2` construction — the L13 reflexive-addressing witness — is the second of the announced six steps but carries no step label, breaking the enumerated structure the section promises and forcing the reader to reconstruct which block is "step 2." This is a navigability defect in a slot that explicitly claims a numbered structure.
**Required**: Add a *"Step 2: adding the meta-link `a₂`"* heading at the `a₂` block so the six labeled steps match the six named states `Σ_1..Σ_6`.

## OUT_OF_SCOPE

### Topic 1: Global content-subspace invariant
The `s_C`-residence scoping of L9, L11b, L14, L14a is explicitly flagged in Open Questions. Promoting `s_C`-residence to a global content-side invariant (so disjointness covers all of `dom(Σ.C)`) is a content-model change belonging to a content/ASN-0036-side revision, not this link ASN.

VERDICT: REVISE
