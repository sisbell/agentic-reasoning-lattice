# Revision Categorization — ASN-0026 review-3

**Date:** 2026-03-08 00:42

## Issue 1: P7 quantifier admits CREATENEWVERSION violation
Category: INTERNAL
Reason: The fix is a quantifier restriction to pre-state documents. The corrected formulation is fully specified in the review and derivable from the ASN's own definitions of Sigma.D and CREATENEWVERSION.

## Issue 2: P7 "applied to" is ambiguous for COPY
Category: INTERNAL
Reason: The ASN already describes COPY as writing to a target document (operations table: "Inserts mappings to existing I-addresses"). The fix is a definitional clarification — restating P7 in terms of "write target" — derivable from the ASN's own operation descriptions.

## Issue 3: P4 derivation misses nesting-prefix case
Category: INTERNAL
Reason: ASN-0001 already provides GlobalUniqueness as a lemma covering all cases including nesting prefixes. The fix is replacing the incomplete two-case derivation with a direct citation of that existing lemma.

## Issue 4: P9 does not require injective mapping for new positions
Category: INTERNAL
Reason: The injectivity requirement follows from the ASN's own P4 (distinct allocation acts produce distinct addresses) and its observation that INSERT creates one V-mapping per fresh address. The fix is adding an explicit injectivity clause that the ASN's own reasoning already demands.
