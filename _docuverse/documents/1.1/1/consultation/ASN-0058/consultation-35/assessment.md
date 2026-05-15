# Channel Assignment — ASN-0058 review-35

**Date:** 2026-05-15 00:29

## Issue 1: M16a's citation of S7d for T4-validity is misplaced
Reason: The fix is a citation correction internal to ASN-0036's structure. S7d covers document tumblers; T4-validity for `dom(C)` is licensed by the framework-level T10a-conformance assumption already named in S4/S7 — both visible in ASN-0036 without further evidence.

## Issue 2: Set D is used without formal definition
Reason: The fix is definitional cleanup using existing state vocabulary (`M(Σ, d)` from ASN-0036). The required formalization — `D(Σ) = {d : M(Σ, d) is defined}` — is derivable from the ASN's own framing.

## Issue 3: ContentReference precondition (iv) `m ≥ 2` is redundant
Reason: The redundancy proof composes S8a (`#v ≥ 2`) and S8-depth (common depth) from ASN-0036 — both already cited. The derivation is structural and internal.

## Issue 4: M-int's Component-m reduction does not handle `k = 0` explicitly
Reason: The case split uses OrdinalShiftBase (this ASN's convention), T3, and TumblerAdd (ASN-0034) — all already invoked elsewhere in M-int. Pure proof completion.

## Issue 5: M15's supporting argument does not address the claim it supports
Reason: The required reformulation is a structural frame condition over M6f/M7f, which the ASN already states. The fix consists of relocating the justification within existing material; no external evidence or design-intent question is needed.

## Issue 6: Forward references compromise structural ordering
Reason: Reordering M16a before M6 (or factoring M6(d) into a corollary) is purely an organizational restructuring within the existing content.
