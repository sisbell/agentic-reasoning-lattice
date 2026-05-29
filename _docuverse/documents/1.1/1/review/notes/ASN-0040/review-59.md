# Review of ASN-0040

## REVISE

### Issue 1: B9 cites the wrong unboundedness axiom

**ASN-0040, §Unbounded growth (B9 proof)**: "The final component of cₙ equals n — a value that grows without bound. That no ceiling constrains this component is precisely T0(a) (UnboundedComponentValues): for any bound M' ∈ ℕ, there exists a tumbler in T whose value at that position exceeds M'."

**Problem**: T0(a) is not the load-bearing fact, and the attribution is backwards. T0(a) asserts that the *set T contains some tumbler* with an arbitrarily large component at a position — an existence statement about T's richness. B9 does not consult that; it *constructs* the specific element c_{m+k+1} = inc(c_{m+k}, 0). What the construction actually needs is (a) inc(·, 0) is total on T (TA5 closure, guaranteeing c_{m+k+1} ∈ T), and (b) ℕ is closed under successor so the ordinal n+1 ∈ ℕ (NAT-closure). The proof in fact derives the unboundedness of the component; it does not consume T0(a) as a premise. The proof even hedges by adding "ℕ is closed under successor" in the Axiom line, which is the real justification.

**Required**: Replace the T0(a) appeal with the operative facts: inc totality on T (TA5(c)) for existence of each cₙ, and ℕ successor closure (NAT-closure) for unbounded ordinal values. If T0(a) is to be retained, state explicitly which step consumes it as a premise rather than asserting "precisely T0(a)" for a property the construction establishes.

### Issue 2: B0a is pre-stated before its definition (forward-reference accretion)

**ASN-0040, §State space and transitions**: "B0a partitions Σ into baptismal operations and s.B-frame operations and constrains both classes' action on s.B; Σ is not enumerated exhaustively."

**Problem**: This sentence restates B0a's content one section before B0a is actually defined (in §The baptismal registry), where the same partition is given in full. The preview adds nothing the reader can use yet — B6, Bop, and `next` are all still undefined — so it is content duplicated in different words, the exact accretion pattern flagged for `review-mode.anti-bloat`.

**Required**: Drop the preview sentence; the framework paragraph need only name s.B as the new state component and point to B0a's definition. State the partition once, at B0a.

### Issue 3: Proof-economy meta-prose around s.B ⊆ T

**ASN-0040, §The baptismal registry**: "The set-membership constraint `s.B ⊆ T` needs no separate induction: B10 (§B10) establishes that every t ∈ s.B satisfies T4, and T4-validity entails t ∈ T."

**Problem**: This is prose about the document's proof structure (why a separate induction is unnecessary) attached to a definition, justified by a forward pointer to B10. It does not advance the meaning of s.B; it justifies an absence. This is the "new prose explains why something is/isn't needed rather than what it says" pattern.

**Required**: Remove it. If the containment s.B ⊆ T deserves recording, fold it into B10's postcondition as a one-line corollary (T4 ⟹ t ∈ T) rather than as a structural aside at the definition site.

### Issue 4: Repeated re-assertion of B4 read-semantics

**ASN-0040, Bop freshness / B1 target-namespace case / B4**: "(The children value used here is read against the precondition state and committed by the same edge, by B4.)" … "(read against precondition state B, by B4)" … "read against the precondition state s and committed on one edge".

**Problem**: The same atomicity clarification is restated three times across §Bop, §B1, and §B4. The point is genuine, but stating it once (at B4) and citing B4 by label elsewhere suffices; the inline parentheticals are defensive re-assertions the reader skips past.

**Required**: Keep the full statement at B4; reduce the in-proof occurrences to a bare "(by B4)" or remove them where the surrounding reasoning already operates on the precondition state.

## OUT_OF_SCOPE

### Topic 1: Content-storage predicate Occupied (B3)

**Why out of scope**: B3 introduces `Occupied`, which belongs to content storage (explicitly OUT_OF_SCOPE). The ASN handles this correctly by phrasing B3 as a *forward requirement* on a future ASN rather than defining content storage here, and the ghost-element concept it anchors is intrinsic to baptism. No revision needed — this is the right way to record the baptism↔content boundary; flagged only to confirm it is not in-scope content modeling.

### Topic 2: Cross-branch (non-co-reachable) address uniqueness

**Why out of scope**: B8 deliberately scopes uniqueness to co-reachable acts and notes cross-branch collisions are unaddressed. Since two incomparable branches are alternative histories never jointly observed, unconditional uniqueness across branches is not even desirable here; this is correctly deferred, not an error.

VERDICT: REVISE
