# Channel Assignment — ASN-0086 review-146

**Date:** 2026-06-01 03:22

## Issue 1: R7a's proof invokes L-ContiguousPrefix at Σ' without requiring the pre-state Σ to be substrate-conforming
Reason: The fix is internal — the required hypothesis ("Σ substrate-conforming") and the layer's preservation property that derives Σ' conformance are both already defined in the ASN (Definition — substrate-conforming layer, L-ContiguousPrefix's own induction). No design intent or implementation evidence is needed; the gap is a missing hypothesis the existing machinery supplies.

## Issue 2: Definition — Nullified carries a defensive justification enumerating a downstream consumer
Reason: Pure editorial trim — removing meta-prose that names a downstream consumer. Derivable from the ASN alone.

## Issue 3: Emit_K Definition states the type-index/value-argument distinction twice
Reason: Pure editorial de-duplication within one Definition block. Derivable from the ASN alone.
