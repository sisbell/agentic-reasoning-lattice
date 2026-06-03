# Review of ASN-0098

This note is mathematically careful — the proofs show their cases, boundary conditions (empty arrangement, empty retention, `R = ∅`) are handled explicitly, no `✓`-as-proof or "by similar reasoning" hand-waves survive, and every external reference is to a foundation ASN (0034/0036/0043/0047/0093). The operation coverage is exhaustive over the ASN-0047 vocabulary. The findings below are bloat and redundancy, which the active `review-mode.anti-bloat` classifier directs me to surface at source.

## REVISE

### Issue 1: Unused four-clause T4-validity verification of F-members
**ASN-0098, Boundary and Width Behaviour (F definition)**: "Moreover, every `a ∈ F` satisfies T4 (HierarchicalParsing, ASN-0034) directly from its structural form, independent of whether `d` is registered. For `a = [d, 0, s, k]` ... all four T4 clauses hold: `d` contributes exactly two non-adjacent zeros... the first component `a_1 = d_1 ≠ 0` ... the last component `a_{#a} = k ≥ 1 ≠ 0`."
**Problem**: No downstream claim consumes the T4-validity of a full F-candidate `a`. LP-Fin's admissibility argument uses the T4-validity of the *document component* `d` (from F's set-builder conjunct `zeros(d) = 2 ∧ d satisfies T4`), not of `a`; LP-Sub gets store-T4-validity from StoreT4Validity (ASN-0093); LP19a/LP19/LP12b use only the structural form, L0 subspace identifiers, and T1 ordering. The four-clause derivation is dead weight — a defensive demonstration that F is "well-formed" that no proof leans on.
**Required**: Either cite the consuming site or delete the verification, retaining only the structural-form facts (`#a = #d + 3`, `zeros(a) = 3`, `#E(a) = 2`) that are actually used.

### Issue 2: L12 (link immutability) stated twice
**ASN-0098, State Components** ("The link store is immutable: by L12, `(A Σ → Σ', a ∈ dom(Σ.L) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a))`") **and Immutability of the Stored Link** ("By L12 of ASN-0043, for every state transition `Σ → Σ'`, every `a ∈ dom(Σ.L)` persists in `dom(Σ'.L)` with `Σ'.L(a) = Σ.L(a)`...").
**Problem**: The same foundation invariant is restated in full in two sections. The second restatement adds nothing before LP2 is derived from it.
**Required**: Drop one statement; the Immutability section can open directly with the LP2 specialization.

### Issue 3: Self-restating conclusion in the arrangement-fixing template
**ASN-0098, Frame Conditions (Projection invariance under arrangement-fixing transitions)**: "Hence none of content allocation, link allocation, provenance recording, or node/account creation can displace any projection; in particular, creating a new link cannot retroactively affect the projection of any other link, and provenance bookkeeping displaces nothing."
**Problem**: The "in particular" clause re-asserts two instances of the sentence's own first half. The general claim already covers link allocation and provenance recording; the restatement is emphasis, not content.
**Required**: Keep the general conclusion or one concrete instance, not both.

### Issue 4: Defensive exhaustiveness clause in degenerate configurations
**ASN-0098, The Projection Operation (third degenerate configuration)**: "...L3 constrains neither the optional slots `4, …, N` nor the type slot's coverage, so non-emptiness can arise only at slots `3, …, N`."
**Problem**: The trailing inventory of which slots L3 does/does not constrain does not advance the degenerate-case point (empty from/to ⟹ empty projections at slots 1,2). It reads as a defensive enumeration.
**Required**: End the sentence at the established fact (empty slots 1,2 ⟹ empty projections there); drop the slot-inventory tail.

## OUT_OF_SCOPE

### Topic 1: Reverse-discovery, V-order reflection, cross-document operation comparison, link-canonical contraction
**Why out of scope**: These are correctly deferred to the Open Questions section as future ASN territory; they are not gaps in this note's stated claims.

VERDICT: REVISE
