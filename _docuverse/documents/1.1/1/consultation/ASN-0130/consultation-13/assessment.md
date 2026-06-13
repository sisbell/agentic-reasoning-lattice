# Channel Assignment — ASN-0130 review-13

**Date:** 2026-06-13 00:39

## Issue 1: The parameter reading does not cover ℕ-sorted parameters in PD0's aggregate rule
Reason: Internal. The soundness of extending the aggregate threshold from "ℕ literal" to "bound ℕ value" follows from PD0's own monotone-count ground (ASN-0129, quoted in the finding) plus PR5's existing fixity argument — both already in the corpus. PD0 is a synthesis construct rather than Nelson design intent, and udanax-green has no PD-certifier, so neither channel adds anything; the author selects option (a) and invokes the count-monotone ground directly.

## Issue 2: The certification-coverage lint conflates non-predicate definitions, which it can never exclude
Reason: Internal. Every fact the qualification needs is on the page: non-predicate registrability (PR0/PR-ENC/PR5a check (0)), check (0)'s outright certification-rejection, and PL's fixed read surface excluding result sort (ASN-0129's *Structural reads only* / PC4, cited in the finding). No design-intent or implementation evidence is required to add the caveat.

## Issue 3: Use-site inventory in PR-VIEW
Reason: Internal. Pure deletion of a redundant forward-reference; the dependency is restated at PR5/PR5a where it belongs, so removal is editorial and derivable from the ASN alone.

## Issue 4: The "substrate parameter" deferral is stated twice
Reason: Internal. Pure de-duplication — the scope section already carries the deferral (plus the non-redundant typing-decidability point), so dropping the PR-ENC aside is editorial and self-contained.
