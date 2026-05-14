# Channel Assignment — ASN-0042 review-40

**Date:** 2026-05-14 05:23

## Issue 1: O3's dependency list omits O15 and O14
Reason: Pure bookkeeping fix — the proof body already cites O15 explicitly and relies on O14 for the iterated-O12 reachability argument. The required dependencies are derivable from reading the proof against the table.

## Issue 2: O8's dependency list omits O15
Reason: Same pattern as Issue 1 — the proof body explicitly invokes O15 (PrincipalClosure) for the "π' can enter Π only via the delegation transition" step. Table-vs-proof bookkeeping; no external evidence needed.

## Issue 3: PrefixBaptismCoupling's dependency list omits O13
Reason: The Case 1 (carry-forward) step in the proof explicitly applies O13 (PrefixImmutability). The fix is to align the dependency list with what the proof already cites.

## Issue 4: O8's "trajectory passes through Σ_d^{post}" argument is implicit
Reason: The reviewer has already articulated the explicit chain (condition (iii) + O12 monotonicity + uniqueness of introduction event). All cited properties are internal to the ASN; the fix is proof-rewriting with no new content.

## Issue 5: Worked example's hwm = 5 is inconsistent with the explicit baptisms
Reason: The inconsistency is between the ASN's worked example and the `hwm`/`Bop` semantics already imported from ASN-0040 (B1 ContiguousPrefix, B6 ValidDepth). The fix — either narrate document-level baptisms at slots 1–5 or rebuild with smaller hwm — is derivable from the foundation citations already in this ASN.

## Issue 6: Properties Introduced entry for `acct(a)` misdescribes the construction
Reason: The ASN body defines `acct(a) = N(a) ++ [0] ++ U(a)` explicitly; the table entry just needs to be rewritten to match. Internal consistency fix.

## Issue 7: `dom(π)` notation collides with `dom(A)` from T10a
Reason: Notation choice within the authorial scope of the ASN. The reviewer offers two acceptable resolutions (rename or disambiguation note); the foundation reading from T10a is already documented in ASN-0034 and ASN-0040. No design-intent or implementation-evidence question is open.
