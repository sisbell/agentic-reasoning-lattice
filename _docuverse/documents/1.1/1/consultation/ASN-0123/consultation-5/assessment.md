# Channel Assignment — ASN-0123 review-5

**Date:** 2026-06-12 23:43

## Issue 1: The forker is named `π` in the operation and `π'` in V9 — the symbol for the central parameter is swapped between sections.
Reason: Pure notational consistency — the reviewer prescribes the exact rename (keep `π` as the forker per `VERSION(π, d_src)`, introduce `π_o := ω(d_src)` for the owner in V9), and the math is already locally self-consistent within each section. A symbol choice depends on neither design intent nor implementation evidence; derivable from the ASN alone.

## Issue 2: V-WF's cross-owner realizability silently presupposes an account-tier forker.
Reason: The presupposition is a mathematical fact derivable from foundations the ASN already cites — O1a admits node-tier principals (`zeros(pfx(π)) = 0`), `E_doc` requires `zeros = 2`, so producing a document under a node prefix needs an intermediate account baptism and cannot be "one K.δ." Stating it (qualifying V-WF, or keeping the general cross-owner identity allocation out of scope as the branch already declares) is an internal specification edit; the design framing favoring account-holder forkers ("account-holder forked it into being" [LM 4/17]; "Another user … is free to create his or her own alternative version" [LM 2/32–2/40]) is already quoted in the ASN. Neither channel needed.
