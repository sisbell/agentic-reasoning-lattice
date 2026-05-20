# Channel Assignment — ASN-0086 review-77

**Date:** 2026-05-19 18:29

## Issue 1: Numerical inconsistency in strict-strengthening argument
Reason: Pure tumbler-arithmetic check against the ASN's own length-computation conventions and the chain shown. Fix is either correcting `#d + 3 + 2` to `#d + 4` or extending the chain by one step — derivable from the ASN's own tumbler algebra.

## Issue 2: R0a Case 1 reverse direction is a substitution-claim, not a derivation
Reason: Proof-presentation issue internal to R0a. The fix is either carrying out the symmetric derivation in 2–3 lines or invoking a named symmetry lemma — no external channel input is needed.

## Issue 3: R0's substrate-invariant discharge omits ASN-0093 M/C invariants
Reason: The missing invariants (M0, M1, C0, C1, C1b, C1c, C-fin) are already enumerated in the ASN's own substrate-conforming layer Definition and discharge identically by K.λ's Frame on `(Σ.C, Σ.M)`. Internal symmetry fix.

## Issue 4: DEF-Consequence label used in Properties Introduced table but undefined in type-label key
Reason: Pure labeling-consistency fix. Either add DEF-Consequence to the key paragraph or relabel R6b as DEF — derivable from the ASN's own taxonomy choice.

## Issue 5: Worked Sketch does not exhibit a K.σ-prefix scenario
Reason: The fix adds an auxiliary worked step using K.σ and K.λ mechanics already defined in the ASN (and inherited from ASN-0093 SubAllocatorAxiom, already cited). All needed structure is on-page.

## Issue 6: L5/L6/L8 categorization in substrate-conforming catalog (a)
Reason: Categorization turns on whether L5/L6/L8 are state-bound invariants requiring per-step preservation or definitional commitments that hold by well-formedness. Resolving requires the ASN-0043 catalog's own treatment of these invariants, which the reviewer cites directly.
Gregory question: In ASN-0043's catalog, are L5 (EndsetSetSemantics), L6 (SlotDistinction), and L8 (TypeByAddress) stated as state invariants over `Σ.L` requiring preservation across transitions, or as definitional commitments / function definitions that hold wherever the link store is well-formed?
