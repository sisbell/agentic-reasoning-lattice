# Channel Assignment — ASN-0121 review-13

**Date:** 2026-06-09 01:59

## Issue 1: H-component spans cited as denoting subtrees without the unit-depth condition PrefixSpanCoverage requires
Reason: The mathematical gap (PrefixSpanCoverage's unit-depth precondition) is internal, but resolving it requires a design decision the ASN cannot settle alone — whether the home-set was intended as prefix-only (subtree) specifications or general span-sets. That is Nelson's design intent. Gregory cannot adjudicate, since the back end ignores the home-set entirely (dead-code guard), so it provides no evidence on the intended H span shape.
Nelson question: Was the home-set of FINDLINKSFROMTOTHREE intended to bound residence only by whole-subtree prefixes (node/account/document), or may it carry arbitrary-width spans denoting sub-document residence ranges?

## Issue 2: FL-WILD table entry says all-wildcard links are "matched on" their endsets
Reason: Pure wording fix derivable from the ASN itself — the FL-WILD prose already states the correct distinction (all-wildcard admits without consulting endsets; only constrained requests match on the first three), so the table entry just needs to align with the prose. No design intent or implementation evidence is required.
