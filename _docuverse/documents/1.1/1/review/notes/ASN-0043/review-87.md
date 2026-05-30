# Review of ASN-0043

## REVISE

### Issue 1: `home` is used across two sections before it is defined, via a chain of forward pointers
**ASN-0043, Subspace Residence (L1a, L1c) and Home and Ownership (Definition — LinkHome)**:
- L1a: "By L1c's T4-validity postcondition (below), T4b's projections `N(a)`, `U(a)`, `D(a)` … are well-defined"
- L1c postcondition: "the document-level prefix `home(a) = N(a).0.U(a).0.D(a)` … this is the field-extraction formula named `home` and developed further under Home and Ownership below"
- LinkHome: "the same `home(a)` first used in L1c's postcondition"

**Problem**: Three separate paragraphs in two sections defer to one another for the definition of `home` — exactly the "multiple paragraphs defer to the same downstream location" pattern. `home(a) = N(a).0.U(a).0.D(a)` is a pure field-extraction formula requiring only L1 (`zeros(a)=3`) and T4-validity; nothing forces it to appear after L1a/L1c.
**Required**: Define `home` once before its first use (it can sit immediately after L1, since T4-validity is the only dependency), then have L1a, L1c, and LinkHome reference that single definition without the "(below)" / "first used in" / "developed further below" provenance prose.

### Issue 2: The T7-disjointness discharge is fully restated four times
**ASN-0043, L0a**: "T4-validity is discharged on each side: for `a ∈ dom(Σ.L)`, by L1c's T4-validity postcondition; for `b ∈ dom(Σ.C)`, by S7b's postcondition … combined with T4b's definitional domain … being precisely the T4-valid subset of `T` … With T4-validity discharged and `zeros(a) = zeros(b) = 3` … T7 applies pairwise …"
**Problem**: The same multi-step T7 discharge (T4-validity per side + equal zero counts + distinct subspaces ⟹ distinct addresses) is spelled out in full in L0a, then again in FSP's `L0` bullet, again in the worked example's `L0` step, and again in the `L9` ghost step. The derivation is load-bearing once; the repetitions are transcriptions of the same argument the reader must re-skim.
**Required**: Carry the disjointness derivation once (in L0a) and reduce the later instances to a citation ("by the L0a discharge, with `zeros = 3` and distinct subspaces").

### Issue 3: L0a carries implementation rationale in a definition slot
**ASN-0043, L0a**: "Conforming systems whose content is entirely `s_C`-resident — Gregory's implementation among them, by the granfilade discriminator's exhaustive assignment of `TEXTATOM = 1` (i.e., `s_C`) to all stored content — enjoy the global disjointness … as a corollary."
**Problem**: L0a is a definition (`dom(Σ.C)|_{s_C}`) plus a derived disjointness. The corollary-about-Gregory is justificatory prose explaining *why the scoping is acceptable*, not advancing the definition. The same point is restated in the Open Questions ("Scope of content-side disjointness"). This is the "new prose explaining why X is needed rather than what it says" pattern.
**Required**: Keep the definition and the one-line scoped disjointness; move the "global disjointness as corollary" remark to the single Open Question that already raises it.

### Issue 4: L1c contains commentary on what the chain "records" rather than content
**ASN-0043, L1c**: "Each step is locally T10a-admissible: `kᵢ ∈ {0, 1, 2}` … The one fact not already recorded in the chain above is where the field separator lands: the first step seats the field-separating zero at position `#s + 1` …"
**Problem**: "The one fact not already recorded in the chain above" is meta-narration about the formal statement, not a step in it. The separator-position fact is then re-used in the `s = home(a)` postcondition, so it belongs *in* the chain/postcondition, not in a sentence describing the chain's coverage.
**Required**: State the separator position as a clause of the chain (or of the `s = home(a)` postcondition) and delete the framing sentence.

### Issue 5: Repeated "outside this ASN's scope" essay paragraphs in structural slots
**ASN-0043, L12 and L10**:
- L12: "The mechanism by which the old link ceases to be discoverable … is outside this ASN's scope."
- L12: "Note what L12 does not address. Whether a link remains *discoverable* … remain *resolvable* … what it means for a link to be 'removed' … outside this ASN's scope."
- L10: "We observe that L10 characterizes the structural affordance … Whether a conforming system must implement subtype-aware query operations … outside this ASN's scope."
**Problem**: These are three multi-sentence scope-boundary essays attached to invariant statements. The Scope section and Open Questions already enumerate operations, discoverability, resolution, and query-interface as out of scope. The inline restatements are noise the reader skips past to reach the next claim.
**Required**: Delete the inline scope essays; a single pointer to the Scope section suffices. If any specific exclusion is load-bearing for L12 (e.g., immutability ≠ removal), compress to one clause.

### Issue 6: L9 / L11b preconditions say "all L- and S-invariants" but enumerate lemmas as if they were state invariants
**ASN-0043, L9 and L11b**: "for any state `Σ` satisfying all invariants of this ASN (L0–L14, L-fin) …" / "(A Σ satisfying all L- and S-invariants … :: … Σ' satisfies all L- and S-invariants)" where the enumeration is given as "L0–L14, L-fin, and ASN-0036's S0–S3 …"
**Problem**: The range "L0–L14" sweeps in L2, L9, L10, L11a, L11b, L12a, L12b, L13 — all labeled LEMMA/THM (derived consequences), not state-local invariants a state is checked against. A state does not "satisfy L11b" (an existence claim about extensions) the way it satisfies L0. FSP gets this right by listing only the state-local set ("L0, L1, L1a, L1b, L1c, L3, L5, L6, L11a, L14, L14a, L-fin"); L9/L11b should match it. As written, the precondition is either circular (L9 requires Σ to satisfy L9) or imprecise.
**Required**: Replace "all L- and S-invariants (L0–L14, …)" in the L9 and L11b statements with the same state-local enumeration FSP uses. Also reconcile FSP's listing of L11a as "state-local" — L11a is a cross-event allocation claim, not a per-state predicate; state which sense FSP preserves.

## OUT_OF_SCOPE

### Topic 1: Link/content consistency under transclusion
The Open Questions already defer "What invariants must hold between the link store and the content store when the same I-address appears in multiple arrangements via transclusion?" This is correctly future territory (it concerns the interaction of S5 with the link layer), not a gap in this ASN's invariant set.

### Topic 2: Coverage-equivalence of distinct span decompositions for query
The Coverage definition correctly notes coverage is lossy and L5 keeps distinct decompositions distinct; whether differing decompositions with equal coverage should be query-equivalent is properly listed as an Open Question and belongs to the query-interface ASN.

VERDICT: REVISE
