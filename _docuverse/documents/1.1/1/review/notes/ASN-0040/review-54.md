# Review of ASN-0040

## REVISE

### Issue 1: B4 asserts a serialization grain that the Open Questions still treats as unresolved

**ASN-0040, §Atomicity (B4)**: "B4's scope is *per-namespace*: B7 guarantees baptisms under distinct (p, d) pairs produce disjoint outputs, so the minimum serialization grain is the namespace, not the entire system."

**ASN-0040, Open Questions**: "What is the minimal serialization grain for baptism — must operations be serialized per-parent per-depth, or per-parent across all depths?"

**Problem**: B4 answers this question — namespace = (p, d) = per-parent-per-depth — while the Open Questions list poses it as open. The note cannot both decide and defer the same point. (Relatedly, the Open Question "may a parent simultaneously baptize children at both d = 1 and d = 2?" is already answered affirmatively by the B6 validity table plus B7's S(p,1) ∩ S(p,2) = ∅; it too reads as stale.)

**Required**: Either delete the B4 scope claim and leave the grain genuinely open, or delete the stale Open Questions. Pick one and make them consistent.

### Issue 2: The hwm Justification duplicates B2 and forward-defers its own derivation

**ASN-0040, §hwm Justification**: "It follows that the prefix's maximum is its last element cₘ — the identity max(children(B, p, d)) = cₘ derived once at B2 below, where the next-address derivation from m is carried."

**Problem**: This paragraph states the conclusion (max = cₘ, count is a sufficient statistic) and then admits the actual derivation lives "at B2 below." B2 then re-derives max = cₘ and next = c_{hwm+1} in full. Two paragraphs assert the same result, with the earlier one a forward pointer to the later — exactly the "defers to a downstream location" / "two paragraphs say the same thing" accretion pattern. The reader works through the justification only to be told the work is elsewhere.

**Required**: Either prove max = cₘ once in the hwm Justification and have B2 cite it, or reduce the hwm Justification to the definition and let B2 carry the derivation. Do not state-and-defer.

### Issue 3: Meta-prose justifying the modeling choice in B0a

**ASN-0040, §The baptismal registry**: "We state the closure law directly on the operation vocabulary Σ rather than on an opaque predicate 'produced by baptism'."

**Problem**: This sentence explains *why the author chose this formulation* rather than advancing what B0a says. It is the "prose justifies modeling choice" pattern flagged by the anti-bloat classifier. The closure law stands on its own; the contrast with a rejected alternative adds nothing a reader needs.

**Required**: Delete the sentence. State B0a directly.

### Issue 4: B4's atomicity prose carries non-advancing reasoning that overlaps B8

**ASN-0040, §Atomicity (B4)**: "B0a guarantees that no other operation modifies s.B between any two transitions, so within a single Σ-transition the read of `s.B ∩ S(p, d)` is exact, and across two same-namespace baptismal transitions β₁, β₂, exactly one of `β₁; β₂` or `β₂; β₁` describes their relative order in the transition sequence — there is no third option of overlap."

**Problem**: The "exactly one of β₁;β₂ or β₂;β₁ … no third option of overlap" reasoning is the linear-ordering-along-a-path argument that B8 Case 1 makes again (and properly, under the co-reachability hypothesis). Stated here as loose prose it neither defines atomicity (what B4 *says*) nor proves anything (B8 does the work), so it sits between the two and must be skipped to follow either.

**Required**: Keep B4 to the atomicity assertion (single edge, no s_mid, computed-and-committed-together). Move any ordering reasoning into B8 where it is actually used, or delete it as redundant.

## OUT_OF_SCOPE

### Topic 1: The Occupied predicate and the four-way ghost partition

**ASN-0040, §Ghost elements (B3)** introduces `Occupied : T × 𝒮 → {⊤, ⊥}` and a four-way classification of (baptized × occupied) configurations.

**Why out of scope**: Content storage and retrieval are explicitly deferred. B3 is correctly framed as a *forward requirement* (it does not define Occupied here), and the ghost-element concept itself is legitimately part of baptism — so this is not an error. But the four-way partition table anticipates content semantics that belong to the future content-storage ASN; that ASN, not this one, should own the partition. Stating the forward requirement (`Occupied(t, s) ⟹ t ∈ s.B`) is sufficient here.

VERDICT: REVISE
