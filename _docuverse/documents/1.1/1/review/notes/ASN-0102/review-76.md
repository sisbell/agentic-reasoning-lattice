# Review of ASN-0102

I checked the COPY transition definition, the wp/S3★ argument, the X1–X16 derivations, the invariant discharge in X14, and the five worked examples. The mathematics is sound: the three-class tiling in X16 partitions `[1, n_S+W]` correctly, S2/S3★/S8a/D-SEQ are discharged for the modified subspace, the cross-origin and merge arguments (X8/X11/X12) hold, and the coupling discharge (J0/J1★/J1'★) is valid. The edge cases the checklist demands — empty subspace, append, self-transclusion overlapping the displaced region, zero-width (excluded by PC1) — are all present and bite distinct claims. No correctness or missing-case defect found.

The findings below are the anti-bloat / meta-prose patterns this cycle is asked to surface.

## REVISE

### Issue 1: Procedural filler in structural slots
**ASN-0102, end of "Definition of COPY"**: "The half of the definition that distinguishes COPY from every content-creating operation is `Σ'.C = Σ.C`. **We now derive its consequences.**"
**Problem**: "We now derive its consequences" is a procedural announcement that does not advance the argument — the section header and the claim sequence already convey it. The same pattern recurs as connective filler elsewhere.
**Required**: Delete the announcement; let the first claim (X1) follow the substantive sentence directly.

### Issue 2: Use-site inventory and special-case framing aside in X14
**ASN-0102, X14**: "For a standalone, self-coupling COPY the natural framing is `B = Σ`, where this coincides with the split by prior membership at COPY's own pre-state. `Old` is non-empty exactly when `d` already holds some copied content at `B` — in particular under self-transclusion (`d_s = d`) or when a prior step already placed the same content in `d`."
**Problem**: The general boundary-`B` argument already subsumes the `B = Σ` case; the first sentence is a special-case framing aside that adds no obligation. The second sentence is a use-site inventory ("in particular under self-transclusion … or when a prior step …") enumerating when `Old` arises rather than advancing the discharge. Both are the patterns flagged for this mode.
**Required**: Drop the `B = Σ` aside (the general argument stands), and cut the "in particular …" enumeration; the worked self-transclusion example already exhibits the `Old ≠ ∅` case concretely.

### Issue 3: The same boundary case-split is restated three times
**ASN-0102, X14**: the J1'★ discharge, the P4★ paragraph ("From P4★ at `B` together with composite-wide J1★: take any `(a, d) ∈ Contains_C(Σ_clo)` … If `a ∈ ran_{s_C}(B.M(d))` … Otherwise …"), and the P4a discharge ("**mirroring the P4★ argument**, since COPY's elementary post-state `Σ'` is not in general a trace state. … If `(a, d) ∈ R_B` … Otherwise …") each run the identical "in `R_B` ? then pre-existing : else composite-wide coupling" case-split.
**Problem**: Three near-verbatim restatements of one boundary argument; the note itself signals the duplication with "mirroring the P4★ argument." This is the "multiple paragraphs say the same thing" pattern.
**Required**: Factor the boundary case-split into one stated sub-argument and have J1'★, P4★, and P4a each invoke it, rather than re-deriving it in full three times.

### Issue 4: X2 restates X1 without independent content
**ASN-0102, X2 (NoFreshAllocation)**: "*Derivation.* A content-creating allocation extends `dom(Σ.C)`; by X1 that set is unchanged, so the frontier from which the next address is drawn is unchanged."
**Problem**: X2's content is wholly entailed by X1 (its derivation is a one-line appeal to X1), and the table lists it as a peer claim. It reads as a relabeling of X1 rather than a derived consequence carrying new information.
**Required**: Either fold X2 into X1 as a corollary sentence, or state explicitly what X2 adds beyond X1 (e.g., the precise allocation-frontier handle `max{a' : origin(a')=d}` it underwrites) so the separate claim earns its place.

## OUT_OF_SCOPE

(none — the note correctly defers INSERT/DELETE mechanics and link discoverability, and the Open Questions are appropriately forward-looking.)

VERDICT: REVISE
