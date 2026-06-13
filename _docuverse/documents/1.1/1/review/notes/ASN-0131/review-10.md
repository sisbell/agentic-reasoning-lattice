# Review of ASN-0131

I checked the operation definition, the decidability argument, the worked instance address-by-address, and each of the eighteen claims — with particular attention to the two non-trivial derivations (the sole-bearer iff in RE-RET and the weakest precondition in RE-CWP) and the full transition taxonomy in RE-EDIT. The findings below record what I verified and why the gaps a Dijkstra-style read would hunt for are not present.

## REVISE

(none)

The substantive checks:

- **Worked instance is exact.** `e₁`'s first span `(a₂, δ(2, #a₂))` has reach `shift(a₂, 2) = a₄` (via TS3), so `{a₂, a₃} ⊆ coverage` with `a₄` correctly excluded by the open upper bound; `e₂`'s prefix-subtree coverage `{t : a₁ ≼ t}` correctly excludes the siblings `a₂, a₃, a₄`; and the `coverage(e₃) ∩ dom(Σ.C) = ∅` argument is right to lean on field-segment **agreement propagating the subspace identifier along ≼** (Prefix/T4) rather than T7 — the note even flags why T7 and the naive "every extension carries the identifier" reading both fail. The five postconditions read off `{(1, e₁)}` correctly, including the genuine exercise of RE-WHOLE (the `a₄`-span volunteered out-of-region).

- **RE-RET both halves hold.** Forward (sole bearer ⟹ drop) rests on `addressable(Σ') = (addressable(Σ) ∖ {ℓ}) ∪ {b}` (R6a monotone-nullified + R-Scope single-tuple + L12a), with `b`'s three endsets non-touching for a content region — `∅` trivially, the to-set by the same field-agreement argument applied to `ℓ`'s genuine `s_L` element-level address, and the type-set `R` **honestly flagged as an imposed discipline, not a derivation**. Backward (other live bearer ⟹ survive) correctly invokes R0a (antichain ⟹ `ℓ ⋠ ℓ'`) and R-Scope to confine the nullification to `ℓ`, leaving `ℓ'` addressable with value fixed (L12) and image fixed (K.λ frames M). The iff is properly scoped to content-region + disciplined-R.

- **RE-CWP is correctly derived.** The disjoint decomposition `image(W,d,Σ) = I_R ⊎ Δ` (D-CWP bridge) reduces "dropped" to `coverage(e) ∩ Δ ≠ ∅ ∧ coverage(e) ∩ I_R = ∅`; `Avail` is genuinely pre/post-invariant (K.μ⁻ frames `Σ.L`, hence `nullified`); the `R = ∅` boundary collapses to `RE = ∅` as claimed; and the "strictly finer than D-CWP" observation is right — same-endset vs same-link is exactly where a from/to-split link separates them. The non-injectivity is handled correctly by taking `Δ` at the I-address level, not the V-position level.

- **RE-EDIT classifies all eight transition kinds correctly,** including the dual nature of `K.μ⁻` (content-subspace contraction moves the answer through the image; link-subspace-only contraction is the `Δ = ∅` case) and the K.μ⁺_L "image unchanged" sharpening of F-IMG-MONO to equality under `W ⊆ s_C` (the new position is `s_L`, hence outside W) — supplied with its inline derivation, not merely asserted.

- **RE-UDIST, RE-SEL, decidability, boundary cases** all check: image distributes over union unconditionally; `sel = findlinks_V ∩ addressable` unfolds correctly via F-V/F-FIND/F-MATCH; the answer is finite/computable over `I` (S8-fin) and `dom(Σ.L)` (L-fin); and the three degenerate inputs (empty image, no addressable links, empty endset slot) are read straight off the definition.

All ASN references are to foundation ASNs (0034, 0036, 0043, 0047, 0053, 0058, 0082, 0086, 0093, 0098, 0127); the image machinery and existence/discovery taxonomy are cited from ASN-0127, not rebuilt; and `addressable`/`Avail`/`touch_W` are new abbreviations over foundation notions, not reinventions. The operation is a pure query (`Σ' = Σ`), so it carries no invariant-preservation obligation — the strongest possible frame, trivially discharged.

## OUT_OF_SCOPE

The seven Open Questions are appropriately deferred, not gaps in this ASN: whole-vs-touching-span surfacing (the RE-WHOLE/RE-CLIP split, with RE-WHOLE correctly held provisional), multiplicity-vs-dedup, the rendered V-position mode (ASN-0082 territory), intersection-distributivity (genuinely blocked by non-injectivity, M13/M14 — and no stated claim relies on it), non-co-resident link stores (BEBE), type-slot matching against content, and the link-subspace region. Each is new territory the content-subspace restriction deliberately fences off, with the points such a query would reopen (notably the emitter conjunct in retraction stability) flagged at the spot they arise.

VERDICT: CONVERGED
