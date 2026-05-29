# Channel Assignment — ASN-0036 review-174

**Date:** 2026-05-29 05:39

## Issue 1: S5's "genuine strand state" checklist omits several always-on invariants
Reason: Internal fix. The omitted invariants (S7a, S7d, S8-depth, D-CTG, D-MIN) are all defined within this ASN; verifying them against the two explicit witness constructions, or precisely defining "genuine strand state," is a mechanical check derivable from the ASN's own content.

## Issue 2: S8a is a renamed restatement of the domain-restriction axiom, with re-derivation prose
Reason: Internal fix. The ASN itself establishes the equivalence via T0; consolidating to one canonical statement is a purely editorial decision requiring no external evidence or design intent.

## Issue 3: S7a axiom buried under justification prose
Reason: Internal fix. Trimming justification prose down to one motivating line uses material already present in the ASN (the existing Nelson quote and axiom statement); no new design intent or implementation evidence is required.
