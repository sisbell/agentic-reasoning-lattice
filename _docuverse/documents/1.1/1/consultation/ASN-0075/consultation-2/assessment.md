# Channel Assignment — ASN-0075 review-2

**Date:** 2026-05-25 13:40

## Issue 1: D-DISCR construction omits K.ρ steps required for J1★
Reason: The fix is fully derivable from ASN-0047's frame rules already cited in the ASN — K.μ⁺ leaves R unchanged, K.ρ is the dedicated provenance-recording step, and the reviewer specifies exactly which K.ρ insertions to make. No design-intent or implementation evidence is needed.

## Issue 2: Worked example K.μ~(d_B) is the identity permutation
Reason: The fix is internal — K.μ~'s admissibility clause (ii) is a stated constraint in ASN-0047, and inspection of the M(d_B) state at that step shows the permutation is id, so removing the step suffices. No external channel needed.

## Issue 3: Worked example omits K.ρ steps
Reason: Same structural issue as Issue 1 — the K.ρ insertions are mechanically determined by ASN-0047's J1★ and frame rules, and the reviewer points to J4's fork composite as a worked template. Internal fix.

## Issue 4: D-ACT uses reflexive-transitive closure where equivalence closure is needed
Reason: This is a definitional/mathematical correction with two clearly stated options (symmetrize or take equivalence closure). The fix follows from standard set-theoretic reasoning; neither design intent nor implementation evidence bears on it.
