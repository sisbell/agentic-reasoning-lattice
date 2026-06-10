# Review of ASN-0126

This is a carefully built note. The projection bridge cleanly inherits ASN-0086 by showing `→_sh` only *restricts* the C/M/L dynamics (it never adds a transition ASN-0086's `→` lacks), so every ASN-0086 safety property transfers to the smaller reachable set; the partiality of `Sh-conf` is handled honestly by the (i)-before-(ii) gate ordering; the retraction breakage is correctly diagnosed (empty-from `Nullify` has no `→_sh` image) and re-expressed; and the worked illustration checks P3/P4 and the born-nullified separation against concrete tumblers, including the `g`-at-lower-endpoint detail. RegisteredAdmissible even catches that non-emptiness must transfer from the stored representative `K_j` to the emitted `K`. The one remaining issue is accreted prose, consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Op-set carry-over paragraph re-derives results already on the page

**ASN-0126, "Retraction as an attributed Binary" (final paragraph)**: "The two operations carry over asymmetrically. `Observe_K` ... carries over genuinely unchanged ... `Emit_K` carries over but is now *gated* ... requiring K registered and `Sh-conf(K, F, G)`. The empty-from `Nullify` ... is *superseded* by the attributed-Binary wrapper `Nullify_Binary` defined here ..."

**Problem**:
- The "Emit_K is gated, requiring K registered and `Sh-conf`" leg restates "The shape-gated emit." The "Nullify superseded by Nullify_Binary" leg restates a sentence from *earlier in this same section*: "This `Nullify_Binary` is the live retraction operation the framework supplies in place of the empty-from `Nullify`." Two of the three legs of the "asymmetric analysis" re-derive conclusions already established; only Observe_K's pass-through (a legitimate operation-behavior statement) and the bottom-line set `{Emit_K, Observe_K, Nullify_Binary}` are new. The commit that "expand[ed] op-set carry-over paragraph with asymmetric analysis" is the accretion; the analysis re-narrates rather than advances.
- "The two operations carry over asymmetrically," placed immediately after the three-element set `{Emit_K, Observe_K, Nullify}`, is momentarily ambiguous about which two are meant — it resolves to "the two that carry over," with `Nullify` a third, superseded, case, but the reader has to back-fill that.

**Required**: Compress to the load-bearing content — the final operation set plus Observe_K's pass-through — and replace the Emit/Nullify re-derivations with the pointers already available ("The shape-gated emit"; the wrapper definition above). If the three-way contrast is worth keeping, name three operations, not "two."

## OUT_OF_SCOPE

### Topic 1: Multi-app registry construction and coverage-class collision

C0 requires the *final* `Σ_init.registry` to be well-formed (unique coverage-class keys), but the note does not model how multiple apps' declarations are merged into that registry, nor how a collision — two apps wanting the same coverage class under different shapes — is resolved.

**Why out of scope**: The note specifies the registry's static properties (well-formedness, invariance across the dynamics); the construction and coordination of `Σ_init.registry` is a separate operational-semantics concern, adjacent to the note's own Open Question 4, not a defect in the guarantees this note states.

VERDICT: REVISE
