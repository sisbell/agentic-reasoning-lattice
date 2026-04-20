# Revision Categorization — ASN-0042 review-4

**Date:** 2026-03-15 21:19

## Issue 1: O8 formalization admits the pre-delegation state, where the claim is false
Category: INTERNAL
Reason: The fix is replacing `→*` with `→⁺` — a formalization correction derivable from the ASN's own prose ("never *regains*") and the definition of `delegated_Σ` condition (iii).

## Issue 2: O6 derived guarantee `pfx(ω(a)) ≼ acct(a)` stated without derivation
Category: INTERNAL
Reason: All three ingredients — definition of `ω`, O1a, and definition of `acct(a)` — are already present in the ASN. The derivation is a chain of facts already stated.

## Issue 3: O4 inductive argument omits the preservation step
Category: INTERNAL
Reason: The missing step requires only O12 (principal persistence) and O13 (prefix immutability), both already stated as axioms in the ASN. One sentence combining them closes the induction.
