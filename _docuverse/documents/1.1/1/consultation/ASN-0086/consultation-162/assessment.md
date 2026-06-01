# Channel Assignment — ASN-0086 review-162

**Date:** 2026-06-01 05:55

## Issue 1: P1-gates-postcondition-not-emission explained three times
Reason: Purely editorial deduplication — the fix is to state the gating distinction once in Definition — Nullify and have the other two definitions cite it. All content is already present in the ASN; no design intent or implementation evidence is needed.

## Issue 2: NestedLinkWitness separation gloss recurs as inline meta-prose
Reason: Editorial consolidation — the witness and strict-containment chain are fully developed in the Remark and definitions already; the fix replaces re-narration with a citation. Derivable from the ASN alone.

## Issue 3: Emit_K domain paragraph restates the containment already defined
Reason: Pure redundancy removal — the containment is stated verbatim in Definition — state-local-conforming state, so the trailing restatement in the Emit_K signature can simply be dropped with a citation. No external channel needed.
