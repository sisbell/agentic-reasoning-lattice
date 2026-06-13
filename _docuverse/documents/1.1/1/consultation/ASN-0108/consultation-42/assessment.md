# Channel Assignment — ASN-0108 review-42

**Date:** 2026-06-13 06:30

## Issue 1: The "no re-delivery" cursor-advance induction is stated twice, with an explicit forward-deferral announcement
Reason: Purely structural/expository — the induction is already present (twice) in the ASN; the fix consolidates it into W5 and replaces the W9b copy with a citation, dropping the meta-prose announcement. No design intent or implementation evidence is at stake, only the document's own organization.

## Issue 2: W9's "global guarantee" paragraph re-derives W5's clause-1 analysis instead of citing it
Reason: Purely expository — the clause-1 sufficiency/non-necessity, cancellation, and cut-point-failure mechanics are already established in W5 (and already cited from W9); the fix trims the redundant re-derivation down to W9's local-vs-global distinction and obtains the rest by citation. Derivable from the ASN alone.
