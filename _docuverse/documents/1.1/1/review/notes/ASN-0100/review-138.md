# Review of ASN-0100

I checked the substrate decomposition, the four worked-case arithmetic, the invariant discharges (S0/P0, S2, S3★, D-CTG★/D-MIN★/D-SEQ★, S8★, the S7/C1b/C1c bullet, P6, the provenance couplings), the closed-interval reduction with its off-prefix exclusion, and both wp computations. The mathematics is sound: the three regions are correctly disjoint and exhaustive, the K.μ⁻-fires condition is consistent, the empty/append/prepend/deep-subspace boundaries are all covered, and the operation stays abstract (no implementation drift, no non-foundation cross-references). My findings are the prose-accretion patterns this anti-bloat cycle asks for.

## REVISE

### Issue 1: Inheritance bookkeeping and a forward/backward meta-prose pair around INS.I3-coincide
**ASN-0100, §Effect Three**: "the content-frame-independent arrangement lemmas I3 establishes of that arrangement transfer to M'(d) restricted to those two regions — specifically I3-S2 (functionality), I3-VP (S8a well-formedness), I3-VD (fixed depth), and I3-fin (finiteness), each a property of the arrangement alone. INSERT re-derives S3 (§Referential integrity) and S7 (§Post-state V-position well-formedness) independently rather than inheriting them."
**Problem**: This is a downstream use-site inventory (which four lemmas transfer) plus a forward pointer to two sections, paired with a matching backward justification in §Referential integrity — "we re-derive referential integrity directly rather than inheriting I3-S3, because growing dom(C) (INS.C) violates I3's content frame I3-C, on which I3-S3's proof premise rests." Both passages narrate the proof's inherit-vs-re-derive *bookkeeping* rather than advancing the argument; the reader must skip them to reach the actual derivation. The defensive "restriction equality, not an equality of whole arrangements" sentence in the same paragraph is the same pattern.
**Required**: State the coincidence once and let the inheriting sections cite I3-VP/I3-VD/I3-fin at point of use. Drop the lemma-enumeration, the "rather than inheriting them" framing, and the paired "because … I3-C" justification; the re-derivation stands on its own without explaining why inheritance was declined.

### Issue 2: Branch-selection point stated twice in adjacent paragraphs
**ASN-0100, §Effect One**: paragraph 4 already says `a_0` "is either `[d.0.s_C.1]` (if `d` had no prior content emissions …) or `inc(a_prev, 0)` …", and the next paragraph restates the same fact — "Branch selection keys on `dom(C)`, not the arrangement: when residual `origin = d` content persists … the *subsequent*-emission branch fires off the persisted frontier … even when `V_{s_C}(d) = ∅`."
**Problem**: Two adjacent paragraphs assert the same branch-selection rule, and the dedicated re-insertion worked example demonstrates it a third time. Two of the three are redundant.
**Required**: Keep the concrete example (examples are not bloat) and one statement of the rule; fold paragraph 5 into paragraph 4 or delete it.

### Issue 3: Identity-by-allocation stated twice in one section
**ASN-0100, §Identity Through Allocation**: "if two allocations carry coinciding bytes, that coincidence is observable but produces no shared identity" — then the corollary repeats "Value coincidence at `Σ.C(a_k^{(1)}) = Σ.C(a_k^{(2)})` is observable but does not produce identity."
**Problem**: The same sentence appears twice in the same section in different words.
**Required**: State it once; the corollary needs only the disjointness conclusion (`origin` distinct, sets disjoint by SubAllocatorBundle), not a second copy of the value-coincidence remark.

## OUT_OF_SCOPE

(none — the §Bounding the Scope exclusions correctly defer link-subspace insertion, COPY, DELETE, REARRANGE, version creation, and replication.)

VERDICT: REVISE
