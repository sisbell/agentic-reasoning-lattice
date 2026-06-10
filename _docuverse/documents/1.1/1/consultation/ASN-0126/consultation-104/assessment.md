# Channel Assignment — ASN-0126 review-104

**Date:** 2026-06-10 12:05

## Issue 1: Corollary RangeSterilization is stated in general form but proven only at the worked instance
Reason: Both remedies are formal work over material the ASN already cites — EmitAddress's two branches, L-ContiguousPrefix, the wp C3 conjunct, and R6c all come from ASN-0086, and the induction plus the no-other-coverage proviso are derivable from them; the design question of whether sterilization should be prevented is already parked in OQ7 and need not be resolved to fix the statement/proof mismatch.

## Issue 2: P-tgt is established at Σ but consumed at π(Σ) without the B1 carry
Reason: The fix is a one-line citation of B1, which the note itself establishes — both P-tgt disjuncts read only `A_rel` and `a_emit`, already shown B1-shared. Entirely internal.

## Issue 3: Ghost-root counterexample's exclusions rest on uncited foundations
Reason: The missing citations are to L1b (ASN-0043) and EmitAddress's branch shapes (ASN-0086), both prior-ASN results already in the note's reference set, and the bridge/B1 routing follows the note's own established pattern. No design-intent or implementation evidence is needed to add them.

## Issue 4: Abutting-spans witness — the interval-union equality is under-justified
Reason: The needed ordering facts (`a < m < b`) follow from T12 well-formedness / TA-strict, which the note already cites elsewhere (RegisteredAdmissible invokes exactly this postcondition); the fix is a one-line internal derivation.

## Issue 5: Forward-reference and justification accretion (anti-bloat)
Reason: Pure editorial deduplication — choosing which of the duplicate deferrals, justifications, and supersession statements to keep requires only the ASN's own text.
