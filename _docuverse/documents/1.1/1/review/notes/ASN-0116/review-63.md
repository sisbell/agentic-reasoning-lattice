# Review of ASN-0116

This is a strong, carefully built ASN. I verified the valid-composite decomposition (clause 1 step-by-step and clause 2 couplings), the gapped/filled bridge, IP0–IP6, the I-*/F-* clauses, the boundary cases (front J=1, append J=N+1, empty in both emission sub-cases, large n), and the link-survival/discoverability analysis. The mathematics is sound. Two minor items remain.

## REVISE

### Issue 1: P7 miscategorized as a composite-boundary property

**ASN-0116, "The document remains one coherent sequence"**: "…and the content-store validity S7b/C1/C1b/C1c of the freshly allocated run, together with the composite-boundary properties P7 and P7a."

**Problem**: In ASN-0047's ExtendedReachableStateInvariants, P7 (ProvenanceGrounding, tagged INV) is a *per-state invariant* — it sits in the per-state conjunction `… ∧ P6 ∧ P7 ∧ P8 ∧ …`. Only P7a (ProvenanceCoverage, tagged PROP) is a composite-boundary property (`P4★ ∧ P4a ∧ P7a`). The ASN calls both "composite-boundary properties." The conclusion (both hold at the post-state, which is a composite boundary) is unaffected, but the citation of *which* clause of the foundation theorem delivers P7 is wrong. Elsewhere the ASN gets these categories right (S8-fin "at the composite boundary Σ" as a per-state invariant that also holds there; P4★ and P7a correctly cited as composite-boundary), so this is an isolated slip, not a systematic misreading.

**Required**: List P7 among the per-state invariants it delivers, reserving "composite-boundary property" for P7a (and P4★, P4a). E.g., "…together with P7 (per-state) and the composite-boundary property P7a."

### Issue 2: Forward-reference pre-announcement in F-SUB (anti-bloat)

**ASN-0116, INSERT *Frame*, clause F-SUB**: "The `⊆` half is load-bearing for RAN below, which reads the cross-subspace image equality off this position-set equality."

**Problem**: This sentence advances none of F-SUB's content; it enumerates a downstream consumer (RAN). The `⊆` half is part of the stated set equality regardless of who later uses it, and RAN already cites F-SUB at its own use site ("Across the other subspaces F-SUB fixes the per-position images…"). The pre-announcement is exactly the use-site/forward-reference pattern the anti-bloat classifier targets — it compounds across cycles. (This is the clearest instance; the rest of the prose is substantive — the maximal-run non-maximality analysis, IP4's containment-direction case split, and the IP6 containment-vs-emptiness wp are genuine derived consequences, not padding.)

**Required**: Drop the trailing clause; let RAN cite F-SUB where it consumes it.

## OUT_OF_SCOPE

The four Open Questions (transclusion at a shared insertion point, concurrent-insertion freshness without a serializer, transclusion-provenance with a foreign origin, post-fragmentation obligations on the inserted run) are correctly deferred and match the declared scope exclusions. Nothing in the body claims results about COPY/DELETE/REARRANGE/MAKELINK that should be moved out. No additions needed.

VERDICT: REVISE
