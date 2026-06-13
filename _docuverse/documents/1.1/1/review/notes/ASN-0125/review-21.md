# Review of ASN-0125

I checked the operation contracts (EL6, EL7), the discipline-maintenance induction (EL-DM), the monotonicity and frame claims, and the constructions (EL9-2, EL10, the worked example) against the foundations. The mathematics is sound: EL0's wp argument is correct, the `nullified` frame splits (unconditional vs. edit-disciplined) in EL6(iv)/EL7(iv) are each discharged, the (iv)→(vi) dependence in EL7 is non-circular, the EL11(a) projection biconditional and EL13 commutation are airtight, and every boundary I tried (empty store Σ₀, first/subsequent emission, fork, mutual-supersession standoff, registry churn, `j = n` last-link de-listing) is covered. The worked example checks against the contracts position-by-position. The one finding below is prose duplication flagged by the anti-bloat classifier, not a correctness gap.

## REVISE

### Issue 1: EL13 and EL14(d) state the same design conclusion in different words

**ASN-0125, EL13 (closing paragraph)**: "any global most-recent-wins rule is undefinable from state; any definable global tie-break ... carries no authority. The substrate will not manufacture a clock it does not have — so it cannot, even in principle, crown a winner among independent claimants. Adjudication is pushed where the design wants it: to readers, and to further, attributable claims."

**ASN-0125, EL14(d)**: "No canonical selector exists. Any selector is a function of the state; 'the most recently asserted' is not such a function across homes (EL13) ... What the layer owes the reader is therefore disclosure, not decision ... applied as the reader's declared policy, not the substrate's silent one."

**Problem**: These two paragraphs deliver the identical conclusion triple — *(a)* no global/canonical selector is a state function, *(b)* it carries no authority / forcing it would distort the record, *(c)* adjudication is the reader's. EL14(d) is the designated home for this conclusion (it is the "no canonical selector" sub-clause of CurrencyRelational, it already cites EL13 for the temporal input, and it is strictly more complete — it adds the fork dimension and the concrete disclosure content). EL13's version restates it, with the "will not manufacture a clock ... crown a winner" sentence adding metaphor and emphasis rather than a new fact. This is exactly the "two paragraphs in the same document say the same thing in different words" pattern the anti-bloat mode targets: a precise reader reaching EL14(d) re-reads EL13's close.

**Required**: Trim EL13's closing to the consequence that is *specific* to temporal erasure — cross-home claim order is not a state function, so no *temporal* selector ("most-recent-wins") is definable, while per-home order is recoverable from addresses (T9). Drop the clock metaphor sentence and the general "no canonical selector / adjudication to readers" essay, leaving that conclusion to EL14(d), which already owns and cites it.

## OUT_OF_SCOPE

None. The note confines itself to supersession; the adjacent operations listed in Scope (MAKELINK, FOLLOWLINK, READLINK, version/document operations, retrieval, replication) are not given claims, and the genuinely adjacent topics — retraction authority, supersession-of-retraction, meta-claims, span-level endset correspondence, edit/listing coupling, subtype-family closure — are correctly held as Open Questions rather than defined here. The EL9-2 and EL10 constructions use foundation transitions (K.μ⁻, K.μ⁺_L) to establish properties of the original-after-edit; they do not define new document operations, so they stay in scope.

VERDICT: REVISE
