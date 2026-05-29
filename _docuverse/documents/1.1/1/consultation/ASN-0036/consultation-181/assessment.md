# Channel Assignment — ASN-0036 review-181

**Date:** 2026-05-29 06:23

## Issue 1: S2 introduced purely as a citable restatement of the type declaration
Reason: Purely editorial — strip the use-site meta-prose and restate S2 as its plain content. The fix touches only wording of an existing property; no design intent or implementation evidence is in question.

## Issue 2: S8a is a duplicate of the domain-restriction axiom, flagged as such in its own prose
Reason: Internal consolidation — fold the per-component form into the domain-restriction axiom or strike the "restated per-component for citation" framing. The equivalence to `zeros(v)=0` is already grounded in T0 (ASN-0034); no external channel needed.

## Issue 3: S8 Case j = m re-derives a foundation result inline that its own Depends already packages
Reason: Internal de-duplication — collapse the inline NAT-discrete promotion to the single named dependency already in the Depends list, or vice versa. Both the step and its packaging are present in the ASN; the fix is a citation choice.
