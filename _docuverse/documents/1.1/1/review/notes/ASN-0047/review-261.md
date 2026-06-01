# Review of ASN-0047

## REVISE

### Issue 1: "⟹ ¬L14a" misrepresents the relationship to a foundation invariant
**ASN-0047, *Amendments to existing transitions* and *Properties Introduced* (Local extensions table)**: "**L14a amendment.** In the extended state, S3★ + CL-OWN supersede ASN-0043's L14a." and the table row deriving "S3★ + CL-OWN ⟹ ¬L14a".

**Problem**: ASN-0043's L14a (NonTranscludability) is explicitly scoped — its statement opens "In any `s_C`-resident system (L0a): `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∉ dom(Σ.L))`". The extended two-subspace state is, by construction, *not* `s_C`-resident: K.μ⁺_L deliberately maps link-subspace V-positions into `dom(L)`. So L14a's hypothesis is unmet and the invariant is simply *inapplicable* here. Writing "⟹ ¬L14a" asserts that a verified foundation invariant is *false*, when in fact only its precondition fails to hold. S3★ itself is handled correctly by contrast — the ASN notes "S3 remains valid when restricted to states with no link-subspace mappings" — so the L14a treatment is the inconsistent one.

**Required**: Reframe as "the extended state does not satisfy L14a's `s_C`-resident hypothesis (L0a), so L14a is inapplicable in this regime," paralleling the S3/S3★ treatment, rather than deriving the negation of a foundation invariant.

### Issue 2: Garbled sentence in the D-SEQ★ derivation (Case m ≥ 3, Step 1)
**ASN-0047, *Amendments to existing transitions*, D-SEQ★ derivation**: "The inner range contains at least j = 2 = m − 1 when m = 3 (the smallest case where the u_M construction below places M at the terminal position j + 1 = m, with the trailing range j + 2..m empty)."

**Problem**: The clause "contains at least j = 2 = m − 1" is not parseable — it conflates the index `j` with a count of positions, equates `j` with `m − 1` as if asserting a fact, and forward-references the `u_M` construction that only appears later in the same step. A reader cannot determine what is being claimed at the point the sentence is read. This sits at the head of a load-bearing inductive step (Step 1 establishes that all inner positions are fixed at 1).

**Required**: Restate as a clear claim about the inner index range — e.g., "the inner positions `2 ≤ j ≤ m − 1` form a nonempty range for `m ≥ 3`, degenerating to the single position `j = 2` at `m = 3`" — and remove the forward dependency on the `u_M` construction from this orienting sentence.

### Issue 3: Meta-prose restating what P0 already guarantees
**ASN-0047, *Destruction confinement*, after the P3 proof**: "Content-store invariance under arrangement mutation — the generalisation this theorem names — follows from P0 by the arrangement frames: every M-mutating transition (K.μ⁺, K.μ⁺_L, K.μ⁻, and K.μ~ by composition of K.μ⁻ and K.μ⁺) carries `C' = C` in its frame, so no arrangement mutation touches `dom(C)` or any stored value, which is exactly what P0's append-only, value-immutable content store already guarantees."

**Problem**: Per the anti-bloat directive, this paragraph advances no reasoning: it re-derives a trivial consequence ("M-mutating transitions frame C") that is already stated in each transition's frame line and already subsumed by P0, then closes by acknowledging it is "exactly what P0 ... already guarantees." It restates the premise as if it were a result. The precise reader must skip past it to reach the substantive next paragraph (which makes the genuine confinement point).

**Required**: Delete the paragraph, or compress to a single clause if a pointer from P3 back to P0's frame coverage is judged useful.

## OUT_OF_SCOPE

None — the ASN stays within state, transitions, and invariants; the deferred topics in Open Questions are correctly future-ASN territory.

VERDICT: REVISE
