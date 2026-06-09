# Channel Assignment — ASN-0126 review-20

**Date:** 2026-06-09 07:41

## Issue 1: "register against" contradicts the immutable registry
Reason: Internal. The note already supplies both pieces — Registry permanence fixes the registry at `Σ_init`, and C0 commits `Σ_init.registry`'s contents — so reconciling "register against" (conformance) vs "register" (add entry, init-only) is a wording disambiguation derivable from the ASN's own model.

## Issue 2: `|·|` overloaded between arity and span count
Reason: Internal. Choosing a non-colliding symbol for span count and applying it consistently is a pure notation fix; both meanings (arity per ASN-0043, span count coined here) are already defined in-note.

## Issue 3: retraction re-expression buried under stacked authority rationale
Reason: Internal anti-bloat. The structural claim (R Binary; attributed form `|F|=1,|G|=1`) and its citations already exist in the note; trimming the authority essay to one citation and moving narrative to a sidecar removes no content that needs re-sourcing.

## Issue 4: Binary-≠-unit-depth restated four-plus times
Reason: Internal anti-bloat. The single load-bearing reason (a `δ(2,#t)` span is Binary-conformant) is already stated; deleting the three restatements requires nothing external.

## Issue 5: span-count-vs-coverage divergence duplicated for F then G
Reason: Internal anti-bloat. Both the divergence and the udanax-green coalescing justification are already present once; generalizing to "any single-span slot" and dropping the second pass is reorganization of existing material.

## Issue 6: meta-prose justifying the wp artifact and the gate/landing split
Reason: Internal anti-bloat. Removing the "proper depth artifact" framing and the "drawn once in X" pointer is deletion of self-referential commentary; the wp derivation and P4 already carry the argument.

## Issue 7: repeated deferral to Open questions #4 and duplicated "no free-floating materials" quote
Reason: Internal anti-bloat. Collapsing duplicate deferrals and using the existing Nelson quote once is deduplication of material already in the note.

## Issue 8: defensive preamble before C0
Reason: Internal anti-bloat. The necessary observation (P1 freezes contents but not `Σ_init` well-formedness) is already stated; compressing the "we must be careful" rehearsal to one motivating sentence is local editing.
