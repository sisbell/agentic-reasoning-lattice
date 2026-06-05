# Channel Assignment — ASN-0100 review-76

**Date:** 2026-06-05 04:30

## Issue 1: Forward-reference deferral and document-ordering justification for INS.M-exhaustive
Reason: Purely editorial — removing placement/ordering commentary and letting the existing proof stand requires no design intent or implementation evidence; the proof already lives in the ASN.

## Issue 2: Identity-by-allocation restated three times
Reason: Consolidation of a proposition already fixed by INS.C and INS.alloc within the ASN; deduplication is internal and needs no external channel.

## Issue 3: Worked-example stipulation imagines out-of-scope pre-states
Reason: The fix removes out-of-scope speculation and restates the chain-shift applicability condition already present in the ASN; no design intent or code evidence is needed.

## Issue 4: Meta-prose explaining why a lemma does *not* apply
Reason: Editorial removal of rejected-alternative signposting; the operative lemmas (C1a, the S4 argument) are already cited and discharged in the ASN.

## Issue 5: Worked example asserts "specialises INS.proj" without exhibiting π
Reason: Numerically instantiating INS.proj's own formula against the existing worked-example values is fully derivable from the ASN's definitions of π and N_{ℓ,i}; no external channel required.
