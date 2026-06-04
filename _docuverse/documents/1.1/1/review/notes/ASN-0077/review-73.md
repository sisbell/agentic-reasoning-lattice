# Review of ASN-0077

I checked the proof structure, the foundation citations (all to ASN-0034/0036/0047/0053/0058 — no improper cross-references; no direct ASN-0093 citation in the body), the boundary cases, the worked example, and the two weakest-precondition computations. The correctness scaffolding is sound: the singleton-I-span proof exhausts `#b < #a`, `#b = #a`, `#b > #a`; O11/O11′ exhaust both subspace sub-cases; O13/O14 are correctly stated as existential negative claims; and the worked example exercises the multi-origin result, both negative witnesses, and the wp probe. The residual issues are the meta-prose accretion this note's `review-mode.anti-bloat` classifier flags.

## REVISE

### Issue 1: Claims Introduced table carries use-site inventories and proof-dependency annotations
**ASN-0077, Claims Introduced table**: e.g. "SDP | ... ; cited by O11, O11', O11.1"; "WF_V | ... the six conjuncts (i)–(vi) shared by the SHOWORIGIN_V precondition and the O11-series / O13 references"; "O11.1 | ... (corollary discharging the post-state admissibility that O11★★ relies on)"; "O11★★ | ... proved by induction using O11, O11', and O7".
**Problem**: This is the flagged pattern "a definition's introduction enumerates downstream consumers ('this is consumed by X, Y, Z') rather than advancing the definition's meaning." The Statement column should state what the claim says; "cited by O11, O11', O11.1" and "shared by ... the O11-series / O13 references" are downstream-consumer inventories, and the proof-method annotations ("proved by induction using …") restate the body rather than the claim. These rot as the dependency graph shifts.
**Required**: Reduce each row's Statement to the claim itself. Drop the "cited by"/"shared by … references"/"relies on" clauses and the proof-method recaps.

### Issue 2: SDP and O11.1 introductions are forward-reference framing
**ASN-0077, lemma SDP intro**: "Several of the preservation arguments below turn on a single fact … We extract it once." **And O11.1 intro**: "Both O11 and O11' assume σ well-formed at the pre-state Σ. To chain these single-step claims into multi-step lemmas, we extract the post-state preservation of well-formedness as a stand-alone corollary."
**Problem**: Both are meta-prose explaining *why a result is positioned where it is* and *which later results will consume it*, rather than advancing the lemma/corollary content. This matches the flagged patterns "multiple paragraphs … defer to the same downstream location" and prose that justifies extraction/ordering.
**Required**: State SDP and O11.1 directly with their preconditions and conclusions; drop the "we extract it once / to chain … below" framing. A reader reaching O11★★ already sees the citation.

### Issue 3: Summary closing sentence duplicates its own bullet list
**ASN-0077, Summary**: the three primitives (1)–(3) are immediately followed by "Every other property — span containment monotonicity … — follows from these three," and then the final sentence re-enumerates O5/O5★, O6/O6★, O7, O11/O11′, O14 with the same content.
**Problem**: "two paragraphs in the same document say the same thing in different words." The bulleted recap and the trailing prose sentence carry the same inventory.
**Required**: Keep one. Either the three primitives plus a one-line "all other claims derive from these," or the prose sentence — not both.

## OUT_OF_SCOPE

### Topic 1: Unified content+link origin operation; intermediate-chain surfacing; native-vs-transcluded distinction; historical containment from Σ.R
**Why out of scope**: These are the note's own Open Questions and correctly deferred — each would be a new operation with its own guarantees, not a correction to SHOWORIGIN as specified here.

VERDICT: REVISE
