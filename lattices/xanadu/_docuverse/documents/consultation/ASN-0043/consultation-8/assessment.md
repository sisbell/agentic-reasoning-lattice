# Revision Categorization — ASN-0043 review-8

**Date:** 2026-03-17 00:51



## Issue 1: L11 non-injectivity formal statement is universally quantified but should be existential
Category: INTERNAL
Reason: The correct existential formulation is already present in the prose and witness construction within the ASN. The fix is replacing the formal statement with the existential version the proof actually establishes — no external evidence needed.

## Issue 2: L9 proof cites wrong finiteness property
Category: INTERNAL
Reason: The fix requires replacing an incorrect citation (S8-fin) with a correct argument from properties already established in ASN-0034 and ASN-0036 (T0(a), T9, S7a). All necessary reasoning is internal to the existing ASN stack.

## Issue 3: L9 proof omits verification of six properties
Category: INTERNAL
Reason: The six omitted properties are all trivially verified from definitions and lemmas already present in the ASN. The fix is adding a single acknowledgment line — no external evidence or design intent needed.
