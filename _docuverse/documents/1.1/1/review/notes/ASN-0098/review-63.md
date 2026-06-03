# Review of ASN-0098

This ASN is unusually thorough — the projection function is cleanly separated from coverage and stored link value, every K.μ operation has an explicit displacement proof with exact-difference characterisations, boundary cases (empty endset, empty arrangement, R=∅ contraction) are handled, the wp analysis (LP12a) is non-trivial, and a two-branch worked trace verifies the key postconditions. Cross-references are confined to foundation ASNs. The mathematics holds up under checking: LP-Fin's interval count, LP11's bijection rebinding, LP19a's freshness-vs-tightness contradiction, and the LP20 partition all verify. No correctness defects found, no drift (META not warranted).

The findings below are the anti-bloat patterns this note's classifier directs me to surface.

## REVISE

### Issue 1: Duplicate formalization of the same Nelson motif in two sections
**ASN-0098, LP10 and the paragraph following LP12a**: LP10 closes with "The link survives on whatever V-positions remain. This is Nelson's 'if anything is left at each end' condition made precise." The post-LP12a paragraph opens "The phrase 'anything is left at each end' can now be stated formally: discoverability from `d` requires that, for at least one slot `i`, `coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅`."
**Problem**: Two paragraphs in different sections both claim to render the same Nelson phrase "precise"/"formal." They in fact formalize different propositions (partial-deletion survival vs. the discoverability nonemptiness condition), but the repeated "made precise / stated formally" framing reads as the same rhetorical move executed twice, which is exactly the cross-section duplication that accretes across cycles.
**Required**: Anchor the Nelson phrase at one site (the discoverability characterisation is the stronger one), and at the other site state the proposition directly without re-invoking "made precise."

### Issue 2: Worked-trace closing paragraph restates the thesis rather than advancing the trace
**ASN-0098, A Worked Trace (final paragraph)**: "At no point during either branch of this trace did the link itself change. The link's address, endsets, coverage, and slot ordering remained byte-identical from `Σ` through `Σ_2` … and from `Σ` through `Σ_3` … What displaced was the projection, and the displacement was entirely a function of the operations applied to the documents' arrangements."
**Problem**: This is a verbatim re-assertion of LP13 (UnconditionalLinkPersistence) and LP2 (SlotInvariance), already proven. It introduces no new computation and is not a step in the trace; it is a summary essay in the trace's terminal slot. The trace's own per-state `project(...)` lines already demonstrate the point.
**Problem severity note**: borderline — a one-line takeaway tying the trace to LP13 would be defensible; the current paragraph is a full restatement.
**Required**: Cut to at most a single sentence citing LP13/LP2, or remove — the trace's computed projection values already carry the conclusion.

## OUT_OF_SCOPE

### Topic 1: Open Questions section
**Why out of scope**: The seven open questions (reverse-discovery primitive, V-order/I-order reflection under K.μ~, link-to-link induced discovery, fork-composite link-subspace non-transclusion, link-canonical contraction disjointness) are correctly deferred as future-ASN territory and are not defects here. No action.

META: not applicable — the ASN defines a live projection operation over mutable arrangement state plus its displacement invariants, which are implementation-independent system guarantees, not implementation mechanics.

VERDICT: REVISE
