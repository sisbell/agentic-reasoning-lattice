# Channel Assignment — ASN-0132 review-1

**Date:** 2026-06-13 03:19

## Issue 1: CN-MONO's weakest precondition drops the "no pre-existing retraction covers ℓ" conjunct
Reason: Internal. The review names both resolution paths and both bottom out at foundations the ASN can cite directly — either carry the missing conjunct verbatim from FL-WP(a) (ASN-0121, the lemma the step already claims to specialize), or discharge it via R0a/FlatLinkDomain (ASN-0086), under which the flat link domain forces any pre-existing retraction target `t ≼ ℓ` to equal `ℓ`, contradicting freshness. The correct wp follows from the cited lemma without design intent or implementation evidence.

## Issue 2: E-INV is cited for a preservation it does not establish
Reason: Internal. This is a pure citation swap, and the discharging facts are all already named and present — L12/LP13 (UnconditionalLinkPersistence, ASN-0043) for value/domain fixity, CN-LOC (this ASN) for `sat` reading only `Σ.L(a)` and `home(a)`, and `L_R^{Σ'} = L_R^Σ` (from "not a retraction") for addressability. Replacing the wrong-predicate E-INV citation with these requires no external input.

## Issue 3: No concrete worked example grounds the multiplicity, retraction, or orphan claims
Reason: Internal. The example instantiates only machinery the ASN and ASN-0121 already define (`sat`, `addressable`, `coverage`, `touch`, `lift`, `nullified`); the transclusion and appearance multiplicities enter as scenario premises that CN-LOC shows the count ignores, so the numbers are computable from the spec's own definitions without implementation evidence or design intent.

## Issue 4: CN-STAB lists a redundant hypothesis
Reason: Internal. The redundancy is established by a fact the ASN already leans on — `nullified` is a function of `Σ.L` (FL-LOC, ASN-0121, underpinning CN-LOC) — so `Σ'.L = Σ.L` entails `nullified(Σ') = nullified(Σ)`, and recognizing this needs nothing external.
