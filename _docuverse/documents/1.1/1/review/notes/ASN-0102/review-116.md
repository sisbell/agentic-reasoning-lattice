# Review of ASN-0102

The correctness machinery is sound. The wp(COPY, S3★) reduction, the X15 tiling (three classes partition `[1, n_S+W]` cleanly), the provenance routing (RR + carried/recorded routes discharging J1★/J1'★ via P4★ at the pre-state boundary), and the five boundary-exercising examples (cross-origin, self-transclusion, empty-subspace, append, coalescing) are all carried with genuine depth. Boundary coverage is thorough (W≥1 excludes zero-copy, self-copy handled, empty/append handled). Cross-references are all to foundation ASNs. I have no correctness or missing-case findings.

The findings below are anti-bloat (the note carries `review-mode.anti-bloat`).

## REVISE

### Issue 1: X14 restates its thesis twice and explores a case the operation excludes
**ASN-0102, X14 (Atomicity)**: The paragraph opens with "Elementary status is a deliberate modeling choice, not a reachability necessity — the post-state Σ' is also reachable by a valid composite" and closes with "COPY is therefore *defined* as elementary so that the transient contraction … is never observable, not because no valid composite reaches Σ'."
**Problem**: These two sentences state the same point (elementary = choice, not necessity), bracketing the construction — the "two paragraphs say the same thing in different words" pattern. Additionally, the parenthetical "(The naive *displace-then-fill* and *fill-then-displace* orderings, by contrast, do fail `ValidComposite★` clause (1)…)" imagines decompositions that COPY's definition (a single elementary transition) excludes; the contract-then-extend construction already discharges the composite-reachability claim, so the failure analysis of orderings COPY never performs does not advance it. This is reviser-drift: prose imagining a case the carrier already excludes.
**Required**: Keep the modeling-choice thesis once and the contract-then-extend construction (it proves the claim). Drop the closing restatement and the naive-orderings parenthetical.

### Issue 2: X9's framing sentence is meta-commentary on the claim's shape
**ASN-0102, X9 (SourceHandling)**: "The guarantee splits by whether the source is the target, and the two halves are *different properties* — non-alteration in one case, pre-state resolution in the other."
**Problem**: This narrates the structure of the claim rather than advancing it; X9(a) and X9(b) state the two halves directly and self-evidently differ. Minor, but it is the kind of structural meta-prose that compounds across cycles.
**Required**: Remove the framing sentence; let X9(a)/X9(b) stand.

## OUT_OF_SCOPE

The Open Questions (re-displacement discoverability, transitive containment, time-varying resolution views, identity under unreachable allocator) are correctly deferred to future ASNs and not flagged.

VERDICT: REVISE
