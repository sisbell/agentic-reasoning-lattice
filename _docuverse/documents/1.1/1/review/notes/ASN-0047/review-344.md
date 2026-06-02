# Review of ASN-0047

I checked the transition model's correctness (the K.* elementary transitions, the K.μ~ decomposition, the coupling constraints J0/J1★/J1'★, the fork composite J4, and the reachable-state induction) and found the mathematical argument sound — boundary cases (empty document, first insertion, full clearance, orphan link, duplicate-I-address fork, constant-valued content subspace) are each handled. No correctness defects, no improper cross-ASN references (only foundations 0034/0036/0043/0045/0093 are cited).

The findings below are anti-bloat (the note carries `review-mode.anti-bloat`): meta-prose and reviser-drift that a reader must skip past to follow the reasoning. They are paragraph-level trims, not the structural split declined in prior cycles.

## REVISE

### Issue 1: Division-of-labor scaffolding in the K.δ discharge section
**ASN-0047, "K.δ case (ii) discharge and parent-allocator activation"**: "This section supplies only what the K.δ box omits: the *parent-allocator activation* ... and ... the spawnPt premise ... The per-sub-case freshness reading (FrontierEquivalence / ChildSpawnFreshness) and the spawn-admissibility conjuncts ... are discharged at the K.δ box and are not repeated here."

**Problem**: This is organizational narration about which paragraph proves what, not reasoning. It tells the reader what the section is *not* doing before any claim is advanced. The per-`k` paragraphs that follow already name their own discharge sources inline, so the preamble's bookkeeping is redundant scaffolding. This is the flagged "prose justifies document ordering / what is discharged elsewhere" pattern.

**Required**: Delete the division-of-labor preamble; open directly with "By `k`, the parent-allocator activation:" and let each sub-case state its own discharge. Drop the "are discharged at the K.δ box and are not repeated here" clause.

### Issue 2: Downstream-consumer enumeration in inline lemmas
**ASN-0047, J1★ section**: "*Content-boundedness of the content-subspace range (reused below).* ... — the *range-new discharge* invoked by the P7a per-property argument below." And **"Sub-allocator activation (SubAllocatorBundle)"**: "The standing properties of these chains are foundation facts, cited at their use sites: each chain is a T10a-conforming ..."

**Problem**: Both tag a fact with where it will later be consumed ("invoked by the P7a per-property argument below," "cited at their use sites"). The downstream-consumer annotation is the flagged accretion pattern — it advances no reasoning at the point of statement and rots if the consumer moves. The P7a argument already re-derives the range-new fact at its own site, so the forward pointer is pure cross-referencing.

**Required**: State the content-boundedness fact without the "invoked by ... below" tail; the consuming site can cite it. In SubAllocatorBundle, drop "cited at their use sites" — the lemma either states the standing properties or it doesn't; the use-site framing is noise.

### Issue 3: Hypothetical asides outside the traced scenario in worked examples
**ASN-0047, "Worked example: fork with subsequent insertion"**: "(Forking the *version* d₂ to a further d₃ = inc(d₂, 1) would be case (b') of ParentAllocatorDispatch: `A_v(d₂)` would be a child of `A_v(d₁)`, because d₂ inhabits `A_v(d₁)`'s tracked domain ...)"

**Problem**: The parenthetical introduces an operation that is not part of the traced composite — it imagines a *different* fork to illustrate case (b'). The worked example's job is to verify the postconditions of the steps it actually takes; the case-(b') aside belongs to ParentAllocatorDispatch's own statement, where (a')/(b') are already enumerated. This is the flagged "paragraph imagines a case the carrier already handles elsewhere" pattern, and the k=0 subsequent-version fork example *does* exercise case (b') concretely, making the hypothetical doubly redundant.

**Required**: Remove the parenthetical. If the (a')/(b') distinction needs an example, the dedicated "subsequent-version fork (k=0)" trace already supplies it.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link/content withdrawal
The ASN's K.μ⁻ models only suffix removal; interior compaction-and-renumber (the implementation's `DELETEVSPAN`) is correctly deferred — it is already logged as an Open Question, not a gap in this ASN.

VERDICT: REVISE
