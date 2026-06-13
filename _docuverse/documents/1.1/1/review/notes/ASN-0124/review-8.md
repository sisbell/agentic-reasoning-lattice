# Review of ASN-0124

I checked all 35 introduced claims against their derivations and the declared foundations (ASN-0034/0036/0043/0045/0047/0053/0058/0082/0093/0098/0127). The constructions that carry real proof weight — FD-NEUT(c), FD-LOSSY, the FD-FRESH insertion composite, the FD-VDYN(d) absorption example, and the Worked Illustration — I verified step-by-step against the K-vocabulary preconditions and the J0/J1★/J1'★ coupling discharge. Spot summary of the load-bearing checks:

- **FD-IMGC** (`image_C = image ∩ dom(C)`): both inclusions sound — the (⊇) direction correctly forces `subspace(v) = s_C` on the witness via S3★ + SD, since a single I-address cannot sit in both stores.
- **FD-VERS**: `ran_C(d_new, Σ') = ran_C(d_op, Σ)` follows from J4's derived range identity plus the fork's framing of every prior arrangement; the biconditional `d_new ⟺ d_op` is correctly stated against `Σ'` (using `d_op`'s membership invariance).
- **FD-FRESH**: the clear-and-rebuild composite is a valid composite — intermediate preconditions hold (cleared state satisfies the per-subspace shape package vacuously), and J1★/J1'★ pin range-new = `A_new` initial-to-final. The net-effect match to ASN-0082's I3/I3-L/I3-V is correct, and the conclusion's restriction `I ⊆ dom(Σ_pre.C)` is exactly what neutralizes the freshly-allocated material.
- **FD-VDYN(d)**: `image_C(W, d_q, Σ') = image_C(π⁻¹(W), d_q, Σ)` correctly restricts F-IMG-SWING through subspace-preservation; the necessary-but-not-sufficient absorption analysis and its witness ({d_q, d_x} arranging both addresses) check out.
- **FD-WITNESS / FD-GHOST / FD-COINC**: the (⊆)/(⊇) directions correctly route through P4a (witness existence) and P4★ + P2 (witness persistence); the FD-COINC parenthetical that a reorder's decomposition contains K.μ⁻ yet satisfies the *semantic* range-non-decreasing hypothesis is a precise, non-trivial distinction, handled correctly.

Edge cases are covered: empty/fresh document (FD-FIND degenerate), full clearance (FD-CWP `Ret = ∅`), first-insertion and pure-append branches (FD-FRESH), `I = ∅` (FD-COOC universe-relative reading), ghost addresses (FD-GROUND), coincidental equal values (FD-IDENT(b), S4), same-origin siblings (FD-IDENT(c)). No proof-by-"similarly" or proof-by-checkmark; every multi-case argument (FD-STEP, FD-VDYN) is split per case. Foundation usage is correct — `image_C` is a thin, justified restriction of ASN-0127's cited `image`, not a rebuild, and dynamics cite F-IMG-MONO/CONTR/SWING rather than re-deriving them. No non-foundation cross-ASN references.

**Anti-bloat pass.** Forward references are lean label-pointers (FD-SOUND→historical-companion, FD-PART→FD-COOC/FD-IDENT, FD-NONMONO→FD-VDYN), not accumulated meta-prose; none blocks following a claim. The closest candidates to section-justifying meta-prose ("methodology mirrors ASN-0127's existence lane"; "derived independently because the predicate differs") are brief and, in the second case, load-bearing for the de-duplication rationale against ASN-0127. The "pointing/containing" refrain (FD-VDYN, FD-NONMONO, Worked Illustration) recurs three times but in distinct slots (law / methodology / example). These do not meet the stated "skip past to follow a claim" bar.

## REVISE

None.

## OUT_OF_SCOPE

The Open Questions correctly defer genuine future territory rather than papering over gaps: interior-state coherence (the gap between atomic steps where P4★ need not hold), temporal/version-rank provenance, attribution-bearing answer refinement, past-state arrangement reach, distributed availability vs. silent omission, asker authority, provenance compaction, and multiplicity exposure. Each is new state/operation territory, not an omission in this note. The historical-companion claims (FD-HIST…FD-COINC) stay correctly within scope — they characterize the provenance-keyed query as the present-tense operation's contrast, deriving locally from ASN-0047's apparatus, and are load-bearing for the green-implements-historical thesis.

VERDICT: CONVERGED
