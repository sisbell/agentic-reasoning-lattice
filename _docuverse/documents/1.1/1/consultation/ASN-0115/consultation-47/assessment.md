# Channel Assignment — ASN-0115 review-47

**Date:** 2026-06-10 04:24

## Issue 1: Depth-compatibility is folded into V-spec well-formedness as an undefined-state "minting-time requirement" that no claim uses
Reason: The fix is a self-contained formalization cleanup, derivable from the ASN's own content. The ASN already defines `depthcompat(ρ, Σ)`, already routes the operative depth check through the `act` consulting-state override, and already has claims R0–R11 that reference only `act` — so dropping the redundant, ill-defined minting-time gate from V-spec well-formedness and collapsing the prose into the single `act` definition preserves the constraint's operative role and changes no behavior. No design-intent question arises (the constraint stays, only its framing is simplified) and no implementation evidence is needed (the reviewer confirms the claims are unaffected).
