# Channel Assignment — ASN-0123 review-13

**Date:** 2026-06-13 01:39

## Issue 1: The VD biconditional is false, by the ASN's own severance theorem
Reason: The fix is internal consistency — the ASN already proves the correct scope (V9's severance theorem makes `¬(d_src ≼ v)` a theorem for cross-owner forks, and V7 already states such forks fall in "neither `S(d,1)` nor `{e : d ≺ e}`"). Restricting the biconditional to address-encoded derivation requires only the `derives` definition, V9, and S1/StreamPrefix, all present in the note; the reviewer even supplies acceptable forms.

## Issue 2: The operation's domain restriction is disclosed in prose but absent from the precondition list
Reason: The fix is purely placement — the restriction `(ω(d_src) = π ∨ zeros(pfx(π)) = 1)` is already derived and justified within the ASN (the identity clause and V-WF establish why the node-tier non-owner path is excluded), so elevating it to a bulleted precondition surfaces a constraint the note already states, with no new design intent or implementation evidence required.
