# Channel Assignment — ASN-0098 review-49

**Date:** 2026-06-02 15:58

## Issue 1: K.σ referenced outside the declared working frame
Reason: Derivable from the ASN itself. The ASN declares its frame as "ASN-0047 transition-model layered over ASN-0093," names ASN-0047's atomic vocabulary (K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ) excluding K.σ, and LP8 already asserts K.σ and K.δ-IsDocument have structurally identical effects on Σ.M. Dropping the K.σ disjunct and stating over K.δ-IsDocument follows from the frame declaration without external input.

## Issue 2: "Tightness is state-relative" stated twice, near-verbatim
Reason: Pure editorial deduplication internal to the ASN — keep the state-relativity statement at the definition, collapse the achievability restatement to one sentence. No design intent or implementation evidence at stake.

## Issue 3: Provenance-indifference claim restates its own opening
Reason: Internal editorial fix — the load-bearing LP12-inspection derivation is already present mid-paragraph; the closing restatement is removed to a single clause. Derivable from the ASN alone.

## Issue 4: Minor — `F` introduced informally before its formal definition
Reason: Internal editorial reorganization — fold the zero-extension exclusion remark into the formal definition's surrounding prose and delete the duplicate informal gloss. No external channel needed.
