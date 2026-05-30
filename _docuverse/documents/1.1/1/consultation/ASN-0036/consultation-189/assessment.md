# Channel Assignment — ASN-0036 review-189

**Date:** 2026-05-29 22:57

## Issue 1: Foundation properties referenced under invented names
Reason: Purely a renaming to match canonical foundation labels (T1 — LexicographicOrder, TumblerAdd — TumblerAdd); the correct names are already fixed in ASN-0034 and require no design intent or implementation evidence.

## Issue 2: S8's I-side "structural shape" claim is restated four times and pulls in dependencies it never uses
Reason: This is internal proof hygiene — the partition argument's actual dependencies are visible in the proof, and determining that `zeros = 3`/T4-validity is consumed by nothing is derivable from the ASN's own text.

## Issue 3: S2 postcondition adds nothing beyond the partial-function axiom
Reason: Whether S2's postcondition restates the `T ⇀ T` declaration, and how to reformulate or fold it, is entirely a matter of the ASN's own definitions and contract structure.
