# Channel Assignment — ASN-0125 review-12

**Date:** 2026-06-13 11:27

## Issue 1: EL6(v) asserts discipline preservation without the argument that EL-DM and EL12 rely on
Reason: Fix is internal — every ingredient of the required argument is already in the ASN (Df-DISC(ii)'s claim schema, ASSERTop's precondition `x ≠ y` and `x, y ∈ dom(Σ.L)`, Vocabulary fact V's domain monotonicity, L12), and the structurally identical proof is already written out at EL7(vi).

## Issue 2: EL11(b) states a conditional equality unconditionally
Reason: Fix is internal — the correction is a formal tightening using machinery already present: the antichain collapse `old(e) ≼ y ⟺ old(e) = y` needs `y ∈ dom(Σ.L)` (R0a, cited throughout), EL4 supplies the coverage computation, and ASN-0086's `Observe_K` semantics is taken as given in the substrate section.

## Issue 3: EL-DM's statement and its Df-DISC lead-in carry use-site inventory and meta-prose around a forward reference
Reason: Fix is internal and purely editorial — strip the five-site use-inventory and the "we owe a demonstration / we assemble it" roadmap framing, leaving EL-DM's existing base/step proof intact; no design intent or implementation evidence is at issue.

## Issue 4: The "menu was shorter than it looked" remark restates eliminations already established in EL2 and EL3
Reason: Fix is internal and purely editorial — replace the redundant value-space/address-space RQ re-enumeration with back-references to EL2(b)/(c) and EL3, keeping the collapse insight and the already-quoted Nelson LM 4/29 framing that are present in the text.
