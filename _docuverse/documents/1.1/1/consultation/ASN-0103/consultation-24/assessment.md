# Channel Assignment — ASN-0103 review-24

**Date:** 2026-06-08 08:09

## Issue 1: The non-invocation of GlobalUniqueness/B8/T9/T10 is argued at three separate sites
Reason: Pure editorial deduplication — consolidate the non-invocation caveat to one site and keep the positive S0+B7 route. The proof content is already present in the ASN; no design intent or implementation evidence is needed.

## Issue 2: The ω-deferral / E↔B-coupling essay is restated across five slots
Reason: Internal restructuring — move the ω/O5 deferral into Open Question 6 and reduce the other sites to a one-line pointer. The deferral reasoning is self-contained in the ASN; no channel input required.

## Issue 3: A version-dominance paragraph imagines a case the dominance scope already excludes, then declares it moot
Reason: Internal proof trim — collapse the off-chain case to the one-line divergence argument already stated. The distinctness fact is derivable from T1 within the ASN; no channels needed.

## Issue 4: The first-case version-dominance argument forward-references the subsequent case for the same proof it then repeats in full
Reason: Internal refactor — factor the shared first-fork operand argument into one sub-lemma cited from both cases. Both derivations are already in the ASN; no external input required.

## Issue 5: Use-site inventories in the `D_A` and Effect One development
Reason: Editorial cleanup — strip the "each used below" / "load-bearing facts below" framing and state consequences at their use sites. Purely a prose change; no channels.

## Issue 6: B7 invoked for the version chains without discharging its B6 precondition
Reason: Internal proof completion — the B6 premise for `(d_i, 1)` is derivable from facts already in the ASN (`d_i` T4-valid, `zeros(d_i)=2`, depth-1 bound `2 ≤ 3`), matching the parallel cross-account discharge. No channels needed.

## Issue 7: CND.A-act prose explains why the assumption is needed rather than stating it
Reason: Editorial trim of labeled-rationale anti-pattern — keep the axiom statement plus the SubAllocatorBundle-analogue citation. The Nelson quote currently in the prose is being cut, not added, so no channel input is required.
