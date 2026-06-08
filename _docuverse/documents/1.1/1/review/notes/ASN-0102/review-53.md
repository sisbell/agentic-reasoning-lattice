# Review of ASN-0102

## REVISE

### Issue 1: X8 builds a "canonical count" notion only to dismiss it

**ASN-0102, X8 (RunFragmentation)**: "What we count below is the strictly *local* in-isolation merge of `B_copy` among its own blocks. The whole-arrangement canonical count is a different, smaller number, reduced further by the two boundary absorptions of X12... this paragraph treats only the in-isolation count, and X12 treats the boundary merges that complete the global picture." — and later — "This count is local to `B_copy`: in the whole-arrangement canonical form (M12 of `Σ'.M(d)`) the copied blocks have *no* independent count... The two notions are distinct — the in-isolation count `≤ k` measures fragmentation internal to the copied region; the whole-arrangement M12 count of `Σ'.M(d)` is generally smaller still."

**Problem**: The same in-isolation-vs-whole-arrangement distinction is stated twice in different words (pattern 7), and X8 defers to X12 three separate times for the boundary merges (pattern 4). The "in-isolation canonical count" is an intermediate notion the paragraph constructs and then explicitly nullifies ("the copied blocks have *no* independent count"). A reader chasing the actual claim — constructed region is `k` blocks, independent of `W`, canonicalization may reduce it — must skip past this layered apparatus.

**Required**: State once that the constructed region is `k` blocks (independent of `W`); that within-reference blocks never merge; that inter-reference I-adjacent boundaries coalesce; and that whole-arrangement canonicalization additionally absorbs at the two boundaries (X12). Drop the duplicated "two notions are distinct" passage and the repeated X12 deferrals.

### Issue 2: Claims-table rows X8 and X14 carry essay content

**ASN-0102, Claims Introduced table**: The X8 row ("...in-isolation canonical count of the copied region `≤ k`, equality iff no inter-reference boundary is I-adjacent; whole-arrangement M12 count of `Σ'.M(d)` is distinct and reduced further by X12 boundary absorption") and the X14 row (a full paragraph enumerating B-premise machinery, J0/J1★/J1'★, P7/P4★/P4a/P7a, "link/entity Class (a) invariants (incl. ActivatedEmission) vacuous," P3) reproduce the prose body verbatim in compressed form.

**Problem**: A summary table slot is holding paragraph-length restatement of the section it indexes (essay content in a structural slot). This duplicates the prose rather than summarizing it.

**Required**: Reduce both rows to a one-line statement of the claim (as the other rows do), letting the prose carry the discharge detail.

## OUT_OF_SCOPE

### Topic 1: Later re-displacement, derivative-source containment, time-varying views, allocator unreachability
**Why out of scope**: The four Open Questions correctly defer these to future ASNs; they are not gaps in COPY's contract.

VERDICT: REVISE
