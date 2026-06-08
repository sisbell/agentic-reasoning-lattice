# Review of ASN-0111

## REVISE

### Issue 1: Orphaned-instance worked example re-derives FOLLOWLINK machinery instead of verifying the READLINK postcondition

**ASN-0111, "A worked read" (orphaned instance)**: "Discoverability quantifies over slots (LP12, ASN-0098 …), so we dispatch all three. … by the `#d ≤ #d_0` bound … LP-Fin Corollary … the two are disjoint, so the link store meets neither coverage … With all three slots unwitnessed, `discoverable_from(a, d, Σ)` is false for every `d`, and the link is orphaned."

**Problem**: The READLINK-relevant claim RL8 needs only one line — `readlink(a, Σ) = (F, ∅, Θ)` holds because the read consults `Σ.L` alone, independent of arrangement. The entire per-slot discoverability dispatch (LP12, LP-Fin Corollary, subspace disjointness, LP20) verifies that the example link *is* orphaned, which is a projection/FOLLOWLINK-domain fact and not one of this operation's postconditions. The note even prefaces it with "We do not re-derive here…" and then re-derives it. The reader must work through a half-page of resolution machinery to reach the one sentence that bears on `readlink`.

**Required**: State orphanhood as a hypothesis ("suppose `a` is orphaned at `Σ`") and verify only the READLINK obligation — that `readlink(a, Σ)` returns `(F, ∅, Θ)` unchanged because it reads `Σ.L` and no arrangement. Drop the three-slot discoverability derivation.

### Issue 2: Accreted disambiguation parentheticals in the from-set bullet

**ASN-0111, "A worked read" (from-set bullet)**: "The element-level content I-addresses *lying within* `coverage(F)` — the `dom(C)` members inside the coverage intervals, reserving 'arranged' for the `Σ.M` sense used in RL8 — are … three I-addresses that host content and lie *inside* `coverage(F)`, to be distinguished from the coverage intervals themselves."

**Problem**: This is terminology-policing prose, not example content. The clause "reserving 'arranged' for the `Σ.M` sense used in RL8" and the trailing "to be distinguished from the coverage intervals themselves" read like clarifications relocated from prior review cycles. The substantive point — three content addresses sit inside the coverage intervals — is stated, then re-stated with a distinction the reader must hold against a downstream section (RL8). The reader navigates around meta-prose to follow the example.

**Required**: State the three I-addresses and that they are unarranged once, plainly. Remove the cross-reference to RL8's terminology and the "to be distinguished from" restatement.

### Issue 3: Motivational essay in the nesting preamble

**ASN-0111, "Faithful disclosure of nesting"**: "Compound and faceted structures are built this way."

**Problem**: This sentence advances no claim and supports no step in RL6; it is essay framing appended to the structural setup. RL6's concrete link→link instance in the worked read already demonstrates nesting fidelity.

**Required**: Remove the editorial sentence; keep the structural setup (an endset may name a link via the L13 reflexive span) that RL6 actually uses.

## OUT_OF_SCOPE

### Topic 1: Output-level link identity for distinct same-structure links

The third Open Question — distinguishing two distinct links with identical recorded structure — is correctly deferred. `readlink(a, Σ) ≡ Σ.L(a)` returns the endset tuple without the address, so identical-structure links return identical values; only the caller's held key `a` distinguishes them. The note handles this via RL-HOME (home derivable from the key) and the open question rather than over-specifying the read's output, which is the right call.

### Topic 2: Resolution of endsets against arrangements

FOLLOWLINK/projection (mapping recorded spans to current positions) is properly excluded; RL8 only asserts the read is arrangement-independent.

VERDICT: REVISE
