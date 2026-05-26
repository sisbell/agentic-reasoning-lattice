# Channel Assignment — ASN-0094 review-81

**Date:** 2026-05-25 17:37

```
## Issue 1: Forward reference EffectiveWpSimplification → RetractionSelfFreshness
Reason: Pure structural reordering within the ASN — move RSF before EWS. No design intent or implementation evidence required; RSF's proof dependencies are all earlier and the forward reference is self-evidently fixable internally.
```

```
## Issue 2: Sh0–Sh4 lemma statements omit the empty-baseline precondition
Reason: The baseline is already stated in the Initial-State Baseline section and acknowledged in Open Questions; the fix mechanically lifts the precondition into each lemma statement. Internal.
```

```
## Issue 3: Tuple-Classifier walkthrough setup contradicts Per-walkthrough convention
Reason: The reviewer provides two clean options (relax convention or restructure walkthrough), both resolvable from the ASN's own definitions. No external evidence needed.
```

```
## Issue 4: CaseAClosureForLK lemma's proof is unusually terse
Reason: The discharge content already exists inline within the statement; the fix is reorganizing it into a structured proof body. Pure exposition refactor.
```

```
## Issue 5: "Audit-slice set-semantics commitment" referenced but not formally named
Reason: The Nullify Compatibility section already establishes the set-semantics departure as load-bearing; the reviewer's two options (formally name or replace terminology) are both derivable from existing ASN content.
```

```
## Issue 6: EffectiveWpSimplification's Step 3.5 reads as inserted afterthought
Reason: Pure renumbering fix from 1–4 with a 3.5 insertion to a clean 1–5 sequence. No semantic change.
```

```
## Issue 7: SHCD preservation Case A omits the four-class enumeration
Reason: The four-class enumeration exists verbatim in Sh4's and FDD's preservation theorems within the same ASN; SHCD's Case A mirrors it mechanically by copying the structure and citing the same case-equation discharges.
```
