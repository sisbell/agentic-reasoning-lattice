# Channel Assignment — ASN-0075 review-55

**Date:** 2026-06-03 09:31

## Issue 1: D-SUBSP proves an impossibility about a case the operation's domain already excludes
Reason: Internal fix — collapsing the witness-impossibility contradiction proof into the one-line consequence of `output ⊆ dom(C)` is a restructuring derivable entirely from the ASN's own definitions (L14, the output set-builders); no design intent or implementation evidence is at stake.

## Issue 2: Worked example reuses the K.δ account-bundling shorthand without re-establishing it
Reason: Internal fix — the account-then-document bundling shorthand is already defined within the ASN (D-DISCR section); re-stating or citing it at the worked example's setup is a self-contained editorial correction.

## Issue 3: Defensive construction-justification prose in D-DISCR
Reason: Internal fix — dropping meta-justification sentences and trimming redundant bundle-pattern restatements is pure prose pruning derivable from the ASN alone.

## Issue 4: D-BOUND dressed as an "axiom" with prose about how it discharges a hypothesis
Reason: Internal fix — relabeling D-BOUND as the operation's boundary precondition and dropping the "axiom"/"discharges structurally" framing is a terminology correction; D-WIT and D-EXH already carry the composite-boundary hypothesis explicitly within the ASN.
