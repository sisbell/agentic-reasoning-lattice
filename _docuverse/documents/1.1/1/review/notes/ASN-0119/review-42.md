# Review of ASN-0119

The mathematics is sound and unusually thorough. I checked the import structure, the permutation algebra (RA1/RA2 via R-PPERM/R-SPERM/R-PIV/R-SWP), both worked examples arithmetically (pivot `ABCDE → ACDEB`, swap `ABCDEF → AEFCDB`, and the two-move composite through `ACDBE`), the full ASN-0047 invariant discharge (every conjunct of ExtendedReachableStateInvariants is accounted for), the P4a trace induction, and the footprint-transport reasoning (RA7a/b/c) including the four contiguity configurations. All check out. The content-subspace-range invariance closing J1★ — distinct from the full-range RA1 — is correctly identified rather than conflated, and the S3★ derivation handles both subspaces explicitly. No correctness gap found.

The findings below are the forward-reference accretions this review mode targets. They are minor, but they compound.

## REVISE

### Issue 1: the value-dependent link invariants are discharged once but bracketed by a forward and a backward signpost
**ASN-0119, "What is preserved"**: The single discharge sits in the S8★ paragraph —
> "the value-dependent CL-OWN/CL-UNIQ ride untouched on the frozen s_L frame"

— but is pre-announced one paragraph earlier (contiguity paragraph):
> "the value-dependent link-subspace invariants (S8★, CL-OWN, CL-UNIQ, **discharged below**) rest"

and re-referenced from the later closure-rule paragraph:
> "the only conjuncts not so keyed being CL-OWN and CL-UNIQ, **already discharged above** on the frozen s_L frame"

**Problem**: Three mentions across three paragraphs, with a "discharged below" and an "already discharged above" bracketing the one place the work happens. This is precisely the "multiple paragraphs defer to the same downstream location" pattern — the reader holds a forward promise, then is sent back to it. The S8★ paragraph is adjacent; the pre-announcement carries no information the reader doesn't reach in the next sentence.
**Required**: Discharge CL-OWN/CL-UNIQ once (in the value-dependent paragraph with S8★) and drop both the forward "discharged below" and the backward "already discharged above." The closure-rule paragraph can name them as the non-frame-keyed exceptions without re-litigating their discharge.

### Issue 2: RA6 is cited before it is introduced
**ASN-0119, "What is preserved" (closure rule)**: "every conjunct keyed only on frame-frozen components — dom(C) and its values by RA0, E and R inert, **dom(L) and its values by RA6** — is preserved by those frames."
**ASN-0119, "Links"** (several sections later): "we extend that frame with an explicit clause — REARRANGE writes only M(d), so Σ'.L = Σ.L **(RA6)**"
**Problem**: The label RA6 is consumed by the L-family discharge in the closure rule but not assigned until the Links section. RA0/RA1/RA2 are stated-then-used; RA6 is the lone label used-then-stated, forcing a forward search. (The bare fact `Σ'.L = Σ.L` does appear unlabeled in "The two streams," so the content is available — only the label is out of order, which is the navigation cost.)
**Required**: Introduce RA6 — or attach the label to the link-store frame fact where it is first stated — before the transition-invariant discharge that consumes it.

## OUT_OF_SCOPE

### Topic 1: REARRANGE at V-position depth > 2
**Why out of scope**: The operation is confined to depth 2 (`#v = 2`), inherited from ASN-0084's CutSequence (CS4). The ASN explicitly disclaims other depths ("We make no claim about other subspaces or other depths"). Since the strand/link model admits `m_S ≥ 2` (S8a), documents with text-subspace depth `> 2` are genuinely uncovered — but that is a future ASN building on a deeper REARRANGE_K, not a defect here. Noting it only so the depth-2 restriction is not mistaken for generality.

META: (not applicable — the ASN defines an operation on state and discharges the system invariants abstractly; it has not drifted into implementation mechanics, and the Gregory references are correctly framed as conformance evidence, not specification.)

VERDICT: REVISE
