# Review of ASN-0107

The specification is technically sound — `sat`/`match`/`num` are well-defined, the existence/discovery split is correct, E1–E4 and the wp in R6 check out, and the worked instance correctly exercises P1, P2, E4, D2, and R2. The issues below are the accreted meta-prose and redundancy this note's `anti-bloat` classifier asks me to surface, plus one tautological framing.

## REVISE

### Issue 1: A2 states its conclusion twice and carries a defensive parenthetical
**ASN-0107, "How the Count Changes: Content Added", A2**: the paragraph first says the count "rises by exactly those shared links that satisfy all three slots — a number bounded above by the shared (discoverable) links and below by `0`", then restates the identical content later: "the count rises by exactly that subset, and equals all from-discoverable shared links only when every one of them has its to/type endpoints arranged in `d_new` too."
**Problem**: One claim, said twice in one paragraph. Separately, the parenthetical "(These `Wᵢ` are query *regions* ... not document subspaces ... not an appeal to any nonexistent 'to-' or 'type-subspace')" explains a *misreading* (slot index vs. subspace) rather than advancing the claim — reviser drift, content that reads as a relocated answer to a prior confusion.
**Required**: State the rise-by-satisfying-shared-links bound once. Delete the subspace-vs-region parenthetical; the slot/subspace distinction is already fixed by the `sat` definition (`eᵢ`) and ASN-0047's subspace partition.

### Issue 2: Claims-table entries are essays in a structural slot
**ASN-0107, "Claims Introduced"**: e.g. D2's cell — "The discovery count is non-monotone: extension raises `Qᵢ`, contraction lowers it, reordering preserves it iff the image sets `{M(d_q)(u):u∈π⁻¹(Wᵢ)∩dom}` and `{M(d_q)(u):u∈Wᵢ∩dom}` agree — setwise fixity of `Wᵢ` is sufficient (e.g. whole subspace) but not necessary (content sharing can preserve the image without it)". A2, R1, and R5 cells are likewise multi-clause paragraphs.
**Problem**: The summary table should carry terse one-line statements; these reproduce whole derivations. Essay content in a structural slot.
**Required**: Reduce each cell to a single declarative line; the body already holds the qualifications.

### Issue 3: `sat` section repeats "no part need be constrained"
**ASN-0107, "State and the Counting Request"**: across one paragraph and the following "Well-definedness" paragraph the same point is made three ways — "We impose no well-formedness constraint requiring any part to be constrained", "Under the standard triple, then, `Q = (T, T, T)` counts every link whose from- and to-endsets are non-empty", "No part need be constrained for `num` to be defined", then again "if any `Qᵢ = ∅` then `sat` fails universally and `num = 0`".
**Problem**: The legitimacy of `Q=(T,T,T)` and the totality of `num` are restated repeatedly, padded with Nelson-quote justification ("the architecture is built to *serve* such breadth, not reject it").
**Required**: State once that every part may be `T` or `∅`, that `num` is total, and that empty parts force `num = 0`. Drop the defensive justification.

### Issue 4: R1 is over-provisioned with "load-bearing because" prose and a redundant closing
**ASN-0107, R1**: opens "No transition removes a link from `dom(Σ.L)`, so `num` registers no 'retraction' ... the existence count never falls", attaches a "This proviso is load-bearing because ..." sub-paragraph to each of (P-last), (P-slot), (P-sole), then closes "It is, in particular, not the action of a per-link delete operation, which does not exist."
**Problem**: The closing duplicates the opening; the per-proviso justifications each imagine the case the proviso excludes (the (P-slot) note constructs a `Wᵢ ∩ Wⱼ` overlap that the claim then forbids), which is exactly the reviser-drift pattern of explaining why a precondition is needed rather than stating the claim.
**Required**: State the three provisos and the `Δnum_disc ∈ {−1,0}` result. Move the "without proviso X, Δ ≤ −2" reasoning into R2 (the general multi-link case it already subsumes), or cut it. Delete the duplicated "no per-link delete" closing — it is the opening sentence and R5.

### Issue 5: The D2 reordering biconditional is a tautology presented as a result
**ASN-0107, D2, reordering bullet**: "the forward image of a *fixed sub-region* `Wᵢ` is preserved exactly when the two image sets agree: `Qᵢ(Σ') = Qᵢ(Σ) ⟺ {Σ.M(d_q)(u) : u ∈ π⁻¹(Wᵢ) ∩ dom} = {Σ.M(d_q)(u) : u ∈ Wᵢ ∩ dom}`."
**Problem**: The right side of the `⟺` is the definitional expansion of `Qᵢ(Σ') = Qᵢ(Σ)`, so the biconditional asserts `A = B ⟺ A = B`. It advances nothing; the load-bearing content is the *sufficient* condition (π fixes `Wᵢ` setwise) and the not-necessary note.
**Required**: Drop the tautological biconditional and lead directly with the sufficient condition and the content-sharing counterexample to necessity.

## OUT_OF_SCOPE

### Topic 1: num_disc when d_q ∉ dom(Σ.M)
The discovery definition scopes itself to "a querying document `d_q ∈ dom(Σ.M)`" and inherits `project`'s partiality from ASN-0098. The note carefully established `num`'s totality but leaves `num_disc`'s domain restriction implicit. This is adequately handled by the stated precondition; a separate partiality claim would be new territory, not an error here.

VERDICT: REVISE
