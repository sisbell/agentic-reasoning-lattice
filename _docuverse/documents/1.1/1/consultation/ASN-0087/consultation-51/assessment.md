# Channel Assignment — ASN-0087 review-51

**Date:** 2026-06-04 01:10

## Issue 1: LP-Sub miscited to establish `ℓ ∈ F` for the fresh address
Reason: Purely a citation-correctness fix. The correct justification (`ℓ` is an `A_L(d)` emission, form `[d, 0, s_L, k]` via FirstEmission/ChainDiscipline ASN-0093, `origin(ℓ)=d` T4-valid with `zeros(d)=2` by M0, then F's definition) is entirely derivable from already-referenced foundation ASNs. No design intent or implementation evidence is at stake.

## Issue 2: Scope mismatch when M-FreshExcl is reused on a prior link
Reason: Internal restatement of a lemma's carrier — generalize M-FreshExcl to any `x ∈ F` with `x ∉ dom(Σ.C) ∪ dom(Σ.L)` and any standardly-authored endset. The underlying logic is already present in the ASN; only its quantifier scope needs broadening. No external channel needed.
