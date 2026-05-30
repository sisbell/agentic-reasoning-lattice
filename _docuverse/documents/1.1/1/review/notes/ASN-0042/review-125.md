# Review of ASN-0042

The core mathematics is sound. I checked the O2 longest-match construction (non-emptiness → chain → finiteness → unique maximum), the O3/O8 refinement arguments, the NestingByDelegation induction, the O6 account-field biconditional, the O9 node-field case split, and the O10 fork construction (both `hwm_0 = 0` field-opening and `hwm_0 ≥ 1` sibling-advance branches, the B6 check, the Form A/B non-coverage analysis, and the worked-example arithmetic). I found no correctness gap, no missing boundary case, no circular dependency among the derived invariants. The findings below are accretion patterns flagged by the `review-mode.anti-bloat` classifier — prose the precise reader must skip past, which compounds across cycles.

## REVISE

### Issue 1: O17b deferral parenthetical does not advance the claim
**ASN-0042, O17b (BaptismalRegistryCoupling)**: "(That this prefix is the next-reachable `next(Σ.B, p, d)` for a B6-valid `(p, d)` is owned by condition (v) of the delegation predicate, not restated here.)"
**Problem**: This sentence states only *where a fact lives* ("owned by condition (v)", "not restated here") — document-coordination meta-prose, not content of the coupling axiom. It matches the flagged pattern "multiple paragraphs defer to the same downstream location." The reader must skip it to reach the actual principal-introduction equation that follows.
**Required**: Delete the parenthetical. The principal-introduction clause `Σ'.B = Σ.B ∪ {pfx(π')}` stands on its own; condition (v) is cited where it is actually used (O18, Freshness-(v)).

### Issue 2: Freshness of `pfx(π')` is derived twice by different routes
**ASN-0042, O18 proof and Freshness-(v)**: O18 proves `pfx(π') ∉ Σ.B` via "Freshness has a single source of truth: condition (v) fixes `pfx(π') = next(Σ.B, p, d)` … and ASN-0040's `Bop` postcondition `next(s.B, p, d) ∉ s.B` gives `pfx(π') ∉ Σ.B`." Freshness-(v)'s "(fresh)" clause then re-derives the *same* fact: "O18 (DelegationBaptizes) gives `pfx(π') ∈ Σ'.B ∖ Σ.B`, so in particular `pfx(π') ∉ Σ.B`."
**Problem**: Two paragraphs establish `pfx(π') ∉ Σ.B`. O18 grounds it directly in condition (v); Freshness-(v) re-routes it through O18. The phrase "single source of truth" is contradicted by the existence of the second derivation. This is the "two paragraphs say the same thing in different words" pattern.
**Required**: Pick one site. Either Freshness-(v) grounds freshness directly in condition (v) (and O18 cites Freshness-(v)), or O18 owns it and Freshness-(v)'s "(fresh)" clause is a one-line citation of O18 with no re-derivation.

### Issue 3: Internal proof-step citations where a named lemma exists
**ASN-0042, SelfOwnershipAtPrefix** and **O10 non-coverage analysis**: "Write `C(pfx(π)) = {…}` … (the same comprehension used locally in the O2 proof)"; and "by the covering-chain lemma (O2's Step 2 — any two prefixes of the same address are `≼`-comparable)".
**Problem**: The covering-chain lemma is a *named, separately-stated* result (PrefixesOfCommonAddressAreComparable). Citing "the same comprehension used locally in the O2 proof" and "O2's Step 2" points the reader at the interior of another proof rather than the named lemma — a use-site cross-reference that rots if O2's internal structure changes. Matches the flagged "see X / deferred to Y" pattern.
**Required**: Cite the named lemma directly ("by the covering-chain lemma") and drop the parenthetical references to O2's internal step numbering and the local comprehension reuse.

### Issue 4: SelfOwnershipAtPrefix re-explains O2's own guarantee inline
**ASN-0042, SelfOwnershipAtPrefix**: "so `ω_Σ(pfx(π))` is defined (O2 supplies `ω : Σ.B → Π_Σ` as a total function in every reachable state)."
**Problem**: The parenthetical restates O2's postcondition verbatim at a use site rather than simply citing O2. Combined with Issue 3, this proof carries three separate gloss-restatements of facts O2 already owns. The argument's actual step — `π` achieves the strictly longest match at its own prefix — is short and clear; the surrounding restatements are the noise.
**Required**: Reduce to a bare citation: "`ω_Σ(pfx(π))` is defined by O2." Let the cited contract carry its own statement.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer invariants
The Open Questions correctly defer transfer semantics (the divergence of inalienable provenance O6 from effective owner O2 once transfer is permitted). This is new state and new operations, not a gap in the refinement-only regime this ASN specifies.

### Topic 2: Cross-node identity federation
O9 establishes node-locality; what a federation layer must satisfy to remain O9-consistent is correctly left to a future ASN.

VERDICT: REVISE
