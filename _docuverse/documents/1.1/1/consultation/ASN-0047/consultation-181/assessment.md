# Channel Assignment — ASN-0047 review-181

**Date:** 2026-05-31 22:59

## Issue 1: "Why-needed" rationale prose around K.δ conjuncts does not advance the spec
Reason: Pure prose deletion and direct restatement of inc-chain conformance; the conjuncts and FrontierEquivalence already carry the load, and L1c's chain is already fully specified in the ASN. No design intent or implementation evidence required.

## Issue 2: Two cross-layer properties stated in one section, proved in another, with explicit deferral prose
Reason: Structural reorganization — relocating P4a/P7a statements to their proof site and collapsing duplicated Class (b) framing. Both properties and their derivations are already fully present in the ASN; this is an internal editorial move.

## Issue 3: Worked-example enumeration of excluded attempts is reviser-drift
Reason: Editorial trimming of redundant guard re-application; the preconditions cited already appear in the ASN's K.δ definition. Derivable from the ASN alone.
