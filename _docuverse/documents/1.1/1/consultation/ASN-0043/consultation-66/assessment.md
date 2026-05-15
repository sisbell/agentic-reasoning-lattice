# Channel Assignment — ASN-0043 review-66

**Date:** 2026-05-14 17:48

```
## Issue 1: PrefixSpanCoverage misplaced
Reason: Pure relocation decision — the lemma's content and proof are unchanged, only its hosting ASN moves. The destination (span-algebra or tumbler-algebra ASN) is already flagged in memory note span-algebra-gap.md. No design-intent or implementation evidence needed.
```

```
## Issue 2: L0 content-side strengthening understated
Reason: Editorial restructuring of an already-accepted fact. The ASN already concludes that `s_C` becomes a global system constant; the fix is to surface this as a labeled invariant (e.g., L0a) and audit ASN-0036's content-store invariants for downstream implications. Both are derivable from existing ASN-0043 and ASN-0036 text.
```

```
## Issue 3: L9 Case A freshness left implicit
Reason: The cleaner derivation is fully internal — use Case A's hypothesis (no existing link has home = d') with chain-prefix-preservation (home(a) = d') to force a ∉ dom(Σ.L) directly, dropping the GlobalUniqueness appeal. All ingredients are already in the ASN.
```

```
## Issue 4: L1c's "Reading of the chain" paragraph creates a notational debt that is not paid
Reason: The choice between formalizing "allocation events" (option a) or routing through purely structural facts (option b) hinges on whether the implementation meaningfully distinguishes event firings from address-production chains. Gregory's evidence informs whether option (a) is even motivated, or whether option (b) is the right path.
Gregory question: Does udanax-green's allocator (e.g., findisatoinsertmolecule, docreatelink) track distinct "allocation events" as first-class objects separate from the sequence of inc steps that produce addresses, or is the event/chain distinction absent at the implementation level?
```
