# Review of ASN-0047

## REVISE

### Issue 1: S3★ preservation under K.μ~ is circular as written
**ASN-0047, *Decomposition of K.μ~*, Step (A) and the Class (a) verification matrix (S3★ / K.μ~ cell)**: matrix cell reads "by admissibility (i) (carried on π)"; Step (A) states "Admissibility clause (i) hands us both `S3★(Σ')` and `S3★-aux(Σ')` as hypotheses on the candidate π. From these we derive subspace preservation."

**Problem**: Admissibility clause (i) *stipulates* `S3★(Σ')` as a precondition for π to fire. Step (A) then derives subspace preservation from that stipulated `S3★(Σ')`, and subspace preservation is in turn what Step (B) needs so the rebuild's K.μ⁺ amendment (new positions are content-subspace) can fire and produce a post-state "consistent with `S3★(Σ')`." Discharging "K.μ~ preserves S3★" by assuming S3★ holds at the post-state is circular. The π_swap witness escapes (its clause (i) is "verified by construction," domain fixity independent of the post-state package), but that establishes only *non-vacuity*, not that an arbitrary admissible π preserves S3★ non-circularly.

**Required**: A clean non-circular route already exists and should be made primary: K.μ~ = K.μ⁻ + K.μ⁺ as an elementary composite; K.μ⁻ preserves S3★ by restriction and K.μ⁺ preserves it by its amendment (content-subspace new positions → dom(C)), both already proved as Class (a) cells. The K.μ⁺ step's *own* content-subspace precondition is exactly subspace preservation on the content subspace — so realizable π are precisely the subspace-preserving ones, with no appeal to `S3★(Σ')`. Either restate the discharge via the elementary decomposition, or explicitly reclassify K.μ~'s S3★ as filter-enforced (guarded) rather than "derived," and drop Step (A)'s dependence on the post-state hypothesis.

### Issue 2: Sub-allocator family organizational/inventory meta-prose
**ASN-0047, *Allocator hierarchy under documents*, "Sub-allocator names"**: "Five members of the family are named in this ASN, three rooted at a document and two rooted at higher entity-hierarchy levels." ... "The three d-rooted sub-allocators (`A_C(d), A_L(d), A_v(d)`) share the document `d` as their common root; the two entity-hierarchy generalisations ... sit one level higher ... Across the family, the first-emission rule is uniform ... and the subsequent-emission rule is uniformly `inc(prev, 0)`."

**Problem**: This is counting/organization meta-prose about the naming scheme rather than content that advances a claim. The per-member definitions immediately above already state each anchor, first-emission, and subsequent-emission rule; the "five members, three rooted / two rooted" recap and the "across the family ... uniform" restatement add no reasoning the reader needs to follow any downstream proof. This is the family-inventory accretion pattern the anti-bloat classifier flags.

**Required**: Delete the membership-count sentence and the "common root / one level higher / uniform rule" recap; retain only the per-member definitions actually consumed by ParentAllocatorDispatch and the K.δ discharge.

### Issue 3: Defensive self-justification around the imposed J1'★ coupling
**ASN-0047, *Scoped coupling constraints*, J1'★ derivation**: "The step-local wp just computed motivates J1'★ but does not by itself establish the composite-Σ' form ... The gap is closed by **J1'★ itself**. Consider a *record-then-strip* composite ... What renders this composite invalid is J1'★'s Σ'-witness form, imposed as a ValidComposite★ clause-(2) coupling ..."

**Problem**: J1'★ is a coupling the ASN explicitly *imposes* ("We *impose* this as the composite-scoped coupling J1'★"). The surrounding multi-paragraph passage defends *why* the imposition is needed and argues its own non-circularity ("the gap is closed by J1'★ itself") rather than stating what J1'★ requires. This is the "new prose around an axiom explains why the axiom is needed rather than what it says" / "defensive justification" accretion pattern. The substantive content — the range-based statement of J1'★ and its bijective pairing with J1★'s difference set — is already given in the formal box below.

**Required**: Reduce to: (a) the wp computation motivating the coupling, (b) the formal J1'★ statement, and (c) one sentence that it is imposed at the composite boundary (Σ → Σ') as a clause-(2) constraint. Remove the "gap is closed by J1'★ itself" self-referential defense and the record-then-strip walkthrough (or move the latter to a worked example if it carries a concrete trace, which it does not in its current abstract form).

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
**Why out of scope**: The ASN explicitly defers a fork-time link-inheritance mechanism (requiring K.μ⁺_L steps in the fork composite) to a future ASN, and the fork definition correctly starts the forked document's link subspace empty. This is new territory, not an error.

### Topic 2: Link-withdrawal / tombstoning mechanism
**Why out of scope**: Reconciling Nelson's tombstoning (LM 4/9) with D-CTG★/D-MIN★ (interior link withdrawal) is correctly identified as requiring a mechanism outside K.μ⁻'s presentational-removal contract, and is listed as an open question.

VERDICT: REVISE
