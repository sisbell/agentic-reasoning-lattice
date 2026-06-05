# Channel Assignment — ASN-0102 review-25

**Date:** 2026-06-05 08:08

## Issue 1: Standalone-composite restriction imposed for proof convenience, not justified intrinsically
Reason: The formal provenance discharge (whether P4★ can be re-established mid-composite) is internal, but deciding whether the restriction is intrinsic or an artifact needs design intent (was COPY meant to be a standalone act?) and evidence (does the implementation ever compose copy with other operations atomically?).
Nelson question: Was the COPY/inclusion operation intended to stand alone as its own atomic act, or to be composable as a step within a larger editing transaction?
Gregory question: In udanax-green, is `docopy` ever invoked as a non-final sub-step inside a larger atomic transaction, or is it always issued as a standalone operation?

## Issue 2: Meta-prose roadmap in "The cardinal question"
Reason: Pure structural-prose removal; the three sub-questions are answered by X1–X16, so deleting the roadmap framing is derivable from the ASN's own content.

## Issue 3: X15 parenthetical explains why a design choice is needed rather than stating the claim
Reason: Deletion of justification-of-axiom prose; the claim is already established by the preceding sentence, so the fix is internal.

## Issue 4: X15 restates X10(b)'s snapshot-resolution argument
Reason: De-duplication against X10(b), already present in the note; replacing the re-derivation with a cross-reference is internal.

## Issue 5: Closing essay recapitulates conclusions
Reason: Trimming a recap of results already proven in X1–X16 while keeping the substantive COPY/K.μ⁺ distinction; entirely derivable from the ASN.
