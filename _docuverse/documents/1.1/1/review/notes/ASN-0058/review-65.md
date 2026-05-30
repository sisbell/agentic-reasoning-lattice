# Review of ASN-0058

## REVISE

*(none)*

## Findings summary (no action required)

I verified the following load-bearing arguments and found them complete:

- **M0/M1/M5(b)** — strict monotonicity of `k ↦ v+k` correctly case-split (TS4 at `k=0`, TS5 for `k≥1`); the `n=1` singleton boundary is handled separately before the monotonicity step.
- **M-int** — both bounds (`(x)_m ≤ (y)_m < (x)_m + n`) are derived by explicit T1 appeals with the proper-prefix branch excluded by equal depth; the `k=0` (T3) and `k≥1` (TumblerAdd) reduction cases are both closed.
- **M7 necessity** — the three V-position cases (gap `v₂>v₁+n₁`, adjacent, overlap `v₂<v₁+n₁`) are exhaustive; overlap is correctly discharged by M7-cov via M-int rather than hand-waved.
- **M12a/M12b/M12** — RunDisjointness (equal-starts + equal-widths via trichotomy), NoExtension (the unit-shift `δ(1,m)` injectivity argument depends on depth-`m` validity, which is properly established through OrdShiftHom + S8-depth before use), and the two-inclusion `B = R` argument all hold. The partition corollary's right/left extension phases preserve conditions 1 and 3 as claimed.
- **C0** — `k<m` is refuted by an injective infinite family `wⱼ` whose membership in `⟦σ⟧` is verified at both endpoints; contradiction with S8-fin is valid.
- **C2** — the `dom(f) = D_m = E`, `|E| = ℓₘ` chain is set-equality at each step; partition + M0 deliver the width sum.
- **M16a** — the structural decomposition rests on T10a.4 (T4-validity) and S7b (`zeros=3`), both inherited from the origin() framework of ASN-0036; the shift's action point `#a` lies strictly above the document prefix, so the prefix is copied unchanged.

Both worked examples (canonical decomposition; content-reference resolution) exercise the key postconditions against concrete tumblers, including the non-mergeable cross-origin boundary (M16). Case coverage, concrete grounding, and per-step citation all meet the bar. Prose around forward references (M6→M16b deferral, empty-case discharge in M2) is single-sited, and analogies/glosses fall within the protected "what the claim does / does not assert" and "analogy" categories.

VERDICT: CONVERGED
