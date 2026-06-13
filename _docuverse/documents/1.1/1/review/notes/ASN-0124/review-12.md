# Review of ASN-0124

I checked this ASN against the foundations exhaustively — every introduced claim's derivation, the validity of each construction as a K-vocabulary composite, the boundary cases, and the completeness of the transition coverage. It holds.

## What I verified

**Transition coverage is exhaustive (the Dijkstra-critical property).** FD-FRAME covers {K.α, K.δ, K.λ, K.μ⁺_L, K.ρ}; FD-STEP covers {K.μ⁺, K.μ⁻, K.μ~}. Together that is the entire atomic vocabulary plus the named composite — every transition is classified as a non-mover or a mover, with no kind left to "by similar reasoning." FD-VDYN's four cases likewise partition all transitions by whether they touch a *named* document's content arrangement. This is the place such specifications usually fail, and it does not fail here.

**The foundational equalities are real, not asserted.** FD-IMGC's `image_C = image ∩ dom(C)` is proved both directions, with the (⊇) direction correctly leaning on S3★-aux + S3★ + SD to rule out the s_L case. FD-RAN's alignment with `Contains_C` unfolds to the same existential. The FD-STEP clauses each track `ran_C(d,·)` precisely (∪N for K.μ⁺, ↾Ret for K.μ⁻, reindex-invariant for K.μ~) and the finddocs formulas follow.

**The constructions are valid composites, checked step-by-step.** I traced FD-NEUT(c), FD-LOSSY (the Σ² leg: K.α subsequent-emission → K.μ⁻ full content clear `n'_{s_C}=0<1` → K.μ⁺ rebuild at [1,1] → K.ρ), and FD-FRESH (iterated K.α → clear → rebuild → K.ρ) against each step's elementary precondition at its intermediate state and against J0/J1★/J1'★ initial-to-final. The "old images' mid-composite absence is harmless because couplings are initial-to-final" argument is correct, and the freshness fact `A_new ∩ I = ∅` (from `I ⊆ dom(Σ_pre.C)` and K.α freshness) is what closes the re-entry computation. The cleared intermediate state satisfies the per-state package vacuously (D-CTG★/D-MIN★/D-SEQ★ quantify over non-empty subspaces).

**The wp analyses are non-trivial.** FD-CWP correctly reduces survival to `enabled ∧ ran_Ret∩I≠∅` with the Ret=∅ boundary, and the whole-answer-preservation biconditional uses "contraction never creates membership" properly. FD-VDYN(d)'s necessity/insufficiency split — image motion necessary but not sufficient, with the absorption witness (d_q, d_x both arranging a and b) and the non-absorbed worked-illustration case (d_C dropping) — is sound.

**The historical companion checks against ASN-0047.** FD-SUPER (via FD-SOUND + P4★), FD-WITNESS (⊆ via P4a, ⊇ via P4★+P2+M1), FD-GHOST (the k=n term cancellation), and FD-COINC all derive correctly from declared dependencies. The worked illustration's ghost computation `finddocs_R({a₃})={d_A,d_B,d_C}`, `ghosts={d_A,d_B}` is consistent end to end.

**No illegal references, no anti-bloat accretion warranting revision.** Every cited ASN (0034/0036/0043/0045/0047/0053/0058/0082/0093/0098/0127) is a foundation; FD-IMGC/FD-RAN re-restrict ASN-0127's image rather than rebuild it, honoring the scope directive. I scanned for the flagged accretion patterns (axiom rationale, deferral chains, ordering justifications, consumer-enumeration, duplicate paragraphs): none introduces a new axiom, the forward references are single pointers rather than repeated deferrals to one site, and the multiple consequences drawn from FD-LOCAL (origin-neutrality in FD-NEUT, value-blindness in FD-IDENT) are distinct results, not restatements. The FD-COINC syntactic-condition parenthetical ("a reorder's decomposition contains K.μ⁻ though its net effect satisfies the hypothesis") is correct precision, not bloat — "no K.μ⁻ step" genuinely implies range-non-decreasing.

## REVISE

None.

## OUT_OF_SCOPE

The Open Questions correctly defer the genuinely new territory: interior-composite coherence, when-contained (provenance ordering), attribution-bearing answer refinement, past-state arrangement reach, the distributed availability model, asker authority, provenance compaction, and multiplicity exposure. Each is a future-ASN concern, not a gap in this one. The implementation-evidence deviations (green computes the historical `finddocs_R`, not live `finddocs`; reach is single-server) are honestly mapped to FD-HIST and the single-state completeness semantics rather than papered over.

VERDICT: CONVERGED
