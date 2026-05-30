# Review of ASN-0042

## REVISE

### Issue 1: O10 invokes ASN-0040 reachability of the registry without a base case
**ASN-0042, "The Fork as Ownership Boundary" (O10 proof, *Construction*)**: "By O17b (BaptismalRegistryCoupling), `Σ.B` is an ASN-0040-reachable registry, so `hwm` and `next` are well-defined on it (their B1 and finiteness preconditions hold)."
**Problem**: O17b is a *per-transition* coupling — it states each ownership transition restricts to a `Bop` or a registry-frame step. That establishes only the inductive step. To conclude any reachable `Σ.B` is ASN-0040-reachable (and hence that B1 ContiguousPrefix, `hwm`, `next`, B6 apply), you need the base case: that `Σ₀.B` is itself ASN-0040-reachable / conforms to B₀ conf. (contiguous-prefix, finite, T4). O14's only registry clauses are coverage and "every initial principal's prefix lies in `Σ₀.B`" — neither asserts contiguity or B₀-conformance. The worked example silently patches this ("well-formedness ... is ASN-0040's responsibility"; "we assume the bootstrap state was seeded"), but the abstract axiom set does not. O10's appeal to B1 in the Form-B non-coverage analysis, and to `hwm`/`next` in the construction, is therefore ungrounded for the general reachable state. PrefixBaptismCoupling and the O10 `children`-bound argument inherit the same gap.
**Required**: Add a bootstrap axiom (or an O14 clause) asserting `Σ₀.B` is an ASN-0040-reachable registry conforming to B₀ conf., so that O17b's step relation yields full ASN-0040-reachability of every reachable `Σ.B` by induction. Then the B1/`hwm`/`next` preconditions are discharged.

### Issue 2: O6 forward direction applies `fields`, T4b, T4c to `a` without discharging T4(a)
**ASN-0042, "Structural Provenance" (O6 proof, forward direction)**: "By T4b (UniqueParse), the node field `N(a)` consists of the components of `a` preceding the first zero ... By T4c (LevelDetermination), a tumbler with no zeros is a node-level address ..."
**Problem**: Every application of `fields(a)`, T4b, and T4c to the address `a` carries the precondition `T4(a)`. The proof's preamble discharges only O1a (for principals), not `T4(a)`. AccountPrefix (used in the *reverse* direction) explicitly cites O17 to obtain T4 of its argument; the forward direction does not, yet it is the half that decomposes `a`.
**Required**: Cite O17 (AllocatedAddressValidity) once at the head of the forward direction to discharge `T4(a)` from `a ∈ Σ.B`, as O9 and AccountPrefix already do.

### Issue 3: `odom` naming paragraph is notational defense, not reasoning
**ASN-0042, "Ownership Domains" (Definition OwnershipDomain)**: "We write `odom` rather than `dom` deliberately: ASN-0034/0040 already bind `dom(A)` to an *allocator's* enumeration domain ... so a distinct symbol prevents collision."
**Problem**: This sentence-and-a-half justifies a symbol choice rather than advancing the definition's meaning — the anti-bloat pattern "new prose ... explains why ... rather than what it says." The definition `odom(π) = {a ∈ T : pfx(π) ≼ a}` stands on its own; the collision rationale belongs in a commit message, not the contract.
**Required**: Reduce to the bare definition (optionally a parenthetical "`odom`, distinct from ASN-0034's allocator `dom`"); delete the justification prose.

### Issue 4: "Summary of the Model" carries reviser-drift / honesty meta-prose
**ASN-0042, "Summary of the Model"**: "But the reachable-state results do not all follow from those three primitives alone ... The honest summary is therefore: one ownership predicate and one longest-match rule, together with state-dynamics axioms ..."
**Problem**: The framing "The honest summary is therefore" is meta-commentary patching a prior over-minimal claim (the "spare at its core / three primitives" assertion it immediately walks back). The *content* — listing which axioms are load-bearing — is fine, but the rhetorical correction of an earlier sentence in the same paragraph is the residue of a previous review cycle, not reasoning the reader needs.
**Required**: State the dependency directly (the static layer plus the named state-dynamics axioms yield O1–O18) without the self-correcting "spare core ... but actually ... honest summary" arc.

## OUT_OF_SCOPE

### Topic 1: Bootstrap registry conformance as an ASN-0040 obligation
**Why out of scope**: The *internal* well-formedness of `Σ₀.B` (B1 contiguity within each stream, B6 depth validity) is ASN-0040's responsibility; ASN-0042 need only *assert the link* (Issue 1), not re-prove ASN-0040's seed invariants.

VERDICT: REVISE
