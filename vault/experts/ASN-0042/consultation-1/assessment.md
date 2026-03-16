# Revision Categorization — ASN-0042 review-1

**Date:** 2026-03-15 19:57

## Issue 1: O3 is falsified by delegation
Category: INTERNAL
Reason: The contradiction is between O3, O7, and O8 — all defined within the ASN. The counterexample is constructed entirely from the ASN's own definitions, and all three proposed resolutions (restrict, reformulate as monotonic refinement, or two-phase model) are derivable from the existing properties.

## Issue 2: O1a is false for finer-than-account prefixes, creating cascading inconsistencies
Category: BOTH
Reason: The resolution requires knowing whether Nelson intended document/version-level delegation to create full ownership principals (same status as account-level) or subordinate allocators, and whether Gregory's code has any ownership predicates operating below account granularity.
Nelson question: When you describe delegation at document and version levels ("Whoever owns a specific node, account, document or version may in turn designate new nodes, accounts, documents and versions"), do the delegates at document/version level hold the same kind of ownership authority as account-level holders, or is their authority a subordinate concept — allocator rights without full ownership standing?
Gregory question: Beyond `tumbleraccounteq`, does the udanax-green codebase contain any ownership or authorization check that discriminates at finer than account level — e.g., verifying that a session owns a specific document prefix before permitting operations on that document's elements?

## Issue 3: Injectivity of pfx required but unstated
Category: INTERNAL
Reason: This is a missing axiom in the well-definedness argument for O2. The fix is to add `pfx` injectivity as a stated axiom. No external evidence is needed — the gap is purely logical.

## Issue 4: O2 well-definedness relies on an implicit coverage axiom
Category: INTERNAL
Reason: The derivation path is already present in the ASN: O5 ensures allocation only occurs within an existing principal's domain, so every allocated address is born under a covering prefix. The fix is to make this derivation explicit rather than parenthetical.

## Issue 5: No concrete example
Category: INTERNAL
Reason: The ASN contains all definitions and properties needed to construct a worked example. This is a presentation gap, not a knowledge gap.

## Issue 6: O4 numbering gap
Category: INTERNAL
Reason: Editorial issue — either close the numbering gap or document the omission. No external input needed.
