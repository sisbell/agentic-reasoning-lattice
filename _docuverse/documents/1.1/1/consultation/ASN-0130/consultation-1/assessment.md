# Channel Assignment — ASN-0130 review-1

**Date:** 2026-06-12 08:17

## Issue 1: The merged-span F is not address-denoting — condition (iv), PR1's statement, and the PR5 lint all break on it
Reason: The defect and both repair options (Multi-shape with G=enc(A_def), or coverage-based start-resolution) live entirely in the corpus's own formal machinery — AD, ShapeConformance, and QD from ASN-0126/0128. The `pdef` tuple is this note's invention with no counterpart in Nelson's design or udanax-green, so the fix is internal.

## Issue 2: Identity-by-start is not well-defined — injectivity does not give prefix-freeness, and expansion's address-to-term resolution is never specified
Reason: The encoding is explicitly a substrate parameter of this note's own discipline, and the resolution procedure, prefix-freeness fix, and shift/inc identity (TA5(c)/OrdinalShift, ASN-0093) are all derivable from the ASN plus its dependency cone. Internal fix.

## Issue 3: The emission route is unspecified and the idem=⊤ dedup claim has no operative mechanism
Reason: Pinning `register_pred`'s contract is a question about ASN-0128's Emit_K/I1/I1a/K.λ_sh machinery — protocol-layer constructs defined within the corpus, with the `Nullify_Binary` wrapper precedent already available as the template. Neither external channel has evidence on these.

## Issue 4: "Registered signature" and reference application are never defined
Reason: Signatures, an application typing rule, and substitution discipline are extensions to ASN-0129's PL, a language this lattice defines; neither Literary Machines nor udanax-green contains a predicate language to consult. The fix is internal language design constrained by ASN-0129's WT and PC rules.

## Issue 5: Registration's success postcondition ignores born-nullified deposits, and the note's operations get no wp analysis
Reason: The born-nullified condition (C3, RangeSterilization) and the wp derivation pattern (WP, I6, DR) are fully established in ASN-0126/0128; the fix is mechanical application of that framework to the note's two operations. Internal.

## Issue 6: PR1's transfer citation does not establish the claim as stated
Reason: The finding itself supplies the correct chain — per-step content clauses (C0, ASN-0093), B2's transition-invariant clause, RP-b, induction — all in-corpus. This is citation plumbing, derivable without external grounding.

## Issue 7: PR2's strict-precedence argument assumes one registration event per definition; the note's own de-registration semantics breaks that assumption
Reason: The earliest-successful-registration restatement is sketched in the finding and uses only the note's own de-registration/re-registration semantics plus the active-slice dedup rule (I2, ASN-0128). Internal proof repair.
