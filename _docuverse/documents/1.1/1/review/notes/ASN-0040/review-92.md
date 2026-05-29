# Review of ASN-0040

The mathematical core is sound. I worked the proofs of S0, S(p,d) canonical form, B5/B5a, B6 (both directions), B7 (all three case splits), B1, B2, B8 (both cases), B9, Bop freshness, and B_fin, and checked the dependency graph for circularity (B1↔next↔B2, B_fin↔next, B7 independence from B1). Each holds. The co-reachability restriction in B8 correctly handles branching state space, and Bop's freshness argument is properly proved without appeal to contiguity. My findings are confined to non-advancing prose, which this note's anti-bloat classifier directs me to surface.

## REVISE

### Issue 1: Unused consequence after S1
**ASN-0040, §The sibling stream (paragraph after S1)**: "the entire stream lies within the set {t ∈ T : p ≼ t}, which forms a contiguous interval under T1 by T5 (ContiguousSubtrees)."
**Problem**: This derived fact is never consumed downstream. B7 obtains stream disjointness directly; B8 obtains uniqueness from ordering/disjointness; nothing invokes the "stream ⊆ contiguous T1 interval" property. It is a true aside that the reader must skip past to follow the argument — non-advancing prose.
**Required**: Either cut the sentence, or wire it into a claim that actually uses it (none currently does).

### Issue 2: Use-site note in a precondition slot
**ASN-0040, §Depth and field structure, B5 Formal Contract**: "*Preconditions:* p ∈ T with d ≥ 1. (In the baptismal context, d ∈ {1, 2} by B6(ii).)"
**Problem**: B5 is a general lemma valid for every d ≥ 1; its proof never uses the {1,2} restriction. The parenthetical is a use-site inventory (where the lemma is later applied) parked in the precondition slot, which should state what B5 *requires*, not where it is consumed.
**Required**: Drop the parenthetical. The d ∈ {1,2} restriction is already stated and discharged at the call site (B6).

### Issue 3: Restatement of an already-discharged case
**ASN-0040, §Namespace disjointness (paragraph after B7 proof)**: "This is precisely the unequal-length-parents case: position 2 reads as the lone zero separator from the ([1], 2) form and as the last component of [1, 0] from the ([1, 0], 1) form … The T4-validity of p' (B6(i)) … is exactly the hypothesis that closes that case."
**Problem**: The counterexample itself (the ([1,0],1) vs ([1],2) aliasing) is legitimate content — it establishes that B6(i) is load-bearing for B7. But the quoted sentences re-walk B7's unequal-length-parents case, which the proof body already discharged. The reader meets the same argument twice in adjacent paragraphs.
**Required**: Keep the counterexample as a one-line necessity note; delete the re-derivation of the position-2 reading, which duplicates the proof.

## OUT_OF_SCOPE

### Topic 1: The Occupied predicate and content storage (B3)
**Why out of scope**: B3 references a future `Occupied : T × 𝒮 → {⊤,⊥}` predicate; content storage is explicitly deferred. B3 is correctly framed as a *forward requirement* on whichever ASN introduces content, not a claim proved here — so it is the proper boundary statement rather than an error. No action needed; flagged only to confirm it stays a forward requirement and does not accrete content-storage mechanics.

VERDICT: REVISE
