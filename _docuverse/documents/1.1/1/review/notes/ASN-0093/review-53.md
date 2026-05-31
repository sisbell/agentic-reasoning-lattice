# Review of ASN-0093

## REVISE

### Issue 1: L0 C-clause is described both as "proved" and as a "precondition"

**ASN-0093, intro + L0 + discharge matrix**: The opening paragraph says the substrate adds "the C-clause of L0 (content subspace partition) ... *proved within this note*." The L0 section instead says "the C-clause is a new substrate commitment, *pinned as a joint precondition* of the sub-allocator discipline." The discharge matrix (L0 row, K.α column) then *proves* it: "discharged at new key on C-clause: E(a)₁ = s_C read from the pinned emission — FirstEmission / DisjointSubAllocatorChains."

**Problem**: Three locations disagree on the C-clause's status. The matrix discharges it as a theorem (derived from the emission structure / ChainPrefixExtension), so "a new substrate commitment, pinned as a joint precondition" mischaracterizes a derived invariant as an assumption. "Precondition of the sub-allocator discipline" is also backwards — the discipline (b_C(d) = inc(d,2) landing at s_C) *yields* E(a)₁ = s_C; it is not fed the clause as input.

**Required**: State L0's C-clause uniformly as a derived invariant (proved at the new key by FirstEmission/DisjointSubAllocatorChains). Drop "pinned as a joint precondition."

### Issue 2: Event-local framing sentence is proof-bookkeeping, not argument

**ASN-0093, "Discharge of stated invariants," Simultaneous-induction framing**: "The FirstEmissionFreshness and SubsequentEmissionFreshness lemmas are *event-local*: each is a one-shot freshness obligation discharged at the K.α/K.λ binding precondition that commits the emission, not a state property carried in the per-state IH conjunction."

**Problem**: This is rationale about *why* certain lemmas sit outside the IH conjunction — proof-protocol meta-prose of exactly the flagged kind. The freshness lemmas are cited where used (the precondition clauses and the SD matrix rows); the inductive argument does not need a paragraph defending the partition of obligations into "carried in IH" vs "event-local."

**Required**: Delete the sentence. The first sentence ("proved by simultaneous induction ... the conjunction of every such property") is sufficient.

### Issue 3: SD's L14-coincidence paragraph does not advance SD's derivation

**ASN-0093, SD (StoreDisjointness)**: "Here SD coincides with ASN-0043's L14 (DualPrimitive): L0's C-clause forces dom(C) = dom(C)|_{s_C}, so the unsliced dom(C) ∩ dom(L) = ∅ and L14's s_C-sliced dom(L) ∩ dom(C)|_{s_C} = ∅ are the same statement."

**Problem**: SD's derivation (L0 + SC-NEQ + StoreT4Validity + T7) is complete in the preceding sentences. The L14-coincidence note is an equivalence-to-a-foundation-lemma aside — inventory prose that the reader must step past to reach the actual closure of `dom(C) ∩ dom(L) = ∅`.

**Required**: Remove the paragraph, or compress to a one-clause parenthetical if the L14 identity must be recorded.

### Issue 4: Inline provenance duplicates the Properties Introduced "Source" column

**ASN-0093, invariant statements (C0, C1, C1b, C1c, C2, L1, L1a, L1b, L1c, L3, L12)**: Each restated invariant carries an inline tag — "This is ASN-0036's S0/S1 restated for the substrate," "content-side analog of L1b," "This is ASN-0043's L3 restated for the substrate," etc. The Properties Introduced table already records the same provenance in its Source column ("restated from ASN-0036 S0/S1," "content-side analog of L1b (ASN-0036...)," ...).

**Problem**: The same source attribution appears twice, once inline and once in the table. For a stack with this many restated invariants the inline tags accumulate without advancing the invariant's meaning; the table is the single authoritative place for provenance.

**Required**: Drop the inline "restated from / analog of" sentences and let the Properties Introduced table carry source attribution.

## OUT_OF_SCOPE

(none — the note's deferrals to arrangement mutation, entity stratification, provenance, coupling, and withdrawal are correctly scoped out.)

VERDICT: REVISE
