# Channel Assignment — ASN-0036 review-92

**Date:** 2026-05-11 04:34

## Issue 1: NAT-discrete citation missing from S8's Depends
Reason: Pure citation hygiene — the NAT axioms invoked at each "(NAT)" annotation are already defined in ASN-0034. The fix requires only auditing the proof body against ASN-0034's NAT-* catalog and adding the missing references to Depends lists.

## Issue 2: S8's auxiliary lemma derives more than its stated postcondition claims
Reason: The proof body already establishes the field-structure preservation facts (`zeros = 3`, `#E ≥ 2` preserved across shifts), and T4's `t_{#t} ≠ 0` clause is defined in ASN-0034. The fix is to lift these derived facts into explicit postconditions and cite T4's existing clause — no external channel needed.
