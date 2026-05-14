# Channel Assignment — ASN-0042 review-56

**Date:** 2026-05-14 11:14

## Issue 1: O7(c) postcondition only addresses condition (ii), not condition (vi)
Reason: The fix is internal — the ASN's own chain-construction proof already checks both (ii) and (vi) per link; the postcondition wording just needs broadening or an explicit note that (vi) is a separate re-checking obligation. No design intent or implementation evidence needed.

## Issue 2: O8 single-step "trajectory must pass through Σ_d^post" argument conflates two readings of `delegated_Σ`
Reason: This is a formal modeling clarification — choosing whether `delegated_Σ` denotes a witness to an actual transition or satisfaction of conditions at a state. The proofs are sound under the witness reading; a single sentence in the Delegation definition resolves the ambiguity. Internal.

## Issue 3: AccountField definition is stated in the prose, but Postcondition (c) is not separately verified against the `zeros(a) = 1` branch
Reason: The verification is already given inline in the AccountPrefix proof (Case `zeros(a) = 1`). The fix is to fold that justification into the AccountField specification's Definition or Postcondition (c) slot. Internal.

## Issue 4: Inductive preservation arguments for O1a, O1b, T4 are sketched but not laid out with explicit base/step over reachability
Reason: The fix is a closing sentence per preservation paragraph naming the O14 base case and trivial non-delegation step, matching the explicit pattern already used for FiniteRegistry and PrefixBaptismCoupling. Internal.

## Issue 5: SelfOwnershipAtPrefix verification at `a_6 = pfx(π_A)` references the general property but the *Worked Example* prose suggests it is being established there
Reason: Presentational — rename the worked-example paragraph or insert an opening sentence marking it as verification rather than derivation. The general property is already derived in the *Exclusivity Invariant* section. Internal.

## Issue 6: The Worked Example's Fork trajectory verification convention is stated, but at least one Bop call's preconditions are not exhibited in the running narrative
Reason: Presentational — either inline the namespace-baptism B6/B1 checks at the trajectory site or restate the verification convention to make the cross-paragraph deferral explicit before the cumulative Σ_2.B claim. Internal.
