# Channel Assignment — ASN-0131 review-4

**Date:** 2026-06-13 05:48

## Issue 1: The "full taxonomy" of stability omits K.δ and K.ρ
Reason: Internal — the conclusion follows directly from RE-LOC (already proven: `RE` is a function of `Σ.M(d)` and `Σ.L` alone) applied to two transitions whose frames are elementary and uncontested (K.δ adds only a fresh entity's arrangement, leaving `M(d)` and `L` fixed; K.ρ touches only `Σ.R`). The review itself supplies the LP8/LP14 citations, and even absent them RE-LOC carries the argument, so no design or implementation input is required.

## Issue 2: Retraction is a K.λ; RE-RET and the taxonomy do not account for the emitted retraction link entering addressable(Σ')
Reason: The fix rests on retraction being realized as a single K.λ (`Nullify = Emit_R`) that emits an addressable link in the very step it nullifies its target, with a specific endset structure — a model fact from ASN-0086 that ASN-0131 does not contain (it frames re-emission as a separate future act). The structure of the emitter, which is what makes the "iff" hold for content regions, is an implementation question for the evidence channel.
Gregory question: Is retraction realized as a single K.λ step `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1,#a))})` that emits a new link `b` — addressable in `Σ'` — whose endsets are `∅` (from), a to-endset targeting the link address `a`, and a type endset, none of which cover content?

## Issue 3: The domain of W is left unspecified; the unconditional claims hold only for content regions
Reason: This is a scope decision the ASN cannot settle internally (the narrative is content-centric, RE-DEF admits arbitrary `W`); a faithful choice needs both the designer's intended domain for the operation and the realizing FEBE operation's actual input domain.
Nelson question: Is RETRIEVEENDSETS intended to query a content (text-subspace) passage specifically, or any region of V-positions, including positions in the link subspace?
Gregory question: What does udanax-green's RETRIEVEENDSETS accept as its region argument — content-subspace spans only, or arbitrary V-positions that (via S3★) could resolve to link addresses?

## Issue 4: Worked example — the `coverage(e₃) ∩ dom(Σ.C) = ∅` step rests on an overgeneralized claim and a misapplied T7 citation
Reason: The corrected argument depends on precise tumbler-algebra facts not invoked in ASN-0131 — T4b's restriction of the E-projection to T4-valid (zeros=3) tumblers and field-segment agreement of `E₁` under prefix — and the note already erred on exactly this algebra, so the replacement reasoning should be confirmed against the address-algebra evidence rather than re-derived in place.
Gregory question: Among T4-valid (zeros=3) tumblers, does `θ ≼ c` force the subspace identifier to agree (`E(c)₁ = E(θ)₁`) by field-segment agreement on positions `1..#θ`, and is `T4b`'s `E`-projection defined only on T4-valid tumblers — so that "extension preserves `E₁`" holds for content addresses but fails for T4-invalid extensions like `θ.0.x`?
